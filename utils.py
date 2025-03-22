from random import Random
from typing import Literal

import numpy as np


def encode_int(num: int, size: int = 8, endian: Literal["little", "big"] = "big", encoding: str = "utf-8"):
    return num.to_bytes(size, endian).decode(encoding)


def decode_int(string: str, endian: Literal["little", "big"] = "big", encoding: str = "utf-8"):
    return int.from_bytes(string.encode(encoding), endian)


def create_sequence(
        max_capacity: int,
        rand_seed: int | None = None
) -> list[int]:
    sequence = [i for i in range(max_capacity)]
    if rand_seed is not None:
        prng = Random(rand_seed)
        prng.shuffle(sequence)
    return sequence


def create_checkerboard(height, width):
    M = np.zeros((height, width), dtype=int)
    M[1::2, ::2] = 1
    M[::2, 1::2] = 1
    return M
