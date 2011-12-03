import socket
import json
from time import time
from threading import RLock
#from poclbm import realsocket

class SocketLogger:
    """This class will handle witing messages to a socket."""
    
    lock = RLock()
    UPDATE_TIME = 1.0

    def __init__( self, miner, socketaddress = None): 
        self.miner = miner
        self.sock = socket.realsocket( socket.AF_INET, socket.SOCK_DGRAM )
        self.hostport = socketaddress
        self.lastUpdate = 0
    
    def reportFound(self, hash, accepted):
        with self.lock:
            msg = { "op"     : "share"
                  , "time"   : time()
                  , "device" : str(self.miner.options.device)
                  , "share"  : accepted
                  }
            self.sock.sendto( json.dumps( msg ), self.hostport )

    def updateStatus(self, rate, force=False):
        #only update if last update was more than a second ago
        dt = time() - self.lastUpdate
        if force or time() // self.UPDATE_TIME > self.lastUpdate // self.UPDATE_TIME:
            #rate = self.rate if (not self.miner.idle) else 0
            status = { "op"     : "status"
                     , "time"   : time()
                     , "device" : str(self.miner.options.device)
                     , "data"   : { "rate"     : float(rate)
                                  , "accepted" : self.miner.share_count[0]
                                  , "rejected" : self.miner.share_count[1]
                                  }
                     }
            self.sock.sendto( json.dumps( status ), self.hostport )
            self.lastUpdate = time()
