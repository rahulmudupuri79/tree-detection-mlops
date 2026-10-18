"""Convert one normalized YOLO bounding-box label to pixel coordinates.

This is a tiny teaching example; it does not load or train a model.
"""
from dataclasses import dataclass


@dataclass
class YoloLabel:
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float


def parse_label(line: str) -> YoloLabel:
    values = line.split()
    if len(values) != 5:
        raise ValueError("A YOLO detection label must contain exactly 5 values.")
    class_id = int(values[0])
    x_center, y_center, width, height = map(float, values[1:])
    if any(value < 0 or value > 1 for value in (x_center, y_center, width, height)):
        raise ValueError("Normalized coordinates and dimensions must be between 0 and 1.")
    return YoloLabel(class_id, x_center, y_center, width, height)


def main() -> None:
    # Example image dimensions: 800 pixels wide, 600 pixels tall.
    image_width = 800
    image_height = 600
    label_line = "0 0.5 0.5 0.2 0.4"

    label = parse_label(label_line)
    box_width = label.width * image_width
    box_height = label.height * image_height
    x_min = (label.x_center * image_width) - box_width / 2
    y_min = (label.y_center * image_height) - box_height / 2
    x_max = x_min + box_width
    y_max = y_min + box_height

    print(f"Image size (width, height): ({image_width}, {image_height})")
    print(f"YOLO label: {label_line}")
    print(f"Class ID: {label.class_id}")
    print(f"Bounding-box size (width, height): ({box_width:.0f}, {box_height:.0f}) pixels")
    print(
        "Bounding-box corners (x_min, y_min, x_max, y_max): "
        f"({x_min:.0f}, {y_min:.0f}, {x_max:.0f}, {y_max:.0f})"
    )


if __name__ == "__main__":
    main()
