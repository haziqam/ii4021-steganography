import matplotlib.pyplot as plt
from PIL import Image

def show_images(plain_image_path: str, stego_image_path: str):
    plain_image = Image.open(plain_image_path)
    stego_image = Image.open(stego_image_path)

    _, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(plain_image)
    axes[0].axis("off")
    axes[0].set_title("")

    axes[1].imshow(stego_image)
    axes[1].axis("off")
    axes[1].set_title("Image 2")

    plt.show()

if __name__ == "__main__":
    show_images("samples/01.bmp", "samples/stego.bmp")