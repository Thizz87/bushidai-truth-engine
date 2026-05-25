from rdflib import Graph

def validate_ttl(file_path="education/bushidai_communication_lesson.ttl"):
    g = Graph()
    try:
        g.parse(file_path, format="turtle")
        print(f"✅ Turtle syntax is VALID!")
        print(f"   {len(g)} triples succesvol geladen.")
        print(f"   BushiDAI-graph is klaar voor gebruik.")
        return True
    except Exception as e:
        print(f"❌ Turtle syntax ERROR:")
        print(str(e))
        return False

if __name__ == "__main__":
    validate_ttl()