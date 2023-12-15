from enum import Enum
from langchain.document_loaders import OnlinePDFLoader, PyPDFLoader
from langchain.embeddings.llamacpp import LlamaCppEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, NLTKTextSplitter, CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

pdf_links = []
pdf_filenames = []

class SplitModes(Enum):
    CHARACTER = 'character'
    RECURSIVE_CHAR = 'recursive_character'
    NLTK = 'nltk'
    
def ingest_pdf(db_path, pdf_path:str, split_mode=SplitModes.RECURSIVE_CHAR, chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_CHUNK_OVERLAP):
    if pdf_path.startswith("http"):
        loader = OnlinePDFLoader(pdf_path)
    else:
        loader = PyPDFLoader(pdf_path)
    
    pdf_docs = loader.load()

    if split_mode == 'character':
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    elif split_mode == "recursive_character":
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    elif split_mode == 'nltk':
        text_splitter = NLTKTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    else:
        raise ValueError("Please specify the split mode.")
        
    documents = text_splitter.split_documents(pdf_docs)
    embeddings = LlamaCppEmbeddings()
    faiss_db = FAISS.from_documents(documents=embeddings)
    faiss_db.save_local(db_path)
