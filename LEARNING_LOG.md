# Learning Log

## Python version
Python 3.13 is the selected project version. The shared terminal output has not yet confirmed the exact interpreter version.

## Current milestone
**Phase 1 — First successful inference (complete)**

## Status
- [ ] Confirm the interpreter is Python 3.13.
- [x] Run pretrained inference on the sample image — terminal output supplied by user.
- [x] Save annotated output image — script reported `C:\\Jobs\\tree-detection-mlops\\artifacts\\bus_annotated.jpg`.
- [x] Open and visually inspect the annotated image (user confirmed complete).
- [x] Open the MLflow UI and verify the run, parameters, metrics, and image artifact (user confirmed complete).

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

These values are copied from the user's terminal output. User confirmed the MLflow UI checks and annotated-image inspection are complete.

## Concepts introduced
- **Inference:** using an already-trained model to make predictions.
- **Bounding box:** a rectangle around a predicted object.
- **Class label:** the category predicted by the model.
- **Confidence score:** the model's score for a particular prediction.
- **Experiment tracking:** recording parameters, metrics, and artifacts so runs can be inspected and compared.

## Issue encountered
MLflow initially rejected the filesystem tracking backend. The script now uses a local SQLite database (`mlflow.db`); the user confirmed the experiment is visible in the UI.

## Phase 2 — Image and dataset fundamentals
**Current lesson:** inspect image dimensions, channels, and pixel values.

- [ ] Confirm Python 3.13 with `py -3.13 --version`.
- [ ] Run `python src/inspect_image.py`.
- [ ] Explain the printed dimensions, array shape, mode, and RGB pixel values in your own words.
- [ ] Complete the follow-up exercise.

The inspection script reads the generated `artifacts/bus_annotated.jpg`. Results are not recorded as verified until the user runs it and shares the output.
