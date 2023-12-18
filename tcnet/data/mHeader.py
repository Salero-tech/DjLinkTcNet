from dataclasses import dataclass
from helper.helper import littleEndianToInt, removeZeroBytes


@dataclass
class mHeader:
    id: int
    versionMajor: int
    versiionMinor: int
    header: str
    msgType: int
    name: str
    seq: int
    nodeType: int
    options: int
    micro: int
    
    def __init__(self, data) -> None:
        # managment header
        self.id = littleEndianToInt(data[0:2])
        self.versionMajor = int.from_bytes(data[2:3])
        self.versiionMinor = int.from_bytes(data[3:4])
        self.header = data[4:7].decode("utf-8")
        self.msgType = int.from_bytes(data[7:8])
        self.name = removeZeroBytes(data[8:16]).decode("utf-8")
        self.seq = int.from_bytes(data[16:17])
        self.nodeType = int.from_bytes(data[17:18])
        self.options = littleEndianToInt(data[18:20])
        self.micro = littleEndianToInt(data[20:24])

    def getBytes (self):
        pass

