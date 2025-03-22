import imageio.v3 as iio
import numpy as np

import image_lsb
from utils import create_sequence, encode_int, decode_int


def video_to_frames(video_path: str) -> np.ndarray:
    return iio.imread(video_path, plugin="pyav", index=None).astype(np.int8, copy=False)


def frames_to_video(frames: list[np.ndarray], output_path: str, fps: int = 30):
    with iio.imopen(output_path, "w", plugin="pyav") as out_file:
        out_file.init_video_stream("libx264", fps=fps)
        out_file.write(frames)


def embed_message(frames: list[np.ndarray], message: str, seed: int):
    frames_sequence = create_sequence(len(frames), seed)
    message_parts = [message[i:i + frames[0].size // 2] for i in range(0, len(message), frames[0].size // 2)]
    frames_count = encode_int(len(message_parts))

    start_frame = frames[frames_sequence[0]]
    msg_sequence = create_sequence(start_frame.size, seed)
    image_lsb.embed_message(start_frame, frames_count, msg_sequence)

    for message_part, frame_idx in zip(message_parts, frames_sequence[1:]):
        msg_sequence = create_sequence(frames[frame_idx].size, seed)
        image_lsb.embed_message(frames[frame_idx], message_part, msg_sequence)

    return frames


def extract_message(frames: list[np.ndarray], seed: int):
    frames_sequence = create_sequence(len(frames), seed)

    start_frame = frames[frames_sequence[0]]
    msg_sequence = create_sequence(start_frame.size, seed)
    frames_count_str = image_lsb.extract_message(start_frame, msg_sequence)
    frames_count = decode_int(bytes(ord(x) for x in frames_count_str))
    frames_count = 1

    message_parts: list[str] = []
    for frame_idx in frames_sequence[1:frames_count + 1]:
        msg_sequence = create_sequence(frames[frame_idx].size, seed)
        message_part = image_lsb.extract_message(frames[frame_idx], msg_sequence)
        message_parts.append(message_part)
    return "".join(message_parts)


def video_lsb(video: list[np.ndarray], embed: bool, message: str = None, seed: int = None):
    """Wrapper function to embed or extract message from video using LSB method"""
    if embed:
        assert message is not None
        return embed_message(video, message, seed)
    else:
        return extract_message(video, seed)


if __name__ == "__main__":
    video = video_to_frames("samples/test.avi")
    message = "secret message !!!"
    seed = 3

    embedded_video = embed_message(video, message, seed)

    result = extract_message(embedded_video, seed)

    print(result)
