import openai
import faiss
import json
import numpy as np
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class SemanticSearcher:
    def __init__(self, index_path, meta_path):
        self.index = faiss.read_index(index_path)
        with open(meta_path, encoding="utf-8") as f:
            self.meta = json.load(f)

    def search(self, query, k=3):
        embed = openai.Embedding.create(
            model="text-embedding-3-small",
            input=query[:3000]
        )["data"][0]["embedding"]

        vec = np.array([embed], dtype="float32")
        distances, indices = self.index.search(vec, k)
        return [self.meta[i]["filename"] for i in indices[0]]
