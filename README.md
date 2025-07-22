
# 📚 Native Language QA — RAG++ with Multi-turn Conversation

A **Retrieval-Augmented Generation (RAG)** chatbot that:
- Indexes **native language documents** (PDF, DOCX, TXT)
- Uses **OCR** for scanned pages
- Extracts **summaries** and **entities**
- Answers questions by **retrieving fresh context** from *all* indexed docs every time
- Supports **multi-turn conversation** with follow-up Q&A

---

## 🚀 How it works

✅ **Architecture**  
- **Vector Store:** Documents are split & embedded using **Cohere embeddings** (`llama-index-embeddings-cohere`).
- **Storage:** The vector index is saved locally for fast retrieval.
- **Retriever:** On each user query, the retriever searches **all indexed chunks**.
- **LLM:** A **Cohere LLM** generates the final answer using both the user’s question and retrieved context.
- **Chat Memory:** Uses a simple conversation history to handle follow-up questions.

✅ **Tools Used**
- [Cohere](https://cohere.com) — for embeddings & LLM completions.
- [LlamaIndex](https://www.llamaindex.ai/) — for vector store, retriever, and orchestration.
- [FAISS](https://github.com/facebookresearch/faiss) — optional for local vector storage backend.
- **OCR:** `pytesseract` + `pdf2image` + `PyMuPDF` for page text extraction.
- [Streamlit](https://streamlit.io) — for the local web UI.

---

## 🌍 Native Language Support

- Any language your documents are written in will be embedded as raw text.
- OCR processes **scanned pages**, converting non-searchable PDFs to plain text.
- As long as Cohere’s embedding & generation models understand the language, your QA works.
- This makes the pipeline flexible for **Arabic, French, English**, etc.

---

## ⚙️ Key Features

- 🔍 **Cross-document:** Every query re-searches **all** indexed pages — no stale cache.
- 🧩 **Hybrid chunks:** Uses page-level + chunk-level text + OCR to get the best signal.
- 🗣️ **Multi-turn chat:** Tracks chat history so follow-ups stay in context — but **always** retrieves fresh docs.
- 📑 **Rich metadata:** Shows file name, folder, page number, summary & entities for transparency.

---

## 🏷️ Limitations & Improvements

- **Trial API Limits:** The free Cohere API has low rate & quota limits → production needs a paid plan.
- **Chain-of-thought:** Cross-passage reasoning can be improved with advanced prompt chaining.
- **Chunking:** For huge docs, more granular chunking & smart overlap could boost accuracy.
- **Better memory:** Right now the chat memory is simple → can be expanded with full conversation trees.
- **Deployment:** Runs locally on Streamlit — production should use a secure backend.

---

## 🖥️ How to Run

1️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

2️⃣ **Set your API key**  

Get your Cohere API key and **add it to your environment**:

```bash
Replace your key in config.py

Here: COHERE_API_KEY = os.getenv("COHERE_API_KEY", "your_cohere_api_key")
```

3️⃣ **Run the app**
```bash
streamlit run main.py
```

4️⃣ **Open in your browser:**  
[http://localhost:8501](http://localhost:8501)

---

## 📂 Project Structure

.
├── cohere_client.py   # Wraps Cohere API: embed, summarize, extract entities, chat
├── ingestion.py       # Loads docs, runs OCR, builds vector index
├── query_engine.py    # Retrieves relevant chunks, calls Cohere LLM with context
├── main.py            # Streamlit UI with multi-turn conversation
├── test_script.py     # Local test script for single-turn & follow-ups
├── config.py          # Reads Cohere API key
├── requirements.txt   # All Python dependencies
└── .gitignore         # Ignores venv, cache, API secrets
└── storage/           # Saved vector index

---

## ✅ Example

- **Q:** Who is Charbel?  
- **A:** [Full bio from CV]

- **Q:** What is The Phoenix Alliance?  
- **A:** [Details from the Phoenix doc — cross-doc tested!]

- **Q:** What’s his phone number? *(Follow-up)*  
- **A:** [Pulls from same CV — chat memory + fresh search]

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

## 🤝 Contributing

Feel free to fork, tweak chunking, switch to OpenAI, or wrap as an API.
PRs are welcome!

---

## 📄 License

This project is provided as a technical demo — adjust and adapt for your needs!

---

## 📬 Questions?

Message Charbel LEBBOUS | charbellebbousf@gmail.com | [\[YOUR GITHUB HANDLE\]](https://github.com/CharbelLebbous)

Happy building! 🚀

---

**Made with ❤️ and Cohere**