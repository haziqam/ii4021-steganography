from random import Random
from typing import Literal

import numpy as np


def encode_int(num: int, size: int = 8, endian: Literal["little", "big"] = "big"):
    byte = num.to_bytes(size, endian)
    return "".join([chr(x) for x in byte])


def decode_int(byte: bytes, endian: Literal["little", "big"] = "big"):
    return int.from_bytes(byte, endian)


def create_sequence(
        max_capacity: int,
        rand_seed: int | None = None
) -> list[int]:
    sequence = [i for i in range(max_capacity)]
    if rand_seed is not None:
        prng = Random(rand_seed)
        prng.shuffle(sequence)
    return sequence


def reshuffle_sequence(
        sequence: list[int],
        rand_seed: int | None = None
) -> list[int]:
    if rand_seed is not None:
        prng = Random(rand_seed)
        prng.shuffle(sequence)
    return sequence


def create_checkerboard(height, width):
    M = np.zeros((height, width), dtype=int)
    M[1::2, ::2] = 1
    M[::2, 1::2] = 1
    return M
