
from pathlib import Path
from datetime import datetime

import cv2
import mss
import numpy as np


def main():
    # Save captures inside the NOVA project.
    output_dir = Path("captures")
    output_dir.mkdir(exist_ok=True)

    with mss.mss() as screen:
        # Monitor 0 represents the virtual desktop.
        # This includes all monitors if multiple displays are connected.
        monitor = screen.monitors[0]

        print("NOVA Screen Capture Test")
        print("-" * 30)
        print(f"Display: {monitor['width']} x {monitor['height']}")
        print("Capturing your screen...")

        # Capture one frame from the entire display.
        shot = screen.grab(monitor)

        # Convert the frame into an OpenCV image.
        frame = np.array(shot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Generate a unique filename.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = output_dir / f"capture_{timestamp}.png"

        # Save the captured image.
        success = cv2.imwrite(str(image_path), frame)

        if not success:
            raise RuntimeError("Failed to save the screenshot.")

        print(f"Capture successful: {image_path.resolve()}")
        print(f"Image dimensions: {frame.shape[1]} x {frame.shape[0]}")
        print("NOVA's eyes are working!")


if __name__ == "__main__":
    main()
