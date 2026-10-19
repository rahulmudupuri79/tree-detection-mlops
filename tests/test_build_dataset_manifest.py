"""Tests for dataset inventory and provenance validation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from build_dataset_manifest import build_manifest  # noqa: E402


def make_dataset(root: Path) -> tuple[Path, Path]:
    for split in ("train", "val"):
        (root / "images" / split).mkdir(parents=True)
        (root / "labels" / split).mkdir(parents=True)
        image_path = root / "images" / split / f"{split}_one.png"
        Image.new("RGB", (16, 12), (12, 34, 56)).save(image_path)
        (root / "labels" / split / f"{split}_one.txt").write_text(
            "0 0.5 0.5 0.25 0.25\n",
            encoding="utf-8",
        )
    metadata_path = root / "metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "source": "Synthetic test fixture",
                "source_version": "fixture-v1",
                "license": "CC0-1.0",
                "attribution": "Synthetic data created by this test",
                "access_date": "2026-10-19",
                "notes": "Generated in a temporary directory.",
            }
        ),
        encoding="utf-8",
    )
    return root, metadata_path


def test_manifest_has_stable_fingerprint_and_counts(tmp_path: Path) -> None:
    root, metadata = make_dataset(tmp_path / "dataset")

    first = build_manifest(root, metadata)
    second = build_manifest(root, metadata)

    assert first["dataset_fingerprint_sha256"] == second["dataset_fingerprint_sha256"]
    assert first["image_count"] == 2
    assert first["split_counts"] == {"train": 1, "val": 1, "test": 0}
    assert first["annotation_row_count"] == 2
    assert len(first["files"][0]["image_sha256"]) == 64


def test_missing_label_is_rejected(tmp_path: Path) -> None:
    root, metadata = make_dataset(tmp_path / "dataset")
    (root / "labels" / "train" / "train_one.txt").unlink()

    try:
        build_manifest(root, metadata)
    except ValueError as exc:
        assert "Missing label file" in str(exc)
    else:
        raise AssertionError("Expected missing label to be rejected")


def test_placeholder_provenance_is_rejected(tmp_path: Path) -> None:
    root, metadata = make_dataset(tmp_path / "dataset")
    data = json.loads(metadata.read_text(encoding="utf-8"))
    data["license"] = "REPLACE_WITH_VERIFIED_LICENSE"
    metadata.write_text(json.dumps(data), encoding="utf-8")

    try:
        build_manifest(root, metadata)
    except ValueError as exc:
        assert "placeholder" in str(exc)
    else:
        raise AssertionError("Expected placeholder metadata to be rejected")
