# Tree Detection & MLOps Learning Lab

A hands-on, incremental project for learning computer vision and the **machine-learning lifecycle**: data governance, reproducible training, experiment tracking, model evaluation, registry/lineage, and monitoring.

## Learning approach

We work one milestone at a time. Commands and results are only marked complete after they have been run and verified. The API/container work is supporting engineering, not the main learning objective.

## MLOps-first roadmap

1. **Dataset governance:** verify provenance and permitted use, validate images/labels, create a deterministic dataset manifest and fingerprint, and prevent split leakage.
2. **Reproducible training pipeline:** make dataset/configuration/code inputs explicit and capture outputs consistently.
3. **Experiment tracking:** log parameters, metrics, artifacts, dataset fingerprint, code revision, and model checkpoint with MLflow.
4. **Model evaluation gates:** define task-appropriate acceptance criteria and automatically reject poor candidate models.
5. **Model registry and lineage:** connect approved model versions to their source data, run, configuration, and evaluation report.
6. **Monitoring and drift:** track input-data changes and, when labels become available, real model performance.
7. **Controlled retraining:** train candidates from approved data updates and promote only when they pass evaluation gates.
8. **Supporting engineering:** retain CI, Docker, and the FastAPI reference service as tools that support the lifecycle.

## Current model limitations

The first tree experiment used only five training images and two validation images. Its measured detection quality was extremely poor, so it is a learning baseline, not a usable detector. We must not draw reliable generalization conclusions from this tiny dataset.

The existing screenshots were described as Google Maps imagery. Confirm the terms that apply to the specific imagery and intended ML use before training further or publishing/distributing derived artifacts. Prefer a dataset whose image and annotation rights explicitly permit the intended use.

## Hardware assumptions

The initial workflow targets Windows with 16 GB RAM and supports CPU execution. It does not assume an NVIDIA GPU. Dataset and training steps should be sized for the available hardware.

## Quick start (Windows PowerShell)

Use Python 3.13 for this project:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/first_inference.py
```

The first run downloads pretrained YOLO26n weights and a sample image. It should create `artifacts/bus_annotated.jpg` and log a run to the local SQLite database `mlflow.db`.

To inspect the experiment:

```powershell
mlflow ui --backend-store-uri sqlite:///./mlflow.db
```

Open http://127.0.0.1:5000 in a browser.

## Dataset governance milestone

Read [dataset governance](docs/dataset_governance.md) before preparing training data. The required contract is:

```text
datasets/<dataset-name>/
├── images/{train,val,test}/
├── labels/{train,val,test}/
└── dataset_metadata.json
```

The test split is optional until it is ready, but any split that exists must have matching label files. Use an empty label file for an intentionally empty image; a missing label file is ambiguous.

Copy `configs/dataset_metadata.example.json` and replace every placeholder with verified source/version/license/attribution details. Then run the structural validator and generate a manifest:

```powershell
python src/validate_yolo_dataset.py --images-dir datasets/<dataset-name>/images/train --labels-dir datasets/<dataset-name>/labels/train
python src/build_dataset_manifest.py --dataset-root datasets/<dataset-name> --metadata datasets/<dataset-name>/dataset_metadata.json --output artifacts/dataset_manifest.json
```

The manifest records file hashes, image metadata, label hashes, annotation-row counts, split counts, and a dataset fingerprint. It detects file changes; it does not verify visual annotation quality, license validity, or statistical representativeness.

## Quality checks

After activating the virtual environment:

```powershell
python -m pip install -r requirements-dev.txt
ruff check src tests
python -m pytest -q
```

GitHub Actions currently runs Ruff and pytest. These checks do not train a model or establish model accuracy. Dataset-manifest tests use synthetic images and do not require downloading a dataset.

## Supporting inference service

A reference FastAPI service is available in `src/inference_api.py`; see [production operations](docs/production_operations.md). It is a supporting example, not the center of this learning path. Its tests use a fake model and generated images, and do not establish tree-detector accuracy.

## Progress tracking

See [LEARNING_LOG.md](LEARNING_LOG.md). Do not record a milestone as complete until its commands have been run and the evidence reviewed.
