
# 📚 Semantic RAG Chatbot with Multi-Turn & Cohere

This project is a **native language QA chatbot** that performs **retrieval-augmented generation (RAG)** on local documents.  
It uses **LlamaIndex** + **Cohere** to:
- Build a vector index from PDFs, DOCX, and TXT files (with OCR for scanned PDFs)
- Query all indexed documents every time — guaranteeing fresh answers
- Optionally support **multi-turn conversation**, so follow-up questions have context
- Display retrieved chunks, metadata, summaries, and named entities

---

## 🚀 Features

✅ Hybrid RAG (summaries, entities, full text)  
✅ Page-level OCR for scanned PDFs  
✅ Cross-document search — answers always come from **all indexed files**  
✅ Multi-turn conversation tracking (Streamlit session state)  
✅ Interactive Streamlit web app

---

## 🗂️ Project Structure

```
.
├── cohere_client.py      # Wraps Cohere API calls (embedding, summary, extraction, answer gen)
├── ingestion.py          # Handles OCR, text extraction, metadata enrichment, index build
├── query_engine.py       # Runs queries against the vector index + calls Cohere to compose answers
├── main.py               # Streamlit front-end
├── test_script.py        # Simple tests for single-turn and multi-turn queries
├── config.py             # Loads COHERE_API_KEY
├── requirements.txt      # All dependencies
└── storage/              # Saved vector index
```

---

## ⚙️ Requirements

- Python 3.9+
- [Cohere API Key](https://dashboard.cohere.com/api-keys)

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup

1️⃣ Get your Cohere API key and **add it to your environment**:

```bash
Replace your key in config.py

Here: COHERE_API_KEY = os.getenv("COHERE_API_KEY", "your_cohere_api_key")


---

## 📥 Index your documents

1. Place your **PDF**, **DOCX**, or **TXT** files in a folder.
2. Run the Streamlit app:

```bash
streamlit run main.py
```

3. Enter your folder path and click **Build Index**.

---

## 💬 Ask questions

- Once the index is built, type your question and click **Get Answer**.
- The app:
  - Retrieves relevant context chunks across **all docs**
  - Composes an answer using Cohere’s LLM with multi-turn memory
  - Displays retrieved metadata for full transparency

---

## ✅ Example usage

Try:

```
Q: Who is Charbel?
Q: What is The Phoenix Alliance?
Q: What is his phone number?
```

Answers will combine fresh retrieval and your conversation history.

---

## 🧩 Tests

Run the included test script to verify:

```bash
python test_script.py
```

---

## 🗂️ Tech Stack

- **Python** — main glue
- **Streamlit** — web UI
- **LlamaIndex** — vector store & retrieval
- **Cohere** — embeddings, summarization, entity extraction, final LLM answers
- **PyMuPDF + pytesseract** — robust PDF text extraction with OCR fallback

---

## ⚠️ Notes

- Keep your **Cohere usage limits** in mind (10 calls/minute for free tier), that's why we added sleep(6) and the "build index" process takes around 2 minutes.
- The vector index is stored in `./storage` — rebuild if your docs change.

---

## 📄 License

This project is provided as a technical demo — adjust and adapt for your needs!

---

**Made with ❤️ and Cohere**
