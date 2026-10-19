"""API tests use a fake detector and synthetic images; no model weights are downloaded."""

from __future__ import annotations

from io import BytesIO
from typing import Any

from fastapi.testclient import TestClient
from PIL import Image

from src.inference_api import create_app


class FakeTensor:
    def __init__(self, values: list[Any]) -> None:
        self.values = values

    def tolist(self) -> list[Any]:
        return self.values


class FakeBoxes:
    xyxy = FakeTensor([[1.0, 2.0, 30.0, 40.0]])
    conf = FakeTensor([0.91])
    cls = FakeTensor([0.0])


class FakeResult:
    boxes = FakeBoxes()
    names = {0: "tree"}


class FakeModel:
    def predict(self, **kwargs: Any) -> list[FakeResult]:
        assert kwargs["source"].mode == "RGB"
        assert kwargs["device"] == "cpu"
        return [FakeResult()]


def image_bytes(format_name: str = "PNG") -> bytes:
    stream = BytesIO()
    Image.new("RGB", (32, 24), color="white").save(stream, format=format_name)
    return stream.getvalue()


def make_client(max_upload_bytes: int = 1024 * 1024) -> TestClient:
    app = create_app(
        model_loader=lambda _: FakeModel(),
        model_path="fake-model.pt",
        max_upload_bytes=max_upload_bytes,
    )
    return TestClient(app)


def test_liveness_and_readiness() -> None:
    with make_client() as client:
        assert client.get("/health/live").json() == {"status": "alive"}
        response = client.get("/health/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}


def test_prediction_returns_detection_contract() -> None:
    with make_client() as client:
        response = client.post(
            "/predict",
            files={"file": ("tree.png", image_bytes(), "image/png")},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["model"] == "fake-model.pt"
    assert payload["image_width"] == 32
    assert payload["image_height"] == 24
    assert payload["inference_ms"] >= 0
    assert payload["detections"] == [
        {
            "class_id": 0,
            "class_name": "tree",
            "confidence": 0.91,
            "xyxy": [1.0, 2.0, 30.0, 40.0],
        }
    ]


def test_invalid_image_is_rejected() -> None:
    with make_client() as client:
        response = client.post(
            "/predict",
            files={"file": ("not-an-image.png", b"not an image", "image/png")},
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Upload must be a valid image"


def test_oversized_upload_is_rejected() -> None:
    with make_client(max_upload_bytes=16) as client:
        response = client.post(
            "/predict",
            files={"file": ("large.png", image_bytes(), "image/png")},
        )

    assert response.status_code == 413
    assert "upload limit" in response.json()["detail"]


def test_empty_upload_is_rejected() -> None:
    with make_client() as client:
        response = client.post(
            "/predict",
            files={"file": ("empty.png", b"", "image/png")},
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty"
