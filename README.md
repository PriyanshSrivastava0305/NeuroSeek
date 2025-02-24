# 🚀 NeuroSeek: AI-Powered Knowledge Retrieval & Search

An AI-powered news search tool using **Retrieval-Augmented Generation (RAG)** to fetch relevant news articles based on user queries.  
Built with **LangChain, FAISS Vector Store, Llama3, and Streamlit**, this project allows users to search and refine AI-generated results dynamically.  

---

## 🚀 Features
- **Web Scraping**: Extracts relevant data from Wikipedia and other sources.
- **Vector Search with FAISS**: Efficient similarity search using embeddings.
- **RAG Pipeline**: Generates precise answers by retrieving relevant content.
- **LLM Integration**: Uses **Llama3** for high-quality responses.
- **Human-in-the-Loop UI**: Users can refine and regenerate responses dynamically.
- **Streaming Support**: Real-time response generation in Streamlit.

---

## 📜 Sample Data
The dataset is collected from **Wikipedia**, using the following page:  
🔗 [Large Language Model - Wikipedia](https://en.wikipedia.org/wiki/Large_language_model)

### **Example Queries**:
1. *What is a large language model?*
2. *How do LLMs work?*
3. *What is the difference between RNN and Transformer models?*
4. *What are the limitations of large language models?*

---

## 🛠️ Technologies Used
- **Python 3.12**
- **Streamlit** (UI)
- **LangChain** (RAG Pipeline)
- **FAISS** (Vector Search)
- **Llama3** (LLM for response generation)
- **BeautifulSoup** (Web Scraping)
- **GroqCloud API** (LLM backend)
- **OpenAI Whisper** (Speech-to-Text Support - Future)

---

## 🔧 Installation & Setup

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/yourusername/ai-news-search.git
cd ai-news-search
```

### **2️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Application**  
```bash
streamlit run app.py
```

---

## 🛠️ Future Work
🚀 The project is evolving! Here’s what’s coming next:  
✅ **Multiple URL Support** – Allow users to scrape multiple sources dynamically.  
✅ **Multiple Model Support** – Let users switch between **Llama3, Mixtral, and Gemma2**.  
✅ **Caching Layer** – Use Redis or local caching to **speed up repeated queries**.  
✅ **Fine-Tuning** – Enhance model response accuracy with domain-specific data.  
✅ **User Feedback System** – Implement a **rating** or **correction mechanism** for AI responses.  



## 📌 License
This project is licensed under the MIT License.
=======
## 🔗 **Live Demo**  
[Streamlit App](https://neuroseek354.streamlit.app/)  

