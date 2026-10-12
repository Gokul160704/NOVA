
import time
from pathlib import Path

import cv2
import mss
import numpy as np
import win32gui

OUTPUT_DIR = Path("captures")
OUTPUT_DIR.mkdir(exist_ok=True)

GAME_TITLE = "Slay the Spire 2"
COMPARE_WIDTH = 320
CHANGE_THRESHOLD = 8.0
SAVE_COOLDOWN = 3.0
FPS = 20


def main():
    previous_frame = None
    last_saved = 0.0
    frame_count = 0

    print("NOVA foreground-only capture started.")
    print("Capture runs only while Slay the Spire 2 is foreground.")
    print("Press Ctrl+C to stop.\n")

    try:
        with mss.MSS() as screen:
            while True:
                hwnd = win32gui.FindWindow(None, GAME_TITLE)

                # Never capture another application.
                if (
                    not hwnd
                    or win32gui.IsIconic(hwnd)
                    or win32gui.GetForegroundWindow() != hwnd
                ):
                    previous_frame = None
                    time.sleep(0.2)
                    continue

                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bottom - top

                if width <= 0 or height <= 0:
                    previous_frame = None
                    time.sleep(0.2)
                    continue

                region = {
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height,
                }

                image = np.array(screen.grab(region))
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

                compare_height = max(
                    1, int(height * COMPARE_WIDTH / width)
                )
                small = cv2.resize(
                    image, (COMPARE_WIDTH, compare_height)
                )

                now = time.monotonic()
                frame_count += 1

                if previous_frame is not None:
                    difference = float(
                        np.mean(cv2.absdiff(small, previous_frame))
                    )

                    if (
                        difference >= CHANGE_THRESHOLD
                        and now - last_saved >= SAVE_COOLDOWN
                    ):
                        filename = OUTPUT_DIR / (
                            time.strftime("event_%Y%m%d_%H%M%S")
                            + ".png"
                        )
                        if cv2.imwrite(str(filename), image):
                            last_saved = now
                            print(f"Gameplay saved: {filename}")

                previous_frame = small
                time.sleep(1 / FPS)

    except KeyboardInterrupt:
        print(f"\nNOVA capture stopped. Frames processed: {frame_count}")


if __name__ == "__main__":
    main()
