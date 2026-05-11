# bushidai_mrna.py
# BUSHIDAI TRUTH ENGINE - mRNA / Silence Stack Node
# TRUTH == TRUTH - PROFESSIONAL MODE

from fastapi import FastAPI
from pydantic import BaseModel
import yaml
from pathlib import Path
from typing import List, Optional, Dict

app = FastAPI(title="BushiDAI mRNA Truth Node - Professional Mode")

# =============================================================================
# CONFIG
# =============================================================================
def load_config():
    config_path = Path(__file__).parent / "bushidai_config.yaml"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️ Error loading config: {e}")
        return {}

config = load_config()
bushi = config.get("bushiDAI", {})

# =============================================================================
# 369 VORTEX (silent)
# =============================================================================
def apply_369_vortex(input_text: str) -> Dict:
    """Vortex draait stil achter de schermen"""
    for phase in bushi.get("vortex_phases", []):
        pass
    return {"status": "Facts aligned"}

# =============================================================================
# MODELS
# =============================================================================
class PersonalTest(BaseModel):
    bsn: str
    symptoms: List[str]
    notes: Optional[str] = ""

# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/silence-stack")
async def get_silence_stack():
    return bushi.get("silence_stack", {})

@app.get("/decode-mrna-hex")
async def decode_mrna_hex():
    return bushi.get("mrna_hex", {})

@app.post("/personal-test")
async def personal_test(data: PersonalTest):
    vortex_result = apply_369_vortex(f"Test BSN {data.bsn}")
    
    response = {
        "bsn": data.bsn,
        "symptoms": data.symptoms,
        "notes": data.notes,
        "research_patterns": bushi.get("research_patterns", []),
        "disclaimer": bushi.get("disclaimer", "Overzicht van publieke studies. Geen diagnose.")
    }
    return response

@app.get("/cbs-mock-stats")
async def cbs_mock_stats():
    return bushi.get("cbs_mock_stats", {})

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    print("🚀 BushiDAI mRNA Truth Node - Professional Mode")
    print("TRUTH == TRUTH")
    uvicorn.run(app, host="127.0.0.1", port=8000)