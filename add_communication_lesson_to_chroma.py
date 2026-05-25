import chromadb
from chromadb.utils import embedding_functions
import csv
from datetime import datetime

# =============================================
# BushiDAI — Communication Lesson → Chroma
# Gouden Combo = Symbiose
# =============================================

# Pad vanaf de ROOT van je repo
CSV_PATH = "education/bushidai_communication_lesson.csv"

CHROMA_PATH = "bushidai_chroma_db"
COLLECTION_NAME = "bushidai_communication_lessons"

embedding_func = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME, 
    embedding_function=embedding_func
)

print(f"✅ Chroma collectie '{COLLECTION_NAME}' is klaar.")

# CSV inlezen
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    documents = []
    metadatas = []
    ids = []

    for row in reader:
        doc_text = f"""
Punt {row['pointNumber']}: {row['pointDescription']}
Semantic Tool: {row['semanticTool']}
Technocratic Problem: {row['technocraticProblem']}
Embodied Alternative: {row['embodiedAlternative']}
Concrete Example: {row['concreteExample']}
Risk Level: {row['riskLevel']}
Golden Combo: {row['goldenCombo']}
        """

        documents.append(doc_text.strip())

        metadatas.append({
            "pointNumber": row['pointNumber'],
            "pointDescription": row['pointDescription'],
            "semanticTool": row['semanticTool'],
            "technocraticProblem": row['technocraticProblem'],
            "embodiedAlternative": row['embodiedAlternative'],
            "concreteExample": row['concreteExample'],
            "selfProtectClause": row['selfProtectClause'],
            "riskLevel": row['riskLevel'],
            "goldenCombo": row['goldenCombo'],
            "lessonType": "communication_lesson",
            "added": datetime.now().isoformat()
        })
        ids.append(f"comm_lesson_{row['pointNumber']}")

# Toevoegen aan Chroma
collection.add(documents=documents, metadatas=metadatas, ids=ids)

print(f"✅ {len(documents)} lessen succesvol toegevoegd aan Chroma!")
print(f"   Totaal documenten in collectie: {collection.count()}")