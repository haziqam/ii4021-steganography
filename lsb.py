from PIL import Image
from bit import get_lsb, set_lsb, get_bit_at_index, set_bit_at_index
from random import Random

# TODO:
# 1) Embed-nya ga harus di byte blue (bisa dibuat ganti-gantian)
# 2) Explore case ukuran image ga cukup buat nyimpen pesan
# 3) Explore case image tidak RGB (grayscale ato item putih)
# 3) Explore cara nyimpen message length di image

def set_lsb_at_position(pixels, x: int, y: int, message_bit: int):
    r, g, b = pixels[x, y]
    b = set_lsb(b, message_bit)
    pixels[x, y] = (r, g, b)

def get_lsb_at_position(pixels, x: int, y: int) -> int:
    _, _, b = pixels[x, y]
    return get_lsb(b)

def embed_message_sequentially(image: Image, message: str) -> Image:
    pixels = image.load()
    width, height = image.size

    for idx, c in enumerate(message):
        for i in range(8):
            x = idx % width
            y = idx // width
            message_bit = get_bit_at_index(ord(c), i)
            set_lsb_at_position(pixels, x, y, message_bit)

    return image

def embed_message_random_position(image: Image, message: str, seed: int) -> Image:
    prng = Random(seed)
    pixels = image.load()
    width, height = image.size

    for c in message:
        for i in range(8):
            x = prng.randint(0, width - 1)
            y = prng.randint(0, height - 1)
            message_bit = get_bit_at_index(ord(c), i)
            set_lsb_at_position(pixels, x, y, message_bit)

    return image

def extract_message_sequentially(image: Image, seed: int, message_length: int) -> str:
    pixels = image.load()
    width, height = image.size

    message = ""
    for idx in range(message_length):
        current_byte = 0
        for j in range(8):
            x = idx % width
            y = idx // width
            message_bit = get_lsb_at_position(pixels, x, y)
            current_byte = set_bit_at_index(current_byte, j, message_bit)

        message += chr(current_byte)

    return message
    
def extract_message_random_position(image: Image, seed: int, message_length: int) -> str:
    prng = Random(seed)
    pixels = image.load()
    width, height = image.size

    message = ""
    for _ in range(message_length):
        current_byte = 0
        for j in range(8):
            x = prng.randint(0, width - 1)
            y = prng.randint(0, height - 1)
            message_bit = get_lsb_at_position(pixels, x, y)
            current_byte = set_bit_at_index(current_byte, j, message_bit)

        message += chr(current_byte)

    return message

if __name__ == "__main__":
    image_path = "samples/01.bmp"
    image = Image.open(image_path).convert("RGB")
    message = "secretmessage"
    seed = 3
    
    embedded_image = embed_message_random_position(image, message, seed)

    
    print(extract_message_random_position(embedded_image, seed, len(message)))
