# ingest_documents.py
# Automatisch ALLE documenten uit de folder ./documents in Chroma laden
# Dit is de echte lokale RAG oplossing

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
import os

print("🚀 BushiDAI Document Ingester started")

chroma_client = chromadb.PersistentClient(path="./bushidai_chroma_db")

embedding_func = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="nomic-embed-text"
)

collection = chroma_client.get_or_create_collection(
    name="bushidai_truth",
    embedding_function=embedding_func
)

def ingest_folder(folder_path: str = "./documents"):
    path = Path(folder_path)
    if not path.exists():
        os.makedirs(path)
        print(f"📁 Map '{folder_path}' aangemaakt. Drop hier je PDFs, txt, md bestanden in.")
        return

    files = list(path.glob("**/*.*"))
    print(f"🔍 {len(files)} bestanden gevonden in {folder_path}")

    for i, file_path in enumerate(files):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            doc_id = f"doc_{file_path.stem}_{i}"
            
            collection.add(
                documents=[text],
                metadatas=[{"filename": file_path.name, "path": str(file_path)}],
                ids=[doc_id]
            )
            print(f"✅ Toegevoegd: {file_path.name}")
        except Exception as e:
            print(f"❌ Fout bij {file_path.name}: {e}")

    print(f"\n🎯 Klaar! {len(files)} documenten ingeladen in Chroma.")

if __name__ == "__main__":
    ingest_folder()
