from dataclasses import dataclass
from helper.helper import littleEndianToInt, removeZeroBytes, intToLittleEndian, addZeroBytes

@dataclass
class mHeader:
    HEADER_WITH = 24 #bytes
    id: int
    versionMajor: int
    versionMinor: int
    header: str
    msgType: int
    name: str
    seq: int
    nodeType: int
    options: int
    micro: int
    
    def __init__(self, id, versionMajor, versionMinor, header, msgType, name, seq, nodeType, options, micro) -> None:
        self.id = id
        self.versionMajor = versionMajor
        self.versionMinor = versionMinor
        self.header = header
        self.msgType = msgType
        self.name = name
        self.seq = seq
        self.nodeType = nodeType
        self.options = options
        self.micro = micro

    @staticmethod
    def fromBytes (data):
        id = littleEndianToInt(data[0:2])
        versionMajor = int.from_bytes(data[2:3])
        versionMinor = int.from_bytes(data[3:4])
        header = data[4:7].decode("utf-8")
        msgType = int.from_bytes(data[7:8])
        name = removeZeroBytes(data[8:16]).decode("utf-8")
        seq = int.from_bytes(data[16:17])
        nodeType = int.from_bytes(data[17:18])
        options = littleEndianToInt(data[18:20])
        micro = littleEndianToInt(data[20:24])

        return mHeader(id, versionMajor, versionMinor, header, msgType, name, seq, nodeType, options, micro)

    def getBytes (self):
        res:list[bytes] = []
        res.append(intToLittleEndian(self.id, 2))
        res.append(self.versionMajor.to_bytes())
        res.append(self.versionMinor.to_bytes())
        res.append(self.header.encode("utf-8"))
        res.append(self.msgType.to_bytes())
        res.append(addZeroBytes(self.name.encode("utf-8"), 8))
        res.append(self.seq.to_bytes())
        res.append(self.nodeType.to_bytes())
        res.append(intToLittleEndian(self.options, 2))
        res.append(intToLittleEndian(self.micro, 4))


        return b''.join(res)

