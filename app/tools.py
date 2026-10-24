import os
import sys
import re
import requests
from datetime import datetime

from prompts import (
    SYSTEM_STYLE, PLATFORM_RULES, TREND_IDEAS, CAPTION,
    HASHTAGS, REEL_SCRIPT, REVIEWER,
)

sys.stdout.reconfigure(encoding="utf-8")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")


def ask_ollama(prompt, max_tokens=250, model=MODEL):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "30m",
        "options": {"num_predict": max_tokens, "temperature": 0.7},
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=900)
    r.raise_for_status()
    return r.json()["response"].strip()


def log_tool(name):
    print(f"[Tool Called]: {name}")


def trend_idea_generator(topic, platform, tone):
    log_tool("Trend Idea Generator")
    return ask_ollama(TREND_IDEAS.format(style=SYSTEM_STYLE, topic=topic,
                                         platform=platform, tone=tone), 150)


def caption_writer(topic, platform, tone, angle):
    log_tool("Caption Writer")
    rules = PLATFORM_RULES.get(platform, "Clear and concise.")
    return ask_ollama(CAPTION.format(style=SYSTEM_STYLE, topic=topic, platform=platform,
                                     tone=tone, angle=angle, rules=rules), 250)


def hashtag_generator(topic, platform):
    log_tool("Hashtag Generator")
    return ask_ollama(HASHTAGS.format(style=SYSTEM_STYLE, topic=topic,
                                      platform=platform), 60)


def reel_script_generator(topic, tone):
    log_tool("Reel Script Generator")
    return ask_ollama(REEL_SCRIPT.format(style=SYSTEM_STYLE, topic=topic, tone=tone), 200)


def content_reviewer(platform, content):
    log_tool("Content Reviewer")
    return ask_ollama(REVIEWER.format(style=SYSTEM_STYLE, platform=platform,
                                      content=content), 200)


def file_saver(topic, platform, text, folder="saved_results"):
    log_tool("File Saver")
    slug = re.sub(r"[^a-z0-9]+", "_", topic.lower()).strip("_")[:40]
    plat = re.sub(r"[^a-z0-9]+", "_", platform.lower()).strip("_")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, folder, f"{slug}_{plat}_{stamp}.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path