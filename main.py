import sys
from argparse import ArgumentParser
from enum import Enum

from PIL import Image

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
    argparse.add_argument(
        "--format",
        type=SteganoFormat,
        choices=list(SteganoFormat),
        help="file format for steganography",
    )
    argparse.add_argument(
        "--method",
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
    stegano_format: SteganoFormat = args.format
    stegano_method: SteganoMethod = args.method
    seed: int | None = args.seed

    print(file_path, stegano_format, seed)

    message_lines: list[str] = []
    for line in sys.stdin:
        message_lines.append(line)

    message = "".join(message_lines)

    match stegano_format:
        # Use lazy import, does it make sense here? 🤔
        case SteganoFormat.IMAGE:
            match stegano_method:
                case SteganoMethod.LSB:
                    from image_lsb import image_lsb
                case SteganoMethod.BPCS:
                    from image_bpcs import image_bpcs
            pass
        case SteganoFormat.AUDIO:
            pass
        case SteganoFormat.VIDEO:
            pass
