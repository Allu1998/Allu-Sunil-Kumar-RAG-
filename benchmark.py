import requests
import time
import sys

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000"
RAG_ENDPOINT = f"{API_URL}/generate-response/"
BASELINE_ENDPOINT = f"{API_URL}/baseline-response/"
TEST_QUESTION = "What is VUCA?" # Use a question relevant to your documents

print("=== Benchmark Script Started ===")
sys.stdout.flush()

# --- BENCHMARKING LOGIC ---
print(f"Sending test question: '{TEST_QUESTION}'")
sys.stdout.flush()

# 1. Measure RAG Response Time
try:
    print("\nTesting RAG pipeline...")
    sys.stdout.flush()
    payload = {"question": TEST_QUESTION}
    
    start_time_rag = time.time()
    response_rag = requests.post(RAG_ENDPOINT, json=payload, timeout=600)
    end_time_rag = time.time()
    
    rag_duration = end_time_rag - start_time_rag
    print(f"RAG Response Time: {rag_duration:.2f} seconds") # [cite: 346]
    sys.stdout.flush()
    # print(f"RAG Response: {response_rag.json()['response']}") # Uncomment to see the response
except Exception as e:
    print(f"Error testing RAG pipeline: {e}")
    sys.stdout.flush()

# 2. Measure Baseline LLM Response Time
try:
    print("\nTesting Baseline LLM...")
    sys.stdout.flush()
    payload = {"question": TEST_QUESTION}

    start_time_baseline = time.time()
    response_baseline = requests.post(BASELINE_ENDPOINT, json=payload, timeout=600)
    end_time_baseline = time.time()

    baseline_duration = end_time_baseline - start_time_baseline
    print(f"Baseline Response Time: {baseline_duration:.2f} seconds") # [cite: 348]
    sys.stdout.flush()
    # print(f"Baseline Response: {response_baseline.json()['response']}") # Uncomment to see the response
except Exception as e:
    print(f"Error testing Baseline pipeline: {e}")
    sys.stdout.flush()

print("=== Benchmark Script Finished ===")
sys.stdout.flush()