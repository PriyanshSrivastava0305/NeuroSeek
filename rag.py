from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

def load_index():
    """Load FAISS vector store."""
    return FAISS.load_local("faiss_index", HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))

def generate_answer(query):
    """Retrieve relevant articles and generate a response."""
    vectorstore = load_index()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = Ollama(model="mistral")

    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
    response = qa_chain.run(query)
    
    return response

if __name__ == "__main__":
    query = input("Enter your search query: ")
    print(generate_answer(query))
