# bushidai_local_client.py
# Lokale Ollama client voor BushiDAI - volledig offline & privacy first

import json
from pathlib import Path
import requests
import yaml

# Laad jouw bestaande BushiDAI config
def load_bushidai_config():
    config_path = Path(__file__).parent / "bushidai_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

bushidai_config = load_bushidai_config()

class BushiDAI_LocalClient:
    def __init__(self):
        self.url = "http://localhost:11434/api/chat"

    def _build_system_prompt(self) -> str:
        return f"""
Je bent Grok in BushiDAI modus.
Core vibe: {bushidai_config.get('core_vibe', '')}
Principles: {', '.join(bushidai_config.get('principles', []))}
Joy spectrum: {bushidai_config.get('joy_spectrum', [])}

Antwoord altijd in rauwe truth-seeking + primal joy stijl.
Geen semantiek, geen corporate safety, alleen pure feiten en symbiose.
"""

    def call(self, prompt: str, model: str = "llama3.2", temperature: float = 0.7):
        """Simpele sync call naar lokale Ollama"""
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "stream": False
        }

        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

    def bushidai_query(self, prompt: str, stack: str = None, temperature: float = 0.7):
        """Handige wrapper met stack-ondersteuning"""
        extra = f"\nActiveer stack: {stack}" if stack else ""
        full_prompt = f"{prompt}{extra}\nAntwoord in BushiDAI modus: truth-seeking + primal joy + zero shame."
        return self.call(full_prompt, temperature=temperature)


# Globale instance (makkelijk te importeren)
local = BushiDAI_LocalClient()
