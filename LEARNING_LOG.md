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


### User decision — continue local image inspection

- [x] User chose to keep the nine existing images as the working examples for local learning.
- [ ] Inspect image dimensions, formats, and color modes with `python src/inspect_tree_images.py`.
- [ ] Review the output and decide on a tree-labeling approach before any model training.

We can use the files to learn image inspection and annotation workflows, but this choice does not establish permission to train on, redistribute, or publish models based on the underlying Google Maps imagery. Confirm applicable rights before those uses.

### Dataset provenance and rights caution — Google Maps screenshots
- [x] User clarified that the nine images are screenshots they captured from Google Maps satellite/top-down neighborhood views.
- [ ] Do not use these screenshots to train, validate, test, or publish as a reusable dataset unless the applicable rights/terms are confirmed.
- [ ] Recommended path: replace them with imagery whose license explicitly permits machine-learning use, or obtain permission for the intended use.
- [ ] Consider removing the screenshots from the public repository while resolving rights and neighborhood-location privacy concerns.
- [ ] Choose an explicitly licensed aerial/tree-detection dataset and record source, version, license, and attribution.

The act of capturing a screenshot does not itself grant rights to the underlying Google Maps imagery. Current Google Maps Platform terms expressly restrict use of Google Maps Content to improve ML/AI models; the applicable terms depend on how the content was obtained and used.


### Nine-image inspection — results supplied by user

- [x] Confirmed the script finds nine PNG files in `datasets/trees/`.
- [x] Recorded that all nine report mode RGBA and have different dimensions.
- [ ] Check alpha-channel values to determine whether any pixels are transparent.
- [ ] Decide whether conversion to RGB is appropriate; preserve the original files.

Observed dimensions (width × height): 327×445, 428×367, 415×517, 417×353, 505×337, 360×411, 447×422, 275×197, and 518×297. RGBA indicates an alpha channel, but does not by itself prove that any pixel is transparent.



### Alpha-channel check — results supplied by user

- [x] Run `python src/check_image_alpha.py` on all nine images.
- [x] Confirmed every alpha channel has min/max 255 and zero pixels below 255.
- [x] Concluded that dropping alpha will not discard visible transparency.
- [ ] Run `python src/prepare_tree_images.py` to create RGB JPEG working copies under `datasets/trees_rgb/`.
- [ ] Verify the output files and dimensions; keep original PNGs unchanged.

A preparation script was added at `src/prepare_tree_images.py`. It converts each image to RGB and saves a JPEG copy at quality 95 in a separate folder. JPEG encoding is lossy, so originals are preserved; if pixel-exact lossless copies are preferred, use RGB PNG output instead.



### RGB preparation — user supplied output

- [x] Created nine RGB JPEG copies in `datasets/trees_rgb/`.
- [x] Confirmed each copy retained its source image's dimensions.
- [x] Original PNGs were preserved.
- [ ] Next: annotate one image with the single class `tree` and inspect the exported YOLO label file.

Annotation guidance was added to `docs/tree_annotation_guide.md`. It defines consistent rules for individual crowns, overlapping crowns, and ambiguous cases. Because the imagery was described as Google Maps screenshots, applicable rights should be confirmed before training, publishing, or distributing a dataset/model based on it.



### Annotation validation — next milestone

- [x] User reports that YOLO `.txt` annotations are extracted into a local folder.
- [ ] Run `src/validate_yolo_dataset.py` against the actual image and label folders.
- [ ] Confirm the seven labeled training images have matching label files and valid box values.
- [ ] Keep the six intended test images separate from training; for quantitative evaluation, annotate their ground truth separately and do not train on those labels.
- [ ] Manually inspect a few boxes on the images; structural validation cannot confirm that boxes correctly surround tree crowns.

A validator was added at `src/validate_yolo_dataset.py`. It checks image/label basename matching, YOLO's five-field detection format, numeric normalized coordinates, class IDs, positive box sizes, and image boundaries. Missing label files are warnings because unlabeled test images may be intentional; labels with no matching image and invalid label values are errors.



### YOLO annotation structural review

- [x] Found seven committed label files under `datasets/annotations/`, named `1.txt` through `7.txt`, matching images `1.jpg` through `7.jpg` in `datasets/trees_rgb/`.
- [x] Reviewed the committed label text: 17 bounding boxes total. Each row has five numeric values, class ID `0`, normalized center/size coordinates, positive width and height, and boxes within normalized image boundaries.
- [ ] Run the local validator script to confirm the same result from the Windows checkout.
- [ ] Visually inspect the boxes against the image pixels; numeric validation cannot verify annotation quality.
- [ ] Annotate the six held-out test images separately before measuring test performance. Keep their labels out of training.

Current status: **structural checks of the committed label text pass**. This is not yet a visual quality review or model evaluation.


### Local YOLO validation — completed

- [x] User ran `python src/validate_yolo_dataset.py --images-dir datasets/trees_rgb --labels-dir datasets/annotations` locally.
- [x] Validator reported 13 images and 7 label files.
- [x] All seven label files parsed successfully: image 1 has 1 box, 2 has 2, 3 has 1, 4 has 3, 5 has 6, 6 has 2, and 7 has 2 — 17 annotated boxes total.
- [x] Validator reported 6 warnings for images 8–13, no errors; these are expected because the images are reserved for testing and currently have no label files.
- [ ] Visually review boxes against image content. Structural validation does not prove that each box tightly and correctly encloses a tree.
- [ ] Annotate test images separately before quantitative evaluation; do not include test labels in training.

Status: **structural validation passed; visual annotation quality and test ground truth remain outstanding.**


### First tree-model training and prediction — user supplied terminal output

- [x] Confirmed the local environment: Python 3.13.16, Ultralytics 8.4.182, PyTorch 2.14.1+cpu; CPU-only run.
- [x] Completed a 5-epoch YOLO26n training run using 5 training images and 2 validation images.
- [x] Confirmed the run saved `best.pt` and `last.pt`.
- [x] Ran prediction on `datasets/trees_rgb/8.jpg` with the trained `best.pt` checkpoint.
- [x] Opened the prediction output and confirmed the image had no predicted boxes.
- [ ] Improve the experiment only after confirming the imagery's applicable rights and selecting data permitted for ML use.
- [ ] Use a suitably licensed dataset with enough labeled examples and a held-out evaluation set before drawing conclusions about model quality.

Reported end-of-training validation metrics:
- Precision: 0.00333
- Recall: 0.5
- mAP50: 0.0103
- mAP50-95: 0.00387

The model predicted **no detections** on image 8 at confidence threshold 0.10. Image 8 currently has no ground-truth label, so this is a visual prediction check, not a measurable test result. With only five training images, two validation images, and five epochs, these results are not evidence of a reliable tree detector.

The actual training output directory reported by Ultralytics was `runs/detect/runs/tree_detection/first_experiment`; the prediction directory was `runs/detect/runs/tree_detection/predict_image_8`. These paths are based on the user's terminal output. The dataset was described as Google Maps screenshots; this log records the experiment but does not establish that the imagery may lawfully be used for model training or publication. Confirm applicable terms before further training or sharing derived artifacts.


### Training-curve review — results.csv supplied by user

- [x] Reviewed the five epoch rows from `results.csv`.
- [x] Recorded that per-epoch precision stayed at 0.00333, recall at 0.5, mAP50 at 0.01053, and mAP50-95 at 0.00394.
- [x] Observed that validation box/class/L1 losses are identical across all five rows (2.24818, 7.38486, and 0.02417); this deserves investigation and should not be interpreted as evidence of improvement.
- [x] Observed that training box loss and class loss fluctuate and are higher at epoch 5 than epoch 1.
- [ ] Before changing epochs or hyperparameters, verify the dataset configuration, labels, and the small validation set; a two-image validation set makes metrics very unstable.
- [ ] Confirm rights for the Google Maps screenshots before further model training or sharing model artifacts.

The per-epoch `results.csv` values are the source for this review. They show very poor measured detection quality on the current tiny validation set, not a reliable estimate of how a tree detector would perform on new imagery. The earlier end-of-training console summary showed slightly different mAP values (mAP50 0.0103 and mAP50-95 0.00387); retain both records rather than silently treating them as identical.


### Validation annotation visual check — image 6

- [x] User ran the label-preview script for image 6.
- [x] User confirmed the boxes looked correctly placed around the trees in image 6.
- [ ] Visually inspect validation image 7 as well.
- [ ] Confirm imagery usage rights before additional training.

This is a user-reported visual review of image 6 only. It does not establish annotation quality for all images or explain the poor validation metrics.


### Validation annotation visual check — image 7

- [x] User ran the label-preview script for image 7.
- [x] User confirmed the boxes looked correctly placed around the trees in image 7.
- [x] Both validation images (6 and 7) have now received a user-reported visual review.
- [ ] Confirm imagery usage rights before additional training.
- [ ] Expand the permitted, labeled dataset and validation set before interpreting metrics or tuning the model.

This records visual review of the two validation images only. With just two validation images, model-quality estimates remain highly unstable. The identical validation loss values in the five-epoch CSV remain unexplained.


### MLOps foundation scaffold — created on feature branch

- [x] Added GitHub Actions workflow for linting and tests.
- [x] Added separate development dependencies for pytest and Ruff.
- [x] Added pytest configuration and four automated tests for the YOLO dataset validator.
- [x] Added an MLOps readiness checklist that separates current foundations from production gaps.
- [x] Updated the README with local quality-check commands and CI scope.
- [ ] Confirm the pull-request CI run passes.
- [ ] Run the quality checks locally in the Windows virtual environment and review results.

Changes are on branch `feat/mlops-foundation` pending review. No local training or inference was run as part of this repository scaffold. CI checks code style and validator behavior; it does not verify model accuracy, data rights, or production readiness.
