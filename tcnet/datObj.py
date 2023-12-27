from dataclasses import dataclass
from tcnet.data.mHeader import mHeader
from tcnet.data.optIn import optIn
from tcnet.data.optOut import optOut
from tcnet.data.message import message
from tcnet.data.statusPacket import StatusPacket
from  tcnet.data.metaData import MetaData
from  tcnet.data.metricData import MetricData

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
        package = StatusPacket(self.nodeCount, self.listenerPort, [0]*8, [3]*8, [1]*8, 24, 0, "test"*8)
        return message(self.header(5), package, self.ip).getBytes()
    
    @property
    def metaData (self):
        package = MetaData(1, "Hello world", "World Hello", 3, 0)
        return message(self.header(200), package, self.ip).getBytes()
    
    @property
    def MetricData (self):
        package = MetricData(1,3,0,1,80000,60000,327668,99999,20000,32768,0)
        return message(self.header(200), package, self.ip).getBytes()