"""ScriptGen: CLI tool that generates structured YouTube scripts using the Gemini API (free tier).

Setup:
    Get a free API key at https://aistudio.google.com (no card required)
    export GEMINI_API_KEY=your_key

Usage:
    python generate.py --niche finance --topic "how to start investing with $100" --tone casual --minutes 8
"""

import argparse
import os
import sys
from datetime import datetime

import requests

from prompts import build_prompt

MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def parse_args():
    p = argparse.ArgumentParser(description="Generate a structured YouTube script.")
    p.add_argument("--niche", required=True, help="Content niche, e.g. finance, health, tech")
    p.add_argument("--topic", required=True, help="Video topic")
    p.add_argument("--tone", default="conversational",
                   choices=["conversational", "authoritative", "storytelling", "energetic"],
                   help="Narration tone")
    p.add_argument("--minutes", type=int, default=8, help="Target video length in minutes")
    p.add_argument("--out", default="output", help="Output directory")
    return p.parse_args()


def generate(prompt: str, key: str) -> str:
    r = requests.post(
        URL,
        params={"key": key},
        json={"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"maxOutputTokens": 8000,
                                   "thinkingConfig": {"thinkingBudget": 0}}},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]


def main():
    args = parse_args()

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("Set GEMINI_API_KEY first. Free key at https://aistudio.google.com")

    prompt = build_prompt(args.niche, args.topic, args.tone, args.minutes)
    print(f"Generating {args.minutes}-minute {args.tone} script: {args.topic} [{args.niche}]")

    script = generate(prompt, key)

    os.makedirs(args.out, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c if c.isalnum() or c in " -" else "" for c in args.topic)[:40].strip().replace(" ", "_")
    path = os.path.join(args.out, f"{args.niche}_{safe_topic}_{stamp}.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {args.topic}\n\n")
        f.write(f"Niche: {args.niche} | Tone: {args.tone} | Target: {args.minutes} min\n\n---\n\n")
        f.write(script)

    words = len(script.split())
    print(f"Done. {words} words (~{words // 140} min narration) -> {path}")


if __name__ == "__main__":
    main()
