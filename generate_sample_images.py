from pathlib import Path
import numpy as np
from PIL import Image


OUTPUT_DIR = Path("dataset/raw")


def generate_random_image(width: int, height: int, filename: str):
    array = np.random.randint(
        0,
        255,
        (height, width, 3),
        dtype=np.uint8
    )

    image = Image.fromarray(array)
    image.save(OUTPUT_DIR / filename)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    samples = [
        (640, 480, "sample_01.jpg"),
        (800, 600, "sample_02.jpg"),
        (1024, 768, "sample_03.jpg"),
        (512, 512, "sample_04.png"),
        (300, 900, "sample_05.jpg"),
    ]

    for width, height, name in samples:
        generate_random_image(width, height, name)

    print("Sample images generated in dataset/raw")


if __name__ == "__main__":
    main()
