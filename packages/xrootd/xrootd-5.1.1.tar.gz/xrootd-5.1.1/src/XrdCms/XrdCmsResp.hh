#ifndef __CMS_RESP__
#define __CMS_RESP__
/******************************************************************************/
/*                                                                            */
/*                         X r d C m s r e s p . h h                          */
/*                                                                            */
/* (c) 2007 by the Board of Trustees of the Leland Stanford, Jr., University  */
/*                            All Rights Reserved                             */
/*   Produced by Andrew Hanushevsky for Stanford University under contract    */
/*              DE-AC02-76-SFO0515 with the Department of Energy              */
/*                                                                            */
/* This file is part of the XRootD software suite.                            */
/*                                                                            */
/* XRootD is free software: you can redistribute it and/or modify it under    */
/* the terms of the GNU Lesser General Public License as published by the     */
/* Free Software Foundation, either version 3 of the License, or (at your     */
/* option) any later version.                                                 */
/*                                                                            */
/* XRootD is distributed in the hope that it will be useful, but WITHOUT      */
/* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or      */
/* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public       */
/* License for more details.                                                  */
/*                                                                            */
/* You should have received a copy of the GNU Lesser General Public License   */
/* along with XRootD in a file called COPYING.LESSER (LGPL license) and file  */
/* COPYING (GPL license).  If not, see <http://www.gnu.org/licenses/>.        */
/*                                                                            */
/* The copyright holder's institutional names and contributor's names may not */
/* be used to endorse or promote products derived from this software without  */
/* specific prior written permission of the institution or contributor.       */
/******************************************************************************/

#include "XrdOuc/XrdOucErrInfo.hh"
#include "XrdSys/XrdSysPthread.hh"

#include "XProtocol/YProtocol.hh"

/******************************************************************************/
/*                          X r d C m s R e s p C B                           */
/******************************************************************************/

class XrdCmsRespCB : XrdOucEICB
{
public:

void Done(int &Result, XrdOucErrInfo *eInfo, const char *Path=0)
         {respSync.Post();}

void Init() {while(respSync.CondWait()) {}}

int  Same(unsigned long long arg1, unsigned long long arg2) {return 0;}

void Wait() {respSync.Wait();}

     XrdCmsRespCB() : respSync(0) {}
    ~XrdCmsRespCB() {}

private:

XrdSysSemaphore     respSync;
};

/******************************************************************************/
/*                            X r d C m s R e s p                             */
/******************************************************************************/

class XrdOucBuffer;
  
class XrdCmsResp : public XrdOucEICB, public XrdOucErrInfo
{
public:
friend class XrdCmsRespQ;

static XrdCmsResp *Alloc(XrdOucErrInfo *erp, int msgid);

       void        Done(int &Result, XrdOucErrInfo *eInfo, const char *Path=0)
                        {Recycle();}

inline int         ID() {return myID;}

       void        Reply(const char   *Man, XrdCms::CmsRRHdr &rrhdr,
                         XrdOucBuffer *netbuff);

static void        Reply();

       int         Same(unsigned long long arg1, unsigned long long arg2)
                       {return 0;}

static void        setDelay(int repdly) {RepDelay = repdly;}

       XrdCmsResp() : XrdOucErrInfo(UserID) {next = 0; myBuff = 0;}
      ~XrdCmsResp() {}

private:
       void Recycle();
       void ReplyXeq();

static XrdSysSemaphore        isReady;
static XrdSysMutex            rdyMutex;  // Protects the below
static XrdCmsResp            *First;
static XrdCmsResp            *Last;

static XrdSysMutex            myMutex;  // Protects above and below
static XrdCmsResp            *nextFree;
static int                    numFree;
static const int              maxFree = 300;
static int                    RepDelay;

XrdCms::CmsRRHdr    myRRHdr;
XrdOucBuffer       *myBuff;
char                theMan[128];

XrdCmsRespCB        SyncCB;
XrdCmsResp         *next;
int                 myID;
char                UserID[64];
};
  
/******************************************************************************/
/*                           X r d O d c R e s p Q                            */
/******************************************************************************/
  
class XrdCmsRespQ
{
public:
       void        Add(XrdCmsResp *rp);

       void        Purge();

       XrdCmsResp *Rem(int msgid);

       XrdCmsRespQ();
      ~XrdCmsRespQ() {Purge();}

private:

       XrdSysMutex  myMutex;  // Protects above and below
static const int    mqSize = 512;

XrdCmsResp         *mqTab[mqSize];
};
#endif
