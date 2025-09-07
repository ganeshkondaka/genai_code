from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path= Path(__file__).parent /"nodejs_pdf_notes.pdf"

#loading
loader=PyPDFLoader(pdf_path)
docs=loader.load()

#chunking
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=400
    )

split_docs=text_splitter.split_documents(documents =docs)

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
    #dont need to mentions the openai api key, it will be picked up automatically
)

# Using [embedding_model] create embeddings of [split_docs] and store in DB
vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

print("Indexing of Documents Done...")