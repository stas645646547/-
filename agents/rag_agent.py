import os
from utils.file_parsing import extract_texts_from_data

class RAGAgent:
    def __init__(self, data_folder=None):
        self.data_folder = data_folder or "data"

    async def search(self, legal_query, lang):
        # Загружаем все тексты из папки data
        texts = extract_texts_from_data(self.data_folder)
        # Простой фильтр по ключевым словам
        relevant = [t for t in texts if legal_query.lower() in t.lower()]
        if not relevant:
            return ""
        # Можно добавить [источник], если хочешь ссылаться на файл/статью
        return "\n\n".join(relevant[:5])
