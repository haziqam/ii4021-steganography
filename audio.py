from random import Random
from numpy import ndarray
import soundfile as sf

from bit import get_bit_at_index, set_bit_at_index, set_lsb, get_lsb

def set_lsb_at_position(audio: ndarray, message_bit: int, x: int, y: int | None = None) -> None:
    element = audio[x, y]
    audio[x, y] = set_lsb(element, message_bit)

def get_lsb_at_position(audio: ndarray, x: int, y: int | None = None) -> int:
    return get_lsb(audio[x, y])

def embed_message_sequentially(audio: ndarray, message: str):
    for idx, c in enumerate(message):
        for i in range(8):
            if len(audio.shape) == 1: # Audio is mono: 1 dimensional (message index = audio index)
                message_bit = get_bit_at_index(ord(c), i)
                set_lsb_at_position(audio, message_bit, idx)
            else: # Audio is stereo: 2 dimensional (message is spread across both dimensions)
                _, width = audio.shape
                x = idx % width
                y = idx // width
                message_bit = get_bit_at_index(ord(c), i)
                set_lsb_at_position(audio, message_bit, x, y)

    return audio
            
def embed_message_random_position(audio: ndarray, message: str, seed: int) -> ndarray:
    prng = Random(seed)

    for c in message:
        for i in range(8):
            if len(audio.shape) == 1: # Audio is mono: 1 dimensional
                idx = prng.randint(0, len(audio) - 1)
                message_bit = get_bit_at_index(ord(c), i)
                set_lsb_at_position(audio, message_bit, idx)
            else: # Audio is stereo: 2 dimensional
                height, width = audio.shape
                x = prng.randint(0, width - 1)
                y = prng.randint(0, height - 1)
                message_bit = get_bit_at_index(ord(c), i)
                set_lsb_at_position(audio, message_bit, x, y)

    return audio

def extract_message_sequentially(audio: ndarray, message_length: int) -> str:
    message = ""

    for idx in range(message_length):
        current_byte = 0
        for j in range(8):
            if len(audio.shape) == 1: # Audio is mono: 1 dimensional
                message_bit = get_lsb_at_position(audio, idx)
                current_byte = set_bit_at_index(current_byte, j, message_bit)
            else: # Audio is stereo: 2 dimensional
                _, width = audio.shape
                x = idx % width
                y = idx // width
                message_bit = get_lsb_at_position(audio, x, y)
                current_byte = set_bit_at_index(current_byte, j, message_bit)

        message += chr(current_byte)

    return message

def extract_message_random_position(audio: ndarray, seed: int, message_length: int) -> str:
    prng = Random(seed)
    message = ""

    for _ in range(message_length):
        current_byte = 0
        for j in range(8):
            if len(audio.shape) == 1: # Audio is mono: 1 dimensional
                idx = prng.randint(0, len(audio) - 1)
                message_bit = get_lsb_at_position(audio, idx)
                current_byte = set_bit_at_index(current_byte, j, message_bit)
            else: # Audio is stereo: 2 dimensional
                height, width = audio.shape
                x = prng.randint(0, width - 1)
                y = prng.randint(0, height - 1)
                message_bit = get_lsb_at_position(audio, x, y)
                current_byte = set_bit_at_index(current_byte, j, message_bit)

        message += chr(current_byte)

    return message


if __name__ == '__main__':
    message = "secretmessage"
    
    audio1, sr1 = sf.read('samples/01-mono.wav')
    print(audio1.shape, audio1.dtype, sr1)
    # embedded_audio1 = embed_message_sequentially(audio1, message)
    # extracted_message1 = extract_message_sequentially(audio1, len(message))
    # print(extracted_message1)

    audio2, sr2 = sf.read('samples/01-stereo.wav')
    print(audio2.shape, audio2.dtype, sr2)
    # embedded_audio2 = embed_message_sequentially(audio2, message)
    # extracted_message2 = extract_message_sequentially(audio2, len(message))
    # print(extracted_message2)