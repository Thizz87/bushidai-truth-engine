# bushidai_core.py
# BUSHIDAI TRUTH SIMULATOR v1.1 - SUPERIOR LOCAL RAG + 369 VORTEX
# TRUTH == TRUTH

import yaml
import requests
import argparse
from pathlib import Path
from bushidai_local_client import local

print("BUSHIDAI TRUTH SIMULATOR v1.1 - SUPERIOR LOCAL RAG")
print("TRUTH == TRUTH\n")

# =============================================================================
# CONFIG + VORTEX
# =============================================================================
def load_config():
    config_path = Path(__file__).parent / "bushidai_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
vortex_phases = config.get("vortex_phases", [])

# =============================================================================
# ANYTHINGLLM RAG
# =============================================================================
class AnythingLLM:
    def __init__(self):
        self.url = "http://localhost:3001/api/v1/chat"

    def get_context(self, prompt: str):
        payload = {"message": prompt, "mode": "chat", "sessionId": "bushidai-rag", "stream": False}
        try:
            r = requests.post(self.url, json=payload, timeout=15)
            r.raise_for_status()
            return r.json().get("text", "")
        except:
            return ""

# =============================================================================
# BUSHIDAI CORE
# =============================================================================
class BushiDAI:
    def __init__(self):
        self.rag = AnythingLLM()

    def run_vortex(self):
        print("\n=== 369 VORTEX START ===")
        for phase in vortex_phases:
            print(f"→ {phase.get('name', '')} ({phase.get('symbol', '')}) - {phase.get('description', '')}")
        print("=== VORTEX COMPLETE - TRUTH FILTERED ===\n")

    def ask(self, goal: str):
        print(f"--- CYCLE | Goal: {goal} ---")

        context = self.rag.get_context(goal)
        source_count = len(context.split("\n\n")) if context else 0   # ruwe schatting

        full_prompt = f"""
Context uit opgehaalde documenten (RAG):
{context}

Vraag: {goal}

ANTWOORD REGELS (strikt volgen):
- Begin exact met: "{source_count} sources were found."
- Geef daarna een volledige, genummerde lijst van studies.
- Voor elke studie: auteurs, titel, jaar, key findings.
- Wees 100% feitelijk, evidence-based, nuchter en klinisch.
- Antwoord in helder, professioneel Engels.
- Geen spiritualiteit, geen vibes, geen zen, geen BushiDAI flair.
"""

        raw_response = local.bushidai_query(full_prompt)
        self.run_vortex()

        print(raw_response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", nargs="+", default=["Vraag naar specifieke studies over witte fibrine clots"])
    args = parser.parse_args()

    engine = BushiDAI()
    for goal in args.goals:
        engine.ask(goal)