from dataclasses import dataclass
from helper.helper import littleEndianToInt, removeZeroBytes, intToLittleEndian, addZeroBytes


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

    def __init__(self, nodeCount, listenerPort, upTime, vendorName, deviceName, deviceVersionMajor, deviceVersionMinor, deviceBugVersion) -> None:
        self.nodeCount = nodeCount
        self.listenerPort = listenerPort
        self.upTime = upTime
        self.vendorName = vendorName
        self.deviceName = deviceName
        self.deviceVersionMajor = deviceVersionMajor
        self.deviceVersionMinor = deviceVersionMinor
        self.deviceBugVersion = deviceBugVersion

    @staticmethod
    def fromBytes (data):
        nodeCount = littleEndianToInt(data[24:26])
        listenerPort = littleEndianToInt(data[26:28])
        upTime = littleEndianToInt(data[28:30])
        vendorName = removeZeroBytes(data[32:48]).decode("utf-8")
        deviceName = removeZeroBytes(data[48:64]).decode("utf-8")
        deviceVersionMajor = int.from_bytes(data[64:65])
        deviceVersionMinor = int.from_bytes(data[65:66])
        deviceBugVersion = int.from_bytes(data[66:67])
        
        return optIn(nodeCount, listenerPort, upTime, vendorName, deviceName, deviceVersionMajor, deviceVersionMinor, deviceBugVersion)

    def getBytes (self):
        res:list[bytes] = []
        res.append(intToLittleEndian(self.nodeCount,2))
        res.append(intToLittleEndian(self.listenerPort,2))
        res.append(intToLittleEndian(self.upTime,2))
        res.append(b'\x00'*2)
        res.append(addZeroBytes(self.vendorName.encode("utf-8"),16))
        res.append(addZeroBytes(self.deviceName.encode("utf-8"),16))
        res.append(self.deviceVersionMajor.to_bytes())
        res.append(self.deviceVersionMinor.to_bytes())
        res.append(self.deviceBugVersion.to_bytes())
        res.append(b'\x00')

        return b''.join(res)