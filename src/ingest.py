import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
PDF_PATH = os.getenv("PDF_PATH")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PDF_FULL_PATH = os.path.join(BASE_DIR, PDF_PATH)

def ingest_pdf():
    docs = load_documents()
    chunks = split_documents(docs)
    enriched = clean_documents(chunks)

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = create_embeddings()
    store = create_vector_store(embeddings)
    store.add_documents(documents=enriched, ids=ids)

def validate_config():
    required_vars = (
        "GOOGLE_API_KEY",
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
    )

    for var in required_vars:
        if not os.getenv(var):
            raise RuntimeError(f"Environment variable {var} is not set")
    
    if not os.path.exists(PDF_FULL_PATH):
        raise FileNotFoundError(f"PDF não encontrado: {PDF_FULL_PATH}")

def load_documents():
    print(f"Loading PDF from: {PDF_FULL_PATH}")
    return PyPDFLoader(PDF_FULL_PATH).load()

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False
    )
    chunks = splitter.split_documents(docs)
    print(f"Chunks generated: {len(chunks)}")
    return chunks

def clean_documents(chunks):
    return [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in chunks
    ]

def create_embeddings():
    print("Initializing embedding model.")
    return GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL"),
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

def create_vector_store(embeddings):
    print("Connecting to PGVector database.")
    return PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )

if __name__ == "__main__":
    validate_config()
    ingest_pdf()