from typing import Literal


type Bit = Literal[0, 1]

def get_lsb(n: int) -> Bit:
    return n & 1

def set_lsb(n: int, bit: int) -> Bit:
    bit = bit & 1
    return (n & ~1) | bit

def get_bit_at_index(n: int, index: int) -> int:
    """
    Note: Index 0: LSB
    """
    mask = 1 << index
    return (n & mask) >> index

def set_bit_at_index(n: int, index: int, bit: Bit) -> int:
    """
    Note: Index 0: LSB
    """
    bit = bit & 1

    if bit == 1:
        mask = 1 << index
        return n | mask
    
    mask = ~(1 << index)
    return n & mask

if __name__ == '__main__':
    test = 0b10001001

    print('0b', end='')
    for i in range(8):
        print(get_bit_at_index(test, 7 - i), end='')
    print()

    test2 = set_lsb(test, 0)
    print(bin(test2))

    test3 = set_bit_at_index(test, 1, 1)
    print(bin(test3))

