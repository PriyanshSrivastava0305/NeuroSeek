# indexer.py
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

def load_scraped_data(json_path="scraped_data.json"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Scraped data file '{json_path}' not found.")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def preprocess_data(record):
    text = record.get("title", "") + " "
    text += " ".join(record.get("headings", [])) + " "
    text += " ".join(record.get("paragraphs", []))
    return text.strip()

def create_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)
    embeddings = np.array(embeddings, dtype=np.float32)
    return embeddings, model

def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_texts_json(texts, file_path="texts.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=4)
    print(f"Texts successfully saved to {file_path}")

def indexing_main():
    scraped_data = load_scraped_data("scraped_data.json")
    # Support both list or single record formats
    if isinstance(scraped_data, list):
        texts = [preprocess_data(record) for record in scraped_data]
    else:
        texts = [preprocess_data(scraped_data)]
    
    embeddings, _ = create_embeddings(texts)
    index = build_faiss_index(embeddings)
    faiss.write_index(index, "faiss_index.bin")
    print("FAISS index saved to 'faiss_index.bin'")
    save_texts_json(texts, "texts.json")

if __name__ == "__main__":
    indexing_main()
