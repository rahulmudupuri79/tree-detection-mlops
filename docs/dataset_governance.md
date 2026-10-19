# Dataset governance for tree detection

This project treats a dataset as a versioned ML input, not just a folder of images. A model result is only interpretable when we can identify the exact image/annotation files, their split, and their permitted use.

## Required dataset contract

Use this layout for a dataset prepared for training:

```text
datasets/<dataset-name>/
├── images/
│   ├── train/
│   ├── val/
│   └── test/        # optional until a held-out test set is ready
├── labels/
│   ├── train/
│   ├── val/
│   └── test/        # required if images/test exists
└── dataset_metadata.json
```

Every image used in a split must have a same-stem YOLO label file. If an image contains no target objects, use an empty label file; do not omit the file, because a missing label is ambiguous between "no objects" and "not annotated." Keep the test split out of training and routine hyperparameter tuning.

## Provenance metadata

Copy `configs/dataset_metadata.example.json` to `dataset_metadata.json` and fill in the actual values before creating a manifest:

- **source**: dataset owner and canonical URL or acquisition method.
- **source_version**: release, DOI, commit, or a documented acquisition date/version.
- **license**: exact license or terms that apply to the specific imagery and annotations.
- **attribution**: required citation or attribution text; use an explicit value such as "No attribution required under <license>" only after verifying it.
- **access_date**: date the source was accessed or downloaded.
- **notes**: relevant restrictions, transformations, and decisions.

Do not treat a repository's code license as proof that its underlying images have the same license. Do not train on, redistribute, or publish artifacts derived from data until the applicable rights permit the intended use.

## Dataset manifest and fingerprint

Run the existing YOLO structural validator first. Then build a manifest:

```powershell
python src/validate_yolo_dataset.py --images-dir datasets/<dataset-name>/images/train --labels-dir datasets/<dataset-name>/labels/train
python src/build_dataset_manifest.py --dataset-root datasets/<dataset-name> --metadata datasets/<dataset-name>/dataset_metadata.json --output artifacts/dataset_manifest.json
```

The manifest records each image and label file's relative path and SHA-256, image dimensions/format, and annotation-row count. Its dataset fingerprint is derived from the sorted file inventory and hashes. This makes changes detectable even if filenames stay the same.

The manifest is an identity and audit artifact, not proof that labels are visually correct, that the data license is valid, or that the split is statistically representative. Keep the manifest with experiment records; keep raw data out of Git unless size and license explicitly allow committing it.

## Split and leakage rules

- Split by independent source groups where possible (for example, location, acquisition flight, or video), not by randomly scattering near-duplicate frames across splits.
- Fit preprocessing and any data-derived statistics using training data only.
- Use validation data for model selection; reserve test data for final evaluation.
- When data or labels change, create a new dataset fingerprint and rerun validation. Never overwrite the record for an earlier experiment.
- Record label-review status separately: structural checks cannot determine whether a human drew correct boxes around tree crowns.

## Current project status

The previous small experiment used seven labeled images and only two validation images, and its measured detection quality was very poor. That is a learning baseline, not a reliable detector. The earlier screenshots were described as Google Maps imagery; do not use them for additional training or publish derived artifacts until the applicable terms are confirmed. Prefer a dataset whose specific imagery and annotations explicitly permit the intended ML use.
