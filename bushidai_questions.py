# bushidai_questions.py
# BUSHIDAI QUESTIONS ENGINE v1.5 - HOGERE-LEVEL COMPLAINT MATCHING
# TRUTH == TRUTH

from rdflib import Graph
from pathlib import Path
import yaml
import json
from typing import List, Dict, Any

class BushiDAISPARQL:
    """
    BushiDAI Questions Engine
    - Laadt semantic.ttl voor SPARQL queries
    - Hoge-level zoekmethodes op basis van complaint_packages uit config.yaml
    100% lokaal, geen cloud.
    """

    def __init__(self, ttl_file: str = "bushidai_semantic.ttl"):
        self.graph = Graph()
        self.config = self._load_config()
        self.complaint_packages = self.config.get("bushiDAI", {}).get("complaint_packages", [])

        # Laad semantic.ttl
        ttl_path = Path(ttl_file)
        if ttl_path.exists():
            try:
                self.graph.parse(ttl_path, format="turtle")
                print(f"✅ BushiDAI Questions Engine geladen — {len(self.graph)} triples")
            except Exception as e:
                print(f"❌ Fout bij laden van TTL: {e}")
        else:
            print(f"⚠️  {ttl_file} niet gevonden")

    def _load_config(self):
        """Laad bushidai_config.yaml"""
        config_path = Path(__file__).parent / "bushidai_config.yaml"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ Config laden mislukt: {e}")
            return {}

    # ====================== HOGERE-LEVEL SEARCH ======================

    def search_complaints(self, symptoms: str) -> List[Dict]:
        """
        Zoekt matching complaint packages op basis van ingevoerde klachten.
        Dit is de hoofd-methode die bushidai_core.py gebruikt.
        """
        if not symptoms or not self.complaint_packages:
            return []

        symptoms_lower = symptoms.lower()
        matches = []

        for package in self.complaint_packages:
            package_symptoms = package.get("symptoms", "").lower()
            # Match als een van de woorden in de symptoms voorkomt
            if any(word.strip() in symptoms_lower for word in package_symptoms.split(",")):
                matches.append(package)

        return matches

    def get_risk_groups(self, symptoms: str) -> List[Dict]:
        """Geeft alleen risico-groepen + aanbevolen onderzoeken terug"""
        matches = self.search_complaints(symptoms)
        return [
            {
                "risico_groep": p.get("risico_groep"),
                "aanbevolen_onderzoek": p.get("aanbevolen_onderzoek"),
                "urgentie": p.get("urgentie", "Medium")
            }
            for p in matches
        ]

    # ====================== SPARQL BACKWARD COMPATIBILITY ======================

    def query(self, sparql_query: str) -> List[Dict[str, Any]]:
        """Oude SPARQL methode (blijft werken)"""
        try:
            results = self.graph.query(sparql_query)
            return [dict(row) for row in results]
        except Exception as e:
            print(f"❌ SPARQL error: {e}")
            return [{"error": str(e)}]


# Globale instance (makkelijk te importeren)
bushidai_questions = BushiDAISPARQL()

# Voor direct testen
if __name__ == "__main__":
    print("\n=== BushiDAI Questions Test ===")
    test = bushidai_questions.search_complaints("lymfeklierzwelling, tintelingen gezicht, geen koorts")
    print(json.dumps(test, indent=2, ensure_ascii=False))