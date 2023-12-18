from dataclasses import dataclass
from helper.helper import littleEndianToInt


@dataclass
class optOut:
    nodeCount: int
    listenerPort: int

    def __init__(self, data) -> None:
        self.nodeCount = littleEndianToInt(data[24:26])
        self.listenerPort = littleEndianToInt(data[26:28])