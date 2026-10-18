"""Inspect the nine local tree images without modifying them."""

from pathlib import Path
from PIL import Image

IMAGE_DIR = Path("datasets/trees")
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

def main() -> None:
    if not IMAGE_DIR.exists():
        raise SystemExit(
            f"Image folder not found: {IMAGE_DIR.resolve()}\n"
            "Run this script from the project root."
        )

    paths = sorted(
        p for p in IMAGE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not paths:
        raise SystemExit(f"No supported images found in {IMAGE_DIR.resolve()}")

    print(f"Image folder: {IMAGE_DIR.resolve()}")
    print(f"Images found: {len(paths)}")
    print()

    dimensions = set()
    for path in paths:
        with Image.open(path) as image:
            width, height = image.size
            dimensions.add((width, height))
            print(f"File: {path.name}")
            print(f"  Format: {image.format}")
            print(f"  Mode: {image.mode}")
            print(f"  Size (width x height): {width} x {height}")
            print(f"  File size: {path.stat().st_size:,} bytes")
            print()

    if len(dimensions) == 1:
        width, height = next(iter(dimensions))
        print(f"All images share dimensions: {width} x {height}")
    else:
        print("Images have different dimensions:")
        for width, height in sorted(dimensions):
            print(f"  {width} x {height}")

if __name__ == "__main__":
    main()
