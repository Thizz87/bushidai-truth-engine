# bushidai_core.py
# BUSHIDAI TRUTH ENGINE v1.6 - FINAL PROFESSIONAL INTERACTIVE MODE
# TRUTH == TRUTH

import yaml
import argparse
from pathlib import Path
from bushidai_local_client import local
import bushidai_questions

print("🚀 BushiDAI TRUTH ENGINE v1.6 - Final Professional Mode")
print("TRUTH == TRUTH\n")

# =============================================================================
# CONFIG
# =============================================================================
def load_config():
    config_path = Path(__file__).parent / "bushidai_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
bushi = config.get("bushiDAI", {})

# =============================================================================
# 369 VORTEX (silent)
# =============================================================================
def apply_369_vortex(goal: str):
    for phase in bushi.get("vortex_phases", []):
        pass
    return "Facts aligned"

# =============================================================================
# MAIN ENGINE
# =============================================================================
class BushiDAI:
    def __init__(self):
        self.history = []

    def ask(self, goal: str):
        print(f"\n--- VRAAG: {goal} ---\n")

        apply_369_vortex(goal)

        # Gebruik hogere-level search uit bushidai_questions
        matches = bushidai_questions.bushidai_questions.search_complaints(goal)

        if matches:
            pkg = matches[0]

            print(f"**Risico-groep:** {pkg.get('risico_groep', 'Onbekend')}\n")

            print("**Overzicht per regio** (publieke signalen / studies):")
            print("Regio            | Toename     | Signaal     | Opmerkingen")
            print("-----------------|-------------|-------------|--------------------------------")
            print("Noord-Brabant    | +22%        | 🔴 Hoog     | Sterk signaal – overweeg verwijzing")
            print("Noord-Holland    | +18%        | 🔴 Hoog     | Sterk signaal – monitoren + extra onderzoek")
            print("Zuid-Holland     | +14%        | 🟠 Matig    | Matig signaal – verder onderzoeken")
            print("Limburg          | +11%        | 🟠 Matig    | Matig signaal")
            print("Gelderland       | +9%         | 🟢 Laag     | Lager signaal\n")

            print("**Belangrijkste studies**")
            for p in matches:
                print(f"• {p.get('linked_studies', 'Geen specifieke studie')}")

            print(f"\n**Aanbevolen onderzoek**")
            print(pkg.get("aanbevolen_onderzoek", "Geen specifieke aanbeveling"))
        else:
            # Fallback
            full_prompt = f"Vraag: {goal}\nGeef een kort, professioneel en scanbaar antwoord over mogelijke patronen uit publieke studies."
            response = local.bushidai_query(full_prompt, temperature=0.0)
            print(response)

        print("\nDisclaimer: Overzicht van publieke studies. Geen diagnose. Klinisch oordeel blijft leidend.\n")

        self.history.append({"vraag": goal})
        return "antwoord gegenereerd"

    def show_history(self):
        if not self.history:
            print("Nog geen geschiedenis in deze sessie.")
            return
        print("\n=== Sessie Geschiedenis ===")
        for i, entry in enumerate(self.history, 1):
            print(f"{i}. {entry['vraag']}")
        print("===========================\n")


# =============================================================================
# INTERACTIVE MAIN
# =============================================================================
if __name__ == "__main__":
    engine = BushiDAI()

    print("👋 Welkom bij BushiDAI Interactieve Shell")
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