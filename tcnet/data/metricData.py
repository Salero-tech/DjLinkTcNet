from dataclasses import dataclass
from helper.helper import littleEndianToInt, removeZeroBytes, intToLittleEndian, addZeroBytes


@dataclass
class MetricData:
    dataType: int
    layerId: int
    layerState: int
    syncMaster: int
    beatMarker: int
    trackLength: int
    currentPosition: int
    speed: int
    beatNumber: int
    bpm: int
    pitchBend: int
    trackId: int

    def __init__(self, layerId, layerState, syncMaster, beatMarker, trackLength, currentPosition, speed, beatNumber, bpm, pitchBend, trackId) -> None:
        self.dataType = 2
        self.layerId = layerId
        self.layerState = layerState
        self.syncMaster = syncMaster
        self.beatMarker = beatMarker
        self.trackLength = trackLength
        self.currentPosition = currentPosition
        self.speed = speed
        self.beatNumber = beatNumber
        self.bpm = bpm
        self.pitchBend = pitchBend
        self.trackId = trackId

    """
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
    """
    def getBytes (self):
        res:list[bytes] = []
        res.append(self.dataType.to_bytes())
        res.append(self.layerId.to_bytes())
        #reserved
        res.append(b'\x00')
        res.append(self.layerState.to_bytes())
        #reserved
        res.append(b'\x00')
        res.append(self.syncMaster.to_bytes())
        #reserved
        res.append(b'\x00')
        res.append(self.beatMarker.to_bytes())
        res.append(intToLittleEndian(self.trackLength, 4))
        res.append(intToLittleEndian(self.currentPosition, 4))
        res.append(intToLittleEndian(self.speed, 4))
        res.append(b'\x00' *13)
        res.append(intToLittleEndian(self.beatNumber, 4))
        res.append(b'\x00' *51)
        res.append(intToLittleEndian(self.bpm, 4))
        res.append(intToLittleEndian(self.pitchBend, 2))
        res.append(intToLittleEndian(self.trackId, 4))


        return b''.join(res)