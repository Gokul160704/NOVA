
from pathlib import Path
import time
import ollama   

screenshot = Path("captures/event_20261010_222532.png")

if not screenshot.exists():
    raise FileNotFoundError(f"Screenshot not found: {screenshot}")

print(f"Screenshot: {screenshot}")
print("NOVA is analyzing the image...")

start = time.perf_counter()

response = ollama.chat(
    model="qwen2.5vl:3b",
    messages=[
        {
            "role": "user",
            "content": (
                "Analyze this game screenshot. Describe only what is "
                "visibly present: the game screen, important UI elements, "
                "visible cards or items, and the current situation. "
                "Do not guess details that cannot be read. "
                "Keep your answer concise."
            ),
            "images": [str(screenshot.resolve())],
        }
    ],
)

elapsed = time.perf_counter() - start

print("\n========== NOVA'S VISION ==========\n")
print(response["message"]["content"])
print(f"\nAnalysis time: {elapsed:.1f} seconds")
