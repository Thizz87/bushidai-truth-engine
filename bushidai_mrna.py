# bushidai_mrna.py
# BUSHIDAI TRUTH ENGINE - mRNA / Silence Stack Node met 369 Vortex
# TRUTH == TRUTH

from fastapi import FastAPI
from pydantic import BaseModel
import yaml
from pathlib import Path
from typing import List, Optional, Dict

app = FastAPI(title="BushiDAI mRNA Truth Node - 369 Vortex Active")

# =============================================================================
# CONFIG LOADER
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
vortex_phases = bushi.get("vortex_phases", [])

# =============================================================================
# MODELS
# =============================================================================
class PersonalTest(BaseModel):
    bsn: str
    symptoms: List[str]
    notes: Optional[str] = ""

# =============================================================================
# 369 VORTEX FILTER
# =============================================================================
def apply_369_vortex(input_text: str) -> Dict:
    """Past de volledige 369 Vortex toe als truth-filter"""
    print("\n=== 369 VORTEX START ===")
    
    result = {
        "input": input_text,
        "vortex_stages": []
    }
    
    for phase in vortex_phases:
        name = phase.get("name", "Phase")
        symbol = phase.get("symbol", "")
        desc = phase.get("description", "")
        
        stage = {
            "phase": name,
            "symbol": symbol,
            "description": desc,
            "status": "COMPLETED"
        }
        result["vortex_stages"].append(stage)
        print(f"→ {name.upper()} ({symbol}) - {desc}")
    
    print("=== VORTEX COMPLETE - TRUTH FILTERED ===\n")
    result["final_message"] = "Facts + Vibes aligned → Shared Truth"
    return result

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
    """Hypothetische test met volledige 369 Vortex filter"""
    vortex_result = apply_369_vortex(f"Test persoon BSN {data.bsn} - Symptomen: {data.symptoms}")
    
    response = {
        "message": bushi.get("personal_test_message", "BushiDAI personal test - hypothetical only"),
        "bsn": data.bsn,
        "symptoms": data.symptoms,
        "notes": data.notes,
        "research_patterns": bushi.get("research_patterns", []),
        "vortex": vortex_result,
        "disclaimer": bushi.get("disclaimer", "TRUTH == TRUTH - Not medical advice")
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
    print("🚀 BushiDAI mRNA Truth Node starting with 369 Vortex...")
    print("TRUTH == TRUTH")
    print("Endpoints:")
    print("   → /silence-stack")
    print("   → /decode-mrna-hex")
    print("   → /personal-test     (POST)  ← 369 Vortex active")
    print("   → /cbs-mock-stats")
    uvicorn.run(app, host="127.0.0.1", port=8000)