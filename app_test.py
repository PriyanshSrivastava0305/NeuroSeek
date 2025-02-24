import streamlit as st
import faiss
import json
from transformers import pipeline

# Load FAISS index
INDEX_FILE = "faiss_index.bin"
DATA_FILE = "texts.json"

# Load stored text data
with open(DATA_FILE, "r", encoding="utf-8") as f:
    texts = json.load(f)

# Load FAISS index
index = faiss.read_index(INDEX_FILE)

# Load LLM (You can replace with another model)
llm = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1")

def retrieve_text(query, top_k=5):
    """Search FAISS index and return relevant text chunks."""
    query_vector = index.reconstruct(0)  # Replace with actual query embedding
    distances, indices = index.search(query_vector.reshape(1, -1), top_k)
    
    results = [texts[i] for i in indices[0] if i < len(texts)]
    return results

def generate_response(query):
    """Retrieve relevant text and generate an LLM response."""
    context = retrieve_text(query)
    context_str = " ".join(context)
    
    response = llm(f"Answer this based on context: {context_str} \n Question: {query}")
    return response[0]["generated_text"]

# Streamlit UI
st.title("RAG-based QA System")
st.write("Enter your query below:")

user_query = st.text_input("Ask a question:")
if st.button("Submit"):
    if user_query:
        st.write("Searching for relevant information...")
        response = generate_response(user_query)
        st.write("### Response:")
        st.write(response)
    else:
        st.warning("Please enter a query!")
