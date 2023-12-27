from dataclasses import dataclass
from tcnet.data.mHeader import mHeader
from tcnet.data.optIn import optIn
from tcnet.data.optOut import optOut
from tcnet.data.message import message
from tcnet.data.statusPacket import StatusPacket

@dataclass
class DataObj:
    listenerPort: int = 65000
    nodeCount: int = 0
    ip: str = "192.168.178.29"
    id: int = 5457

    def header (self, msgType:int):
        return mHeader(self.id, 3, 1, "TCN", msgType, "TapAdmin", 0, 1,0,0)
    
    @property
    def optIn (self):
        package = optIn(self.nodeCount, self.listenerPort,0,"TapTap", "bridge", 1,1,1)
        return message(self.header(2), package, self.ip).getBytes()
    
    @property
    def optOut (self):
        package = optOut(self.nodeCount, self.listenerPort)
        return message(self.header(3), package, self.ip).getBytes()
    
    @property
    def statusPacket (self):
        package = StatusPacket(self.nodeCount, self.listenerPort, [0]*8, [5]*8, [1]*8, 24, 0, "test"*8)
        return message(self.header(5), package, self.ip).getBytes()