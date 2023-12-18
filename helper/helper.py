from struct import unpack




def littleEndianToInt (endian:bytes) -> int:
    length:int = endian.__len__()
    buffzerSize = "H"*(length//2)

    data = unpack(f'<{buffzerSize}', endian)
    return data[0]


def removeZeroBytes (byt:bytes) -> bytes:
    res:bytearray = []
    for bit in byt:
        if bit == 0:
            continue
        res.append(bit)
    
    return bytes(res)