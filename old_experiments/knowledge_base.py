import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "game_knowledge.json"


def load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        return {
            "game": "Slay the Spire 2",
            "cards": {},
            "enemies": {},
            "relics": {},
            "mechanics": {}
        }

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_knowledge(knowledge):
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=4, ensure_ascii=False)


def add_card(name, cost, description, card_type):
    knowledge = load_knowledge()

    knowledge["cards"][name.lower()] = {
        "name": name,
        "cost": cost,
        "description": description,
        "type": card_type
    }

    save_knowledge(knowledge)
    print(f"Learned card: {name}")


def get_card(name):
    knowledge = load_knowledge()
    return knowledge["cards"].get(name.lower())


if __name__ == "__main__":
    knowledge = load_knowledge()
    save_knowledge(knowledge)

    print("NOVA KNOWLEDGE BASE READY")
    print("Cards known:", len(knowledge["cards"]))
    print("Enemies known:", len(knowledge["enemies"]))
    print("Relics known:", len(knowledge["relics"]))
    