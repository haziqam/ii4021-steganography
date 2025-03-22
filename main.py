import sys
from argparse import ArgumentParser
from enum import Enum

import numpy as np


class ProgramMode(Enum):
    EMBED = "embed"
    EXTRACT = "extract"

    def __str__(self):
        return self.value

    def is_embed(self):
        return self == self.EMBED


class SteganoFormat(Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"

    def __str__(self):
        return self.value


class SteganoMethod(Enum):
    LSB = "lsb"
    BPCS = "bpcs"

    def __str__(self):
        return self.value


if __name__ == "__main__":
    argparse = ArgumentParser("II4021 Steganography tool")
    argparse.add_argument("file", type=str, help="input file path to embed message")
    argparse.add_argument("mode", type=ProgramMode, choices=list(ProgramMode), help="mode to embed or extract message in the stegano media")
    argparse.add_argument(
        "format",
        type=SteganoFormat,
        choices=list(SteganoFormat),
        help="file format for steganography",
    )
    argparse.add_argument(
        "method",
        type=SteganoMethod,
        choices=list(SteganoMethod),
        help="Steganography method for the file specified, note that the method must be suitable with the file format",
    )
    argparse.add_argument(
        "--seed",
        type=int,
        nargs="?",
        help="seed for pseudo-random generator to obscure message & steganography process",
    )
    argparse.add_argument(
        "--out",
        type=str,
        default="result",
        help="result file name",
    )
    args = argparse.parse_args()
    file_path: str = args.file
    mode: ProgramMode = args.mode
    stegano_format: SteganoFormat = args.format
    stegano_method: SteganoMethod = args.method
    seed: int | None = args.seed
    out: str = args.out

    is_embed = mode.is_embed()
    if is_embed:
        message_lines: list[str] = []
        for line in sys.stdin:
            message_lines.append(line)

        message = "".join(message_lines)
    else:
        message = None

    match stegano_format:
        # Use lazy import, does it make sense here? 🤔
        case SteganoFormat.IMAGE:
            from PIL import Image
            image = Image.open(file_path)
            image_mat = np.asarray(image, dtype=np.int8)
            match stegano_method:
                case SteganoMethod.LSB:
                    from image_lsb import image_lsb
                    result = image_lsb(image_mat, is_embed, message, seed)

                case SteganoMethod.BPCS:
                    from image_bpcs import image_bpcs
                    result = image_bpcs(image_mat, is_embed, message, seed)
                case _:
                    result = None

            if is_embed:
                img: Image = Image.fromarray(result.astype(np.uint8))
                img.save(out)
            else:
                with open(out, "w") as f:
                    f.write(result)

        case SteganoFormat.AUDIO:
            pass
        case SteganoFormat.VIDEO:
            pass
