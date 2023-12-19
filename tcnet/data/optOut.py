from dataclasses import dataclass
from helper.helper import littleEndianToInt, intToLittleEndian


@dataclass
class optOut:
    nodeCount: int
    listenerPort: int

    def __init__(self, nodeCount, listenerPort) -> None:
        self.nodeCount = nodeCount
        self.listenerPort = listenerPort

    @staticmethod
    def fromBytes (data):
        nodeCount = littleEndianToInt(data[24:26])
        listenerPort = littleEndianToInt(data[26:28])
        return optOut(nodeCount, listenerPort)
    
    def getBytes (self):
        res:list[bytes] = []
        res.append(intToLittleEndian(self.nodeCount, 2))
        res.append(intToLittleEndian(self.listenerPort, 2))

        return b''.join(res)