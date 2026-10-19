"""Draw YOLO label boxes on copies of images for visual review.

Example:
    python src/preview_yolo_labels.py --image-id 5
    python src/preview_yolo_labels.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def draw_labels(image_path: Path, label_path: Path, output_path: Path) -> int:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    count = 0

    if label_path.exists():
        for line_number, line in enumerate(label_path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 5:
                raise ValueError(f"{label_path}:{line_number}: expected 5 fields")

            class_id = int(parts[0])
            x_center, y_center, box_width, box_height = map(float, parts[1:])

            x1 = (x_center - box_width / 2) * width
            y1 = (y_center - box_height / 2) * height
            x2 = (x_center + box_width / 2) * width
            y2 = (y_center + box_height / 2) * height

            draw.rectangle((x1, y1, x2, y2), outline="red", width=max(2, round(min(width, height) / 300)))
            draw.text((x1 + 3, y1 + 3), f"tree ({class_id})", fill="red", stroke_width=2, stroke_fill="white")
            count += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, quality=95)
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Create image copies with YOLO bounding boxes drawn on them.")
    parser.add_argument("--images-dir", type=Path, default=Path("datasets/trees_rgb"))
    parser.add_argument("--labels-dir", type=Path, default=Path("datasets/annotations"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/label_previews"))
    parser.add_argument("--image-id", help="Optional image basename without extension, e.g. 5")
    args = parser.parse_args()

    if args.image_id:
        image_paths = [args.images_dir / f"{args.image_id}.jpg"]
        if not image_paths[0].is_file():
            parser.error(f"Image not found: {image_paths[0]}")
    else:
        image_paths = sorted(args.images_dir.glob("*.jpg"))

    if not image_paths:
        parser.error(f"No JPG images found in {args.images_dir}")

    total_boxes = 0
    for image_path in image_paths:
        label_path = args.labels_dir / f"{image_path.stem}.txt"
        output_path = args.output_dir / f"{image_path.stem}_preview.jpg"
        count = draw_labels(image_path, label_path, output_path)
        total_boxes += count
        print(f"{image_path.name}: {count} box(es) -> {output_path}")

    print(f"Done. Images previewed: {len(image_paths)}; boxes drawn: {total_boxes}")
    print("Original images and label files were not modified.")


if __name__ == "__main__":
    main()
