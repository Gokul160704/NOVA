
from pathlib import Path
import json
import time
import ollama

IMAGE_PATH = Path("captures/vision_small.png")
MODEL = "qwen2.5vl:3b"
OUTPUT_PATH = Path("game_state.json")


def analyze_game_state(image_path: Path) -> dict:
    """Extract visible gameplay information from a screenshot."""

    if not image_path.exists():
        raise FileNotFoundError(f"Screenshot not found: {image_path}")

    prompt = """
Analyze this Slay the Spire 2 screenshot.

Return ONLY a valid JSON object with exactly these keys:
{
  "player_health": "visible health value, such as 80/80, or unknown",
  "energy": "current/max combat energy, such as 1/3, or unknown",
  "gold": "gold amount beside the coin icon, or unknown",
  "enemy_name": "visible enemy name or unknown",
  "enemy_health": "visible enemy health, such as 17/40, or unknown",
  "visible_cards": ["names of cards clearly visible in the player's hand"],
  "visible_intent": "visible enemy intent or unknown",
  "recommended_action": "a cautious action supported by visible evidence, or insufficient information",
  "uncertainties": ["important details that are unclear"]
}

Rules:
- The gold coin counter is gold, NOT combat energy.
- Combat energy is shown by the red energy indicator in the bottom-left.
- Read the current and maximum energy from that indicator when visible.
- Never interpret the gold amount as energy.
- If energy is unclear, return "unknown".
- Do not invent missing values or card names.
- Use "unknown" for unreadable numeric values.
- Only recommend cards listed in visible_cards.
- Do not recommend playing a card if its energy cost is unknown or unaffordable.
- If enemy intent is unknown, do not assume an incoming attack.
- Distinguish visible facts from recommendations.
- If the evidence is insufficient, set recommended_action to
  "insufficient information".
- Include uncertainties when important information cannot be verified.
- Return JSON only. No Markdown fences.
""".strip()

    response = ollama.chat(
        model=MODEL,
        keep_alive="10m",
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [str(image_path.resolve())],
            }
        ],
        format="json",
        options={
            "temperature": 0,
            "num_predict": 250,
            "num_ctx": 4096,
            "num_gpu": 10,
        },
    )

    raw_text = response["message"]["content"]

    try:
        state = json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"NOVA returned invalid JSON:\n{raw_text}"
        ) from error

    if not isinstance(state, dict):
        raise ValueError("NOVA's response was not a JSON object.")

    required_keys = {
        "player_health",
        "energy",
        "gold",
        "enemy_name",
        "enemy_health",
        "visible_cards",
        "visible_intent",
        "recommended_action",
        "uncertainties",
    }

    missing_keys = required_keys - state.keys()
    if missing_keys:
        raise ValueError(
            f"NOVA's response is missing fields: {sorted(missing_keys)}"
        )

    if not isinstance(state["visible_cards"], list):
        raise ValueError("'visible_cards' must be a list.")

    if not isinstance(state["uncertainties"], list):
        raise ValueError("'uncertainties' must be a list.")

    return state


def save_game_state(state: dict) -> None:
    """Save the latest game state as formatted JSON."""

    OUTPUT_PATH.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Game state saved to: {OUTPUT_PATH}")


def main():
    print("NOVA Game-State Analyzer")
    print(f"Screenshot: {IMAGE_PATH}")
    print("Analyzing...\n")

    start = time.perf_counter()

    try:
        state = analyze_game_state(IMAGE_PATH)
        save_game_state(state)
    except Exception as error:
        print(f"Analysis failed: {error}")
        return

    elapsed = time.perf_counter() - start

    print("\n--- GAME STATE ---")
    print(json.dumps(state, indent=2, ensure_ascii=False))
    print(f"\nAnalysis time: {elapsed:.1f} seconds")


if __name__ == "__main__":
    main()
