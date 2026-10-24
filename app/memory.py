import json
import os
from datetime import datetime

MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "outputs",
    "memory.json",
)


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_to_memory(topic, platform, tone, output_type, saved_file):
    print("[Tool Called]: Memory Tool")
    history = load_memory()
    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic,
        "platform": platform,
        "tone": tone,
        "output_type": output_type,
        "saved_file": saved_file,
    })
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def get_last_entry():
    history = load_memory()
    return history[-1] if history else None