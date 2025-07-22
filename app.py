from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import time

# --- CONFIGURATION ---
VECTOR_DB_DIR = 'data/vectordb'
COLLECTION_NAME = 'collections'
LLM_MODEL = 'llama3'

# --- INITIALIZE MODELS AND DATABASE ---
app = FastAPI()
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
collection = client.get_collection(name=COLLECTION_NAME)

# --- API DATA MODELS ---
class QueryRequest(BaseModel):
    question: str

# --- API ENDPOINTS ---
@app.post("/generate-response/")
def generate_response(request: QueryRequest):
    start_time = time.time()
    try:
        query_embedding = embedding_model.encode(request.question).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        retrieved_context = "\n\n".join(results['documents'][0])
        prompt = f"""
        You are an AI assistant. Answer the user's question based only on the following context.
        If the context is insufficient, say 'I'm sorry, but the provided context doesn't have enough information to answer that.'

        Context:
        {retrieved_context}

        Question:
        {request.question}
        """
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{'role': 'user', 'content': prompt}]
        )
        end_time = time.time()
        duration = end_time - start_time
        return {
            "response": response['message']['content'],
            "response_time_seconds": round(duration, 2)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "RAG API is running. Go to /docs for the interactive API documentation."}