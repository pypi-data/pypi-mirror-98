
#include <memory>
#include <string>
#include <vector>

#include "XrdSys/XrdSysPthread.hh"

#include "XrdHttp/XrdHttpExtHandler.hh"
#include "XrdHttp/XrdHttpUtils.hh"

class XrdOucErrInfo;
class XrdOucStream;
class XrdSfsFile;
class XrdSfsFileSystem;
typedef void CURL;

namespace TPC {
class State;

enum LogMask {
    Debug   = 0x01,
    Info    = 0x02,
    Warning = 0x04,
    Error   = 0x08,
    All     = 0xff
};

class TPCHandler : public XrdHttpExtHandler {
public:
    TPCHandler(XrdSysError *log, const char *config, XrdOucEnv *myEnv);
    virtual ~TPCHandler();

    virtual bool MatchesPath(const char *verb, const char *path);
    virtual int ProcessReq(XrdHttpExtReq &req);
    // Abstract method in the base class, but does not seem to be used
    virtual int Init(const char *cfgfile) {return 0;}

private:

    struct TPCLogRecord {

        TPCLogRecord() : status( -1 ),
                         tpc_status(-1),
                         streams( 1 ),
                         bytes_transferred( -1 )
        {
        }

        std::string log_prefix;
        std::string local;
        std::string remote;
        std::string name;
        int status;
        int tpc_status;
        unsigned streams;
        off_t bytes_transferred;
    };

    int ProcessOptionsReq(XrdHttpExtReq &req);

    static std::string GetAuthz(XrdHttpExtReq &req);

    // Redirect the transfer according to the contents of an XrdOucErrInfo object.
    int RedirectTransfer(CURL *curl, const std::string &redirect_resource, XrdHttpExtReq &req,
        XrdOucErrInfo &error, TPCLogRecord &);

    int OpenWaitStall(XrdSfsFile &fh, const std::string &resource, int mode,
                      int openMode, const XrdSecEntity &sec,
                      const std::string &authz);

#ifdef XRD_CHUNK_RESP
    int DetermineXferSize(CURL *curl, XrdHttpExtReq &req, TPC::State &state,
                          bool &success, TPCLogRecord &);

    // Send a 'performance marker' back to the TPC client, informing it of our
    // progress.  The TPC client will use this information to determine whether
    // the transfer is making sufficient progress and/or other monitoring info
    // (such as whether the transfer is happening over IPv4, IPv6, or both).
    int SendPerfMarker(XrdHttpExtReq &req, TPCLogRecord &rec, TPC::State &state);
    int SendPerfMarker(XrdHttpExtReq &req, TPCLogRecord &rec, std::vector<State*> &state,
        off_t bytes_transferred);

    // Perform the libcurl transfer, periodically sending back chunked updates.
    int RunCurlWithUpdates(CURL *curl, XrdHttpExtReq &req, TPC::State &state,
                           TPCLogRecord &rec);

    // Experimental multi-stream version of RunCurlWithUpdates
    int RunCurlWithStreams(XrdHttpExtReq &req, TPC::State &state,
                           size_t streams, TPCLogRecord &rec);
    int RunCurlWithStreamsImpl(XrdHttpExtReq &req, TPC::State &state,
                           size_t streams, std::vector<TPC::State*> streams_handles,
                           TPCLogRecord &rec);
#else
    int RunCurlBasic(CURL *curl, XrdHttpExtReq &req, TPC::State &state,
                     const char *log_prefix);
#endif

    int ProcessPushReq(const std::string & resource, XrdHttpExtReq &req);
    int ProcessPullReq(const std::string &resource, XrdHttpExtReq &req);

    bool ConfigureFSLib(XrdOucStream &Config, std::string &path1, bool &path1_alt,
                        std::string &path2, bool &path2_alt);
    bool Configure(const char *configfn, XrdOucEnv *myEnv);
    bool ConfigureLogger(XrdOucStream &Config);

    // Generate a consistently-formatted log message.
    void logTransferEvent(LogMask lvl, const TPCLogRecord &record,
        const std::string &event, const std::string &message="");

    static int m_marker_period;
    static size_t m_block_size;
    static size_t m_small_block_size;
    bool m_desthttps;
    int m_timeout; // the 'timeout interval'; if no bytes have been received during this time period, abort the transfer.
    int m_first_timeout; // the 'first timeout interval'; the amount of time we're willing to wait to get the first byte.
                         // Unless explicitly specified, this is 2x the timeout interval.
    std::string m_cadir;
    static XrdSysMutex m_monid_mutex;
    static uint64_t m_monid;
    XrdSysError m_log;
    XrdSfsFileSystem *m_sfs;

    // 16 blocks in flight at 16 MB each, meaning that there will be up to 256MB
    // in flight; this is equal to the bandwidth delay product of a 200ms transcontinental
    // connection at 10Gbps.
#ifdef USE_PIPELINING
    static const int m_pipelining_multiplier = 16;
#else
    static const int m_pipelining_multiplier = 1;
#endif
};
}
