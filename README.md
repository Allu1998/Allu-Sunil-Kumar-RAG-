
# RAG System for Academic Articles

This project is a complete Retrieval-Augmented Generation (RAG) system designed to answer questions based on a collection of academic articles or other documents in PDF format.

It uses a vector database to find relevant context from the documents and provides that context to a Large Language Model (LLM) to generate accurate, source-based answers. The entire system is served via a web API and includes a simple user interface.

-----

## **Features**

  * **Document Ingestion**: Automatically processes multiple PDF files.
  * **Vector Embeddings**: Creates semantic embeddings for efficient text retrieval.
  * **Vector Storage**: Uses **ChromaDB** to store and query document embeddings.
  * **RAG API**: A **FastAPI** backend that takes a question, finds context, and generates an answer using an LLM.
  * **Web UI**: A simple **Streamlit** interface for asking questions and viewing answers.
  * **Local LLMs**: Designed to run with local language models via **Ollama**.

-----

## **Tech Stack**

  * **Backend**: Python, FastAPI
  * **Frontend**: Streamlit
  * **LLM Serving**: Ollama
  * **Vector Database**: ChromaDB
  * **Embeddings**: Sentence-Transformers

-----

## **Installation and Setup**

Follow these instructions to get the project running on a new Windows machine.

#### **1. Prerequisites**

  * **Python 3.8+**: Make sure Python is installed and accessible from your terminal.
  * **Ollama**: Install the [Ollama for Windows](https://ollama.com/) application and ensure it is running.
  * **Git**: You will need Git to clone the repository.

#### **2. Clone the Repository**

```bash
git clone <your-repository-url>
cd <repository-name>
```

#### **3. Set Up Virtual Environment**

Create and activate a Python virtual environment.

```powershell
# Create the environment
python -m venv venv

# Allow activation scripts to run (one-time setup per user)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate the environment
.\venv\Scripts\activate
```

#### **4. Install Dependencies**

Install all the required Python packages.

```bash
pip install -r requirements.txt
```

#### **5. Download an LLM**

Pull a model to be used by Ollama. We recommend `llama3`.

```bash
ollama run llama3
```

-----

## **Usage**

#### **1. Prepare Your Data**

Before running the application, you must process your source documents.

1.  Place all your source PDF files into the `data/raw_input/` directory.
2.  Run the data pipeline script in three steps. This will ingest the PDFs, create embeddings, and store them in the vector database.

<!-- end list -->

```powershell
# Ensure your venv is activated
python main.py ingest
python main.py embed
python main.py store
```

#### **2. Run the Application**

You need two terminals to run the backend and frontend separately.

  * **Terminal 1: Start the Backend API**

    ```powershell
    # Make sure you are in the project directory with venv activated
    uvicorn app:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

  * **Terminal 2: Start the Frontend UI**

    ```powershell
    # Open a new terminal and activate the environment
    .\venv\Scripts\activate
    streamlit run ui_streamlit.py
    ```

    Open your web browser and navigate to the local URL provided by Streamlit to start asking questions.

-----

## **Updating the Knowledge Base**

To add new documents to the system:

1.  Add new PDF files to the `data/raw_input/` directory.
2.  Re-run the complete data pipeline to update the vector database.
    ```powershell
    python main.py ingest
    python main.py embed
    python main.py store
    ```
