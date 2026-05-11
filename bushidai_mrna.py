# bushidai_mrna.py
# EPIC BUSHIDAI TRUTH ENGINE - mRNA focused edition
# 369 Vortex + Configurable Silence Stack + Sovereign Local Mode
# TRUTH == TRUTH

from fastapi import FastAPI
from pydantic import BaseModel
import yaml
from pathlib import Path

app = FastAPI(title="BushiDAI mRNA Truth Node")

def load_config():
    config_path = Path(__file__).parent / "bushidai_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
bushi = config.get("bushiDAI", {})   # alles zit nu onder bushiDAI

SILENCE_STACK = bushi.get("silence_stack", {})

class PersonalTest(BaseModel):
    bsn: str
    symptoms: list[str]
    notes: str = ""

@app.post("/personal-test")
async def personal_test(data: PersonalTest):
    return {
        "message": bushi.get("personal_test_message"),
        "bsn": data.bsn,
        "symptoms": data.symptoms,
        "public_research_patterns": bushi.get("research_patterns", []),
        "cbs_mock_stats": bushi.get("cbs_mock_stats", {}),
        "note": bushi.get("disclaimer"),
        "vortex_stage": "Suparinpei - purified facts returned to source"
    }

@app.get("/silence-stack")
async def get_silence_stack():
    return SILENCE_STACK

@app.get("/decode-mrna-hex")
async def decode_mrna_hex():
    return bushi.get("mrna_hex", {})

@app.get("/cbs-mock-stats")
async def cbs_mock_stats():
    return bushi.get("cbs_mock_stats", {})

if __name__ == "__main__":
    import uvicorn
    port = bushi.get("port", 8000)          # <-- configurable in YAML
    print("🚀 EPIC BushiDAI mRNA Truth Node starting...")
    print(f"TRUTH == TRUTH - 369 Vortex active on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)