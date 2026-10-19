"""Integration tests for the YOLO dataset validator CLI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "src" / "validate_yolo_dataset.py"


def run_validator(images_dir: Path, labels_dir: Path) -> subprocess.CompletedProcess[str]:
    """Run the validator against temporary image and label folders."""
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--images-dir",
            str(images_dir),
            "--labels-dir",
            str(labels_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def make_dataset(tmp_path: Path) -> tuple[Path, Path]:
    """Create a tiny synthetic dataset; image contents are not decoded by this validator."""
    images_dir = tmp_path / "images"
    labels_dir = tmp_path / "labels"
    images_dir.mkdir()
    labels_dir.mkdir()
    (images_dir / "sample.jpg").write_bytes(b"test image placeholder")
    return images_dir, labels_dir


def test_valid_yolo_label_passes(tmp_path: Path) -> None:
    images_dir, labels_dir = make_dataset(tmp_path)
    (labels_dir / "sample.txt").write_text(
        "0 0.5 0.5 0.2 0.2\n",
        encoding="utf-8",
    )

    result = run_validator(images_dir, labels_dir)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Validation PASSED" in result.stdout
    assert "sample.txt: 1 valid tree box(es)" in result.stdout


def test_box_outside_image_fails(tmp_path: Path) -> None:
    images_dir, labels_dir = make_dataset(tmp_path)
    (labels_dir / "sample.txt").write_text(
        "0 0.05 0.5 0.2 0.2\n",
        encoding="utf-8",
    )

    result = run_validator(images_dir, labels_dir)

    assert result.returncode == 1
    assert "box extends beyond the left/right image boundary" in result.stdout


def test_missing_label_is_warning_not_error(tmp_path: Path) -> None:
    images_dir, labels_dir = make_dataset(tmp_path)

    result = run_validator(images_dir, labels_dir)

    assert result.returncode == 0
    assert "Warnings: 1" in result.stdout
    assert "Errors: 0" in result.stdout


def test_label_without_image_fails(tmp_path: Path) -> None:
    images_dir, labels_dir = make_dataset(tmp_path)
    (labels_dir / "orphan.txt").write_text(
        "0 0.5 0.5 0.2 0.2\n",
        encoding="utf-8",
    )

    result = run_validator(images_dir, labels_dir)

    assert result.returncode == 1
    assert "Label has no matching image: orphan.txt" in result.stdout
