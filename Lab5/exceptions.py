"""Власні винятки гри."""


class GameError(Exception):
    """Базовий виняток гри."""


class InventoryFullError(GameError):
    """Немає місця в інвентарі."""


class NotEnoughItemsError(GameError):
    """Недостатньо предметів."""


class RecipeNotFoundError(GameError):
    """Така комбінація інгредієнтів не дає зілля."""
