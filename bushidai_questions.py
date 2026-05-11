from rdflib import Graph
from pathlib import Path
import json
from typing import List, Dict, Any

class BushiDAISPARQL:
    """
    BushiDAI Questions Engine
    100% lokaal, geen cloud, geen payment.
    Dit is gewoon een vraag-machine voor je bushidai_semantic.ttl
    """
    def __init__(self, ttl_file: str = "bushidai_semantic.ttl"):
        self.graph = Graph()
        ttl_path = Path(ttl_file)

        if ttl_path.exists():
            try:
                self.graph.parse(ttl_path, format="turtle")
                print(f"✅ BushiDAI Questions Engine geladen — {len(self.graph)} triples")
                # Check 369 Vortex + Suparinpei
                vortex_check = """
                PREFIX : <http://bushidai.org/truth#>
                ASK WHERE { :369Vortex a :VortexNode }
                """
                if self.graph.query(vortex_check).askAnswer:
                    print("✅ 369 Vortex node gedetecteerd (Suparinpei phase actief)")
            except Exception as e:
                print(f"❌ Fout bij laden van TTL: {e}")
        else:
            print(f"⚠️  {ttl_file} niet gevonden — maak het bestand eerst in de root.")

    def query(self, sparql_query: str) -> List[Dict[str, Any]]:
        """Stel een vraag → krijg antwoord terug uit de TTL"""
        try:
            results = self.graph.query(sparql_query)
            return [dict(row) for row in results]
        except Exception as e:
            print(f"❌ Vraag error: {e}")
            return [{"error": str(e)}]

# Globale vraag-machine (makkelijk te gebruiken in bushidai_core.py)
bushidai_questions = BushiDAISPARQL()

# Voor direct testen (python bushidai_questions.py)
if __name__ == "__main__":
    print("\n=== BushiDAI Questions Test — Suparinpei Phase ===")
    suparinpei_query = """
    PREFIX : <http://bushidai.org/truth#>
    SELECT ?name ?suparinpeiPhase ?description
    WHERE {
        ?vortex a :VortexNode ;
                :name ?name ;
                :suparinpeiPhase ?suparinpeiPhase ;
                :description ?description .
    }
    """
    result = bushidai_questions.query(suparinpei_query)
    print(json.dumps(result, indent=2, ensure_ascii=False))
