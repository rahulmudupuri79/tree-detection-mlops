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


### YOLO label coordinate exercise
- [x] Explain normalized YOLO box values and convert width/height to pixels.
- [x] Correctly answer the example: a label of `0 0.5 0.5 0.2 0.4` on an 800 × 600 image gives a 160 × 240 pixel box.
- [ ] Run `python src/inspect_yolo_label.py` and compare the output with the expected values.
- [ ] Explain what the four pixel corner coordinates represent.

The runnable example is in `src/inspect_yolo_label.py`. Its example label is synthetic and is not a label from a real tree dataset.


### YOLO label coordinate conversion — verified
- [x] Run `python src/inspect_yolo_label.py` successfully; user supplied terminal output.
- [x] Verify the box size is 160 × 240 pixels for an 800 × 600 image.
- [x] Verify the corner coordinates are `(320, 180, 480, 420)`.
- [ ] Next: inspect the relationship between image files and annotation files in a real dataset.


### Dataset layout — lesson introduced
- [x] Record the expected YOLO image/label folder convention in `docs/dataset_layout.md`.
- [x] Document an illustrative `data.yaml`, split meanings, licensing, and data-leakage cautions.
- [ ] Next checkpoint: choose/identify a real tree dataset and verify its class mapping, license, and annotation format before downloading or training.


### Real dataset review — NEON Tree Evaluation Benchmark
- [x] Identify a task-aligned candidate with individual-tree bounding boxes.
- [x] Check class mapping and annotation format: one `Tree` class; Pascal VOC XML bounding boxes.
- [x] Review license notes: repository says CC0, but underlying NEON imagery has separate attribution/data-use terms; check the exact downloaded version and cite it.
- [ ] Choose a small RGB-only subset and inspect an image/XML pair before downloading or converting labels.
- [ ] Record exact source/version and citation; keep dataset files out of Git.

Candidate review is documented in `docs/dataset_layout.md`. No dataset has been downloaded yet.


### User dataset update — repository inspection
- [x] Inspected the GitHub `datasets/trees/` directory on `main`.
- [x] Confirmed nine PNG files are present: `1.png` through `9.png`; combined size is approximately 2.45 MB.
- [ ] Inspect image content/dimensions and confirm provenance/license.
- [ ] Check whether separate annotations exist elsewhere; the inspected `datasets/trees/` directory currently contains images only, with no label files.
- [ ] If these images are intended for training, annotate individual trees before training; images alone are not labeled object-detection examples.

The images are committed to GitHub. Their visual content, source/license, and annotation status have not yet been verified.


### Dataset provenance and rights caution — Google Maps screenshots
- [x] User clarified that the nine images are screenshots they captured from Google Maps satellite/top-down neighborhood views.
- [ ] Do not use these screenshots to train, validate, test, or publish as a reusable dataset unless the applicable rights/terms are confirmed.
- [ ] Recommended path: replace them with imagery whose license explicitly permits machine-learning use, or obtain permission for the intended use.
- [ ] Consider removing the screenshots from the public repository while resolving rights and neighborhood-location privacy concerns.
- [ ] Choose an explicitly licensed aerial/tree-detection dataset and record source, version, license, and attribution.

The act of capturing a screenshot does not itself grant rights to the underlying Google Maps imagery. Current Google Maps Platform terms expressly restrict use of Google Maps Content to improve ML/AI models; the applicable terms depend on how the content was obtained and used.
