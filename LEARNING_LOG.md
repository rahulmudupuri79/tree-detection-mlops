# Learning Log

## Python version
Python 3.13 is the selected project version. The shared terminal output has not yet confirmed the exact interpreter version.

## Current milestone
**Phase 1 — First successful inference**

## Status
- [ ] Confirm the interpreter is Python 3.13.
- [x] Run pretrained inference on the sample image — terminal output supplied by user.
- [x] Save annotated output image — script reported `C:\\Jobs\\tree-detection-mlops\\artifacts\\bus_annotated.jpg`.
- [ ] Open and visually inspect the annotated image.
- [ ] Open the MLflow UI and verify the run, parameters, metrics, and image artifact.

## Verified run output
- Model: `yolo26n.pt`
- Device: CPU (configured in the script)
- Detections: 5
- Inference time reported: 3.677 seconds
- Predicted classes and confidence:
  - person: 0.829
  - bus: 0.824
  - person: 0.763
  - person: 0.561
  - person: 0.431
- Output path reported: `C:\\Jobs\\tree-detection-mlops\\artifacts\\bus_annotated.jpg`

These values are copied from the user's terminal output. User confirmed the MLflow experiment is visible in the UI. The run's metric and artifact details have not yet been confirmed separately.

## Concepts introduced
- **Inference:** using an already-trained model to make predictions.
- **Bounding box:** a rectangle around a predicted object.
- **Class label:** the category predicted by the model.
- **Confidence score:** the model's score for a particular prediction.
- **Experiment tracking:** recording parameters, metrics, and artifacts so runs can be inspected and compared.

## Issue encountered
MLflow raised an exception when using the filesystem tracking backend. The repository script is being updated to use a local SQLite database (`mlflow.db`) instead.

## Next step
Open the visible run in MLflow and confirm the detection_count and inference_seconds metrics plus the annotated image artifact. Then visually inspect the saved image.
