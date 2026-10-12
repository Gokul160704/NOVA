
import time
from pathlib import Path

import cv2
import mss
import numpy as np
import win32gui

WINDOW_TITLE = "Slay the Spire 2"
OUTPUT_DIR = Path("captures")
OUTPUT_DIR.mkdir(exist_ok=True)

hwnd = win32gui.FindWindow(None, WINDOW_TITLE)

if not hwnd:
    raise RuntimeError(
        "Slay the Spire 2 window not found. Make sure the game is open."
    )

left, top, right, bottom = win32gui.GetWindowRect(hwnd)
width = right - left
height = bottom - top

if width <= 0 or height <= 0:
    raise RuntimeError("The game window has invalid dimensions.")

print(f"Found: {WINDOW_TITLE}")
print(f"Window size: {width} x {height}")
print("Capturing the game window in 3 seconds...")
time.sleep(3)

with mss.MSS() as sct:
    region = {
        "left": left,
        "top": top,
        "width": width,
        "height": height,
    }

    image = np.array(sct.grab(region))
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    output = OUTPUT_DIR / "sts2_window_test.png"
    cv2.imwrite(str(output), image)

print(f"Saved test image: {output}")
 