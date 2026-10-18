# Tree Annotation Guide

## Goal

Create consistent bounding-box labels for the nine local learning images. The intended detection class is `tree`.

## Important image-rights note

These images were described as screenshots captured from Google Maps satellite/top-down views. Capturing a screenshot does not itself establish permission to use the underlying imagery for machine-learning training or redistribution. Confirm the applicable terms and permissions before training, publishing, or distributing a dataset/model based on this imagery. This guide covers the annotation workflow only.

## Annotation rules

1. Draw one tight, axis-aligned rectangle around each clearly distinguishable individual tree crown.
2. Include the visible crown, not the surrounding road, roof, lawn, or shadow unless inseparable from the crown.
3. For overlapping crowns, draw separate boxes only when the individual crowns can be distinguished with reasonable confidence.
4. If two or more crowns cannot be separated visually, do not guess. Record the image and region for review.
5. Do not label shrubs, grass, or other vegetation as `tree` unless the project definition is deliberately expanded.
6. Keep every box inside the image boundaries.
7. Use the same class name for every positive example: `tree`.
8. Do not skip hard examples silently; note ambiguous cases so the labeling policy can be reviewed.

## Suggested annotation tool

Use a local desktop annotation tool such as LabelImg or CVAT if its current installation and export options fit your setup. Export in YOLO detection format. Each object line should have:

```text
class_id x_center y_center width height
```

The four box coordinates are normalized to the image width/height and range from 0 to 1. With one class, use class ID `0` for `tree`.

## Label file naming

For YOLO format, image and label basenames must match, for example:

```text
images/train/1.jpg
labels/train/1.txt
```

An image with no trees should still have a corresponding empty label file. Do not fabricate boxes to avoid empty files.

## Before labeling all images

1. Annotate one image first.
2. Review boxes at full resolution.
3. Check the exported `.txt` file and confirm class ID `0`.
4. Apply the same rules to the remaining images.
5. Keep original PNGs and prepared images unchanged; annotation tools should export labels separately.
