users = {
    "user1": {"password": "qwerty1", "grades": [10, 12, 4, 7, 9, 3, 11, 6]},
    "user2": {"password": "pass2023", "grades": [2, 5, 8, 12, 1, 9, 4, 10]},
    "user3": {"password": "kovalenko_pw", "grades": [7, 7, 9, 3, 2, 11, 6, 5]},
    "user4": {"password": "taras123", "grades": [4, 6, 8, 10, 12, 1, 2, 9]},
}

login = input("Логін: ").strip()
password = input("Пароль: ").strip()

if login in users and users[login]["password"] == password:
    grades = users[login]["grades"]
    satisfactory = [g for g in grades if 5 <= g <= 12]
    unsatisfactory = [g for g in grades if 1 <= g <= 4]

    print(f"\n=== Ласкаво просимо, {login}! ===")
    print(f"Перелік усіх ваших оцінок: {grades}")
    print(f"Кількість задовільних оцінок (5-12): {len(satisfactory)} -> {satisfactory}")
    print(f"Кількість незадовільних оцінок (1-4): {len(unsatisfactory)} -> {unsatisfactory}")
else:
    print("Невірний логін або пароль.")
