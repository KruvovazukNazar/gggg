"""Універсальний інвентар зі слотами та стаками."""
from exceptions import InventoryFullError, NotEnoughItemsError


class Inventory:
    def __init__(self, max_slots, stack_size):
        self.max_slots = max_slots
        self.stack_size = stack_size
        self.slots = []  # список [item_id, кількість]

    def free_space(self, item_id):
        """Скільки одиниць цього предмета ще влізе."""
        space = sum(self.stack_size - s[1] for s in self.slots if s[0] == item_id)
        space += (self.max_slots - len(self.slots)) * self.stack_size
        return space

    def add(self, item_id, qty=1):
        if qty <= 0:
            raise ValueError("Кількість має бути додатною")
        if qty > self.free_space(item_id):
            raise InventoryFullError("Недостатньо місця в інвентарі")
        for slot in self.slots:
            if slot[0] == item_id and slot[1] < self.stack_size:
                put = min(qty, self.stack_size - slot[1])
                slot[1] += put
                qty -= put
        while qty > 0:
            put = min(qty, self.stack_size)
            self.slots.append([item_id, put])
            qty -= put

    def count(self, item_id):
        return sum(s[1] for s in self.slots if s[0] == item_id)

    def remove(self, item_id, qty=1):
        if qty <= 0:
            raise ValueError("Кількість має бути додатною")
        if self.count(item_id) < qty:
            raise NotEnoughItemsError("Недостатньо предметів")
        for slot in reversed(self.slots[:]):
            if slot[0] == item_id:
                take = min(qty, slot[1])
                slot[1] -= take
                qty -= take
                if slot[1] == 0:
                    self.slots.remove(slot)
            if qty == 0:
                break

    def summary(self):
        """Список (item_id, загальна кількість) без дублів."""
        result = {}
        for item_id, qty in self.slots:
            result[item_id] = result.get(item_id, 0) + qty
        return list(result.items())
