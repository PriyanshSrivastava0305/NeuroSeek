import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def load_scraped_data(json_path="scraped_data.json"):
    """
    Loads scraped data from a JSON file.
    Expected format is either a single record (dict) or a list of records.
    Each record should contain keys like 'title', 'headings', and 'paragraphs'.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading scraped data: {e}")
        return None

def preprocess_data(record):
    """
    Preprocess a single record from the scraped data.
    Combines title, headings, and paragraphs into one text block.
    """
    text = record.get("title", "") + " "
    text += " ".join(record.get("headings", [])) + " "
    text += " ".join(record.get("paragraphs", []))
    return text.strip()

def create_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    """
    Uses SentenceTransformer to convert a list of texts into embeddings.
    Returns the embeddings as a NumPy array (float32).
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)
    embeddings = np.array(embeddings, dtype=np.float32)
    return embeddings, model

def build_faiss_index(embeddings):
    """
    Builds a FAISS index (L2 distance based) for the given embeddings.
    """
    dimension = embeddings.shape[1]  # Dimension of each embedding vector
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def search_index(index, model, query, texts, k=3):
    """
    Converts a query into an embedding and searches the FAISS index.
    Returns the distances and indices of the top k results.
    """
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype=np.float32)
    distances, indices = index.search(query_embedding, k)
    # Display the results with corresponding text and similarity scores
    print(f"\nTop {k} results for query: '{query}'")
    for score, idx in zip(distances[0], indices[0]):
        print(f"Score: {score:.4f} | Text: {texts[idx]}")
    return distances, indices

def main():
    # 1. Load scraped data (from JSON file produced by your scraping agent)
    scraped_data = load_scraped_data("scraped_data.json")
    if scraped_data is None:
        return

    # Handle both a list of records and a single record
    if isinstance(scraped_data, list):
        texts = [preprocess_data(record) for record in scraped_data]
    else:
        texts = [preprocess_data(scraped_data)]

    # 2. Convert texts into embeddings using a SentenceTransformer model
    embeddings, model = create_embeddings(texts)
    print(f"Generated embeddings for {len(texts)} document(s).")

    # 3. Build a FAISS index with the generated embeddings
    index = build_faiss_index(embeddings)
    print(f"FAISS index created with {index.ntotal} vectors.")

    # 4. (Optional) Save the index to disk for later use
    faiss.write_index(index, "faiss_index.bin")
    print("FAISS index saved to 'faiss_index.bin'.")

    # 5. For demonstration, perform a search on the index using a user query
    query = input("Enter your search query: ")
    search_index(index, model, query, texts, k=3)

if __name__ == "__main__":
    main()
