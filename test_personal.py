# test_personal.py
# BUSHIDAI - Interactieve Shell voor huisartsen
# TRUTH == TRUTH

from bushidai_core import BushiDAI

if __name__ == "__main__":
    engine = BushiDAI()

    print("🚀 BushiDAI Interactieve Shell - Professioneel")
    print("TRUTH == TRUTH")
    print("Typ je vraag en druk op Enter.")
    print("Typ 'exit', 'quit', 'stop' of 'q' om te stoppen.")
    print("Typ 'history' om vorige vragen te zien.\n")

    while True:
        try:
            goal = input("👉 ").strip()

            if goal.lower() in ["exit", "quit", "stop", "q"]:
                print("\nBushiDAI afgesloten.\n")
                break

            if goal.lower() == "history":
                engine.show_history()
                continue

            if not goal:
                continue

            print("\n" + "=" * 90)
            engine.ask(goal)
            print("=" * 90 + "\n")

        except KeyboardInterrupt:
            print("\n\nBushiDAI afgesloten.")
            break
        except Exception as e:
            print(f"\nError: {e}\n")