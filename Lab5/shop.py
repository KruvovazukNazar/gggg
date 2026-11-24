"""Продаж зілль наприкінці дня."""
import random
from potions_data import POTIONS


def current_price(potion_id):
    """Ціна з денним коливанням ±10%."""
    try:
        return max(1, round(POTIONS[potion_id]["price"] * random.uniform(0.9, 1.1)))
    except KeyError:
        return 0


def sell(game, potion_id, qty, price):
    game.potions.remove(potion_id, qty)
    game.gold += price * qty
    return price * qty
