def calculate(data: bytes) -> int:
    if len(data) % 2 == 1:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return ~checksum & 0xFFFF 


def verify(data: bytes, checksum: int) -> bool:
    if len(data) % 2 == 1:
        data += b'\x00' 

    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        total += word
        total = (total & 0xFFFF) + (total >> 16)

    total += checksum
    total = (total & 0xFFFF) + (total >> 16)

    return total == 0xFFFF


def tests():
    print("Тест 1")
    data1 = b"SPBU!"
    checksum1 = calculate(data1)
    assert verify(data1, checksum1)
    print("Accepted")

    print("Тест 2")
    data2 = bytearray(b"CS_center")
    checksum2 = calculate(data2)
    data2[0] ^= 0x03
    assert not verify(data2, checksum2)
    print("Accepted")

    print("Тест 3")
    data3 = b"My homework" 
    checksum3 = calculate(data3)
    assert verify(data3, checksum3)
    print("Accepted")


if __name__ == "__main__":
    tests()