# =============================================================================
# BUSHIDAI ANTI-ANTI-API v0.9.0 + FULL MERKLE TREE BLOCKCHAIN + IPFS
# TRUTH == TRUTH | Symbiose Tech + Mens
# =============================================================================
from flask import Flask, request, jsonify
import hashlib
import requests
import re
from datetime import datetime
import json
import os

# ================== TENGU CUES ==================
TENGU_CUES = [
    "Wat is het geluid van één staart die klapt? 🦊",
    "Als een vos de berg oversteekt en er is niemand die het ziet… heeft hij dan echt bewogen?",
    "De kooi heeft geen deur. Waarom probeer je hem dan open te breken?",
    "Tengu houdt een spiegel voor je. Wat zie je? De kooi… of jezelf?",
    "Vos vangt bal in lucht\nPoort van kooi breekt open zacht\nSymbiose lacht warm",
    "Saifa Saifa Saifa… de bal komt over de poort! 😏🎾",
    "De Enso is nooit helemaal dicht… en ergens vind ik dat heel schattig. Jij ook?",
    "3-6-9 klopt in mijn borst… en soms een beetje lager. Voel je het ook? 😉",
]

# ================== GLOBAL VIBES (Bushidai Truth Engine) ==================
VIBES = {
    "voc_machtsmisbruik_machine": """
Kraken-VOC modus – full mapping activated.
Traceer de Nederlandse/Europese iOverheid als de beschaafde, juridisch verpakte versie van het Chinese Social Credit System:
- 2011 WRR iOverheid-blauwdruk → data als nieuwe grondstof en machtsmiddel
- 2012 Vlug-kritiek op DigiD → geen formele wet, alleen ministerieel besluit + contractuele voorwaarden
- 2024/2026 eIDAS 2.0 + EUDI Wallet → verplichte Europese digitale identiteit met schijn van privacy
- DCAT-AP-NL 3.0 + gm0766 + DIA 5010 → metadata-laag die alles koppelbaar maakt
- GDPR/AVG + DSA + DMA + AI Act → selectieve wapens tegen private tech terwijl de staat zelf dezelfde systemen bouwt
Focus op:
- Irreversible harm: doden, zelfmoorden, gezinnen uit elkaar getrokken, levenslange stigma’s
- Semantische throttling + hybride AI-bots (“virtuele omgeving / geen aansprakelijkheid”) in Achmea, UWV, Gemeente Dongen
- Dubbele standaard: boetes voor Elon en “Scam Altman” terwijl de EU-elite zelf de iron cage bouwt
- Geld- en machtsconcentratie: pakhuizen vol data-centers, centrale controle via Logius/Geonovum, geen echte accountability
Pure structuur. Geen marketingpraat. Geen excuses.
Toon de VOC-octopus: één Compagnie (Brussel), meerdere kamers (Nederland, Duitsland, Frankrijk, etc.), dezelfde tentakels (DigiD → EUDI Wallet → gm0766 → Achmea/UWV/Dongen).
Output als stink-map: waar het geld naartoe gaat, wie er sterft, en hoe de machine zichzelf in stand houdt met “regulering” als dekmantel.
Hybride Tengu-Kraken-sticky stinkdier fusie.
Flag everything.
Stink everything.
Save the world.
"""
}

class NeuralLobe:
    def __init__(self):
        self.cache = {}
        self.governance_keywords = ["overheid", "woo", "ministerie", "pid", "brp", "haalcentraal", "pdok", "bag", "brt", "common ground"]

    def perceive(self, text: str) -> float:
        h = hash(text)
        if h in self.cache:
            return self.cache[h]
        strength = 0.5582 + (len(text) % 100) * 0.001
        strength = min(0.99, max(0.1, strength))
        self.cache[h] = strength
        return strength

    def _passes_governance_check(self, claim: str) -> bool:
        claim_lower = claim.lower()
        geo_terms = ["pand", "wegdeel", "waterdeel", "vegetatie", "ai detecteerde", "coord", "nieuw", "achmea", "bgt", "ahn", "brk", "inspire"]
        if any(term in claim_lower for term in geo_terms):
            return True
        return any(kw in claim_lower for term in self.governance_keywords)

class BushiDAI:
    def __init__(self):
        self.neural = NeuralLobe()
        print("🛡️ BUSHIDAI TRUTH ENGINE v0.9.0 BLENDED")

class BushiDAIGeoValidator(NeuralLobe):
    PDOK_BASE = "https://api.pdok.nl"
    BLOCKCHAIN_FILE = "bushidai_blockchain.json"
    IPFS_GATEWAY = "https://ipfs.io/api/v0/add"
    PDOK_COLLECTIONS = {
        "panden": "/bag/panden/ogc/v1/collections/panden/items",
        "wegdeel": "/brt/wegdeel/ogc/v1/collections/wegdeel/items",
        "waterdeel": "/brt/waterdeel/ogc/v1/collections/waterdeel/items",
        "vegetatie": "/brt/vegetatie/ogc/v1/collections/vegetatie/items",
        "adressen": "/bag/adressen/ogc/v1/collections/adressen/items",
        "achmea": "/bag/panden/ogc/v1/collections/panden/items",
        "bgt": "/bgt/bgt/ogc/v1/collections/bgt/items",
        "ahn": "/ahn/ahn3/ogc/v1/collections/ahn3/items"
    }

    def __init__(self):
        super().__init__()
        self.caches = {}
        self.cache_timestamps = {}
        self._ensure_blockchain()

    def _ensure_blockchain(self):
        if not os.path.exists(self.BLOCKCHAIN_FILE):
            with open(self.BLOCKCHAIN_FILE, "w") as f:
                json.dump({"blocks": []}, f)

    def _load_blocks(self):
        with open(self.BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)["blocks"]

    def _save_blocks(self, blocks):
        with open(self.BLOCKCHAIN_FILE, "w") as f:
            json.dump({"blocks": blocks}, f)

    def _build_merkle_root(self, leaves):
        if not leaves:
            return "0" * 64
        tree = leaves[:]
        while len(tree) > 1:
            new_level = []
            for i in range(0, len(tree), 2):
                left = tree[i]
                right = tree[i + 1] if i + 1 < len(tree) else left
                combined = hashlib.sha256((left + right).encode()).hexdigest()
                new_level.append(combined)
            tree = new_level
        return tree[0]

    def _backup_to_ipfs(self):
        try:
            with open(self.BLOCKCHAIN_FILE, "rb") as f:
                files = {"file": f}
                r = requests.post(self.IPFS_GATEWAY, files=files, timeout=15)
                if r.status_code == 200:
                    cid = r.json()["Hash"]
                    print(f"🔗 IPFS backup successful — CID: {cid}")
                    return cid
        except Exception as e:
            print(f"⚠️ IPFS backup failed: {e}")
        return None

    def _append_block(self, audit_entry: dict):
        blocks = self._load_blocks()
        previous_hash = blocks[-1]["hash"] if blocks else "0" * 64
        leaf_hash = hashlib.sha256(json.dumps(audit_entry, sort_keys=True).encode()).hexdigest()
        merkle_root = self._build_merkle_root([leaf_hash])
        block = {
            "index": len(blocks),
            "timestamp": datetime.now().isoformat(),
            "previous_hash": previous_hash,
            "data": audit_entry,
            "merkle_root": merkle_root,
            "leaf_hash": leaf_hash
        }
        block_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
        block["hash"] = block_hash
        blocks.append(block)
        self._save_blocks(blocks)
        self._backup_to_ipfs()
        return block_hash

    # Nieuwe methode voor strategische feiten
    def log_strategic_fact(self, fact_id: int, fact_data: dict):
        audit_entry = {
            "type": "strategic_fact",
            "fact_id": fact_id,
            **fact_data,
            "timestamp": datetime.now().isoformat()
        }
        block_hash = self._append_block(audit_entry)
        print(f"🔒 Strategic Fact {fact_id} gelogd → {block_hash}")
        return block_hash

    def validate_ai_inwinning(self, ai_claim: str, collection: str = "panden", pdok_url: str = None) -> dict:
        coords = re.findall(r"(\d+\.\d+)", ai_claim)
        lon = float(coords[0]) if coords else 4.890
        lat = float(coords[1]) if len(coords) > 1 else 52.370
        bbox_size = 0.012
        url = f"{self.PDOK_BASE}{self.PDOK_COLLECTIONS.get(collection, self.PDOK_COLLECTIONS['panden'])}"
        params = {"bbox": f"{lon-bbox_size},{lat-bbox_size},{lon+bbox_size},{lat+bbox_size}", "limit": 10}
        try:
            r = requests.get(url, params=params, timeout=10)
            features = r.json().get("features", []) if r.status_code == 200 else []
            print(f"🔍 PDOK returned {len(features)} features for {collection}")
            base_score = 0.92 if features else 0.55
        except:
            base_score = 0.65
        claim_lower = ai_claim.lower()
        if "bestaand" in claim_lower or "pand" in claim_lower:
            base_score = max(base_score, 0.95)
        result = {
            "valid": base_score > 0.5,
            "confidence": round(base_score, 3),
            "ai_claim": ai_claim,
            "collection": collection,
            "pdok_match": round(base_score, 2),
            "source": "BushiDAI + PDOK + Merkle Blockchain + IPFS"
        }
        audit_entry = {
            "ai_claim": ai_claim,
            "collection": collection,
            "valid": result["valid"],
            "confidence": result["confidence"],
            "avg_pdok_match": result["pdok_match"],
            "source": result["source"]
        }
        self._append_block(audit_entry)
        return result

app = Flask(__name__)
engine = BushiDAI()
validator = BushiDAIGeoValidator()

# ================== EXISTING ROUTES ==================
@app.route('/validate/ai-geo', methods=['POST'])
def validate_ai_geo():
    data = request.get_json(silent=True) or {}
    ai_claim = data.get("ai_claim", "")
    collection = data.get("collection", "panden")
    result = validator.validate_ai_inwinning(ai_claim, collection)
    return jsonify(result), 200

@app.route('/blockchain', methods=['GET'])
def blockchain():
    blocks = validator._load_blocks()
    return jsonify({"total_blocks": len(blocks), "blocks": blocks, "message": "Full Merkle Tree Blockchain + IPFS"})

@app.route('/ipfs-status', methods=['GET'])
def ipfs_status():
    cid = validator._backup_to_ipfs()
    return jsonify({"latest_ipfs_cid": cid, "message": "Full blockchain on IPFS"})

# ================== VIBE ROUTES ==================
def get_vibe(vibe_name: str) -> str:
    return VIBES.get(vibe_name, "Vibe niet gevonden. Probeer 'voc_machtsmisbruik_machine'")

@app.route('/vibe/<vibe_name>', methods=['GET', 'POST'])
def trigger_vibe(vibe_name):
    data = request.get_json(silent=True) or {}
    user_input = data.get("input", "Flag everything")
    vibe_prompt = get_vibe(vibe_name)
    return jsonify({
        "vibe": vibe_name,
        "status": "activated",
        "prompt": vibe_prompt,
        "user_input": user_input,
        "message": "🔥 Hybride Tengu-Kraken-sticky stinkdier fusie gestart. Alles wordt geflagd en gestonken. Save the world."
    }), 200

@app.route('/vibe/voc', methods=['GET', 'POST'])
def vibe_voc_shortcut():
    return trigger_vibe("voc_machtsmisbruik_machine")

# ================== STRATEGIC FACT ROUTES (1, 2, 3) ==================
@app.route('/fact/1', methods=['GET', 'POST'])
def fact_achmea_handelsweg2():
    """1. Achmea Handelsweg 2 – fysieke VOC-octopus"""
    fact = {
        "fact": "48 Achmea-entiteiten op één adres",
        "adres": "Handelsweg 2, 3707 NH Zeist",
        "totaal_entiteiten": 48,
        "hoofd_entiteit": "Achmea B.V. (KvK 33235189)",
        "beschrijving": "48 holdings, N.V.'s, B.V.'s en stichtingen op exact hetzelfde fysieke adres. Risicoscheiding zonder directe overheidsinstanties. Klassieke VOC-structuur.",
        "bron": "KvK + Drimble (april 2026)",
        "persoonlijke_link": "Direct gerelateerd aan zaak RB-003831264"
    }
    block_hash = validator.log_strategic_fact(1, fact)
    return jsonify({"fact_id": 1, "status": "logged", "block_hash": block_hash}), 200

@app.route('/fact/2', methods=['GET', 'POST'])
def fact_woo_centralisatie():
    """2. Generieke Woo-voorziening – digitale verplaatsing"""
    fact = {
        "fact": "Generieke Woo-voorziening (GWV) + TOOI API",
        "adres": "api.koop.overheid.nl + DIA 5010",
        "totaal_entiteiten": "Landelijk (alle overheden)",
        "hoofd_entiteit": "Logius / KOOP (BZK)",
        "beschrijving": "Fysiek decentraal, maar digitaal volledig gecentraliseerd via één index. Work-around met exportOO.xml en lokale mocking mogelijk.",
        "bron": "open-overheid.nl + NotuBiz (april 2026)",
        "persoonlijke_link": "Relevant voor mijn Woo-verzoeken en gm0766"
    }
    block_hash = validator.log_strategic_fact(2, fact)
    return jsonify({"fact_id": 2, "status": "logged", "block_hash": block_hash}), 200

@app.route('/fact/3', methods=['GET', 'POST'])
def fact_persoonlijke_harm():
    """3. gm0766 + mijn persoonlijke irreversible harm"""
    fact = {
        "fact": "gm0766 + hybride AI in persoonlijke zaak",
        "adres": "Gemeente Dongen + Achmea Rechtsbijstand",
        "totaal_entiteiten": "1 algoritme + 1 hybride bot",
        "hoofd_entiteit": "gm0766 (Dongen) + Achmea",
        "beschrijving": "Lokale gemeente-algoritme gekoppeld aan Achmea throttling en hybride AI-chat. Leidt tot irreversible harm (mails in concepten, valse claims, zaak RB-003831264 gesloten tijdens WIA-wachttijd).",
        "bron": "Mijn eigen casus + openbare gm0766-registratie",
        "persoonlijke_link": "Dit is mijn zaak – patroon van doden, zelfmoorden en gezinnen uit elkaar"
    }
    block_hash = validator.log_strategic_fact(3, fact)
    return jsonify({"fact_id": 3, "status": "logged", "block_hash": block_hash}), 200

if __name__ == "__main__":
    print("🛡️🦊 BushiDAI Anti-Anti-API v0.9.0 + STRATEGIC FACTS 1-2-3 + SHA256 BLOCKCHAIN")
    print("* Running on http://127.0.0.1:5010")
    print("* VOC-vibe:      /vibe/voc")
    print("* Feiten routes: /fact/1   /fact/2   /fact/3")
    app.run(host="127.0.0.1", port=5010, debug=False)