import sys
import time
import requests

# Windows par emoji print karne ke liye
sys.stdout.reconfigure(encoding="utf-8")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


def ask_ollama(prompt, model=MODEL):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=600)
    response.raise_for_status()
    return response.json()["response"]


if __name__ == "__main__":
    start = time.time()
    result = ask_ollama("Give me 3 viral LinkedIn post ideas about AI internships.")
    print(result)
    print(f"\n[Time taken: {time.time() - start:.1f} seconds]")