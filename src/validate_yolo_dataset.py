"""Validate YOLO detection labels against a folder of images.

Example:
    python src/validate_yolo_dataset.py --images-dir datasets/trees_rgb --labels-dir datasets/annotations
"""

from __future__ import annotations

import argparse
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check image/label pairing and YOLO detection label values."
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        required=True,
        help="Folder containing image files.",
    )
    parser.add_argument(
        "--labels-dir",
        type=Path,
        required=True,
        help="Folder containing YOLO .txt label files.",
    )
    parser.add_argument(
        "--class-count",
        type=int,
        default=1,
        help="Number of classes in the dataset (default: 1 for the tree class).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    images_dir = args.images_dir
    labels_dir = args.labels_dir

    if not images_dir.is_dir():
        print(f"ERROR: image directory does not exist: {images_dir.resolve()}")
        return 2
    if not labels_dir.is_dir():
        print(f"ERROR: label directory does not exist: {labels_dir.resolve()}")
        return 2
    if args.class_count < 1:
        print("ERROR: --class-count must be at least 1.")
        return 2

    images = sorted(
        p for p in images_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )
    labels = sorted(
        p for p in labels_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".txt"
    )

    if not images:
        print(f"ERROR: no supported images found in {images_dir.resolve()}")
        return 2

    image_stems = {p.stem for p in images}
    label_stems = {p.stem for p in labels}
    missing_labels = sorted(image_stems - label_stems)
    orphan_labels = sorted(label_stems - image_stems)

    errors: list[str] = []
    warnings: list[str] = []

    print(f"Images directory: {images_dir.resolve()}")
    print(f"Labels directory: {labels_dir.resolve()}")
    print(f"Images found: {len(images)}")
    print(f"Label files found: {len(labels)}")
    print()

    for stem in missing_labels:
        warnings.append(f"Image has no matching label file: {stem} (unlabeled or empty-label file missing)")
    for stem in orphan_labels:
        errors.append(f"Label has no matching image: {stem}.txt")

    for label_path in labels:
        if label_path.stem not in image_stems:
            continue
        try:
            lines = label_path.read_text(encoding="utf-8-sig").splitlines()
        except OSError as exc:
            errors.append(f"{label_path.name}: could not read file: {exc}")
            continue

        object_count = 0
        for line_number, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line:
                continue
            parts = line.split()
            location = f"{label_path.name}:{line_number}"
            if len(parts) != 5:
                errors.append(
                    f"{location}: expected 5 values (class_id x_center y_center width height), got {len(parts)}"
                )
                continue

            try:
                class_float = float(parts[0])
                coords = [float(value) for value in parts[1:]]
            except ValueError:
                errors.append(f"{location}: all five values must be numeric")
                continue

            if not class_float.is_integer():
                errors.append(f"{location}: class ID must be an integer, got {parts[0]!r}")
                continue
            class_id = int(class_float)
            if not 0 <= class_id < args.class_count:
                errors.append(
                    f"{location}: class ID {class_id} is outside 0..{args.class_count - 1}"
                )
                continue
            if not all(0.0 <= value <= 1.0 for value in coords):
                errors.append(f"{location}: normalized coordinates must be between 0 and 1")
                continue

            x_center, y_center, width, height = coords
            if width <= 0 or height <= 0:
                errors.append(f"{location}: box width and height must be greater than zero")
                continue
            if x_center - width / 2 < -1e-6 or x_center + width / 2 > 1 + 1e-6:
                errors.append(f"{location}: box extends beyond the left/right image boundary")
                continue
            if y_center - height / 2 < -1e-6 or y_center + height / 2 > 1 + 1e-6:
                errors.append(f"{location}: box extends beyond the top/bottom image boundary")
                continue

            object_count += 1

        print(f"{label_path.name}: {object_count} valid tree box(es)")

    print()
    print(f"Warnings: {len(warnings)}")
    for item in warnings:
        print(f"WARNING: {item}")
    print(f"Errors: {len(errors)}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors:
        print("\nValidation FAILED. Fix errors before training.")
        return 1
    if warnings:
        print("\nLabel values passed, but review the missing-label warnings.")
        print("Images reserved for testing may intentionally have no labels yet.")
        return 0

    print("\nValidation PASSED: image/label pairs and YOLO label values look structurally valid.")
    print("This checks file structure, not whether the boxes visually match the trees.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
