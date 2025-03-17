import numpy as np
from PIL import Image

from bit import Bit, get_lsb, set_lsb, get_bit_at_index, set_bit_at_index
from utils import create_sequence


# TODO:
# 1) Embed-nya ga harus di byte blue (bisa dibuat ganti-gantian)
# 2) Explore case ukuran image ga cukup buat nyimpen pesan
# 3) Explore case image tidak RGB (grayscale ato item putih)
# 3) Explore cara nyimpen message length di image


def get_complexity(matrix: Image | np.ndarray, plane: int, channel: int | None = None) -> float:
    width, height = matrix.size
    for x in range(width):
        right_bit = 0
        for y in range(height):
            curr_bit = get_bit_at_position(matrix, x, y, plane, channel)


def set_bit_at_position(pixels, x: int, y: int, message_bit: Bit, plane: int, channel: int | None = None):
    if channel is None:
        byte = set_bit_at_index(pixels[x, y], plane, message_bit)
        pixels[x, y] = byte
    else:
        byte = set_bit_at_index(pixels[x, y][0], plane, message_bit)
        pixels[x, y][channel] = byte


def get_bit_at_position(pixels, x: int, y: int, plane: int, channel: int | None = None) -> Bit:
    if channel is None:
        return get_bit_at_index(pixels[x, y], plane)
    else:
        return get_bit_at_index(pixels[x, y][channel], plane)


def embed_message(image: Image, message: str, sequence: list[int]) -> Image:
    pixels = image.load()
    width, _ = image.size

    # Prepend message length to message (as an 8-bit char)
    message_length_in_byte = chr(len(message))
    message = message_length_in_byte + message

    # Embed message
    for idx, c in enumerate(message):
        for i in range(8):
            target_idx = sequence[idx * 8 + i]
            x = target_idx % width
            y = target_idx // width
            message_bit = get_bit_at_index(ord(c), i)
            set_lsb_at_position(pixels, x, y, message_bit)

    return image


def extract_message(image: Image, sequence: list[int]) -> str:
    pixels = image.load()
    width, _ = image.size

    # Extract message length (first 8 bits)
    message_length = 0
    for i in range(8):
        target_idx = sequence[i]
        x = target_idx % width
        y = target_idx // width
        message_bit = get_bit_at_position(pixels, x, y)
        message_length = set_bit_at_index(message_length, i, message_bit)

    # Extract message
    message: list[str] = []
    for idx in range(1, message_length + 1):
        current_byte = 0
        for j in range(8):
            target_idx = sequence[idx * 8 + j]
            x = target_idx % width
            y = target_idx // width
            message_bit = get_bit_at_position(pixels, x, y)
            current_byte = set_bit_at_index(current_byte, j, message_bit)

        message.append(chr(current_byte))

    return "".join(message)


def image_bpcs(image: Image, embed: bool, message: str = None, threshold: float = 0.3, seed: int = None) -> Image | str:
    """Wrapper function to embed or extract message from image using LSB method"""
    sequence = create_sequence((len(message) + 1) * 8, image.width * image.height, seed)
    if embed:
        assert message is not None
        return embed_message(image, message, sequence)
    else:
        return extract_message(image, sequence)


if __name__ == "__main__":
    image_path = "samples/01.bmp"
    image = Image.open(image_path).convert("RGB")
    message = "secretmessage"
    seed = 3

    sequence = create_sequence((len(message) + 1) * 8, image.width * image.height, seed)

    embedded_image = embed_message(image, message, sequence)

    print(extract_message(embedded_image, sequence))
