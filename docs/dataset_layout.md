# YOLO dataset layout

This is a reference example for the project. It describes the expected structure; it is **not** a downloaded or verified tree dataset.

## Folder layout

```text
datasets/
└── trees/
    ├── images/
    │   ├── train/
    │   │   ├── tree_001.jpg
    │   │   └── tree_002.jpg
    │   ├── val/
    │   │   └── tree_003.jpg
    │   └── test/
    │       └── tree_004.jpg
    ├── labels/
    │   ├── train/
    │   │   ├── tree_001.txt
    │   │   └── tree_002.txt
    │   ├── val/
    │   │   └── tree_003.txt
    │   └── test/
    │       └── tree_004.txt
    └── data.yaml
```

For each labeled image, the label file uses the same filename stem: `tree_001.jpg` pairs with `tree_001.txt`. In a YOLO detection label file, each non-empty line describes one object using:

```text
class_id x_center y_center width height
```

The four box values are normalized relative to the image width and height. An image with no objects can have an empty label file, depending on the dataset and training workflow. Missing label files should be checked rather than silently assumed to mean no objects.

## Example data.yaml

```yaml
path: datasets/trees
train: images/train
val: images/val
test: images/test

names:
  0: tree
```

This example assumes class ID `0` means `tree`. Always use the actual dataset's class mapping. The paths above are relative to the `path` value.

## Dataset split meanings

- **train**: examples used to update model weights.
- **val**: examples used during development to evaluate and compare training checkpoints.
- **test**: held-out examples for a final evaluation; avoid using these repeatedly to tune the model.

Do not put near-duplicate images or images from the same source sequence into different splits without considering data leakage. For tree detection, images from the same location, flight, or video can be highly correlated, so split design matters.

## Before training

1. Confirm the dataset license and permitted use.
2. Read the dataset's class names and annotation format.
3. Check that image/label pairs and split paths are valid.
4. Inspect sample images with their boxes drawn.
5. Keep the raw dataset out of Git unless its size and license make committing it appropriate; record the source and version instead.
