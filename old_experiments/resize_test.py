
from pathlib import Path
import cv2

source = Path("captures/event_20261010_222532.png")
destination = Path("captures/vision_small.png")

image = cv2.imread(str(source))

if image is None:
    raise FileNotFoundError(f"Could not read {source}")

small = cv2.resize(image, (960, 540), interpolation=cv2.INTER_AREA)

if not cv2.imwrite(str(destination), small):
    raise RuntimeError("Failed to save resized image")

print(f"Original: {image.shape[1]}x{image.shape[0]}")
print(f"Resized:  {small.shape[1]}x{small.shape[0]}")
print(f"Saved: {destination}")
