ADMIN_PASSWORD = "admin123"

products = {
    1: {"name": "Навушники", "price": 1299.99, "stock": 5},
    2: {"name": "Павербанк", "price": 799.50, "stock": 3},
    3: {"name": "Миша", "price": 450.00, "stock": 10},
    4: {"name": "Шоколад", "price": 55.90, "stock": 20},
    5: {"name": "Кава 250г", "price": 210.00, "stock": 8},
}

cart = {}

format_price = lambda value: f"{value:.2f}грн"
line_total = lambda pid, qty: products[pid]["price"] * qty
cart_total = lambda: sum(map(lambda item: line_total(item[0], item[1]), cart.items()))
available = lambda: sorted(filter(lambda item: item[1]["stock"] > 0, products.items()))


def read_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Потрібно ввести ціле число.")
        return None


def show_catalog():
    print("\n--- Каталог ---")
    for pid, product in available():
        print(f"[{pid}] {product['name']} - {format_price(product['price'])}")


def add_to_cart():
    show_catalog()
    pid = read_int("Id товару: ")
    qty = read_int("Кількість: ")
    if pid is None or qty is None:
        return
    if pid not in products:
        print("Товару з таким id не існує.")
        return
    if qty <= 0:
        print("Кількість має бути більше нуля.")
        return
    new_qty = cart.get(pid, 0) + qty
    if new_qty > products[pid]["stock"]:
        print(f"На складі лише {products[pid]['stock']} шт.")
        return
    cart[pid] = new_qty
    print("Додано в кошик.")


def show_cart():
    if not cart:
        print("Кошик порожній.")
        return
    print("\n--- Кошик ---")
    for pid, qty in cart.items():
        print(f"[{pid}] {products[pid]['name']} x{qty} = {format_price(line_total(pid, qty))}")
    print(f"Разом: {format_price(cart_total())}")


def remove_from_cart():
    if not cart:
        print("Кошик порожній.")
        return
    show_cart()
    pid = read_int("Id товару для видалення: ")
    if pid is None:
        return
    if pid not in cart:
        print("Цього товару немає в кошику.")
        return
    del cart[pid]
    print("Видалено з кошика.")


def buy():
    if not cart:
        print("Кошик порожній.")
        return
    show_cart()
    total = cart_total()
    for pid, qty in cart.items():
        products[pid]["stock"] -= qty
    cart.clear()
    print(f"Покупку здійснено! Сума: {format_price(total)}")


def admin_panel():
    if input("Пароль адміністратора: ") != ADMIN_PASSWORD:
        print("Невірний пароль.")
        return
    print("\n--- Залишки на складі (адмін) ---")
    for pid, product in sorted(products.items()):
        print(f"[{pid}] {product['name']}: {product['stock']} шт.")


def quit_shop():
    print("До побачення!")
    return False


menu = {
    "1": ("Переглянути каталог", show_catalog),
    "2": ("Додати товар в кошик", add_to_cart),
    "3": ("Переглянути кошик", show_cart),
    "4": ("Видалити товар з кошика", remove_from_cart),
    "5": ("Купити товари з кошика", buy),
    "6": ("Увійти як адміністратор", admin_panel),
    "0": ("Вихід", quit_shop),
}


def main():
    print("Ласкаво просимо до міні-магазину!")
    while True:
        print("\n=== Меню ===")
        for key, (title, _) in menu.items():
            print(f"{key}. {title}")
        choice = input("Ваш вибір: ").strip()
        if choice not in menu:
            print("Невірний пункт меню.")
            continue
        if menu[choice][1]() is False:
            break


if __name__ == "__main__":
    main()
