import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

with open("information.txt","r", encoding="UTF-8") as f:
    context = f.read()

chroma_client = chromadb.Client(Settings(
    persist_directory = "./chroma_store",
    anonymized_telemetry = False
))

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_function = SentenceTransformerEmbeddingFunction(model)

collection = chroma_client.get_or_create_collection(
    name="my_collection",
    embedding_function=embedding_function
)


