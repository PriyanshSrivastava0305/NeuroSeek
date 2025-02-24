# app.py
import streamlit as st
import time
import json
from scraper import scrape_website
from indexer import indexing_main
from rag import load_embedding_model, load_faiss_index, load_local_llm, search_index, generate_response_local

def main():
    st.title("NeuroSeek - AI-Powered Knowledge Retrieval")
    
    # Use session state to manage workflow
    if "indexed" not in st.session_state:
        st.session_state.indexed = False

    # Step 1: Scrape and index if not already done
    st.markdown("### Step 1: Enter a website URL to scrape and index its content")
    if not st.session_state.indexed:
        url = st.text_input("Website URL", key="url_input")
        if st.button("Scrape & Index"):
            if url:
                with st.spinner("Scraping website..."):
                    scraped_data = scrape_website(url)
                    if scraped_data is None:
                        st.error("Scraping failed. Please try a different URL.")
                        return
                    # Save scraped data
                    with open("scraped_data.json", "w", encoding="utf-8") as f:
                        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
                    st.success("Scraping completed and data saved to scraped_data.json.")
                with st.spinner("Indexing data..."):
                    indexing_main()  # This creates faiss_index.bin and texts.json
                    st.success("Indexing completed: FAISS index and texts saved.")
                    st.session_state.indexed = True
            else:
                st.error("Please enter a valid URL.")

    # Step 2: Query mode – show query box only when indexing is complete
    if st.session_state.indexed:
        st.markdown("### Step 2: Enter your query")
        try:
            embed_model = load_embedding_model()
            index, texts = load_faiss_index()
            llm_generator = load_local_llm()
        except Exception as e:
            st.error(f"Error loading models or index: {e}")
            return

        query = st.text_input("Your Query", key="query_input")
        if query:
            with st.spinner("Retrieving relevant documents..."):
                retrieved_texts = search_index(query, embed_model, index, texts, k=3)
                context = "\n".join(retrieved_texts)
                st.markdown("#### Retrieved Context")
                st.write(context)
            with st.spinner("Generating AI response..."):
                response = generate_response_local(query, context, llm_generator)
                st.markdown("#### AI Response")
                st.write(response)

if __name__ == "__main__":
    main()
