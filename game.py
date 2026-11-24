"""Стан гри та ігровий цикл."""
import random
import config as cfg
from exceptions import GameError
from inventory import Inventory
from ingredients_data import INGREDIENTS
from potions_data import POTIONS
from brewing import brew
from shop import current_price, sell
from ui import ask_int, show_inventory


class Game:
    def __init__(self):
        self.day = 1
        self.gold = cfg.START_GOLD
        self.potions = Inventory(cfg.POTION_SLOTS, cfg.POTION_STACK)
        self.ingredients = Inventory(cfg.INGREDIENT_SLOTS, cfg.INGREDIENT_STACK)
        self.give_ingredients(cfg.START_INGREDIENTS)

    def give_ingredients(self, n):
        lost = 0
        for _ in range(n):
            try:
                ing = random.choice(list(INGREDIENTS))
                self.ingredients.add(ing)
                print(f"  + {INGREDIENTS[ing]['name']}")
            except GameError:
                lost += 1
        if lost:
            print(f"  Немає місця: {lost} інгр. втрачено")

    def brew_menu(self):
        items = show_inventory(self.ingredients, INGREDIENTS, "Інгредієнти")
        if not items:
            return
        try:
            a = items[ask_int("Перший інгредієнт (0 - назад): ", 0, len(items)) - 1][0]
            b = items[ask_int("Другий інгредієнт (0 - назад): ", 0, len(items)) - 1][0]
            potion = brew(self, a, b)
            print(f"  Готово: {POTIONS[potion]['name']}!")
        except IndexError:
            print("  Скасовано.")
        except GameError as e:
            print(f"  {e}")

    def recipe_book(self):
        try:
            for p in POTIONS.values():
                a, b = p["recipe"]
                print(f"  {p['name']} = стихія {a} + {b} (ціна ~{p['price']})")
        except KeyError as e:
            print(f"  Помилка даних: {e}")

    def sell_phase(self):
        print("\n--- Вечір: торгівля ---")
        while True:
            items = show_inventory(self.potions, POTIONS, "Зілля")
            if not items:
                return
            prices = {pid: current_price(pid) for pid, _ in items}
            for i, (pid, q) in enumerate(items, 1):
                print(f"  {i}. ціна {prices[pid]} зол.")
            print("Золото:", self.gold)
            c = ask_int("Номер зілля для продажу (0 - закінчити): ", 0, len(items))
            if c == 0:
                return
            try:
                pid, qty = items[c - 1]
                n = ask_int(f"Скільки продати (1-{qty}): ", 1, qty)
                print(f"  Виручка: {sell(self, pid, n, prices[pid])}")
            except GameError as e:
                print(f"  {e}")

    def end_day(self):
        self.sell_phase()
        self.gold -= cfg.DAILY_RENT
        print(f"\nОренда лабораторії: -{cfg.DAILY_RENT}. Золото: {self.gold}")
        self.day += 1
        print(f"\nДень {self.day}. Нові інгредієнти:")
        self.give_ingredients(cfg.DAILY_INGREDIENTS)

    def check_end(self):
        """Повертає текст кінцівки або None."""
        if self.gold >= cfg.WIN_GOLD:
            return "ПЕРЕМОГА! Ти назбирав на Філософський камінь і став великим алхіміком!"
        if self.gold < 0:
            return "ПОРАЗКА. Ти не зміг сплатити оренду — лабораторію закрили."
        if self.day > cfg.MAX_DAYS:
            return "ПОРАЗКА. Час вийшов: гільдія алхіміків відмовила тобі в камені."
        return None

    def run(self):
        print("=== АЛХІМІК ===")
        print(f"Мета: {cfg.WIN_GOLD} золота за {cfg.MAX_DAYS} днів. Оренда {cfg.DAILY_RENT}/день.")
        while True:
            ending = self.check_end()
            if ending:
                print("\n" + ending)
                return
            print(f"\n--- День {self.day}/{cfg.MAX_DAYS} | Золото: {self.gold} ---")
            print("1 Інгредієнти  2 Зілля  3 Варити  4 Рецепти  5 Завершити день  0 Вихід")
            choice = ask_int("> ", 0, 5)
            if choice == 1:
                show_inventory(self.ingredients, INGREDIENTS, "Інгредієнти")
            elif choice == 2:
                show_inventory(self.potions, POTIONS, "Зілля")
            elif choice == 3:
                self.brew_menu()
            elif choice == 4:
                self.recipe_book()
            elif choice == 5:
                self.end_day()
            else:
                print("Гру завершено.")
                return
