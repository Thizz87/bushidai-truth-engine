import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "bushidai_chroma_db"
COLLECTION_NAME = "bushidai_communication_lessons"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name=COLLECTION_NAME)

print(f"✅ Connected to Chroma | Totaal documenten: {collection.count()}\n")

queries = [
    "intermenselijke communicatie",
    "Nafudakake",
    "Symbiose",
    "Toeslagenaffaire",
    "digitale afstand",
    "embodied truth"
]

for q in queries:
    print(f"🔍 Zoeken naar: \"{q}\"")
    results = collection.query(
        query_texts=[q],
        n_results=3
    )
    
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        score = 1 - results['distances'][0][i]
        print(f"   {i+1}. Score: {score:.3f} | Punt {meta['pointNumber']} - {meta['pointDescription']}")
        print(f"       Example: {meta['concreteExample'][:100]}...")
        print(f"       GoldenCombo: {meta['goldenCombo']}\n")
    print("-" * 70)