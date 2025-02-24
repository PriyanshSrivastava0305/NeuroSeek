import streamlit as st
from rag import generate_answer

st.title("📰 AI-Powered News Search")

query = st.text_input("Enter your search query:")
if st.button("Search"):
    if query:
        with st.spinner("Fetching results..."):
            try:
                response = generate_answer(query)
                st.write("### Answer:")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a search query.")
