import numpy as np
import soundfile as sf

from bit import Bit, get_bit_at_index, set_bit_at_index, set_lsb, get_lsb
from utils import create_sequence

def set_lsb_at_position(audio: np.ndarray, message_bit: Bit, i: int, j: int | None = None) -> None:
    if j is None:
        audio[i] = set_lsb(audio[i], message_bit)
    else:
        audio[i, j] = set_lsb(audio[i, j], message_bit)

def get_lsb_at_position(audio: np.ndarray, i: int, j: int | None = None) -> Bit:
    return get_lsb(audio[i, j])

def embed_message(audio: np.ndarray, message: str, sequence: list[int]):
    # Prepend message length to message (as an 8-bit char)
    message_length_in_byte = chr(len(message))
    message = message_length_in_byte + message

    # Embed message
    for idx, c in enumerate(message):
        for i in range(8):
            position = idx * 8 + i
            if len(audio.shape) == 1: # Audio is mono: 1 dimensional (message index = audio index)
                message_bit = get_bit_at_index(ord(c), i)
                set_lsb_at_position(audio, message_bit, sequence[position])
            else: # Audio is stereo: 2 dimensional (message is spread across both dimensions)
                _, width = audio.shape
                message_bit = get_bit_at_index(ord(c), i)
                target_idx = sequence[position]
                dim1 = target_idx // width 
                dim2 = target_idx % width
                set_lsb_at_position(audio, message_bit, dim1, dim2)

    return audio

def extract_message(audio: np.ndarray, message_length: int, sequence: list[int]) -> str:
    # Extract message length (first 8 bits)
    message_length = 0
    for j in range(8):
        if len(audio.shape) == 1: # Audio is mono: 1 dimensional
            message_bit = get_lsb_at_position(audio, sequence[j])
            message_length = set_bit_at_index(message_length, j, message_bit)
        else: # Audio is stereo: 2 dimensional
            _, width = audio.shape
            target_idx = sequence[j]
            dim1 = target_idx // width
            dim2 = target_idx % width
            message_bit = get_lsb_at_position(audio, dim1, dim2)
            message_length = set_bit_at_index(message_length, j, message_bit)

    # Extract message
    message: list[str] = []
    for idx in range(1, message_length + 1):
        current_byte = 0
        for j in range(8):
            position = idx * 8 + j
            if len(audio.shape) == 1: # Audio is mono: 1 dimensional
                message_bit = get_lsb_at_position(audio, sequence[position])
                current_byte = set_bit_at_index(current_byte, j, message_bit)
            else: # Audio is stereo: 2 dimensional
                _, width = audio.shape
                target_idx = sequence[position]
                dim1 = target_idx // width
                dim2 = target_idx % width
                message_bit = get_lsb_at_position(audio, dim1, dim2)
                current_byte = set_bit_at_index(current_byte, j, message_bit)

        message.append(chr(current_byte))

    return "".join(message)

if __name__ == '__main__':
    message = "lorem ipsum dolor"
    seed = 5
    
    audio1, sr1 = sf.read('samples/01-mono.wav', dtype='int16')
    print(audio1.shape, audio1.dtype, sr1)
    sequence1 = create_sequence((len(message) + 1) * 8, audio1.shape[0], None)
    embedded_audio1 = embed_message(audio1, message, sequence1)
    sf.write(
        'samples/01-mono-result-sequential.wav', 
        embedded_audio1,
        sr1,
        subtype='PCM_16'
    )

    embedded_audio_from_file1, sr_from_file1 = sf.read('samples/01-mono-result-sequential.wav', dtype='int16')
    print(embedded_audio_from_file1.shape, embedded_audio_from_file1.dtype, sr_from_file1)
    extracted_message_from_file1 = extract_message(embedded_audio_from_file1, len(message), sequence1)
    print(extracted_message_from_file1)


    audio2, sr2 = sf.read('samples/01-stereo.wav', dtype='int16')
    print(audio2.shape, audio2.dtype, sr2)
    sequence2 = create_sequence((len(message) + 1) * 8, audio2.shape[0] * audio2.shape[1], None)
    embedded_audio2 = embed_message(audio2, message, sequence2)
    sf.write(
        'samples/01-stereo-result-sequential.wav', 
        embedded_audio2,
        sr2,
        subtype='PCM_16'
    )

    embedded_audio_from_file2, sr_from_file2 = sf.read('samples/01-stereo-result-sequential.wav', dtype='int16')
    print(embedded_audio_from_file2.shape, embedded_audio_from_file2.dtype, sr_from_file2)
    extracted_message_from_file2 = extract_message(embedded_audio_from_file2, len(message), sequence2)
    print(extracted_message_from_file2)


    audio3, sr3 = sf.read('samples/01-mono.wav', dtype='int16')
    print(audio3.shape, audio3.dtype, sr3)
    sequence3 = create_sequence((len(message) + 1) * 8, audio3.shape[0], seed)
    embedded_audio3 = embed_message(audio3, message, sequence3)
    sf.write(
        'samples/01-mono-result-random.wav', 
        embedded_audio3,
        sr3,
        subtype='PCM_16'
    )

    embedded_audio_from_file3, sr_from_file3 = sf.read('samples/01-mono-result-random.wav', dtype='int16')
    print(embedded_audio_from_file3.shape, embedded_audio_from_file3.dtype, sr_from_file3)
    extracted_message_from_file1 = extract_message(embedded_audio_from_file3, len(message), sequence3)
    print(extracted_message_from_file1)


    audio4, sr4 = sf.read('samples/01-stereo.wav', dtype='int16')
    print(audio4.shape, audio4.dtype, sr4)
    sequence4 = create_sequence((len(message) + 1) * 8, audio4.shape[0] * audio4.shape[1], seed)
    embedded_audio4 = embed_message(audio4, message, sequence4)
    sf.write(
        'samples/01-stereo-result-random.wav', 
        embedded_audio4,
        sr4,
        subtype='PCM_16'
    )

    embedded_audio_from_file4, sr_from_file4 = sf.read('samples/01-stereo-result-random.wav', dtype='int16')
    print(embedded_audio_from_file4.shape, embedded_audio_from_file4.dtype, sr_from_file4)
    extracted_message_from_file4 = extract_message(embedded_audio_from_file4, len(message), sequence4)
    print(extracted_message_from_file4)