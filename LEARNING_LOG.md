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
- [x] Run `python src/inspect_image.py` — user supplied terminal output.
- [x] Explain dimensions, array shape, image mode, and RGB pixel values.
- [x] Answer the shape check: `(600, 800, 3)` means 800 pixels wide and 600 pixels tall.
- [ ] Complete the dataset-label exercise in the next lesson.

### Verified image-inspection output
- Format/mode: JPEG / RGB
- Image size (width, height): `(810, 1080)`
- NumPy shape (height, width, channels): `(1080, 810, 3)`
- Data type: `uint8`; values range from 0 to 255
- Pixel count: `874,800`
- First pixel RGB: `[172, 146, 119]`
- Center pixel RGB: `[1, 85, 155]`
- Mean RGB values: `[117.81, 114.86, 128.04]`

The user correctly explained that a NumPy shape of `(600, 800, 3)` represents an image 800 pixels wide and 600 pixels tall.
