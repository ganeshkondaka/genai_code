from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

# Take User Query
query = input("YOU : > ")

# Vector Similarity Search [query] in DB
search_results = vector_db.similarity_search(
    query=query
)

# Search Results is a list of objects, one of them look like this --------
#  {
#     "document": 2,
#     "metadata": {
#       "producer": "macOS Version 10.14.1 (Build 18B75) Quartz PDFContext",
#       "creator": "Acrobat PDFMaker 17 for Word",
#       "author": "Andrew Mead",
#       "creation_date": "2019-02-27 14:03:40 UTC",
#       "modified_date": "2019-02-27 14:03:40 UTC",
#       "source": "d:\\mine_\\code_files_@@\\cohort_codes\\myproject_incohort\\Genai\\rag\\nodejs_pdf_notes.pdf",
#       "total_pages": 125,
#       "page": 9,
#       "page_label": "10"
#     },
#     "page_content": {
#       "topic": "Importing Node.js Core Modules",
#       "description": "To get started, let’s work with some built-in Node.js modules. These are modules that come with Node, so there’s no need to install them. The module system is built around the require function.",
#       "code_example": "const fs = require('fs')\n\nfs.writeFileSync('notes.txt', 'I live in Philadelphia')",
#       "note": "The script above uses require to load in the fs module and writeFileSync to write a message to notes.txt. After running, you’ll notice a new notes.txt file."
#     }
#   },

context = "\n\n\n".join([f"Page Content: {result.page_content}\n Page Number: {result.metadata['page_label']}\n File Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
    You are a helpfull AI Assistant who asnweres user query based on the available context
    retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user
    to open the right page number to know more.

    Context:
    {context}
"""

#chat section
chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": query },
    ]
)

print(f"RAG BOT 🤖: {chat_completion.choices[0].message.content}")