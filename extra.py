# app.py
import streamlit as st
import time
import json
from scraper import scrape_url
from indexer import index_documents, load_index
from rag import load_local_llm
from transformers import AutoTokenizer


def truncate_text(text, tokenizer, max_tokens=300):
    """Improved truncation with model-appropriate handling"""
    inputs = tokenizer(
        text,
        truncation=True,
        max_length=max_tokens,
        return_overflowing_tokens=False,
        return_tensors="pt"
    )
    return tokenizer.decode(inputs['input_ids'][0], skip_special_tokens=True)

def generate_answer(query, vectorstore, llm, tokenizer):
    """Enhanced version for structured answers"""
    try:
        # Retrieve more documents with higher quality threshold
        docs = vectorstore.similarity_search(query, k=5, score_threshold=0.75)
        if not docs:
            return "I couldn't find relevant information in the indexed documents."
            
        context = "\n".join([doc.page_content for doc in docs])
        truncated_context = truncate_text(context, tokenizer, max_tokens=500)  # Increased context
        
        # Structured instruction prompt
        prompt = f"""You are an AI research analyst. Analyze this context and compose a structured response:

        Context: {truncated_context}

        Question: {query}

        Format your answer with:
        1. Clear introductory statement
        2. Numbered list of key focus areas
        3. Brief description of each area
        4. Final summary sentence

        If information is incomplete, state what is available:"""
        
        # Generate with controlled parameters
        full_answer = llm(prompt, max_new_tokens=200, temperature=0.3)  # Increased length
        
        # Clean up the output
        answer = full_answer.split("Answer:")[-1].strip()
        
        # Ensure complete sentences
        if "." in answer:
            last_period = answer.rfind(".")
            answer = answer[:last_period+1]
            
        return answer

    except Exception as e:
        return f"Analysis error: {str(e)}"

def main():
    st.title("NeuroSeek - AI-Powered Knowledge Retrieval")
    
    # Initialize state management
    if "indexed" not in st.session_state:
        st.session_state.update({
            "indexed": False,
            "vectorstore": None,
            "llm": None,
            "tokenizer": None
        })

    # Model loading section
    st.markdown("### Step 1: Load AI Model")
    model_name = st.selectbox(
        "Select Model",
        ["gpt2", "google/gemma-7b", "EleutherAI/gpt-j-6B"],
        index=0
    )
    
    if st.button("Initialize Model"):
        with st.spinner("Loading AI model..."):
            try:
                # Get both llm and tokenizer from the loader
                llm, tokenizer = load_local_llm(model_name=model_name)
                st.session_state.llm = llm
                st.session_state.tokenizer = tokenizer
                st.success(f"Loaded {model_name} successfully!")
            except Exception as e:
                st.error(f"Model loading failed: {str(e)}")

    # Indexing section
    st.markdown("### Step 2: Index Content")
    url = st.text_input("Enter website URL")
    if st.button("Scrape & Index") and url:
        with st.spinner("Processing website..."):
            try:
                documents = scrape_url(url)
                if documents:
                    vectorstore = index_documents(documents)
                    st.session_state.vectorstore = vectorstore
                    st.session_state.indexed = True
                    st.success("Indexed successfully!")
                else:
                    st.error("No content found")
            except Exception as e:
                st.error(f"Indexing failed: {str(e)}")

    # Query section
    if st.session_state.indexed and st.session_state.llm:
        st.markdown("### Step 3: Ask Questions")
        query = st.text_input("Enter your question")
        
        if query:
            with st.spinner("Analyzing..."):
                answer = generate_answer(
                    query,
                    st.session_state.vectorstore,
                    st.session_state.llm,
                    st.session_state.tokenizer
                )
                st.markdown("**Answer:**")
                st.write(answer)

if __name__ == "__main__":
    main()