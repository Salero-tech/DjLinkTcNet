from dataclasses import dataclass
from tcnet.data.mHeader import mHeader
from tcnet.data.optIn import optIn
from tcnet.data.optOut import optOut

msgTypeList = {
    2: optIn,
    3: optOut
}




@dataclass
class message:
    header: mHeader
    ip: str
    data:any
    typeAsStr: str

    def __init__(self, dataBytes:bytes, addr:str) -> None:
        self.ip = addr
        self.header = mHeader(dataBytes)
        self.data = msgTypeList[self.header.msgType](dataBytes)
        self.typeAsStr = msgTypeList[self.header.msgType].__name__

    def getBytes (self):
        pass
        