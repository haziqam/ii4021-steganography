def get_lsb(n: int) -> int:
    return n & 1

def set_lsb(n: int, bit: int) -> int:
    return (n & 0b11111110) | bit

def get_bit_at_index(n: int, index: int) -> int:
    mask = 1 << index
    return (n & mask) >> index

def set_bit_at_index(n: int, index: int, bit: int) -> int:
    mask = bit << index
    return n | mask

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

