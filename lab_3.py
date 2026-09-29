ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "1234"


def format_price(price):
    """Ціна у форматі ххх.ххгрн"""
    return f"{price:.2f}грн"


class Product:
    def __init__(self, name, price, count):
        self.name = name
        self.price = price
        self.count = count


class Cart:
    """Кошик: зберігає {товар: кількість}, без дублікатів."""

    def __init__(self):
        self._items = {}

    def add(self, product, qty=1):
        self._items[product] = self._items.get(product, 0) + qty

    def remove(self, product):
        self._items.pop(product, None)

    def quantity_of(self, product):
        return self._items.get(product, 0)

    def is_empty(self):
        return not self._items

    def items(self):
        return list(self._items.items())

    def total(self):
        return sum(map(lambda item: item[0].price * item[1], self._items.items()))

    def clear(self):
        self._items.clear()


class Shop:
    """Уся логіка магазину, без input/print."""

    def __init__(self):
        self.products = [
            Product("Хліб", 25.50, 10),
            Product("Молоко", 40.00, 8),
            Product("Шоколад", 50.00, 5),
            Product("Кава", 100.00, 6),
            Product("Печиво", 35.50, 10),
        ]
        self.cart = Cart()

    def available(self, product):
        return product.count - self.cart.quantity_of(product)

    def add_to_cart(self, number, qty):
        if not 1 <= number <= len(self.products):
            return "Неправильний номер товару"
        if qty < 1:
            return "Кількість має бути більшою за 0"
        product = self.products[number - 1]
        if qty > self.available(product):
            return f"Недостатньо товару. Доступно: {self.available(product)}"
        self.cart.add(product, qty)
        return f"Додано: {product.name} x{qty}"

    def remove_from_cart(self, position):
        items = self.cart.items()
        if not 1 <= position <= len(items):
            return "Неправильний номер"
        product = items[position - 1][0]
        self.cart.remove(product)
        return f"Видалено: {product.name}"

    def checkout(self):
        total = self.cart.total()
        for product, qty in self.cart.items():
            product.count -= qty
        self.cart.clear()
        return total

    def stock_report(self):
        return sorted(self.products, key=lambda p: p.count)


def check_admin(login, password):
    return login == ADMIN_LOGIN and password == ADMIN_PASSWORD


def read_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Введіть ціле число")
        return None


def show_catalog(shop):
    print("\n--- КАТАЛОГ ---")
    for i, p in enumerate(shop.products, start=1):
        print(f"{i}. {p.name} - {format_price(p.price)} (доступно: {shop.available(p)})")


def show_cart(shop):
    print("\n--- КОШИК ---")
    if shop.cart.is_empty():
        print("Кошик порожній")
        return
    for i, (p, qty) in enumerate(shop.cart.items(), start=1):
        print(f"{i}. {p.name} x{qty} = {format_price(p.price * qty)}")
    print("Всього:", format_price(shop.cart.total()))


def add_flow(shop):
    show_catalog(shop)
    number = read_int("Номер товару: ")
    if number is None:
        return
    qty = read_int("Кількість: ")
    if qty is None:
        return
    print(shop.add_to_cart(number, qty))


def delete_flow(shop):
    show_cart(shop)
    if shop.cart.is_empty():
        return
    position = read_int("Який товар видалити? ")
    if position is not None:
        print(shop.remove_from_cart(position))


def buy_flow(shop):
    if shop.cart.is_empty():
        print("Кошик порожній")
        return
    show_cart(shop)
    answer = input("Купити? (так/ні): ").strip().lower()
    if answer == "так":
        total = shop.checkout()
        print(f"Покупка успішна! Сплачено: {format_price(total)}")
    else:
        print("Покупку скасовано")


def admin_flow(shop):
    login = input("Логін: ")
    password = input("Пароль: ")
    if not check_admin(login, password):
        print("Неправильний логін або пароль")
        return
    print("\n--- ЗАЛИШКИ ---")
    for p in shop.stock_report():
        print(f"{p.name} - {p.count} шт.")


def main():
    shop = Shop()
    actions = {
        "1": show_catalog,
        "2": add_flow,
        "3": show_cart,
        "4": delete_flow,
        "5": buy_flow,
        "6": admin_flow,
    }

    while True:
        print("\n--- МІНІ МАГАЗИН ---")
        print("1 - Каталог")
        print("2 - Додати в кошик")
        print("3 - Кошик")
        print("4 - Видалити з кошика")
        print("5 - Купити")
        print("6 - Адміністратор")
        print("0 - Вихід")

        choice = input("Виберіть дію: ").strip()
        if choice == "0":
            print("Вихід...")
            break
        action = actions.get(choice)
        if action:
            action(shop)
        else:
            print("Такого пункту немає")


if __name__ == "__main__":
    main()
