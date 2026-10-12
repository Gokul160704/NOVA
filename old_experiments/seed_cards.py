
from knowledge_base import add_card, get_card

# Initial Ironclad cards.
# Verify these values against your current game version.
INITIAL_CARDS = [
    {
        "name": "Strike",
        "cost": 1,
        "description": "Deal 6 damage.",
        "type": "Attack",
    },
    {
        "name": "Defend",
        "cost": 1,
        "description": "Gain 5 Block.",
        "type": "Skill",
    },
]


def main():
    for card in INITIAL_CARDS:
        existing = get_card(card["name"])

        if existing:
            print(f"Already known: {card['name']}")
            continue

        add_card(
    name=card["name"],
    cost=card["cost"],
    description=card["description"],
    card_type=card["type"],
)

    print("\nNOVA's initial card knowledge is ready.")


if __name__ == "__main__":
    main()
