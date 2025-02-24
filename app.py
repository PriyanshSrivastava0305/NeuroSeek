import streamlit as st
from rag import generate_answer

st.title("📰 AI-Powered News Search")

query = st.text_input("Enter your search query:")
if st.button("Search"):
    if query:
        with st.spinner("Fetching results..."):
            response = generate_answer(query)
        st.write("### Answer:")
        st.write(response)
    else:
        st.warning("Please enter a search query.")
