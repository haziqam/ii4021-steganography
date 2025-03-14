from PIL import Image
from bit import Bit, get_lsb, set_lsb, get_bit_at_index, set_bit_at_index

from utils import create_sequence

# TODO:
# 1) Embed-nya ga harus di byte blue (bisa dibuat ganti-gantian)
# 2) Explore case ukuran image ga cukup buat nyimpen pesan
# 3) Explore case image tidak RGB (grayscale ato item putih)
# 3) Explore cara nyimpen message length di image

def set_lsb_at_position(pixels, x: int, y: int, message_bit: Bit):
    r, g, b = pixels[x, y]
    b = set_lsb(b, message_bit)
    pixels[x, y] = (r, g, b)

def get_lsb_at_position(pixels, x: int, y: int) -> Bit:
    _, _, b = pixels[x, y]
    return get_lsb(b)

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
        message_bit = get_lsb_at_position(pixels, x, y)
        message_length = set_bit_at_index(message_length, i, message_bit)

    # Extract message
    message: list[str] = []
    for idx in range(1, message_length + 1):
        current_byte = 0
        for j in range(8):
            target_idx = sequence[idx * 8 + j]
            x = target_idx % width
            y = target_idx // width
            message_bit = get_lsb_at_position(pixels, x, y)
            current_byte = set_bit_at_index(current_byte, j, message_bit)

        message.append(chr(current_byte))

    return "".join(message)

if __name__ == "__main__":
    image_path = "samples/01.bmp"
    image = Image.open(image_path).convert("RGB")
    message = "secretmessage"
    seed = 3

    sequence = create_sequence((len(message) + 1) * 8, image.width * image.height, seed)

    embedded_image = embed_message(image, message, sequence)

    print(extract_message(embedded_image, sequence))
