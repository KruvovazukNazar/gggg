products = [
    {"id": 1, "name": "Ноутбук Lenovo", "price": 24999.99, "quantity": 5},
    {"id": 2, "name": "Смартфон Samsung", "price": 15999.50, "quantity": 8},
    {"id": 3, "name": "Навушники JBL", "price": 1299.00, "quantity": 20},
    {"id": 4, "name": "Клавіатура Logitech", "price": 899.90, "quantity": 15},
    {"id": 5, "name": "Монітор Dell 24", "price": 6499.00, "quantity": 6},
]

cart = {}


def format_price(price):
    return f"{price:.2f} грн"


def find_product(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


def get_next_id():
    return max((p["id"] for p in products), default=0) + 1


def read_int(prompt):
    value = input(prompt).strip()
    if value.isdecimal():
        return int(value)
    print("Потрібно ввести ціле невід'ємне число.")
    return None


def read_float(prompt):
    value = input(prompt).strip().replace(",", ".")
    try:
        number = float(value)
    except ValueError:
        print("Потрібно ввести число (наприклад 199.99).")
        return None
    if 0 <= number < float("inf"):
        return number
    print("Число має бути невід'ємним і скінченним.")
    return None


def ask_new_price(current_price):
    value = input("Нова ціна (Enter - без змін): ").strip().replace(",", ".")
    if value == "":
        return current_price
    try:
        new_price = float(value)
        if 0 <= new_price < float("inf"):
            return new_price
    except ValueError:
        pass
    print("Некоректна ціна, залишено стару.")
    return current_price


def ask_new_quantity(current_quantity):
    value = input("Нова кількість (Enter - без змін): ").strip()
    if value == "":
        return current_quantity
    if value.isdecimal():
        return int(value)
    print("Некоректна кількість, залишено стару.")
    return current_quantity


def print_menu(title, lines):
    print(f"\n--- {title} ---")
    for line in lines:
        print(line)


def show_products(show_quantity=False):
    title = "ЗАЛИШКИ ТОВАРІВ (АДМІН)" if show_quantity else "КАТАЛОГ ТОВАРІВ"
    print(f"\n===== {title} =====")
    for p in products:
        if show_quantity:
            print(f"[{p['id']}] {p['name']}: {p['quantity']} шт. (ціна: {format_price(p['price'])})")
        else:
            print(f"[{p['id']}] {p['name']} - {format_price(p['price'])}")
    print("=" * (len(title) + 12))


def get_cart_total():
    return sum(find_product(pid)["price"] * qty for pid, qty in cart.items())


def add_to_cart(product_id, qty):
    product = find_product(product_id)
    if product is None:
        print("Товар з таким ID не знайдено.")
        return
    already = cart.get(product_id, 0)
    if already + qty > product["quantity"]:
        print(f"На складі недостатньо товару {product['name']}.")
        return
    cart[product_id] = already + qty
    print(f"Додано: {product['name']} x{qty}")


def remove_from_cart(product_id):
    if product_id in cart:
        del cart[product_id]
        print("Товар видалено з кошика.")
    else:
        print("Такого товару немає в кошику.")


def show_cart():
    if not cart:
        print("\nКошик порожній.")
        return
    print("\n===== ВАШ КОШИК =====")
    for pid, qty in cart.items():
        product = find_product(pid)
        print(f"{product['name']} x{qty} = {format_price(product['price'] * qty)}")
    print(f"Разом: {format_price(get_cart_total())}")
    print("=====================")


def checkout():
    if not cart:
        print("Кошик порожній, нічого купувати.")
        return
    for pid, qty in cart.items():
        product = find_product(pid)
        if qty > product["quantity"]:
            print(f"Недостатньо товару {product['name']} для покупки.")
            return
    total = get_cart_total()
    for pid, qty in cart.items():
        find_product(pid)["quantity"] -= qty
    print(f"\nПокупку оформлено! Сплачено: {format_price(total)}")
    cart.clear()


def add_product():
    print("\n--- Додавання нового товару ---")
    name = input("Назва товару: ").strip()
    if name == "":
        print("Назва не може бути порожньою.")
        return
    price = read_float("Ціна: ")
    if price is None:
        return
    quantity = read_int("Кількість на складі: ")
    if quantity is None:
        return
    products.append({"id": get_next_id(), "name": name, "price": price, "quantity": quantity})
    print(f"Товар «{name}» додано з ID {products[-1]['id']}.")


def edit_product():
    pid = read_int("ID товару для редагування: ")
    if pid is None:
        return
    product = find_product(pid)
    if product is None:
        print("Товар з таким ID не знайдено.")
        return
    print(f"Поточні дані: {product['name']}, {format_price(product['price'])}, "
          f"залишок {product['quantity']} шт.")
    new_name = input("Нова назва (Enter - без змін): ").strip()
    if new_name != "":
        product["name"] = new_name
    product["price"] = ask_new_price(product["price"])
    product["quantity"] = ask_new_quantity(product["quantity"])
    print("Товар оновлено.")


def delete_product():
    pid = read_int("ID товару для видалення: ")
    if pid is None:
        return
    product = find_product(pid)
    if product is None:
        print("Товар з таким ID не знайдено.")
        return
    if input(f"Точно видалити «{product['name']}»? (так/ні): ").strip().lower() != "так":
        print("Видалення скасовано.")
        return
    products.remove(product)
    cart.pop(pid, None)
    print("Товар видалено з каталогу.")


def admin_login():
    login = input("Логін адміністратора: ")
    password = input("Пароль: ")
    if login != "admin" or password != "1234":
        print("Невірний логін або пароль.")
        return

    print("\nВітаємо, адміністраторе!")
    while True:
        print_menu("Адмін-меню", [
            "1. Переглянути залишки товарів",
            "2. Переглянути каталог",
            "3. Додати товар",
            "4. Редагувати товар",
            "5. Видалити товар",
            "0. Вийти з адмін-панелі",
        ])
        choice = input("Ваш вибір: ").strip()
        if choice == "1":
            show_products(show_quantity=True)
        elif choice == "2":
            show_products()
        elif choice == "3":
            add_product()
        elif choice == "4":
            edit_product()
        elif choice == "5":
            delete_product()
        elif choice == "0":
            print("Вихід з адмін-панелі.")
            break
        else:
            print("Немає такого пункту меню.")


def main():
    name = input("Введіть ваше ім'я: ").strip() or "Гість"
    print(f"\nЛаскаво просимо до міні-магазину, {name}!")

    while True:
        print_menu("Меню магазину", [
            "1. Переглянути каталог товарів",
            "2. Додати товар в кошик",
            "3. Видалити товар з кошика",
            "4. Переглянути кошик",
            "5. Оформити покупку",
            "6. Увійти як адміністратор",
            "0. Вийти",
        ])
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            show_products()
        elif choice == "2":
            pid = read_int("ID товару: ")
            if pid is None:
                continue
            qty = read_int("Кількість: ")
            if qty is None:
                continue
            if qty == 0:
                print("Кількість має бути більшою за 0.")
                continue
            add_to_cart(pid, qty)
        elif choice == "3":
            pid = read_int("ID товару для видалення з кошика: ")
            if pid is not None:
                remove_from_cart(pid)
        elif choice == "4":
            show_cart()
        elif choice == "5":
            checkout()
        elif choice == "6":
            admin_login()
        elif choice == "0":
            print("До побачення!")
            break
        else:
            print("Немає такого пункту меню.")


if __name__ == "__main__":
    main()