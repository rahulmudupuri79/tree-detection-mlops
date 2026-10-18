"""Inspect image dimensions, color channels, and pixel values."""

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGE_PATH = ROOT / "artifacts" / "bus_annotated.jpg"


def main() -> None:
    if not IMAGE_PATH.exists():
        raise FileNotFoundError(
            f"Image not found: {IMAGE_PATH}\n"
            "Run src/first_inference.py first to create it."
        )

    with Image.open(IMAGE_PATH) as image:
        print(f"Image path: {IMAGE_PATH}")
        print(f"Image format: {image.format}")
        print(f"Image mode: {image.mode}")
        print(f"Image size (width, height): {image.size}")

        rgb_image = image.convert("RGB")
        pixels = np.asarray(rgb_image)

    height, width, channels = pixels.shape
    print(f"Array shape (height, width, channels): {pixels.shape}")
    print(f"Array data type: {pixels.dtype}")
    print(f"Number of pixels: {height * width:,}")
    print(f"Channels: {channels} (R, G, B)")
    print(f"First pixel RGB values: {pixels[0, 0].tolist()}")
    print(f"Center pixel RGB values: {pixels[height // 2, width // 2].tolist()}")
    print(f"Minimum channel value: {int(pixels.min())}")
    print(f"Maximum channel value: {int(pixels.max())}")
    print(f"Mean channel value: {pixels.mean(axis=(0, 1)).round(2).tolist()}")


if __name__ == "__main__":
    main()
