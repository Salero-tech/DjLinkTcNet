from struct import unpack


def littleEndianToInt (endian:bytes) -> int:
    num: int = int.from_bytes(bytes=endian, byteorder="little")
    return num

def intToLittleEndian (num:int, byteCount:int):

    bits:bytearray = bytearray(num.to_bytes(byteorder='little', length=byteCount))
    
    return bytes(bits)

def removeZeroBytes (byt:bytes) -> bytes:
    res:bytearray = []
    for bit in byt:
        if bit == 0:
            continue
        res.append(bit)
    
    return bytes(res)

def addZeroBytes (byt:bytes, countTotal) -> bytes:
    length = len(byt)
    bytesToCreate = countTotal - length
    
    return byt + b'\x00'*bytesToCreate

def bytesToIntArray (data:bytes) -> list[int]:
    res:list[int] = []

    for bit in data:
        res.append(bit)

    return res

def IntArrayTobytes (data:list[int]) -> bytes:
    res:bytearray = []

    for item in data:
        res.append(item)

    return bytes(res)


def bytesLittleEndianToIntArray (data:bytes, sizeOfEndian:int) -> list[int]:
    res:list[int] = []
    
    byteChunkArray = []
    i = 0
    while i < len(data):
        byteChunkArray.append(data[i:i+sizeOfEndian])
        i += sizeOfEndian

    for chunk in byteChunkArray:
        res.append(littleEndianToInt(chunk))

    return res

def IntArrayTobytesLittleEndian (data:list[int]) -> bytes:
    res:bytearray = []

    for item in data:
        res.append(intToLittleEndian(item, 4))
    return b''.join(res)

def bytesToStringArray (data:bytes, perStrBytes:int) -> list[str]:
    res:list[str] = []
    length = len(data)

    index = 0
    while (index < length):
        res.append(data[index:index+perStrBytes].decode("utf-8"))

    return res

def stringArrayToBytes (data:list[str]) -> bytes:
    res:bytearray = []
    
    for item in data:
        res.append(item.encode("utf-8"))

    return b''.join(res)
