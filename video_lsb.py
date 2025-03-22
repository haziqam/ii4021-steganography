from PIL import Image
import imageio.v3 as iio
import numpy as np
from image_lsb import embed_message, extract_message


def video_to_frames(video_path: str) -> list[Image.Image]:
    frames = iio.imread(video_path, plugin="pyav", index=None)
    pillow_frames = [Image.fromarray(frame) for frame in frames]
    return pillow_frames

def frames_to_video(frames: list[Image.Image], output_path: str, fps: int = 30):
    frame_arrays = [np.array(frame) for frame in frames]
    iio.imwrite(output_path, frame_arrays, plugin="pyav", fps=fps)