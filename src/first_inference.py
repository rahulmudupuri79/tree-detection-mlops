"""Run a first pretrained object-detection inference and log it with MLflow."""

from pathlib import Path
import time

import mlflow
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts"
OUTPUT_IMAGE = OUTPUT_DIR / "bus_annotated.jpg"

MODEL_NAME = "yolo26n.pt"
IMAGE_URL = (
    "https://github.com/ultralytics/assets/releases/download/v0.0.0/bus.jpg"
)


def main() -> None:
    """Run inference, save an annotated image, and record the run."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

<<<<<<< Updated upstream
    # Store MLflow tracking metadata in a local SQLite database.
=======
    # Use a local, repository-relative MLflow tracking directory.
>>>>>>> Stashed changes
    mlflow.set_tracking_uri(f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}")
    mlflow.set_experiment("tree-detection-first-inference")

    with mlflow.start_run():
        mlflow.log_param("model", MODEL_NAME)
        mlflow.log_param("device", "cpu")
        mlflow.log_param("image_source", IMAGE_URL)
        mlflow.log_param("image_size", 320)
        mlflow.log_param("confidence_threshold", 0.25)

        model = YOLO(MODEL_NAME)

        start_time = time.perf_counter()
        results = model.predict(
            source=IMAGE_URL,
            device="cpu",
            imgsz=320,
            conf=0.25,
            verbose=False,
        )
        inference_seconds = time.perf_counter() - start_time

        result = results[0]
        detection_count = len(result.boxes) if result.boxes is not None else 0
        result.save(filename=str(OUTPUT_IMAGE))

        mlflow.log_metric("detection_count", detection_count)
        mlflow.log_metric("inference_seconds", inference_seconds)
        mlflow.log_artifact(str(OUTPUT_IMAGE))

        print(f"Model: {MODEL_NAME}")
        print(f"Detections: {detection_count}")
        print(f"Inference time: {inference_seconds:.3f} seconds")
        print(f"Annotated image: {OUTPUT_IMAGE}")

        for box in result.boxes:
            class_id = int(box.cls.item())
            class_name = result.names[class_id]
            confidence = float(box.conf.item())
            print(f"  {class_name}: confidence={confidence:.3f}")


if __name__ == "__main__":
    main()
