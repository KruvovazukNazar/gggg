"""Варіння зілль."""
from exceptions import RecipeNotFoundError, GameError
from ingredients_data import INGREDIENTS
from potions_data import RECIPES


def find_recipe(ing_a, ing_b):
    try:
        key = tuple(sorted((INGREDIENTS[ing_a]["essence"], INGREDIENTS[ing_b]["essence"])))
        return RECIPES[key]
    except KeyError:
        raise RecipeNotFoundError("Ця суміш нестабільна — зілля не вийшло")


def brew(game, ing_a, ing_b):
    """Варить 1 зілля; при помилці нічого не витрачається. Повертає id зілля."""
    potion_id = find_recipe(ing_a, ing_b)
    if ing_a == ing_b and game.ingredients.count(ing_a) < 2:
        raise GameError("Потрібно 2 одиниці цього інгредієнта")
    if game.potions.free_space(potion_id) < 1:
        raise GameError("Інвентар зілль повний — спочатку продайте зілля")
    game.ingredients.remove(ing_a)
    try:
        game.ingredients.remove(ing_b)
    except GameError:
        game.ingredients.add(ing_a)  # відкат
        raise
    game.potions.add(potion_id)
    return potion_id
