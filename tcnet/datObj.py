from dataclasses import dataclass
from tcnet.data.mHeader import mHeader
from tcnet.data.optIn import optIn
from tcnet.data.optOut import optOut
from tcnet.data.message import message

@dataclass
class DataObj:
    listenerPort: int = 65000
    nodeCount: int = 0
    ip: str = "192.168.178.29"
    id: int = 5457

    @property
    def header (self):
        return mHeader(self.id, 3, 1, "TCN", 2, "TapAdmin", 0, 1,0,0)
    
    @property
    def optIn (self):
        package = optIn(self.nodeCount, self.listenerPort,0,"TapTap", "bridge", 1,1,1)
        return message(self.header, package, self.ip).getBytes()
    
    @property
    def optOut (self):
        package = optOut(self.nodeCount, self.listenerPort)
        return message(self.header, package, self.ip).getBytes()