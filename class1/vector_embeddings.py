# venv\Scripts\activate

# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI()

# text = "dog chases cat"

# response = client.embeddings.create(
#     model="text-embedding-3-small",
#     input=text
# )

# print("Vector Embeddings", response)
# print(len(response.data[0].embedding))


"""Module for generating vector embeddings using Gemini API."""
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

text = "dog chases cat"

# Generate embeddings using Gemini
response = genai.embed_content(
    model="models/embedding-001",
    content=text
)

print("Vector Embeddings", response)
print("Embedding length:", len(response['embedding']))