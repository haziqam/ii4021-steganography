from bit import Bit, get_bit_at_index, set_bit_at_index


def set_bit_at_position(pixels, x: int, y: int, message_bit: Bit, channel: int = None, plane: int = 0):
    if channel is None:
        b = pixels[x, y]
        b = set_bit_at_index(b, plane, message_bit)
        pixels[x, y] = b
    else:
        b = pixels[x, y, channel]
        b = set_bit_at_index(b, plane, message_bit)
        pixels[x, y, channel] = b


def get_bit_at_position(pixels, x: int, y: int, channel: int = None, plane: int = 0) -> Bit:
    b = pixels[x, y] if channel is None else pixels[x, y, channel]
    return get_bit_at_index(b, plane)
