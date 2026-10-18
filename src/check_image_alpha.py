"""Check whether RGBA images contain any non-opaque pixels."""

from pathlib import Path
from PIL import Image
import numpy as np

IMAGE_DIR = Path("datasets/trees")
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

def main() -> None:
    paths = sorted(
        p for p in IMAGE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not paths:
        raise SystemExit(f"No supported images found in {IMAGE_DIR.resolve()}")

    any_transparency = False
    for path in paths:
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            alpha = np.asarray(rgba.getchannel("A"))
            alpha_min = int(alpha.min())
            alpha_max = int(alpha.max())
            transparent_pixels = int(np.count_nonzero(alpha < 255))
            pixel_count = int(alpha.size)
            has_transparency = transparent_pixels > 0
            any_transparency = any_transparency or has_transparency

            print(f"{path.name}:")
            print(f"  Alpha range: {alpha_min} to {alpha_max}")
            print(f"  Pixels not fully opaque: {transparent_pixels:,} / {pixel_count:,}")
            print(f"  Contains transparency: {'yes' if has_transparency else 'no'}")

    print()
    if any_transparency:
        print("At least one image has transparency; inspect its appearance before converting.")
    else:
        print("All inspected images are fully opaque; converting RGBA to RGB would not discard visible transparency.")

if __name__ == "__main__":
    main()
