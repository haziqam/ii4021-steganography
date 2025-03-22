import numpy as np
from PIL import Image

from bit import get_bit_at_index, set_bit_at_index
from image import get_bit_at_position, set_bit_at_position
from utils import create_sequence, reshuffle_sequence, encode_int, decode_int

# TODO: Explore case ukuran image ga cukup buat nyimpen pesan


def get_complexity(matrix: np.ndarray, plane: int, channel: int | None = None) -> float:
    height, width = matrix.shape

    k = 0
    n = height * width

    print([get_bit_at_position(matrix[0, col], plane, channel) for col in range(width)])
    # curr_row = np.apply_along_axis(get_bit_at_position, 1, )
    curr_row = np.array([get_bit_at_position(matrix, 0, col, plane) for col in range(width)])
    print(curr_row)
    for row in range(1, width):
        next_row = np.array([get_bit_at_position(matrix[row, col], plane) for col in range(width)])
        print(curr_row)
        print(curr_row[1:])
        k += np.sum(curr_row[:-1] == curr_row[1:])
        k += np.sum(curr_row == next_row)
        curr_row = next_row

    return k/n


def embed_message(image: np.ndarray, message: str, sequence: list[int], plane: int, msg_length: int = None) -> Image:
    if plane == 0:
        # Prepend message length to message (as an 8-bit char)
        message_length = encode_int(msg_length)
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
                set_bit_at_position(image, x, y, message_bit, channel, plane)
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
                set_bit_at_position(image, x, y, message_bit)

    return image


def extract_message(image: np.ndarray, sequence: list[int], plane: int, message_length: int = None):
    if image.ndim == 3:
        _, width, channels = image.shape  # Extract message length (first 64 bits)
        height_mod = width * channels

        if plane == 0:
            # Extract message
            length_bytes: bytearray = bytearray()
            for idx in range(8):
                seq_idx = idx * 8
                current_byte = 0
                for j in range(8):
                    target_idx = sequence[seq_idx + j]
                    x = target_idx // height_mod
                    y = (target_idx % height_mod) // channels
                    channel = target_idx % channels
                    message_bit = get_bit_at_position(image, x, y, channel, plane)
                    current_byte = set_bit_at_index(current_byte, j, message_bit)

                length_bytes.append(current_byte)
            message_length = decode_int(bytes(length_bytes))

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
                message_bit = get_bit_at_position(image, x, y, channel, plane)
                current_byte = set_bit_at_index(current_byte, j, message_bit)

            message.append(chr(current_byte))

    else:
        _, width, channels = image.shape  # Extract message length (first 64 bits)
        height_mod = width * channels

        if plane == 0:
            # Extract message
            length_bytes: bytearray = bytearray()
            for idx in range(8):
                seq_idx = idx * 8
                current_byte = 0
                for j in range(8):
                    target_idx = sequence[seq_idx + j]
                    x = target_idx % width
                    y = target_idx // width
                    message_bit = get_bit_at_position(image, x, y)
                    current_byte = set_bit_at_index(current_byte, j, message_bit)
                length_bytes.append(current_byte)
            message_length = decode_int(bytes(length_bytes))

        # Extract message
        message: list[str] = []
        for idx in range(1, message_length + 1):
            seq_idx = idx * 8
            current_byte = 0
            for j in range(8):
                target_idx = sequence[seq_idx + j]
                x = target_idx % width
                y = target_idx // width
                message_bit = get_bit_at_position(image, x, y, plane)
                current_byte = set_bit_at_index(current_byte, j, message_bit)

            message.append(chr(current_byte))

    if plane == 0:
        return "".join(message), message_length
    else:
        return "".join(message)


def image_bpcs(image: np.ndarray, embed: bool, message: str = None, threshold: float = 0.3, seed: int = None):
    """Wrapper function to embed or extract message from image using BPCS method"""
    sequence = create_sequence(image.size, seed)
    if embed:
        assert message is not None
        message_parts = [message[i:i + image.size] for i in range(0, len(message), image.size)]
        for plane, message_part in enumerate(message_parts):
            msg_length = len(message) if plane == 0 else None
            embedded_image = embed_message(image, message_part, sequence, plane, msg_length)
            sequence = reshuffle_sequence(sequence, seed)

        return embedded_image
    else:
        message_parts = []
        plane = 0
        sequence = create_sequence(image.size, seed)
        msg_part, msg_length = extract_message(image, sequence, plane)
        message_parts.append(msg_part)
        msg_length = msg_length - image.size + 8  # extra 8 bytes for embedded message length
        while msg_length > 0:
            plane += 1
            sequence = reshuffle_sequence(sequence, seed)
            msg_length = image.size if msg_length > image.size else msg_length
            msg_part = extract_message(image, sequence, plane, )
            message_parts.append(msg_part)
            msg_length -= image.size

        return "".join(message_parts)


if __name__ == "__main__":
    image_path = "samples/01.bmp"
    image = np.asarray(Image.open(image_path), dtype=np.int8)
    message = "secretmessage"
    seed = 3

    sequence = create_sequence(image.size, seed)

    message_parts = [message[i:i + image.size] for i in range(0, len(message), image.size)]
    for plane, message_part in enumerate(message_parts):
        msg_length = len(message) if plane == 0 else None
        embedded_image = embed_message(image, message_part, sequence, plane, msg_length)
        sequence = reshuffle_sequence(sequence, seed)

    message_parts = []
    plane = 0
    sequence = create_sequence(image.size, seed)
    msg_part, msg_length = extract_message(embedded_image, sequence, plane)
    message_parts.append(msg_part)
    msg_length = msg_length - image.size + 8  # extra 8 bytes for embedded message length
    while msg_length > 0:
        plane += 1
        sequence = reshuffle_sequence(sequence, seed)
        msg_length = image.size if msg_length > image.size else msg_length
        msg_part = extract_message(embedded_image, sequence, plane, )
        message_parts.append(msg_part)
        msg_length -= image.size
    print("".join(message_parts))
