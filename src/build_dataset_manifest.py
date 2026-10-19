"""Build a deterministic inventory manifest for a YOLO image dataset.

Run the YOLO structural validator before this script. This script records file
identity and basic image/label metadata; it does not validate box coordinates
or assess visual annotation quality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
REQUIRED_METADATA = ("source", "source_version", "license", "attribution", "access_date")
SPLITS = ("train", "val", "test")
PLACEHOLDER = re.compile(r"replace|todo|unknown|yyyy-mm-dd", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a dataset inventory and SHA-256 fingerprint."
    )
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_metadata(path: Path) -> dict[str, Any]:
    metadata = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a JSON object.")
    for field in REQUIRED_METADATA:
        value = metadata.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Metadata field {field!r} is required.")
        if PLACEHOLDER.search(value):
            raise ValueError(f"Metadata field {field!r} still contains a placeholder.")
    try:
        date.fromisoformat(metadata["access_date"])
    except ValueError as exc:
        raise ValueError("Metadata field 'access_date' must use YYYY-MM-DD.") from exc
    return metadata


def inspect_split(dataset_root: Path, split: str) -> list[dict[str, Any]]:
    images_dir = dataset_root / "images" / split
    labels_dir = dataset_root / "labels" / split
    if not images_dir.is_dir():
        if split == "test" and not labels_dir.exists():
            return []
        raise ValueError(f"Required image split directory is missing: {images_dir}")
    if not labels_dir.is_dir():
        raise ValueError(f"Required label split directory is missing: {labels_dir}")

    images = sorted(
        path for path in images_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not images:
        raise ValueError(f"No supported images found in {images_dir}")

    label_files = {
        path.stem: path
        for path in labels_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".txt"
    }
    image_stems = {path.stem for path in images}
    orphan_labels = sorted(set(label_files) - image_stems)
    if orphan_labels:
        raise ValueError(
            f"Orphan label file(s) in {split}: " + ", ".join(f"{stem}.txt" for stem in orphan_labels)
        )

    records: list[dict[str, Any]] = []
    for image_path in images:
        label_path = label_files.get(image_path.stem)
        if label_path is None:
            raise ValueError(
                f"Missing label file for {split}/{image_path.name}; use an empty .txt "
                "file for an intentionally empty image."
            )
        try:
            with Image.open(image_path) as image:
                image.verify()
            with Image.open(image_path) as image:
                width, height = image.size
                image_format = image.format
                mode = image.mode
        except (OSError, ValueError) as exc:
            raise ValueError(f"Unreadable image {image_path}: {exc}") from exc

        label_text = label_path.read_text(encoding="utf-8-sig")
        annotation_count = sum(1 for line in label_text.splitlines() if line.strip())
        records.append(
            {
                "split": split,
                "image": image_path.relative_to(dataset_root).as_posix(),
                "image_sha256": sha256_file(image_path),
                "width": width,
                "height": height,
                "format": image_format,
                "mode": mode,
                "label": label_path.relative_to(dataset_root).as_posix(),
                "label_sha256": sha256_file(label_path),
                "annotation_rows": annotation_count,
            }
        )
    return records


def build_manifest(dataset_root: Path, metadata_path: Path) -> dict[str, Any]:
    root = dataset_root.resolve()
    if not root.is_dir():
        raise ValueError(f"Dataset root does not exist: {root}")
    metadata = load_metadata(metadata_path)
    records: list[dict[str, Any]] = []
    for split in SPLITS:
        records.extend(inspect_split(root, split))

    if not any(record["split"] == "train" for record in records):
        raise ValueError("Dataset must contain at least one training image.")
    if not any(record["split"] == "val" for record in records):
        raise ValueError("Dataset must contain at least one validation image.")

    fingerprint_input = [
        {
            "split": record["split"],
            "image": record["image"],
            "image_sha256": record["image_sha256"],
            "label": record["label"],
            "label_sha256": record["label_sha256"],
        }
        for record in records
    ]
    fingerprint_bytes = json.dumps(
        fingerprint_input, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    fingerprint = hashlib.sha256(fingerprint_bytes).hexdigest()

    return {
        "manifest_schema_version": 1,
        "dataset_name": root.name,
        "dataset_fingerprint_sha256": fingerprint,
        "metadata": metadata,
        "image_count": len(records),
        "split_counts": {
            split: sum(1 for record in records if record["split"] == split)
            for split in SPLITS
        },
        "annotation_row_count": sum(record["annotation_rows"] for record in records),
        "files": records,
    }


def main() -> int:
    args = parse_args()
    try:
        manifest = build_manifest(args.dataset_root, args.metadata)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Dataset fingerprint: {manifest['dataset_fingerprint_sha256']}")
    print(f"Images: {manifest['image_count']}")
    print(f"Annotation rows: {manifest['annotation_row_count']}")
    print(f"Manifest written to: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
