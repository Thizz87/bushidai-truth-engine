# bushidai_core.py
# BUSHIDAI TRUTH SIMULATOR v1.1 - SUPERIOR LOCAL RAG EDITION
# TRUTH == TRUTH
import yaml
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import ollama
import argparse
from typing import List, Dict

print("BUSHIDAI TRUTH SIMULATOR v1.1 - SUPERIOR LOCAL RAG")
print("TRUTH == TRUTH\n")

# =============================================================================
# CONFIG
# =============================================================================
def load_config():
    config_path = Path(__file__).parent / "bushidai_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()

# =============================================================================
# CHROMA + OLLAMA EMBEDDINGS
# =============================================================================
chroma_client = chromadb.PersistentClient(path="./bushidai_chroma_db")
embedding_func = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="nomic-embed-text"
)

collection = chroma_client.get_or_create_collection(
    name="bushidai_truth",
    embedding_function=embedding_func
)

# =============================================================================
# LOCAL OLLAMA CLIENT (strict scientific mode)
# =============================================================================
def ask_ollama(prompt: str, temperature: float = 0.0) -> str:
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperature}
    )
    return response['message']['content']

# =============================================================================
# BUSHIDAI CORE
# =============================================================================
class BushiDAI:
    def __init__(self):
        self.vortex_phases = config.get("vortex_phases", [])

    def run_vortex(self):
        print("🔥 369 VORTEX START")
        for phase in self.vortex_phases:
            print(f"→ {phase['name']} ({phase['symbol']}) - {phase['description']}")
        print("🔥 VORTEX COMPLETE - TRUTH FILTERED\n")

    def ask(self, goal: str):
        print(f"\n=== VRAAG: {goal} ===\n")

        # 1. RAG retrieval via Chroma
        results = collection.query(
            query_texts=[goal],
            n_results=20,           # haal veel op
            include=["documents", "metadatas"]
        )

        context = "\n\n".join(results["documents"][0]) if results["documents"] else "Geen documenten gevonden."
        source_count = len(results["documents"][0]) if results["documents"] else 0

        # 2. Sterke wetenschappelijke prompt (beter dan AnythingLLM)
        full_prompt = f"""
Je bent een koude, strenge, wetenschappelijke analist.
Gebruik ALLEEN de opgehaalde context hieronder.

Context ({source_count} bronnen gevonden):
{context}

Vraag: {goal}

ANTWOORD REGELS (strikt volgen):
- Begin met: "{source_count} bronnen werden gevonden."
- Geef daarna een volledige, genummerde lijst van studies.
- Voor elke studie: auteur(s), titel, jaar, key findings.
- Wees 100% feitelijk, evidence-based, geen spiritualiteit, geen vibes, geen zen.
- Antwoord in helder, professioneel Engels.
"""

        raw_response = ask_ollama(full_prompt, temperature=0.0)

        # 3. 369 Vortex truth filter
        self.run_vortex()

        print(raw_response)

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", nargs="+", default=["Vraag naar specifieke studies over witte fibrine clots"])
    args = parser.parse_args()

    engine = BushiDAI()

    for goal in args.goals:
        engine.ask(goal)