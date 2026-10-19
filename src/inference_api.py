"""HTTP inference API for the tree-detection model.

The model is loaded at application startup from MODEL_PATH. Keep model weights outside
the container image and mount them read-only at deployment time.
"""

from __future__ import annotations

import io
import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

LOGGER = logging.getLogger("tree_detection.api")


def _load_model(model_path: str) -> Any:
    """Load a YOLO model after validating the configured model path."""
    if not Path(model_path).is_file():
        raise FileNotFoundError(
            f"Model file was not found at {model_path!r}. Set MODEL_PATH to a readable model file."
        )

    # Import lazily so health/API tests do not need to import the heavyweight ML runtime.
    from ultralytics import YOLO

    return YOLO(model_path)


def create_app(
    model_loader: Callable[[str], Any] | None = None,
    *,
    model_path: str | None = None,
    max_upload_bytes: int | None = None,
) -> FastAPI:
    """Create an API instance; injection points make tests independent of model weights."""
    configured_model_path = model_path or os.getenv("MODEL_PATH", "models/best.pt")
    upload_limit = max_upload_bytes or int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))
    image_size = int(os.getenv("IMAGE_SIZE", "640"))
    confidence_threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.25"))
    device = os.getenv("INFERENCE_DEVICE", "cpu")
    loader = model_loader or _load_model
    state: dict[str, Any] = {"model": None}

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        state["model"] = loader(configured_model_path)
        LOGGER.info("Inference model loaded")
        try:
            yield
        finally:
            state["model"] = None

    app = FastAPI(
        title="Tree Detection API",
        description="CPU-friendly object-detection inference endpoint.",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/health/live", tags=["health"])
    def live() -> dict[str, str]:
        """Liveness probe: the process is responding."""
        return {"status": "alive"}

    @app.get("/health/ready", tags=["health"])
    def ready() -> dict[str, str]:
        """Readiness probe: the model finished loading."""
        if state["model"] is None:
            raise HTTPException(status_code=503, detail="Model is not ready")
        return {"status": "ready"}

    @app.post("/predict", tags=["inference"])
    async def predict(file: UploadFile = File(...)) -> dict[str, Any]:
        """Run inference on a validated image upload."""
        try:
            payload = await file.read(upload_limit + 1)
        finally:
            await file.close()

        if not payload:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        if len(payload) > upload_limit:
            raise HTTPException(
                status_code=413,
                detail=f"Image exceeds the {upload_limit}-byte upload limit",
            )

        try:
            with Image.open(io.BytesIO(payload)) as candidate:
                candidate.verify()
            with Image.open(io.BytesIO(payload)) as candidate:
                image = candidate.convert("RGB")
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
            raise HTTPException(status_code=400, detail="Upload must be a valid image") from exc

        model = state["model"]
        if model is None:
            raise HTTPException(status_code=503, detail="Model is not ready")

        started = time.perf_counter()
        try:
            results = model.predict(
                source=image,
                imgsz=image_size,
                conf=confidence_threshold,
                device=device,
                verbose=False,
            )
            result = results[0]
            detections: list[dict[str, Any]] = []
            boxes = result.boxes
            if boxes is not None:
                coordinates = boxes.xyxy.tolist()
                confidences = boxes.conf.tolist()
                class_ids = boxes.cls.tolist()
                for coordinates_xyxy, confidence, raw_class_id in zip(
                    coordinates, confidences, class_ids, strict=True
                ):
                    class_id = int(raw_class_id)
                    names = result.names
                    class_name = (
                        names.get(class_id, str(class_id))
                        if isinstance(names, dict)
                        else names[class_id]
                    )
                    detections.append(
                        {
                            "class_id": class_id,
                            "class_name": str(class_name),
                            "confidence": round(float(confidence), 6),
                            "xyxy": [round(float(value), 2) for value in coordinates_xyxy],
                        }
                    )
        except Exception as exc:
            LOGGER.exception("Model inference failed")
            raise HTTPException(status_code=500, detail="Model inference failed") from exc

        return {
            "model": Path(configured_model_path).name,
            "image_width": image.width,
            "image_height": image.height,
            "inference_ms": round((time.perf_counter() - started) * 1000, 3),
            "detections": detections,
        }

    return app


app = create_app()
