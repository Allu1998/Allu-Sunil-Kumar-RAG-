import os
import sys
import json
import chromadb
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# --- DIRECTORIES AND CONFIG ---
RAW_DIR = 'data/raw_input'
CLEANED_DIR = 'data/cleaned_text'
EMBEDDINGS_DIR = 'data/embeddings'

VECTOR_DB_DIR = 'data/vectordb' # As specified in the system requirements [cite: 36]
COLLECTION_NAME = 'collections' # As specified in the system requirements [cite: 34]

# --- STEP 1: DOCUMENT INGESTION ---
def ingest_documents():
    # ... (code from previous step, no changes needed) ...
    print(f"Starting document ingestion from '{RAW_DIR}'...")
    if not os.path.exists(CLEANED_DIR):
        os.makedirs(CLEANED_DIR)

    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(RAW_DIR, filename)
            print(f"Processing: {filename}")
            try:
                reader = PdfReader(pdf_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

                base_filename = os.path.splitext(filename)[0]
                cleaned_filename = f"{base_filename}_cleaned.txt"
                output_path = os.path.join(CLEANED_DIR, cleaned_filename)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Successfully saved to: {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    print("Document ingestion complete.")

# --- STEP 2: EMBEDDING GENERATION ---
def generate_embeddings():
    # ... (code from previous step, no changes needed) ...
    print("Starting embedding generation...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')

    if not os.path.exists(EMBEDDINGS_DIR):
        os.makedirs(EMBEDDINGS_DIR)

    for filename in os.listdir(CLEANED_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(CLEANED_DIR, filename)
            print(f"Processing: {filename}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                chunks = text_splitter.split_text(text)
                print(f"Split '{filename}' into {len(chunks)} chunks.")

                for i, chunk in enumerate(chunks):
                    embedding = embedding_model.encode(chunk, convert_to_tensor=False).tolist()
                    data = {"source": filename, "chunk_id": i, "text": chunk, "embedding": embedding}

                    base_filename = os.path.splitext(filename)[0]
                    output_filename = f"{base_filename}_chunk_{i}.json"
                    output_path = os.path.join(EMBEDDINGS_DIR, output_filename)

                    with open(output_path, 'w', encoding='utf-8') as json_file:
                        json.dump(data, json_file)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    print("Embedding generation complete.")

# --- STEP 3: STORE EMBEDDINGS IN VECTOR DB ---
def store_in_chromadb():
    print("Starting to store embeddings in ChromaDB...")

    # Initialize the persistent ChromaDB client
    client = chromadb.PersistentClient(path=VECTOR_DB_DIR)

    # Get or create the collection
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # Prepare lists to hold the data for batch insertion
    documents = []
    embeddings = []
    metadatas = []
    ids = []

    # Process each embedding file
    for filename in os.listdir(EMBEDDINGS_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(EMBEDDINGS_DIR, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            documents.append(data['text'])
            embeddings.append(data['embedding'])
            metadatas.append({'source': data['source'], 'chunk_id': data['chunk_id']})
            # Create a unique ID for each chunk
            ids.append(os.path.splitext(filename)[0])

    # Add the data to the collection in a single batch
    if ids:
        collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {len(ids)} embeddings to the '{COLLECTION_NAME}' collection.")
    else:
        print("No embeddings found to add.")

    print("Vector storage complete.")


# --- SCRIPT EXECUTION ---
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please specify a step to run: 'ingest', 'embed', or 'store'")
        sys.exit(1)

    step = sys.argv[1]

    if step == 'ingest':
        ingest_documents()
    elif step == 'embed':
        generate_embeddings()
    elif step == 'store':
        store_in_chromadb()
    else:
        print(f"Unknown step: {step}. Please use 'ingest', 'embed', or 'store'.")
        
