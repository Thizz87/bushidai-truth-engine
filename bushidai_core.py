# bushidai_core.py
# BUSHIDAI TRUTH ENGINE v1.5 - INTERACTIVE PROFESSIONAL MODE
# TRUTH == TRUTH

import yaml
import argparse
from pathlib import Path
from bushidai_local_client import local
import bushidai_questions

print("🚀 BushiDAI TRUTH ENGINE v1.5 - Interactief")
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
# 369 VORTEX (silent backend only)
# =============================================================================
def apply_369_vortex(goal: str):
    """Vortex draait stil achter de schermen"""
    for phase in bushi.get("vortex_phases", []):
        pass
    return "Facts aligned"

# =============================================================================
# MAIN ENGINE
# =============================================================================
class BushiDAI:
    def __init__(self):
        self.history = []   # simpele sessie-history

    def ask(self, goal: str):
        print(f"\n--- VRAAG: {goal} ---\n")

        apply_369_vortex(goal)   # silent

        # SPARQL indien relevant
        if any(x in goal.lower() for x in ["sparql", "query", "ttl"]):
            sparql_result = bushidai_questions.bushidai_questions.query(goal)
            context = str(sparql_result)
        else:
            context = ""

        full_prompt = f"""
Context:
{context}

Vraag: {goal}

Geef een kort, professioneel en direct scanbaar antwoord.
Gebruik tabellen waar het overzichtelijker is.
Wees feitelijk, geen fluff.
"""

        response = local.bushidai_query(full_prompt, temperature=0.0)

        print(response)
        print("\nDisclaimer: Overzicht van publieke studies. Geen diagnose. Klinisch oordeel blijft leidend.\n")

        # Sla op in history
        self.history.append({"vraag": goal, "antwoord": response})

        return response

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
                print("\nBushiDAI afgesloten. Tot de volgende keer.\n")
                break

            if goal.lower() == "history":
                engine.show_history()
                continue

            if not goal:
                continue

            print("\n" + "=" * 85)
            engine.ask(goal)
            print("=" * 85 + "\n")

        except KeyboardInterrupt:
            print("\n\nBushiDAI afgesloten.")
            break
        except Exception as e:
            print(f"\nError: {e}\n")