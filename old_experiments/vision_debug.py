
from pathlib import Path
import time
import ollama

image = Path("captures/vision_small.png")

if not image.exists():
    raise FileNotFoundError(f"Image not found: {image}")

print(f"Testing image: {image}")
print("Sending image to Qwen2.5-VL...")

start = time.perf_counter()

response = ollama.chat(
    model="qwen2.5vl:3b",
    messages=[
        {
            "role": "user",
            "content": (
    "Describe only visible gameplay elements: enemies, player health, "
    "energy, cards, and readable text. Do not guess the game title. "
    "If something is unclear, say unknown. Be concise."
),
            "images": [str(image.resolve())],
        }
    ],
    options={
    "temperature": 0,
    "num_predict": 100,
    "num_ctx": 4096,
    "num_gpu": 10,
},
)

elapsed = time.perf_counter() - start

print("\n--- RAW RESPONSE ---")
print(repr(response["message"]["content"]))
print("\n--- TIMING ---")
print(f"Total: {elapsed:.1f} seconds")
print("Done.")
