
from knowledge_base import get_card

for name in ["Strike", "Defend", "Bash"]:
    card = get_card(name)

    if card:
        print(f"\n{name}:")
        print(f"  Cost: {card['cost']}")
        print(f"  Type: {card['type']}")
        print(f"  Effect: {card['description']}")
    else:
        print(f"\n{name}: Not in NOVA's knowledge base.")
