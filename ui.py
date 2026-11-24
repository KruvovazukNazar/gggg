"""Безпечне введення."""


def ask_int(prompt, low, high):
    while True:
        try:
            value = int(input(prompt))
            if not low <= value <= high:
                raise ValueError
            return value
        except ValueError:
            print(f"  Введіть число від {low} до {high}.")


def show_inventory(inv, data, title):
    print(f"\n== {title} (слотів {len(inv.slots)}/{inv.max_slots}) ==")
    try:
        items = inv.summary()
        if not items:
            print("  порожньо")
        for i, (item_id, qty) in enumerate(items, 1):
            print(f"  {i}. {data[item_id]['name']} x{qty}")
        return items
    except KeyError as e:
        print(f"  Помилка даних: {e}")
        return []
