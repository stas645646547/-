import os
import openai
import faiss
import json
from tqdm import tqdm

openai.api_key = os.getenv("OPENAI_API_KEY")

FOLDER = r"C:\Users\kamst\OneDrive\Рабочий стол\app\data\7 главных законов\חוק הגנת השכר\узлы"
EMBEDDING_MODEL = "text-embedding-3-small"
INDEX_FILE = "wage_law_faiss.index"
META_FILE = "wage_law_meta.json"

def embed_text(text):
    response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=text[:3000]  # ограничим размер
    )
    return response["data"][0]["embedding"]

documents = []
meta = []

for fname in os.listdir(FOLDER):
    if fname.endswith(".md"):
        path = os.path.join(FOLDER, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        documents.append(content)
        meta.append({"filename": fname})

# Эмбеддинги
vectors = []
for doc in tqdm(documents):
    vectors.append(embed_text(doc))

# FAISS index
dimension = len(vectors[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(vectors).astype("float32"))

faiss.write_index(index, INDEX_FILE)
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print(f"Готово! Сохранено: {INDEX_FILE}, {META_FILE}")
