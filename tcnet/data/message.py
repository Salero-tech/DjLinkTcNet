from dataclasses import dataclass
from tcnet.data.mHeader import mHeader
from tcnet.data.optIn import optIn
from tcnet.data.optOut import optOut
from tcnet.data.statusPacket import StatusPacket

msgTypeList = {
    2: [optIn, 68-mHeader.HEADER_WITH],
    3: [optOut, 28-mHeader.HEADER_WITH],
    5: [StatusPacket, 300-mHeader.HEADER_WITH],
    200: [StatusPacket, 0]
}




@dataclass
class message:
    header: mHeader
    ip: str
    data:any
    typeAsStr: str

    def __init__(self, header:mHeader, data:any, addr:str) -> None:
        self.ip = addr
        self.header = header
        self.data = data
        self.typeAsStr = msgTypeList[self.header.msgType][0].__name__

    def fromBytes (header:mHeader, dataBytes:bytes, addr:str):
        data = msgTypeList[header.msgType][0].fromBytes(dataBytes)
        return message(header, data, addr)

    def getBytes (self):
        return self.header.getBytes() + self.data.getBytes()
    
    @staticmethod
    def getDataSize (header:mHeader) -> int:
        return msgTypeList[header.msgType][1]
        