# ingestion.py

# ✅ Import core components from LlamaIndex
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.embeddings.cohere import CohereEmbedding
from cohere_client import CohereClient

# ✅ OCR and PDF handling libraries
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
import fitz  # PyMuPDF for PDF text extraction
import time  # For rate limiting

from llama_index.core import Document  # Document structure for indexing
from config import COHERE_API_KEY

# ✅ Initialize a single instance of the Cohere client
cohere_client = CohereClient()

def extract_page_text_with_ocr(pdf_path):
    """
    Extract text from each page of a PDF.
    Uses both direct text extraction and OCR as a fallback.
    Generates a summary and entity extraction for each page.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        list: A list of LlamaIndex Document objects with text + metadata.
    """
    doc = fitz.open(pdf_path)
    pages = []

    # Loop through each page in the PDF
    for i, page in enumerate(doc, start=1):
        # Try direct text extraction
        text = page.get_text().strip()

        # Run OCR as backup
        images = convert_from_path(pdf_path, first_page=i, last_page=i)
        ocr_text = pytesseract.image_to_string(images[0]).strip()

        # Combine both methods
        combined_text = "\n".join(filter(None, [text, ocr_text]))

        # Generate a summary (API call to Cohere)
        summary = cohere_client.summarize(combined_text)

        # Be mindful of Cohere’s rate limits: 10 calls per minute
        time.sleep(6)

        # Extract named entities & key facts
        entities = cohere_client.extract_entities(combined_text)

        # Create a Document with all metadata
        page_doc = Document(
            text=combined_text,
            metadata={
                "file_name": Path(pdf_path).name,
                "folder_name": Path(pdf_path).parent.name,
                "folder_path": str(Path(pdf_path).parent),
                "page_number": i,
                "summary": summary,
                "entities": entities
            }
        )

        pages.append(page_doc)

    return pages

def load_docs_with_ocr(folder_path: str):
    """
    Load and process all supported files in a folder.
    - PDF files → page-level OCR extraction.
    - .docx, .txt → direct text extraction.
    Each document gets summarized and entity extraction.
    
    Args:
        folder_path (str): Path to the folder with documents.
    
    Returns:
        list: List of Documents ready for indexing.
    """
    docs = []

    for path in Path(folder_path).rglob("*"):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            # Use page-level extraction for PDFs
            pages = extract_page_text_with_ocr(str(path))
            docs.extend(pages)

        elif suffix in [".docx", ".txt"]:
            # Use LlamaIndex's reader for simple text/docx
            reader = SimpleDirectoryReader(input_files=[str(path)])
            loaded_docs = reader.load_data()

            for doc in loaded_docs:
                doc.metadata.update({
                    "file_name": path.name,
                    "folder_name": path.parent.name,
                    "folder_path": str(path.parent),
                    "page_number": None,  # Not paginated
                    "summary": cohere_client.summarize(doc.text),
                    "entities": cohere_client.extract_entities(doc.text)
                })
            docs.extend(loaded_docs)

    return docs

def build_index(folder_path: str):
    """
    Build a vector index using Cohere embeddings.
    Saves the index to local storage for later querying.
    
    Args:
        folder_path (str): Path to the folder with documents.
    
    Returns:
        VectorStoreIndex: The built index.
    """
    # Initialize the Cohere embedding model
    cohere_embed = CohereEmbedding(api_key=COHERE_API_KEY)

    # Load and process all docs
    docs = load_docs_with_ocr(folder_path)

    # Create the index
    index = VectorStoreIndex.from_documents(docs, embed_model=cohere_embed)

    # Persist the index to disk
    index.storage_context.persist(persist_dir="./storage")

    print(f"✅ Index built and saved! Total docs/pages: {len(docs)}")

    return index
