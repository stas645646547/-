import os
from PyPDF2 import PdfReader

def extract_texts_from_data(data_folder):
    all_texts = []
    for root, dirs, files in os.walk(data_folder):
        for f in files:
            path = os.path.join(root, f)
            if f.endswith('.txt') or f.endswith('.md'):
                with open(path, encoding="utf-8") as file:
                    all_texts.append(file.read())
            elif f.endswith('.pdf'):
                try:
                    reader = PdfReader(path)
                    pdf_text = []
                    for page in reader.pages:
                        pdf_text.append(page.extract_text())
                    all_texts.append("\n".join(pdf_text))
                except Exception as e:
                    print(f"Ошибка чтения PDF: {path}: {e}")
    return all_texts
