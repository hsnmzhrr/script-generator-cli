# ScriptGen

CLI tool that generates structured YouTube scripts using the Gemini API (free tier). The prompt template encodes retention structure from professional scriptwriting practice (800+ produced scripts): hook-first, open loops between sections, payoff before CTA.

## Why this exists

Generic "write me a YouTube script" prompts produce scripts that lose viewers in the first 30 seconds. This tool separates the *structure* (encoded once, in `prompts.py`) from the *topic* (supplied per run), so every output follows a retention-tested skeleton.

## Setup

```bash
pip install requests
export GEMINI_API_KEY=your_key_here  # free at aistudio.google.com
```

## Usage

```bash
python generate.py --niche finance --topic "how to start investing with $100" --tone conversational --minutes 8
```

Options:
- `--tone`: conversational | authoritative | storytelling | energetic
- `--minutes`: target video length (words calculated at 140 wpm narration pace)
- `--out`: output directory (default `output/`)

Output is a Markdown file with `## HOOK / SETUP / BODY / PAYOFF / CTA` section markers so an editor can navigate it.

## Design decisions

- **Structure lives in the prompt, not post-processing.** Editing `prompts.py` changes every future script. This mirrors how production scriptwriting teams maintain style guides.
- **Anti-fabrication rule built in.** The prompt explicitly instructs the model to phrase claims qualitatively rather than invent statistics, addressing the most common failure of AI-generated educational content.
- **140 wpm assumption** matches standard faceless-channel narration pace.

## Example output

`output/` is gitignored (it's where your own runs land locally). Three generated samples across different niches and tones are included in `examples/`: finance/conversational, health/storytelling, tech/energetic.
