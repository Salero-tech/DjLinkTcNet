from dataclasses import dataclass, field
from helper.helper import littleEndianToInt, intToLittleEndian, bytesToIntArray, bytesLittleEndianToIntArray, bytesToStringArray, IntArrayTobytes, IntArrayTobytesLittleEndian, stringArrayToBytes


@dataclass
class StatusPacket:
    nodeCount: int
    listenerPort: int
    layerSource:list[int]
    layerStatus:list[int]
    layerTrackId:list[int]
    smpteMode: int
    autoMasterMode:int
    layerName:list[str]

    

    def __init__(self, nodeCount, listenerPort, layerSource, layerStatus, layerTrackId, smpteMode, autoMasterMode, LayerName) -> None:
        self.nodeCount = nodeCount
        self.listenerPort = listenerPort
        self.layerSource = layerSource
        self.layerStatus = layerStatus
        self.layerTrackId = layerTrackId
        self.smpteMode = smpteMode
        self.autoMasterMode = autoMasterMode
        self.layerName =  LayerName

    @staticmethod
    def fromBytes (data):
        nodeCount = littleEndianToInt(data[24:26])
        listenerPort = littleEndianToInt(data[26:28])

        #lets go
        layerSource = bytesToIntArray(data[34:42])
        layerStatus = bytesToIntArray(data[42:50])
        layerTrackId = bytesLittleEndianToIntArray(data[50:83], 4)
        smpteMode = int.from_bytes(data[83:84])
        autoMasterMode = int.from_bytes(data[84:85])
        layerName = bytesToStringArray(data[172:300], 16)
        return StatusPacket(nodeCount, listenerPort, layerSource, layerStatus, layerTrackId, smpteMode, autoMasterMode, layerName)
    
    def getBytes (self):
        res:list[bytes] = []
        res.append(intToLittleEndian(self.nodeCount, 2))
        res.append(intToLittleEndian(self.listenerPort, 2))

        res.append(IntArrayTobytes(self.layerSource))
        res.append(IntArrayTobytes(self.layerStatus))
        res.append(IntArrayTobytesLittleEndian(self.layerTrackId))
        res.append(self.smpteMode.to_bytes())
        res.append(self.autoMasterMode.to_bytes())
        #reserved
        res.append(b'\x00'*87)
        res.append(stringArrayToBytes(self.layerName))




        return b''.join(res)