# BushiDAI Local — Installatie

Eenvoudige lokale AI-chat met 369 Vortex system prompt.  
Geen Docker nodig.

---

## Wat je nodig hebt

| Onderdeel | Waar te downloaden | Opmerking |
|-----------|---------------------|---------|
| **Ollama** | https://ollama.com | Verplicht |
| **Python 3.10+** | https://www.python.org | Verplicht |

---

## Eenmalige setup

1. Maak een map, bijvoorbeeld `BushiDAI`
2. Zet de volgende bestanden in die map:
   - `app.py`
   - `bushidai_local_client.py`
   - `bushidai_config.yaml`
   - `requirements.txt`
   - `start_lokaal.bat` (Windows)
   - `start_lokaal.sh` (Linux/macOS)
3. Open een terminal in die map en voer uit:

```bash
ollama pull qwen2.5:14b
pip install -r requirements.txt