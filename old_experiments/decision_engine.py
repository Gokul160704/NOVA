
from pathlib import Path
import json
from knowledge_base import get_card
def explain_known_cards(card_names):
    print("\nCARD KNOWLEDGE")

    for name in card_names:
        card = get_card(name)

        if card:
            print(
                f"- {card['name']}: "
                f"Cost {card['cost']}, "
                f"{card['type']}. "
                f"{card['description']}"
            )
        else:
            print(f"- {name}: Unknown card; needs verification.")

STATE_PATH = Path("game_state.json")


def load_game_state() -> dict:
    if not STATE_PATH.exists():
        raise FileNotFoundError(
            f"{STATE_PATH} not found. Run game_state.py first."
        )

    with STATE_PATH.open("r", encoding="utf-8") as file:
        state = json.load(file)

    if not isinstance(state, dict):
        raise ValueError("Game state must be a JSON object.")

    return state


def is_unknown(value) -> bool:
    return (
        value is None
        or not str(value).strip()
        or str(value).strip().lower() in {
            "unknown",
            "insufficient information",
            "none",
        }
    )


def evaluate_state(state: dict) -> dict:
    """Produce cautious advice using only the extracted game state."""

    health = state.get("player_health", "unknown")
    energy = state.get("energy", "unknown")
    enemy = state.get("enemy_name", "unknown")
    enemy_health = state.get("enemy_health", "unknown")
    cards = state.get("visible_cards", [])
    intent = state.get("visible_intent", "unknown")

    observations = []
    missing_information = []

    if is_unknown(health):
        missing_information.append("player health")
    else:
        observations.append(f"Player health: {health}")

    if is_unknown(energy):
        missing_information.append("combat energy")
    else:
        observations.append(f"Combat energy: {energy}")

    if is_unknown(enemy):
        missing_information.append("enemy identity")
    else:
        observations.append(f"Enemy: {enemy}")

    if is_unknown(enemy_health):
        missing_information.append("enemy health")
    else:
        observations.append(f"Enemy health: {enemy_health}")

    if not isinstance(cards, list) or not cards:
        missing_information.append("visible cards")
        cards = []
    else:
        observations.append(
            "Detected cards: " + ", ".join(str(card) for card in cards)
        )

    if is_unknown(intent):
        missing_information.append("enemy intent")

    # Do not invent card costs, damage, block, or game mechanics.
    # This initial engine reports what it can safely infer.
    if not cards:
        recommendation = (
            "Wait for a clearer screenshot showing the cards in hand."
        )
    elif is_unknown(energy):
        recommendation = (
            "Check combat energy before choosing a card to play."
        )
    elif is_unknown(enemy_health):
        recommendation = (
            "Verify enemy health before evaluating lethal damage."
        )
    else:
        recommendation = (
            "Cards and basic combat values were detected, but card costs, "
            "effects, and enemy intent are not sufficiently verified. "
            "Inspect those details before choosing a move."
        )

    return {
        "observations": observations,
        "recommendation": recommendation,
        "missing_information": missing_information,
        "automatic_play_enabled": False,
    }


def main():
    try:
        state = load_game_state()
        result = evaluate_state(state)

        print("NOVA DECISION ENGINE")
        print("=" * 35)
        print("\nOBSERVATIONS")

        for observation in result["observations"]:
            print(f"- {observation}")

        print("\nRECOMMENDATION")
        print(result["recommendation"])

        if result["missing_information"]:
            print("\nINFORMATION TO VERIFY")
            for item in result["missing_information"]:
                print(f"- {item}")

        print("\nAutomatic gameplay: DISABLED")

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Decision engine error: {error}")


if __name__ == "__main__":
    main()
explain_known_cards(state.get("visible_cards", []))