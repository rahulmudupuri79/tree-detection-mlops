"""Create RGB copies of the tree images without altering the originals."""

from pathlib import Path
from PIL import Image

SOURCE_DIR = Path("datasets/trees")
OUTPUT_DIR = Path("datasets/trees_rgb")
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

def main() -> None:
    if not SOURCE_DIR.is_dir():
        raise SystemExit(f"Image folder not found: {SOURCE_DIR.resolve()}")

    paths = sorted(
        p for p in SOURCE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not paths:
        raise SystemExit(f"No supported images found in {SOURCE_DIR.resolve()}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Reading originals from: {SOURCE_DIR.resolve()}")
    print(f"Writing RGB copies to: {OUTPUT_DIR.resolve()}")
    print("Original files will not be modified.")
    print()

    for path in paths:
        with Image.open(path) as image:
            rgb = image.convert("RGB")
            output_path = OUTPUT_DIR / f"{path.stem}.jpg"
            rgb.save(output_path, format="JPEG", quality=95)
            print(
                f"{path.name} -> {output_path.name} "
                f"({rgb.width} x {rgb.height}, RGB)"
            )

    print()
    print(f"Created {len(paths)} RGB JPEG copies in {OUTPUT_DIR}.")

if __name__ == "__main__":
    main()
