from rdflib import Graph
import pandas as pd

g = Graph()
g.parse("education/bushidai_communication_lesson.ttl", format="turtle")

print("✅ Graph geladen —", len(g), "triples\n")

sparql_query = """
PREFIX bushidai: <https://bushidai.org/ontology#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>

SELECT 
  ?pointNumber
  ?pointDescription
  ?knowledgeBase
  ?problemDefinition
  ?counterSolution
  ?riskLevel
WHERE {
  ?point a bushidai:LessonPoint ;
         bushidai:pointNumber ?pointNumber ;
         bushidai:description ?pointDescription ;
         bushidai:knowledgeBase ?knowledgeBase ;
         bushidai:problemDefinition ?problemDefinition ;
         bushidai:counterSolution ?counterSolution ;
         bushidai:riskLevel ?riskLevel .
}
ORDER BY ?pointNumber
"""

results = g.query(sparql_query)

rows = []
for row in results:
    rows.append({
        "pointNumber": str(row.pointNumber),
        "pointDescription": str(row.pointDescription),
        "knowledgeBase": str(row.knowledgeBase)[:120] + "..." if len(str(row.knowledgeBase)) > 120 else str(row.knowledgeBase),
        "problemDefinition": str(row.problemDefinition)[:120] + "..." if len(str(row.problemDefinition)) > 120 else str(row.problemDefinition),
        "counterSolution": str(row.counterSolution)[:120] + "..." if len(str(row.counterSolution)) > 120 else str(row.counterSolution),
        "riskLevel": str(row.riskLevel)
    })

df = pd.DataFrame(rows)

# Mooie, leesbare weergave
pd.set_option('display.max_colwidth', 120)
pd.set_option('display.width', 200)
print(df.to_string(index=False))

print("\n✅ SPARQL succesvol uitgevoerd met de nieuwe 3-blok structuur!")
print("   knowledgeBase = echte kennis")
print("   problemDefinition = hoe het misbruikt wordt")
print("   counterSolution = embodied BushiDAI-tegenwicht")