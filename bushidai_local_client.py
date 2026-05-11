# bushidai_local_client.py - OPTIMALE OLLAMA CLIENT
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
        self.model = "llama3.2"          # snel en stabiel

    def _build_system_prompt(self) -> str:
        return """
You are a cold, strict, highly trained scientific analyst.
Answer ALWAYS in clear, structured, evidence-based English.
Be direct, factual and precise. No fluff. No hedging.
"""

    def bushidai_query(self, prompt: str, temperature: float = 0.0):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,      # 0.0 = maximaal feitelijk
            "stream": False,
            "options": {
                "num_ctx": 8192,             # grotere context
                "num_thread": 0              # laat Ollama zelf optimaliseren
            }
        }
        try:
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            return f"OLLAMA ERROR: {e} (is Ollama running?)"

local = BushiDAI_LocalClient()