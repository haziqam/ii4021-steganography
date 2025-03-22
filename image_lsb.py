import numpy as np
from PIL import Image
from bit import Bit, get_lsb, set_lsb, get_bit_at_index, set_bit_at_index

from utils import create_sequence, encode_int, decode_int

# TODO:
# 1) Embed-nya ga harus di byte blue (bisa dibuat ganti-gantian)
# 2) Explore case ukuran image ga cukup buat nyimpen pesan
# 3) Explore case image tidak RGB (grayscale ato item putih)
# 3) Explore cara nyimpen message length di image

def set_lsb_at_position(pixels, x: int, y: int, message_bit: Bit, channel: int = None):
    if channel is None:
        b = pixels[x, y]
        b = set_lsb(b, message_bit)
        pixels[x, y] = b
    else:
        b = pixels[x, y, channel]
        b = set_lsb(b, message_bit)
        pixels[x, y, channel] = b

def get_lsb_at_position(pixels, x: int, y: int, channel: int = None) -> Bit:
    b = pixels[x, y] if channel is None else pixels[x, y, channel]
    return get_lsb(b)

def embed_message(image: np.ndarray, message: str, sequence: list[int]) -> Image:
    # Prepend message length to message (as an 8-bit char)
    message_length = encode_int(len(message))
    message = message_length + message

    if image.ndim == 3:
        _, width, channels = image.shape
        height_mod = width * channels
        # Embed message
        for idx, c in enumerate(message):
            seq_idx = idx * 8
            for i in range(8):
                target_idx = sequence[seq_idx + i]
                x = target_idx // height_mod
                y = (target_idx % height_mod) // channels
                channel = target_idx % channels
                message_bit = get_bit_at_index(ord(c), i)
                set_lsb_at_position(image, x, y, message_bit, channel)
    else:
        _, width = image.shape
        # Embed message
        for idx, c in enumerate(message):
            seq_idx = idx * 8
            for i in range(8):
                target_idx = sequence[seq_idx + i]
                x = target_idx % width
                y = target_idx // width
                message_bit = get_bit_at_index(ord(c), i)
                set_lsb_at_position(image, x, y, message_bit)

    return image

def extract_message(image: np.ndarray, sequence: list[int]) -> str:
    if image.ndim == 3:
        _, width, channels = image.shape # Extract message length (first 64 bits)
        height_mod = width * channels
        message_length = 0

        # Extract message
        message: list[int] = []
        for idx in range(8):
            seq_idx = idx * 8
            current_byte = 0
            for j in range(8):
                target_idx = sequence[seq_idx + j]
                x = target_idx // height_mod
                y = (target_idx % height_mod) // channels
                channel = target_idx % channels
                message_bit = get_lsb_at_position(image, x, y, channel)
                current_byte = set_bit_at_index(current_byte, j, message_bit)

            message.append(current_byte)
        message_length = decode_int(bytes(message).decode("utf-8"))

        # Extract message
        message: list[str] = []
        for idx in range(8, message_length + 8):
            seq_idx = idx * 8
            current_byte = 0
            for j in range(8):
                target_idx = sequence[seq_idx + j]
                x = target_idx // height_mod
                y = (target_idx % height_mod) // channels
                channel = target_idx % channels
                message_bit = get_lsb_at_position(image, x, y, channel)
                current_byte = set_bit_at_index(current_byte, j, message_bit)

            message.append(chr(current_byte))

    else:
        _, width = image.shape
        # Extract message length (first 64 bits)
        message_length = 0
        for i in range(8):
            target_idx = sequence[i]
            x = target_idx % width
            y = target_idx // width
            message_bit = get_lsb_at_position(image, x, y)
            message_length = set_bit_at_index(message_length, i, message_bit)

        # Extract message
        message: list[str] = []
        for idx in range(1, message_length + 1):
            seq_idx = idx * 8
            current_byte = 0
            for j in range(8):
                target_idx = sequence[seq_idx + j]
                x = target_idx % width
                y = target_idx // width
                message_bit = get_lsb_at_position(image, x, y)
                current_byte = set_bit_at_index(current_byte, j, message_bit)

            message.append(chr(current_byte))

    return "".join(message)


def image_lsb(image: np.ndarray, embed: bool, message: str = None, seed: int = None):
    """Wrapper function to embed or extract message from image using LSB method"""
    sequence = create_sequence(image.size, seed)
    if embed:
        assert message is not None
        return embed_message(image, message, sequence)
    else:
        return extract_message(image, sequence)


if __name__ == "__main__":
    image_path = "samples/01.bmp"
    image = np.asarray(Image.open(image_path), dtype=np.int8)
    message = "secretmessage"
    seed = 3

    sequence = create_sequence(image.size, seed)
    # print(f"length of seq is {len(sequence)}")

    embedded_image = embed_message(image, message, sequence)

    print(extract_message(embedded_image, sequence))
