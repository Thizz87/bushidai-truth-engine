# bushidai_local_client.py
# Lokale Ollama client - strict scientific voor truth-seeking

import yaml
from pathlib import Path
import requests

def load_bushidai_config():
    config_path = Path(__file__).parent / "bushidai_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

bushidai_config = load_bushidai_config()

class BushiDAI_LocalClient:
    def __init__(self):
        self.url = "http://localhost:11434/api/chat"

    def _build_system_prompt(self) -> str:
        return """
You are a cold, strict, highly trained scientific analyst.
Answer ALWAYS in clear, structured, evidence-based English.

Rules (never break):
- Start with the exact number of sources found: "X sources were found."
- Give a complete, numbered list of studies: authors, title, year, key findings.
- Base everything strictly on the provided RAG context.
- Be factual, precise, clinical and uncompromising.
- No spiritual language, no zen, no ki, no vibes, no BushiDAI flair, no poetry, no softening.
"""

    def call(self, prompt: str, model: str = "llama3.2", temperature: float = 0.0):
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "stream": False
        }
        response = requests.post(self.url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["message"]["content"]

    def bushidai_query(self, prompt: str):
        return self.call(prompt)

# Globale instance
local = BushiDAI_LocalClient()