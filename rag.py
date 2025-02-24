# rag.py
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline

def load_embedding_model():
    """Load and return the SentenceTransformer model."""
    return SentenceTransformer("all-MiniLM-L6-v2")

def load_faiss_index():
    """Load and return the FAISS index and texts list."""
    if not os.path.exists("faiss_index.bin"):
        raise FileNotFoundError("FAISS index file 'faiss_index.bin' not found. Run the indexing process first.")
    if not os.path.exists("texts.json"):
        raise FileNotFoundError("Texts file 'texts.json' not found. Run the indexing process first.")
    index = faiss.read_index("faiss_index.bin")
    with open("texts.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
    return index, texts

def load_local_llm():
    from transformers import pipeline
    return pipeline('text-generation', model='distilgpt2')

def search_index(query, model, index, texts, k=3):
    """Encode the query, search the FAISS index, and return the top-k retrieved texts."""
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype=np.float32)
    distances, indices = index.search(query_embedding, k)
    retrieved_texts = [texts[idx] for idx in indices[0] if idx < len(texts)]
    return retrieved_texts

def generate_response_local(query, context, generator):
    """Generate a contextual response using the retrieved context and a local LLM."""
    system_prompt = (
        "You are a highly knowledgeable and efficient assistant. Your task is to provide "
        "concise, clear, and accurate answers based solely on the provided context. Your response "
        "should be minimal and directly address the user's query without unnecessary details."
    )
    
    prompt = f"""{system_prompt}
Using the following context, answer the query below in a clean manner and return a minimal response.

Context:
{context}

Query: {query}

Answer:"""
    # Get the tokenizer and encode the prompt
    tokenizer = generator.tokenizer
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    
    # Set the number of new tokens to generate
    max_new_tokens = 50
    
    # Generate output using the underlying model directly
    outputs = generator.model.generate(input_ids, max_new_tokens=max_new_tokens)
    
    # Decode the output and remove the prompt part to extract only the generated answer
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = generated_text[len(prompt):].strip()
    return answer

if __name__ == "__main__":
    # For independent testing of the RAG functions:
    index, texts = load_faiss_index()
    model = load_embedding_model()
    query = input("Enter a query for testing: ")
    results = search_index(query, model, index, texts, k=3)
    print("Retrieved texts:")
    for r in results:
        print(r)
