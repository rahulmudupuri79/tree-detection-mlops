# MLOps Readiness

This repository is a learning and portfolio project, not yet a production ML service. The checklist below distinguishes implemented foundations from work that still needs evidence.

## Implemented in this repository

- [x] Source code and learning notes tracked in Git.
- [x] Local MLflow tracking with a SQLite backend for the first inference example.
- [x] YOLO label-structure validator.
- [x] Automated tests for valid labels, invalid bounds, missing-label warnings, and orphan labels.
- [x] GitHub Actions workflow to lint and test on pushes and pull requests.
- [x] Generated artifacts, model weights, and local MLflow database excluded from Git.

## Not yet production-ready

- [ ] Select a dataset whose license and terms explicitly permit the intended ML use; document source, version, license, and attribution.
- [ ] Add data/version manifests and dataset integrity checks.
- [ ] Pin and audit runtime dependencies; test the chosen Python and platform matrix.
- [ ] Create a reproducible training entry point with configuration and explicit random seeds where supported.
- [ ] Log training parameters, dataset identity, code revision, evaluation metrics, and relevant artifacts to MLflow.
- [ ] Define acceptance thresholds and evaluate on a sufficiently large, representative held-out set.
- [ ] Add model registration and a promotion/approval process.
- [ ] Add a tested inference API, request validation, and structured logging.
- [ ] Add container build and security scanning.
- [ ] Add operational metrics, health checks, monitoring, alerting, rollback, and retraining criteria.
- [ ] Document secrets handling, access control, artifact retention, and backup/recovery for any remote tracking service.

## Local quality checks (PowerShell)

Activate the project virtual environment first, then run:

```powershell
python -m pip install -r requirements-dev.txt
ruff check src tests
python -m pytest -q
```

The test suite uses temporary synthetic image filenames and labels. It does not require downloading model weights, running training, or using the local imagery.

## CI behavior

GitHub Actions runs the lint and unit/integration tests on pushes to `main` and `feat/**`, pull requests targeting `main`, and manual dispatch. A green CI run verifies the configured static checks and tests only; it does not certify model quality, data rights, reproducibility, or production readiness.

## Current experiment caveat

The first tree-detection experiment used a very small training/validation split and yielded very low detection metrics. Treat it as a baseline for learning, not as a validated model. Confirm rights for the existing Google Maps screenshots before any further training or distribution of derived models or artifacts.
