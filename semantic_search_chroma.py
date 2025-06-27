from chromadb.config import Settings
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

class ChromaSemanticSearch:
    def __init__(self, persist_directory="chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="law_articles")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def add_documents(self, texts, metadatas):
        embeddings = self.embedder.encode(texts).tolist()
        ids = [meta["id"] for meta in metadatas]
        self.collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)

    def search(self, query, k=1):
        query_embedding = self.embedder.encode([query]).tolist()
        results = self.collection.query(query_embeddings=query_embedding, n_results=k)
        return results["metadatas"][0] if results["metadatas"] else []