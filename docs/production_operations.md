# Inference API: operations and deployment

This is a production-oriented reference implementation for a portfolio project. It is **not production-certified**: model quality, dependency locking, image provenance, infrastructure, security review, and operational SLOs must be completed for a real deployment.

## Contract

- `GET /health/live`: process liveness; does not prove the model is loaded.
- `GET /health/ready`: returns HTTP 200 only after the model has loaded; otherwise HTTP 503.
- `POST /predict`: multipart form upload with field name `file`; returns image dimensions, inference time, and detections (`class_id`, `class_name`, confidence, and `xyxy` pixel coordinates).
- Invalid images return HTTP 400; uploads above `MAX_UPLOAD_BYTES` return HTTP 413; inference failures return HTTP 500 with a generic message.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `MODEL_PATH` | `models/best.pt` | Model checkpoint path |
| `MAX_UPLOAD_BYTES` | `10485760` | Maximum upload size (10 MiB) |
| `IMAGE_SIZE` | `640` | YOLO inference image size |
| `CONFIDENCE_THRESHOLD` | `0.25` | Detection confidence threshold |
| `INFERENCE_DEVICE` | `cpu` | Inference device; default is CPU |

Do not bake model weights or secrets into the image. Mount a reviewed model artifact read-only and set `MODEL_PATH` accordingly.

## Local run (PowerShell)

Activate the project environment and install `requirements.txt`, then set the path to a reviewed checkpoint:

```powershell
$env:MODEL_PATH = "C:\path\to\approved\best.pt"
$env:INFERENCE_DEVICE = "cpu"
python -m uvicorn src.inference_api:app --host 127.0.0.1 --port 8000
```

Open the interactive API docs at `http://127.0.0.1:8000/docs`. The checkpoint must exist and be readable or startup fails.

## Container

Build the image:

```powershell
docker build -t tree-detection-api:local .
```

Run with a reviewed model file mounted read-only:

```powershell
docker run --rm -p 8000:8000 -e MODEL_PATH=/models/best.pt -v "C:\path\to\approved\best.pt:/models/best.pt:ro" tree-detection-api:local
```

The container runs as a non-root user. The Docker health check checks liveness only; an orchestrator should separately poll `/health/ready` before routing requests.

## Before production

- Establish dataset and model artifact provenance, usage rights, and integrity hashes.
- Pin and lock all transitive dependencies; scan dependencies and the built image for known vulnerabilities.
- Evaluate on a representative, permitted, held-out dataset and define explicit release thresholds.
- Add authentication/authorization, TLS at the ingress, rate limiting, request quotas, and abuse controls before exposing the service publicly.
- Load-test concurrency, memory, latency, and throughput; choose worker counts from measured resource use. The reference container uses one worker to avoid loading duplicate model copies.
- Emit structured request/error/latency metrics and trace IDs; add dashboards and actionable alerts.
- Define SLOs, model promotion/rollback, artifact retention, backup/recovery, incident response, and retraining policy.
- Test deployment in the target environment and document the exact image digest and model version.
