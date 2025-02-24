import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import json

# Cache the SentenceTransformer model so it doesn't reload every time
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

# Cache the FAISS index and texts for faster access
@st.cache_resource
def load_faiss_index():
    index = faiss.read_index("faiss_index.bin")
    with open("texts.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
    return index, texts

# Cache the local LLM generator
@st.cache_resource
def load_local_llm():
    # Using GPT-2 for demonstration; replace with any local model of your choice
    return pipeline('text-generation', model='gpt2')

def search_index(query, model, index, texts, k=3):
    """
    Convert the query into an embedding, search the FAISS index for the top k results,
    and return the corresponding texts as the retrieved context.
    """
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype=np.float32)
    distances, indices = index.search(query_embedding, k)
    retrieved_texts = [texts[idx] for idx in indices[0] if idx < len(texts)]
    return retrieved_texts

def generate_response_local(query, context, generator):
    """
    Builds a prompt from the retrieved context and query, then uses a local LLM
    (via Hugging Face's pipeline) to generate a response.
    """
    prompt = f"""Using the following context, answer the query below.

Context:
{context}

Query: {query}

Answer:"""
    
    # Generate text with the local model; adjust parameters as needed
    generated = generator(prompt, max_length=250, num_return_sequences=1)
    answer = generated[0]['generated_text'][len(prompt):].strip()
    return answer

def main():
    st.title("RAG Pipeline: Retrieval & Response Agent (Local LLM)")
    
    # Load the embedding model, FAISS index with texts, and local LLM generator
    embed_model = load_embedding_model()
    index, texts = load_faiss_index()
    llm_generator = load_local_llm()
    
    st.markdown("Enter a query to retrieve relevant content and generate a contextual response:")
    query = st.text_input("Your Query:")
    
    if query:
        with st.spinner("Retrieving context..."):
            retrieved_texts = search_index(query, embed_model, index, texts, k=3)
            context = "\n".join(retrieved_texts)
            st.markdown("### Retrieved Context")
            st.write(context)
        
        with st.spinner("Generating response..."):
            response = generate_response_local(query, context, llm_generator)
            st.markdown("### Response")
            st.write(response)

if __name__ == "__main__":
    main()
