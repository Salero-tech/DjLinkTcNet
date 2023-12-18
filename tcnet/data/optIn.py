from dataclasses import dataclass
from helper.helper import littleEndianToInt, removeZeroBytes


@dataclass
class optIn:
    nodeCount: int
    listenerPort: int
    upTime: int
    vendorName: str
    deviceName: str
    deviceVersionMajor: int
    deviceVersionMinor: int
    deviceBugVersion: int

    def __init__(self, data) -> None:
        self.nodeCount = littleEndianToInt(data[24:26])
        self.listenerPort = littleEndianToInt(data[26:28])
        self.upTime = littleEndianToInt(data[28:30])
        self.vendorName = removeZeroBytes(data[32:48]).decode("utf-8")
        self.deviceName = removeZeroBytes(data[48:64]).decode("utf-8")
        self.deviceVersionMajor = int.from_bytes(data[64:65])
        self.deviceVersionMinor = int.from_bytes(data[65:66])
        self.deviceBugVersion = int.from_bytes(data[66:67])