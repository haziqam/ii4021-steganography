from typing import Literal

import numpy as np

type Bit = Literal[0, 1]

def get_lsb(n: int) -> Bit:
    return np.bitwise_and(n, 1)

def set_lsb(n: int, bit: Bit) -> Bit:
    bit = bit & 1
    return np.bitwise_or(np.bitwise_and(n, ~1), bit)

def get_bit_at_index(n: int, index: int) -> Bit:
    """
    Note: Index 0: LSB
    """
    mask = 1 << index
    return np.bitwise_and(n, mask) >> index

def set_bit_at_index(n: int, index: int, bit: Bit) -> int:
    """
    Note: Index 0: LSB
    """
    bit = bit & 1

    if bit == 1:
        mask = 1 << index
        return np.bitwise_or(n, mask)
    
    mask = ~(1 << index)
    return np.bitwise_and(n, mask)

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

