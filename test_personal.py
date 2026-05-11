# test_core.py
# BUSHIDAI - Interactieve Shell (dynamisch)
# TRUTH == TRUTH

from bushidai_core import BushiDAI

if __name__ == "__main__":
    engine = BushiDAI()

    print("🚀 BushiDAI Interactieve Shell")
    print("TRUTH == TRUTH")
    print("Typ je vraag en druk op Enter.")
    print("Typ 'exit', 'quit' of 'stop' om te stoppen.\n")

    while True:
        try:
            goal = input("👉 ").strip()

            if goal.lower() in ["exit", "quit", "stop", "q"]:
                print("\nBushiDAI afgesloten.\n")
                break

            if not goal:
                continue

            print("\n" + "=" * 80)
            engine.ask(goal)          # Roept de core aan
            print("=" * 80 + "\n")

        except KeyboardInterrupt:
            print("\n\nBushiDAI afgesloten.")
            break
        except Exception as e:
            print(f"\nError: {e}\n")