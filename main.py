from game import Game


def main():
    try:
        Game().run()
    except (KeyboardInterrupt, EOFError):
        print("\nГру перервано.")
    except Exception as e:
        print(f"Критична помилка: {e}")


if __name__ == "__main__":
    main()
