# add_to_chroma.py
# Vul Chroma met documenten voor BushiDAI
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

chroma_client = chromadb.PersistentClient(path="./bushidai_chroma_db")

embedding_func = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="nomic-embed-text"
)

collection = chroma_client.get_or_create_collection(
    name="bushidai_truth",
    embedding_function=embedding_func
)

def add_document(text: str, metadata: dict = None, id: str = None):
    if metadata is None:
        metadata = {}
    if id is None:
        id = f"doc_{len(collection.get()['ids'])}"
    
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[id]
    )
    print(f"✅ Toegevoegd: {id}")

# =============================================
# VOEG HIER JE DOCUMENTEN TOE
# =============================================

if __name__ == "__main__":
    # Voorbeeld 1: Hulscher autopsy paper
    add_document(
        text="A Systematic Review of Autopsy Findings in Deaths after COVID-19 Vaccination. Hulscher et al. 2024. Conclusie: In 73.9% van de gevallen was vaccinatie waarschijnlijk de oorzaak of grote bijdrager aan de dood. Veel gevallen toonden trombose en myocarditis.",
        metadata={"title": "Hulscher et al. Autopsy Review 2024", "year": 2024, "topic": "amyloid fibrin clots"},
        id="hulscher_2024"
    )

    # Voeg hier meer documenten toe (je kunt tekst uit PDFs kopiëren of hele papers plakken)
    print("Documenten toegevoegd aan Chroma.")
