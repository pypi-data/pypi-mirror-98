//------------------------------------------------------------------------------
// Copyright (c) 2011-2014 by European Organization for Nuclear Research (CERN)
// Author: Lukasz Janyst <ljanyst@cern.ch>
//------------------------------------------------------------------------------
// This file is part of the XRootD software suite.
//
// XRootD is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// XRootD is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with XRootD.  If not, see <http://www.gnu.org/licenses/>.
//
// In applying this licence, CERN does not waive the privileges and immunities
// granted to it by virtue of its status as an Intergovernmental Organization
// or submit itself to any jurisdiction.
//------------------------------------------------------------------------------

#include "XrdCl/XrdClStream.hh"
#include "XrdCl/XrdClSocket.hh"
#include "XrdCl/XrdClChannel.hh"
#include "XrdCl/XrdClConstants.hh"
#include "XrdCl/XrdClLog.hh"
#include "XrdCl/XrdClMessage.hh"
#include "XrdCl/XrdClDefaultEnv.hh"
#include "XrdCl/XrdClUtils.hh"
#include "XrdCl/XrdClOutQueue.hh"
#include "XrdCl/XrdClMonitor.hh"
#include "XrdCl/XrdClMessageUtils.hh"
#include "XrdCl/XrdClXRootDTransport.hh"
#include "XrdCl/XrdClXRootDMsgHandler.hh"
#include "XrdClAsyncSocketHandler.hh"

#include <sys/types.h>
#include <algorithm>
#include <sys/socket.h>
#include <sys/time.h>

namespace XrdCl
{
  //----------------------------------------------------------------------------
  // Outgoing message helper
  //----------------------------------------------------------------------------
  struct OutMessageHelper
  {
    OutMessageHelper( Message              *message = 0,
                      OutgoingMsgHandler   *hndlr   = 0,
                      time_t                expir   = 0,
                      bool                  statefu = 0 ):
      msg( message ), handler( hndlr ), expires( expir ), stateful( statefu ) {}
    void Reset()
    {
      msg = 0; handler = 0; expires = 0; stateful = 0;
    }
    Message              *msg;
    OutgoingMsgHandler   *handler;
    time_t                expires;
    bool                  stateful;
  };

  //----------------------------------------------------------------------------
  // Incoming message helper
  //----------------------------------------------------------------------------
  struct InMessageHelper
  {
    InMessageHelper( Message              *message = 0,
                     IncomingMsgHandler   *hndlr   = 0,
                     time_t                expir   = 0,
                     uint16_t              actio   = 0 ):
      msg( message ), handler( hndlr ), expires( expir ), action( actio ) {}
    void Reset()
    {
      msg = 0; handler = 0; expires = 0; action = 0;
    }
    Message              *msg;
    IncomingMsgHandler   *handler;
    time_t                expires;
    uint16_t              action;
  };

  //----------------------------------------------------------------------------
  // Sub stream helper
  //----------------------------------------------------------------------------
  struct SubStreamData
  {
    SubStreamData(): socket( 0 ), status( Socket::Disconnected )
    {
      outQueue = new OutQueue();
    }
    ~SubStreamData()
    {
      delete socket;
      delete outQueue;
    }
    AsyncSocketHandler   *socket;
    OutQueue             *outQueue;
    OutMessageHelper      outMsgHelper;
    InMessageHelper       inMsgHelper;
    Socket::SocketStatus  status;
  };

  //----------------------------------------------------------------------------
  // Constructor
  //----------------------------------------------------------------------------
  Stream::Stream( const URL *url, const URL &prefer ):
    pUrl( url ),
    pPrefer( prefer ),
    pTransport( 0 ),
    pPoller( 0 ),
    pTaskManager( 0 ),
    pJobManager( 0 ),
    pIncomingQueue( 0 ),
    pChannelData( 0 ),
    pLastStreamError( 0 ),
    pConnectionCount( 0 ),
    pConnectionInitTime( 0 ),
    pAddressType( Utils::IPAll ),
    pSessionId( 0 ),
    pQueueIncMsgJob(0),
    pBytesSent( 0 ),
    pBytesReceived( 0 )
  {
    pConnectionStarted.tv_sec = 0; pConnectionStarted.tv_usec = 0;
    pConnectionDone.tv_sec = 0;    pConnectionDone.tv_usec = 0;

    std::ostringstream o;
    o << pUrl->GetHostId();
    pStreamName = o.str();

    pConnectionWindow  = Utils::GetIntParameter( *url, "ConnectionWindow",
                                                 DefaultConnectionWindow );
    pConnectionRetry   = Utils::GetIntParameter( *url, "ConnectionRetry",
                                                 DefaultConnectionRetry );
    pStreamErrorWindow = Utils::GetIntParameter( *url, "StreamErrorWindow",
                                                 DefaultStreamErrorWindow );

    std::string netStack = Utils::GetStringParameter( *url, "NetworkStack",
                                                      DefaultNetworkStack );

    pAddressType = Utils::String2AddressType( netStack );

    Log *log = DefaultEnv::GetLog();
    log->Debug( PostMasterMsg, "[%s] Stream parameters: Network Stack: %s, "
                "Connection Window: %d, ConnectionRetry: %d, Stream Error "
                "Window: %d", pStreamName.c_str(), netStack.c_str(),
                pConnectionWindow, pConnectionRetry, pStreamErrorWindow );
  }

  //----------------------------------------------------------------------------
  // Destructor
  //----------------------------------------------------------------------------
  Stream::~Stream()
  {
    Disconnect( true );

    Log *log = DefaultEnv::GetLog();
    log->Debug( PostMasterMsg, "[%s] Destroying stream",
                pStreamName.c_str() );

    MonitorDisconnection( XRootDStatus() );

    SubStreamList::iterator it;
    for( it = pSubStreams.begin(); it != pSubStreams.end(); ++it )
      delete *it;

    delete pQueueIncMsgJob;
  }

  //----------------------------------------------------------------------------
  // Initializer
  //----------------------------------------------------------------------------
  XRootDStatus Stream::Initialize()
  {
    if( !pTransport || !pPoller || !pChannelData )
      return XRootDStatus( stError, errUninitialized );

    AsyncSocketHandler *s = new AsyncSocketHandler( *pUrl, pPoller, pTransport,
                                                    pChannelData, 0 );
    s->SetStream( this );

    pSubStreams.push_back( new SubStreamData() );
    pSubStreams[0]->socket = s;
    return XRootDStatus();
  }

  //------------------------------------------------------------------------
  // Make sure that the underlying socket handler gets write readiness
  // events
  //------------------------------------------------------------------------
  XRootDStatus Stream::EnableLink( PathID &path )
  {
    XrdSysMutexHelper scopedLock( pMutex );

    //--------------------------------------------------------------------------
    // We are in the process of connecting the main stream, so we do nothing
    // because when the main stream connection is established it will connect
    // all the other streams
    //--------------------------------------------------------------------------
    if( pSubStreams[0]->status == Socket::Connecting )
      return XRootDStatus();

    //--------------------------------------------------------------------------
    // The main stream is connected, so we can verify whether we have
    // the up and the down stream connected and ready to handle data.
    // If anything is not right we fall back to stream 0.
    //--------------------------------------------------------------------------
    if( pSubStreams[0]->status == Socket::Connected )
    {
      if( pSubStreams[path.down]->status != Socket::Connected )
        path.down = 0;

      if( pSubStreams[path.up]->status == Socket::Disconnected )
      {
        path.up = 0;
        return pSubStreams[0]->socket->EnableUplink();
      }

      if( pSubStreams[path.up]->status == Socket::Connected )
        return pSubStreams[path.up]->socket->EnableUplink();

      return XRootDStatus();
    }

    //--------------------------------------------------------------------------
    // The main stream is not connected, we need to check whether enough time
    // has passed since we last encountered an error (if any) so that we could
    // re-attempt the connection
    //--------------------------------------------------------------------------
    Log *log = DefaultEnv::GetLog();
    time_t now = ::time(0);

    if( now-pLastStreamError < pStreamErrorWindow )
      return pLastFatalError;

    gettimeofday( &pConnectionStarted, 0 );
    ++pConnectionCount;

    //--------------------------------------------------------------------------
    // Resolve all the addresses of the host we're supposed to connect to
    //--------------------------------------------------------------------------
    XRootDStatus st = Utils::GetHostAddresses( pAddresses, *pUrl, pAddressType );
    if( !st.IsOK() )
    {
      log->Error( PostMasterMsg, "[%s] Unable to resolve IP address for "
                  "the host", pStreamName.c_str() );
      pLastStreamError = now;
      st.status        = stFatal;
      pLastFatalError  = st;
      return st;
    }

    if( pPrefer.IsValid() )
    {
      std::vector<XrdNetAddr> addrresses;
      XRootDStatus st = Utils::GetHostAddresses( addrresses, pPrefer, pAddressType );
      if( !st.IsOK() )
      {
        log->Error( PostMasterMsg, "[%s] Unable to resolve IP address for %s",
                    pStreamName.c_str(), pPrefer.GetHostName().c_str() );
      }
      else
      {
        std::vector<XrdNetAddr> tmp;
        tmp.reserve( pAddresses.size() );
        // first add all remaining addresses
        auto itr = pAddresses.begin();
        for( ; itr != pAddresses.end() ; ++itr )
        {
          if( !HasNetAddr( *itr, addrresses ) )
            tmp.push_back( *itr );
        }
        // then copy all 'preferred' addresses
        std::copy( addrresses.begin(), addrresses.end(), std::back_inserter( tmp ) );
        // and keep the result
        pAddresses.swap( tmp );
      }
    }

    Utils::LogHostAddresses( log, PostMasterMsg, pUrl->GetHostId(),
                             pAddresses );

    while( !pAddresses.empty() )
    {
      pSubStreams[0]->socket->SetAddress( pAddresses.back() );
      pAddresses.pop_back();
      pConnectionInitTime = ::time( 0 );
      st = pSubStreams[0]->socket->Connect( pConnectionWindow );
      if( st.IsOK() )
      {
        pSubStreams[0]->status = Socket::Connecting;
        break;
      }
    }
    return st;
  }

  //----------------------------------------------------------------------------
  // Queue the message for sending
  //----------------------------------------------------------------------------
  XRootDStatus Stream::Send( Message              *msg,
                             OutgoingMsgHandler   *handler,
                             bool                  stateful,
                             time_t                expires )
  {
    XrdSysMutexHelper scopedLock( pMutex );
    Log *log = DefaultEnv::GetLog();

    //--------------------------------------------------------------------------
    // Check the session ID and bounce if needed
    //--------------------------------------------------------------------------
    if( msg->GetSessionId() &&
        (pSubStreams[0]->status != Socket::Connected ||
        pSessionId != msg->GetSessionId()) )
      return XRootDStatus( stError, errInvalidSession );

    //--------------------------------------------------------------------------
    // Decide on the path to send the message
    //--------------------------------------------------------------------------
    PathID path = pTransport->MultiplexSubStream( msg, *pChannelData );
    if( pSubStreams.size() <= path.up )
    {
      log->Warning( PostMasterMsg, "[%s] Unable to send message %s through "
                    "substream %d, using 0 instead", pStreamName.c_str(),
                    msg->GetDescription().c_str(), path.up );
      path.up = 0;
    }

    log->Dump( PostMasterMsg, "[%s] Sending message %s (0x%x) through "
               "substream %d expecting answer at %d", pStreamName.c_str(),
               msg->GetDescription().c_str(), msg, path.up, path.down );

    //--------------------------------------------------------------------------
    // Enable *a* path and insert the message to the right queue
    //--------------------------------------------------------------------------
    XRootDStatus st = EnableLink( path );
    if( st.IsOK() )
    {
      pTransport->MultiplexSubStream( msg, *pChannelData, &path );
      pSubStreams[path.up]->outQueue->PushBack( msg, handler,
                                                expires, stateful );
    }
    else
      st.status = stFatal;
    return st;
  }

  //----------------------------------------------------------------------------
  // Force connection
  //----------------------------------------------------------------------------
  void Stream::ForceConnect()
  {
    XrdSysMutexHelper scopedLock( pMutex );
    pSubStreams[0]->status = Socket::Disconnected;
    XrdCl::PathID path( 0, 0 );
    XrdCl::XRootDStatus st = EnableLink( path );
    if( !st.IsOK() )
      OnConnectError( 0, st );
  }

  //----------------------------------------------------------------------------
  // Disconnect the stream
  //----------------------------------------------------------------------------
  void Stream::Disconnect( bool /*force*/ )
  {
    XrdSysMutexHelper scopedLock( pMutex );
    SubStreamList::iterator it;
    for( it = pSubStreams.begin(); it != pSubStreams.end(); ++it )
    {
      (*it)->socket->Close();
      (*it)->status = Socket::Disconnected;
    }
  }

  //----------------------------------------------------------------------------
  // Handle a clock event
  //----------------------------------------------------------------------------
  void Stream::Tick( time_t now )
  {
    //--------------------------------------------------------------------------
    // Check for timed-out requests and incoming handlers
    //--------------------------------------------------------------------------
    pMutex.Lock();
    OutQueue q;
    SubStreamList::iterator it;
    for( it = pSubStreams.begin(); it != pSubStreams.end(); ++it )
      q.GrabExpired( *(*it)->outQueue, now );
    pMutex.UnLock();

    q.Report( XRootDStatus( stError, errOperationExpired ) );
    pIncomingQueue->ReportTimeout( now );
  }
}

//------------------------------------------------------------------------------
// Handle message timeouts and reconnection in the future
//------------------------------------------------------------------------------
namespace
{
  class StreamConnectorTask: public XrdCl::Task
  {
    public:
      //------------------------------------------------------------------------
      // Constructor
      //------------------------------------------------------------------------
      StreamConnectorTask( XrdCl::Stream *stream ):
        pStream( stream )
      {
        std::string name = "StreamConnectorTask for ";
        name += stream->GetName();
        SetName( name );
      }

      //------------------------------------------------------------------------
      // Run the task
      //------------------------------------------------------------------------
      time_t Run( time_t )
      {
        pStream->ForceConnect();
        return 0;
      }

    private:
      XrdCl::Stream *pStream;
  };
}

namespace XrdCl
{
  XRootDStatus Stream::RequestClose( Message *response )
  {
    ServerResponse *rsp = reinterpret_cast<ServerResponse*>( response->GetBuffer() );
    if( rsp->hdr.dlen < 4 ) return XRootDStatus( stError );
    Message            *msg;
    ClientCloseRequest *req;
    MessageUtils::CreateRequest( msg, req );
    req->requestid = kXR_close;
    memcpy( req->fhandle, reinterpret_cast<uint8_t*>( rsp->body.buffer.data ), 4 );
    XRootDTransport::SetDescription( msg );
    msg->SetSessionId( pSessionId );
    NullResponseHandler *handler = new NullResponseHandler();
    MessageSendParams params;
    params.timeout         = 0;
    params.followRedirects = false;
    params.stateful        = true;
    MessageUtils::ProcessSendParams( params );
    return MessageUtils::SendMessage( *pUrl, msg, handler, params, 0 );
  }

  //------------------------------------------------------------------------
  // Check if message is a partial response
  //------------------------------------------------------------------------
  bool Stream::IsPartial( Message *msg )
  {
    ServerResponseHeader *rsphdr = (ServerResponseHeader*)msg->GetBuffer();
    if( rsphdr->status == kXR_oksofar )
      return true;

    if( rsphdr->status == kXR_status )
    {
      ServerResponseStatus *rspst = (ServerResponseStatus*)msg->GetBuffer();
      if( rspst->bdy.resptype == XrdProto::kXR_PartialResult )
        return true;
    }

    return false;
  }

  //----------------------------------------------------------------------------
  // Call back when a message has been reconstructed
  //----------------------------------------------------------------------------
  void Stream::OnIncoming( uint16_t subStream,
                           Message  *msg,
                           uint32_t  bytesReceived )
  {
    msg->SetSessionId( pSessionId );
    pBytesReceived += bytesReceived;

    uint32_t streamAction = pTransport->MessageReceived( msg, subStream,
                                                         *pChannelData );
    if( streamAction & TransportHandler::DigestMsg )
      return;

    if( streamAction & TransportHandler::RequestClose )
    {
      RequestClose( msg );
      delete msg;
      return;
    }

    //--------------------------------------------------------------------------
    // No handler, we cache and see what comes later
    //--------------------------------------------------------------------------
    Log *log = DefaultEnv::GetLog();
    InMessageHelper &mh = pSubStreams[subStream]->inMsgHelper;

    if( !mh.handler )
    {
      log->Dump( PostMasterMsg, "[%s] Queuing received message: 0x%x.",
                 pStreamName.c_str(), msg );

      pJobManager->QueueJob( pQueueIncMsgJob, msg );
      return;
    }

    //--------------------------------------------------------------------------
    // We have a handler, so we call the callback
    //--------------------------------------------------------------------------
    log->Dump( PostMasterMsg, "[%s] Handling received message: 0x%x.",
               pStreamName.c_str(), msg );

    if( !(mh.action & IncomingMsgHandler::RemoveHandler) )
      pIncomingQueue->ReAddMessageHandler( mh.handler, mh.expires );

    if( mh.action & (IncomingMsgHandler::NoProcess|IncomingMsgHandler::Ignore) )
    {
      log->Dump( PostMasterMsg, "[%s] Ignoring the processing handler for: 0x%x.",
                 pStreamName.c_str(), msg->GetDescription().c_str() );

      // if we are handling partial response we have to take down the timeout fence
      if( IsPartial( msg ) )
      {
        XRootDMsgHandler *xrdHandler = dynamic_cast<XRootDMsgHandler*>( mh.handler );
        if( xrdHandler ) xrdHandler->TakeDownTimeoutFence();
      }

      bool delit = ( mh.action & IncomingMsgHandler::Ignore );
      mh.Reset();
      if (delit) delete msg;

      return;
    }

    Job *job = new HandleIncMsgJob( mh.handler );
    mh.Reset();
    pJobManager->QueueJob( job, msg );
  }

  //----------------------------------------------------------------------------
  // Call when one of the sockets is ready to accept a new message
  //----------------------------------------------------------------------------
  std::pair<Message *, OutgoingMsgHandler *>
    Stream::OnReadyToWrite( uint16_t subStream )
  {
    XrdSysMutexHelper scopedLock( pMutex );
    Log *log = DefaultEnv::GetLog();
    if( pSubStreams[subStream]->outQueue->IsEmpty() )
    {
      log->Dump( PostMasterMsg, "[%s] Nothing to write, disable uplink",
                 pSubStreams[subStream]->socket->GetStreamName().c_str() );

      pSubStreams[subStream]->socket->DisableUplink();
      return std::make_pair( (Message *)0, (OutgoingMsgHandler *)0 );
    }

    OutMessageHelper &h = pSubStreams[subStream]->outMsgHelper;
    h.msg = pSubStreams[subStream]->outQueue->PopMessage( h.handler,
                                                          h.expires,
                                                          h.stateful );
    scopedLock.UnLock();
    if( h.handler )
      h.handler->OnReadyToSend( h.msg );
    return std::make_pair( h.msg, h.handler );
  }

  void Stream::DisableIfEmpty( uint16_t subStream )
  {
    XrdSysMutexHelper scopedLock( pMutex );
    Log *log = DefaultEnv::GetLog();

    if( pSubStreams[subStream]->outQueue->IsEmpty() )
    {
      log->Dump( PostMasterMsg, "[%s] All messages consumed, disable uplink",
                 pSubStreams[subStream]->socket->GetStreamName().c_str() );
      pSubStreams[subStream]->socket->DisableUplink();
    }
  }

  //----------------------------------------------------------------------------
  // Call when a message is written to the socket
  //----------------------------------------------------------------------------
  void Stream::OnMessageSent( uint16_t  subStream,
                              Message  *msg,
                              uint32_t  bytesSent )
  {
    pTransport->MessageSent( msg, subStream, bytesSent,
                             *pChannelData );
    OutMessageHelper &h = pSubStreams[subStream]->outMsgHelper;
    pBytesSent += bytesSent;
    if( h.handler )
      h.handler->OnStatusReady( msg, XRootDStatus() );
    pSubStreams[subStream]->outMsgHelper.Reset();
  }

  //----------------------------------------------------------------------------
  // Call back when a message has been reconstructed
  //----------------------------------------------------------------------------
  void Stream::OnConnect( uint16_t subStream )
  {
    XrdSysMutexHelper scopedLock( pMutex );
    pSubStreams[subStream]->status = Socket::Connected;
    Log *log = DefaultEnv::GetLog();
    log->Debug( PostMasterMsg, "[%s] Stream %d connected.", pStreamName.c_str(),
                subStream );

    if( subStream == 0 )
    {
      pLastStreamError = 0;
      pLastFatalError  = XRootDStatus();
      pConnectionCount = 0;
      uint16_t numSub = pTransport->SubStreamNumber( *pChannelData );
      ++pSessionId;

      //------------------------------------------------------------------------
      // Create the streams if they don't exist yet
      //------------------------------------------------------------------------
      if( pSubStreams.size() == 1 && numSub > 1 )
      {
        for( uint16_t i = 1; i < numSub; ++i )
        {
          AsyncSocketHandler *s = new AsyncSocketHandler( *pUrl, pPoller,
                                                   pTransport, pChannelData, i );
          s->SetStream( this );
          pSubStreams.push_back( new SubStreamData() );
          pSubStreams[i]->socket = s;
        }
      }

      //------------------------------------------------------------------------
      // Connect the extra streams, if we fail we move all the outgoing items
      // to stream 0, we don't need to enable the uplink here, because it
      // should be already enabled after the handshaking process is completed.
      //------------------------------------------------------------------------
      if( pSubStreams.size() > 1 )
      {
        log->Debug( PostMasterMsg, "[%s] Attempting to connect %d additional "
                    "streams.", pStreamName.c_str(), pSubStreams.size()-1 );
        for( size_t i = 1; i < pSubStreams.size(); ++i )
        {
          pSubStreams[i]->socket->SetAddress( pSubStreams[0]->socket->GetAddress() );
          XRootDStatus st = pSubStreams[i]->socket->Connect( pConnectionWindow );
          if( !st.IsOK() )
          {
            pSubStreams[0]->outQueue->GrabItems( *pSubStreams[i]->outQueue );
            pSubStreams[i]->socket->Close();
          }
          else
          {
            pSubStreams[i]->status = Socket::Connecting;
          }
        }
      }

      //------------------------------------------------------------------------
      // Inform monitoring
      //------------------------------------------------------------------------
      pBytesSent     = 0;
      pBytesReceived = 0;
      gettimeofday( &pConnectionDone, 0 );
      Monitor *mon = DefaultEnv::GetMonitor();
      if( mon )
      {
        Monitor::ConnectInfo i;
        i.server  = pUrl->GetHostId();
        i.sTOD    = pConnectionStarted;
        i.eTOD    = pConnectionDone;
        i.streams = pSubStreams.size();

        AnyObject    qryResult;
        std::string *qryResponse = 0;
        pTransport->Query( TransportQuery::Auth, qryResult, *pChannelData );
        qryResult.Get( qryResponse );
        i.auth    = *qryResponse;
        delete qryResponse;
        mon->Event( Monitor::EvConnect, &i );
      }

      //------------------------------------------------------------------------
      // For every connected control-stream call the global on-connect handler
      //------------------------------------------------------------------------
      XrdCl::DefaultEnv::GetPostMaster()->NotifyConnectHandler( *pUrl );
    }
    else if( pOnDataConnJob )
    {
      //------------------------------------------------------------------------
      // For every connected data-stream call the on-connect handler
      //------------------------------------------------------------------------
      pJobManager->QueueJob( pOnDataConnJob.get(), 0 );
    }
  }

  //----------------------------------------------------------------------------
  // On connect error
  //----------------------------------------------------------------------------
  void Stream::OnConnectError( uint16_t subStream, XRootDStatus status )
  {
    XrdSysMutexHelper scopedLock( pMutex );
    Log *log = DefaultEnv::GetLog();
    pSubStreams[subStream]->socket->Close();
    time_t now = ::time(0);

    //--------------------------------------------------------------------------
    // If we connected subStream == 0 and cannot connect >0 then we just give
    // up and move the outgoing messages to another queue
    //--------------------------------------------------------------------------
    if( subStream > 0 )
    {
      pSubStreams[subStream]->status = Socket::Disconnected;
      pSubStreams[0]->outQueue->GrabItems( *pSubStreams[subStream]->outQueue );
      if( pSubStreams[0]->status == Socket::Connected )
      {
        XRootDStatus st = pSubStreams[0]->socket->EnableUplink();
        if( !st.IsOK() )
          OnFatalError( 0, st, scopedLock );
        return;
      }

      if( pSubStreams[0]->status == Socket::Connecting )
        return;

      OnFatalError( subStream, status, scopedLock );
      return;
    }

    //--------------------------------------------------------------------------
    // Check if we still have time to try and do something in the current window
    //--------------------------------------------------------------------------
    time_t elapsed = now-pConnectionInitTime;
    log->Error( PostMasterMsg, "[%s] elapsed = %d, pConnectionWindow = %d "
               "seconds.", pStreamName.c_str(), elapsed, pConnectionWindow );

    //------------------------------------------------------------------------
    // If we have some IP addresses left we try them
    //------------------------------------------------------------------------
    if( !pAddresses.empty() )
    {
      XRootDStatus st;
      do
      {
        pSubStreams[0]->socket->SetAddress( pAddresses.back() );
        pAddresses.pop_back();
        pConnectionInitTime = ::time( 0 );
        st = pSubStreams[0]->socket->Connect( pConnectionWindow );
      }
      while( !pAddresses.empty() && !st.IsOK() );

      if( !st.IsOK() )
        OnFatalError( subStream, st, scopedLock );

      return;
    }
    //------------------------------------------------------------------------
    // If we still can retry with the same host name, we sleep until the end
    // of the connection window and try
    //------------------------------------------------------------------------
    else if( elapsed < pConnectionWindow && pConnectionCount < pConnectionRetry
             && !status.IsFatal() )
    {
      log->Info( PostMasterMsg, "[%s] Attempting reconnection in %d "
                 "seconds.", pStreamName.c_str(), pConnectionWindow-elapsed );

      Task *task = new ::StreamConnectorTask( this );
      pTaskManager->RegisterTask( task, pConnectionInitTime+pConnectionWindow );
      return;
    }
    //--------------------------------------------------------------------------
    // We are out of the connection window, the only thing we can do here
    // is re-resolving the host name and retrying if we still can
    //--------------------------------------------------------------------------
    else if( pConnectionCount < pConnectionRetry && !status.IsFatal() )
    {
      pAddresses.clear();
      pSubStreams[0]->status = Socket::Disconnected;
      PathID path( 0, 0 );
      XRootDStatus st = EnableLink( path );
      if( !st.IsOK() )
        OnFatalError( subStream, st, scopedLock );
      return;
    }

    //--------------------------------------------------------------------------
    // Else, we fail
    //--------------------------------------------------------------------------
    OnFatalError( subStream, status, scopedLock );
  }

  //----------------------------------------------------------------------------
  // Call back when an error has occurred
  //----------------------------------------------------------------------------
  void Stream::OnError( uint16_t subStream, XRootDStatus status )
  {
    XrdSysMutexHelper scopedLock( pMutex );
    Log *log = DefaultEnv::GetLog();
    pSubStreams[subStream]->socket->Close();
    pSubStreams[subStream]->status = Socket::Disconnected;

    log->Debug( PostMasterMsg, "[%s] Recovering error for stream #%d: %s.",
                pStreamName.c_str(), subStream, status.ToString().c_str() );

    //--------------------------------------------------------------------------
    // Reinsert the stuff that we have failed to sent
    //--------------------------------------------------------------------------
    if( pSubStreams[subStream]->outMsgHelper.msg )
    {
      OutMessageHelper &h = pSubStreams[subStream]->outMsgHelper;
      pSubStreams[subStream]->outQueue->PushFront( h.msg, h.handler, h.expires,
                                                   h.stateful );
      pSubStreams[subStream]->outMsgHelper.Reset();
    }

    //--------------------------------------------------------------------------
    // Reinsert the receiving handler
    //--------------------------------------------------------------------------
    if( pSubStreams[subStream]->inMsgHelper.handler )
    {
      InMessageHelper &h = pSubStreams[subStream]->inMsgHelper;
      pIncomingQueue->ReAddMessageHandler( h.handler, h.expires );
      h.Reset();
    }

    //--------------------------------------------------------------------------
    // We are dealing with an error of a peripheral stream. If we don't have
    // anything to send don't bother recovering. Otherwise move the requests
    // to stream 0 if possible.
    //--------------------------------------------------------------------------
    if( subStream > 0 )
    {
      if( pSubStreams[subStream]->outQueue->IsEmpty() )
        return;

      if( pSubStreams[0]->status != Socket::Disconnected )
      {
        pSubStreams[0]->outQueue->GrabItems( *pSubStreams[subStream]->outQueue );
        if( pSubStreams[0]->status == Socket::Connected )
        {
          XRootDStatus st = pSubStreams[0]->socket->EnableUplink();
          if( !st.IsOK() )
            OnFatalError( 0, st, scopedLock );
          return;
        }
      }
      OnFatalError( subStream, status, scopedLock );
      return;
    }

    //--------------------------------------------------------------------------
    // If we lost the stream 0 we have lost the session, we re-enable the
    // stream if we still have things in one of the outgoing queues, otherwise
    // there is not point to recover at this point.
    //--------------------------------------------------------------------------
    if( subStream == 0 )
    {
      MonitorDisconnection( status );

      SubStreamList::iterator it;
      size_t outstanding = 0;
      for( it = pSubStreams.begin(); it != pSubStreams.end(); ++it )
        outstanding += (*it)->outQueue->GetSizeStateless();

      if( outstanding )
      {
        PathID path( 0, 0 );
        XRootDStatus st = EnableLink( path );
        if( !st.IsOK() )
        {
          OnFatalError( 0, st, scopedLock );
          return;
        }
      }

      //------------------------------------------------------------------------
      // We're done here, unlock the stream mutex to avoid deadlocks and
      // report the disconnection event to the handlers
      //------------------------------------------------------------------------
      log->Debug( PostMasterMsg, "[%s] Reporting disconnection to queued "
                  "message handlers.", pStreamName.c_str() );
      OutQueue q;
      for( it = pSubStreams.begin(); it != pSubStreams.end(); ++it )
        q.GrabStateful( *(*it)->outQueue );
      scopedLock.UnLock();

      q.Report( status );
      pIncomingQueue->ReportStreamEvent( IncomingMsgHandler::Broken, status );
      pChannelEvHandlers.ReportEvent( ChannelEventHandler::StreamBroken, status );
      return;
    }
  }

  //------------------------------------------------------------------------
  // Force error
  //------------------------------------------------------------------------
  void Stream::ForceError( XRootDStatus status )
  {
    XrdSysMutexHelper scopedLock( pMutex );
    for( size_t substream = 0; substream < pSubStreams.size(); ++substream )
    {
      Log    *log = DefaultEnv::GetLog();
      if( pSubStreams[substream]->status != Socket::Connected ) continue;
      pSubStreams[substream]->socket->Close();
      pSubStreams[substream]->status = Socket::Disconnected;
      log->Error( PostMasterMsg, "[%s] Forcing error on disconnect: %s.",
                  pStreamName.c_str(), status.ToString().c_str() );

      //--------------------------------------------------------------------
      // Reinsert the stuff that we have failed to sent
      //--------------------------------------------------------------------
      if( pSubStreams[substream]->outMsgHelper.msg )
      {
        OutMessageHelper &h = pSubStreams[substream]->outMsgHelper;
        pSubStreams[substream]->outQueue->PushFront( h.msg, h.handler, h.expires,
                                                     h.stateful );
        pSubStreams[substream]->outMsgHelper.Reset();
      }

      //--------------------------------------------------------------------
      // Reinsert the receiving handler
      //--------------------------------------------------------------------
      if( pSubStreams[substream]->inMsgHelper.handler )
      {
        InMessageHelper &h = pSubStreams[substream]->inMsgHelper;
        pIncomingQueue->ReAddMessageHandler( h.handler, h.expires );
        h.Reset();
      }

      pConnectionCount = 0;

      //------------------------------------------------------------------------
      // We're done here, unlock the stream mutex to avoid deadlocks and
      // report the disconnection event to the handlers
      //------------------------------------------------------------------------
      log->Debug( PostMasterMsg, "[%s] Reporting disconnection to queued "
                  "message handlers.", pStreamName.c_str() );

      SubStreamList::iterator it;
      OutQueue q;
      for( it = pSubStreams.begin(); it != pSubStreams.end(); ++it )
        q.GrabItems( *(*it)->outQueue );
      scopedLock.UnLock();

      q.Report( status );

      pIncomingQueue->ReportStreamEvent( IncomingMsgHandler::Broken, status );
      pChannelEvHandlers.ReportEvent( ChannelEventHandler::StreamBroken, status );
    }
  }

  //----------------------------------------------------------------------------
  // On fatal error
  //----------------------------------------------------------------------------
  void Stream::OnFatalError( uint16_t           subStream,
                             XRootDStatus       status,
                             XrdSysMutexHelper &lock )
  {
    Log    *log = DefaultEnv::GetLog();
    pSubStreams[subStream]->status = Socket::Disconnected;
    log->Error( PostMasterMsg, "[%s] Unable to recover: %s.",
                pStreamName.c_str(), status.ToString().c_str() );

    //--------------------------------------------------------------------------
    // Don't set the stream error windows for authentication errors as the user
    // may refresh his credential at any time
    //--------------------------------------------------------------------------
    if( status.code != errAuthFailed )
    {
      pConnectionCount = 0;
      pLastStreamError = ::time(0);
      pLastFatalError  = status;
    }

    SubStreamList::iterator it;
    OutQueue q;
    for( it = pSubStreams.begin(); it != pSubStreams.end(); ++it )
      q.GrabItems( *(*it)->outQueue );
    lock.UnLock();

    status.status = stFatal;
    q.Report( status );
    pIncomingQueue->ReportStreamEvent( IncomingMsgHandler::FatalError, status );
    pChannelEvHandlers.ReportEvent( ChannelEventHandler::FatalError, status );

  }

  //----------------------------------------------------------------------------
  // Inform monitoring about disconnection
  //----------------------------------------------------------------------------
  void Stream::MonitorDisconnection( XRootDStatus status )
  {
    Monitor *mon = DefaultEnv::GetMonitor();
    if( mon )
    {
      Monitor::DisconnectInfo i;
      i.server = pUrl->GetHostId();
      i.rBytes = pBytesReceived;
      i.sBytes = pBytesSent;
      i.cTime  = ::time(0) - pConnectionDone.tv_sec;
      i.status = status;
      mon->Event( Monitor::EvDisconnect, &i );
    }
  }

  //----------------------------------------------------------------------------
  // Call back when a message has been reconstructed
  //----------------------------------------------------------------------------
  void Stream::OnReadTimeout( uint16_t substream, bool &isBroken )
  {
    isBroken = false;

    //--------------------------------------------------------------------------
    // We only take the main stream into account
    //--------------------------------------------------------------------------
    if( substream != 0 )
      return;

    //--------------------------------------------------------------------------
    // Check if there is no outgoing messages and if the stream TTL is elapesed.
    // It is assumed that the underlying transport makes sure that there is no
    // pending requests that are not answered, ie. all possible virtual streams
    // are de-allocated
    //--------------------------------------------------------------------------
    Log *log = DefaultEnv::GetLog();
    SubStreamList::iterator it;
    time_t                  now = time(0);

    XrdSysMutexHelper scopedLock( pMutex );
    uint32_t outgoingMessages = 0;
    time_t   lastActivity     = 0;
    for( it = pSubStreams.begin(); it != pSubStreams.end(); ++it )
    {
      outgoingMessages += (*it)->outQueue->GetSize();
      time_t sockLastActivity = (*it)->socket->GetLastActivity();
      if( lastActivity < sockLastActivity )
        lastActivity = sockLastActivity;
    }

    if( !outgoingMessages )
    {
      bool disconnect = pTransport->IsStreamTTLElapsed( now-lastActivity,
                                                        *pChannelData );
      if( disconnect )
      {
        log->Debug( PostMasterMsg, "[%s] Stream TTL elapsed, disconnecting...",
                    pStreamName.c_str() );
        scopedLock.UnLock();
        //----------------------------------------------------------------------
        // Important note!
        //
        // This destroys the Stream object itself, the underlined
        // AsyncSocketHandler object (that called this method) and the Channel
        // object that aggregates this Stream.
        //----------------------------------------------------------------------
        DefaultEnv::GetPostMaster()->ForceDisconnect( *pUrl );
        return;
      }
    }

    //--------------------------------------------------------------------------
    // Check if the stream is broken
    //--------------------------------------------------------------------------
    XRootDStatus st = pTransport->IsStreamBroken( now-lastActivity,
                                            *pChannelData );
    if( !st.IsOK() )
    {
      isBroken =  true;
      scopedLock.UnLock();
      OnError( substream, st );
    }
  }

  //----------------------------------------------------------------------------
  // Call back when a message has been reconstru
  //----------------------------------------------------------------------------
  void Stream::OnWriteTimeout( uint16_t /*substream*/ )
  {
  }

  //----------------------------------------------------------------------------
  // Register channel event handler
  //----------------------------------------------------------------------------
  void Stream::RegisterEventHandler( ChannelEventHandler *handler )
  {
    pChannelEvHandlers.AddHandler( handler );
  }

  //----------------------------------------------------------------------------
  // Remove a channel event handler
  //----------------------------------------------------------------------------
  void Stream::RemoveEventHandler( ChannelEventHandler *handler )
  {
    pChannelEvHandlers.RemoveHandler( handler );
  }

  //----------------------------------------------------------------------------
  // Install a incoming message handler
  //----------------------------------------------------------------------------
  std::pair<IncomingMsgHandler *, bool>
        Stream::InstallIncHandler( Message *msg, uint16_t stream )
  {
    InMessageHelper &mh = pSubStreams[stream]->inMsgHelper;
    if( !mh.handler )
      mh.handler = pIncomingQueue->GetHandlerForMessage( msg,
                                                         mh.expires,
                                                         mh.action );

    if( !mh.handler )
      return std::make_pair( (IncomingMsgHandler*)0, false );

    bool ownership = mh.action & IncomingMsgHandler::Take;
    if( mh.action & IncomingMsgHandler::Raw )
      return std::make_pair( mh.handler, ownership );
    return std::make_pair( (IncomingMsgHandler*)0, ownership );
  }

  //----------------------------------------------------------------------------
  //! In case the message is a kXR_status response it needs further attention
  //!
  //! @return : a IncomingMsgHandler in case we need to read out raw data
  //----------------------------------------------------------------------------
  uint16_t Stream::InspectStatusRsp( Message             *msg,
                                     uint16_t             stream,
                                     IncomingMsgHandler *&incHandler )
  {
    InMessageHelper &mh = pSubStreams[stream]->inMsgHelper;
    if( !mh.handler ) return false;

    uint16_t action = mh.handler->InspectStatusRsp( msg );
    mh.action |= action;

    if( action & IncomingMsgHandler::RemoveHandler )
      pIncomingQueue->RemoveMessageHandler( mh.handler );

    if( action & IncomingMsgHandler::Raw )
    {
      incHandler = mh.handler;
      return IncomingMsgHandler::Raw;
    }

    if( action & IncomingMsgHandler::Corrupted )
      return IncomingMsgHandler::Corrupted;

    return IncomingMsgHandler::None;
  }

  //----------------------------------------------------------------------------
  // Check if channel can be collapsed using given URL
  //----------------------------------------------------------------------------
  bool Stream::CanCollapse( const URL &url )
  {
    Log *log = DefaultEnv::GetLog();

    //--------------------------------------------------------------------------
    // Resolve all the addresses of the host we're supposed to connect to
    //--------------------------------------------------------------------------
    std::vector<XrdNetAddr> prefaddrs;
    XRootDStatus st = Utils::GetHostAddresses( prefaddrs, url, pAddressType );
    if( !st.IsOK() )
    {
      log->Error( PostMasterMsg, "[%s] Unable to resolve IP address for %s."
                  , pStreamName.c_str(), url.GetHostName().c_str() );
      return false;
    }

    //--------------------------------------------------------------------------
    // Resolve all the addresses of the alias
    //--------------------------------------------------------------------------
    std::vector<XrdNetAddr> aliasaddrs;
    st = Utils::GetHostAddresses( aliasaddrs, *pUrl, pAddressType );
    if( !st.IsOK() )
    {
      log->Error( PostMasterMsg, "[%s] Unable to resolve IP address for %s."
                  , pStreamName.c_str(), pUrl->GetHostName().c_str() );
      return false;
    }

    //--------------------------------------------------------------------------
    // Now check if the preferred host is part of the alias
    //--------------------------------------------------------------------------
    auto itr = prefaddrs.begin();
    for( ; itr != prefaddrs.end() ; ++itr )
    {
      auto itr2 = aliasaddrs.begin();
      for( ; itr2 != aliasaddrs.end() ; ++itr2 )
        if( itr->Same( &*itr2 ) ) return true;
    }

    return false;
  }
}
