# Tree Detection & MLOps Learning Lab

A hands-on, incremental project for learning computer vision, machine learning, experiment tracking, GPU performance engineering, and production ML operations.

## Learning approach

We work one milestone at a time. Commands and results are only marked complete after they have been run and verified.

## Project roadmap

1. **First inference:** run a small pretrained object detector on a sample image, inspect bounding boxes and confidence scores, save an annotated image, and log a run with MLflow.
2. **Data science foundations:** explore datasets, labels, splits, data leakage, and basic statistics.
3. **ML fundamentals:** learn training, loss, optimization, generalization, and object-detection evaluation.
4. **Tree detection:** select a suitable labeled dataset, fine-tune a lightweight model if needed, and evaluate it on held-out images.
5. **Experiment tracking:** compare runs and track parameters, metrics, artifacts, and model versions with MLflow.
6. **Performance engineering:** benchmark CPU/GPU inference where hardware allows; examine memory, latency, throughput, and profiling.
7. **Inference service:** expose predictions through a tested FastAPI service.
8. **CI/CD:** add automated tests, GitHub Actions, and container builds.
9. **Production operations:** progress to Kubernetes, resource controls, monitoring, scaling, and reliability.

## Hardware assumptions

The initial workflow targets Windows with 16 GB RAM and supports CPU inference. It does not assume an NVIDIA GPU. First-time execution requires an internet connection to download dependencies, model weights, and the example image. Later training and dataset steps will be sized after checking the available hardware and data requirements.

## Quick start (Windows PowerShell)

Use Python 3.13 for this project:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/first_inference.py
```

The first run downloads the YOLO26n pretrained weights and sample image. It should create `artifacts/bus_annotated.jpg` and log a run to the local SQLite database `mlflow.db`.

To inspect the experiment:

```powershell
mlflow ui --backend-store-uri sqlite:///./mlflow.db
```

Open http://127.0.0.1:5000 in a browser.

## Important limitation

The initial example image contains common objects and is only used to teach inference. A general-purpose pretrained detector is **not** assumed to reliably detect individual trees. Tree-detection performance must be validated on an appropriate dataset and may require fine-tuning.

## Repository layout

```text
tree-detection-mlops/
├── README.md
├── LEARNING_LOG.md
├── requirements.txt
├── .gitignore
├── artifacts/          # generated output; not committed
├── configs/            # future configuration
├── data/               # datasets; not committed
├── models/             # downloaded weights; not committed
├── notebooks/
├── scripts/
├── src/
│   └── first_inference.py
├── tests/
└── .github/
    └── workflows/
```

## Progress tracking

See [LEARNING_LOG.md](LEARNING_LOG.md). Do not record a milestone as completed until its commands have been run and the evidence reviewed.


## MLOps engineering foundations

The repository now includes a starter quality gate:
- GitHub Actions runs Ruff linting and pytest on pushes to `main` and feature branches, pull requests to `main`, and manual dispatch.
- Unit/integration tests exercise the YOLO dataset validator using temporary synthetic data.
- Development tools are listed separately in `requirements-dev.txt`.
- See [MLOps readiness and gaps](docs/mlops_readiness.md) for implemented foundations and the production-readiness backlog.

### Run quality checks locally (PowerShell)

After activating `.venv`:

```powershell
python -m pip install -r requirements-dev.txt
ruff check src tests
python -m pytest -q
```

CI currently checks code quality and dataset-validator behavior only. It does **not** train a model, validate model accuracy, establish dataset licensing, or make this repository production-ready. Those require separate evidence and milestones.
