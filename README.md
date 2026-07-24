# ScriptGen

CLI tool that generates structured YouTube scripts using the Gemini API (free tier). The prompt template encodes retention structure from professional scriptwriting practice (800+ produced scripts): hook-first, open loops between sections, payoff before CTA.

## Why this exists

Generic "write me a YouTube script" prompts produce scripts that lose viewers in the first 30 seconds. This tool separates the *structure* (encoded once, in `prompts.py`) from the *topic* (supplied per run), so every output follows a retention-tested skeleton.

## Setup

```bash
pip install requests
export GEMINI_API_KEY=your_key_here        # macOS/Linux
$env:GEMINI_API_KEY = "your_key_here"      # Windows PowerShell
```

Free key from aistudio.google.com. The code reads it from the environment at runtime, never from a file.

Two notes on auth and model choice, both of which caused real failures during testing:

- Keys issued since mid-2026 start with `AQ.` rather than the older `AIza`. Both work here. The key is sent in an `x-goog-api-key` header rather than a URL query parameter, so it never appears in logs or stack traces.
- Model is `gemini-2.5-flash` with `thinkingConfig.thinkingBudget` set to 0, so the full token budget goes to the script rather than to internal reasoning.

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
- **Tone is a lookup, not a code path.** `TONE_NOTES` maps each tone flag to written style instructions injected at runtime. Adding a tone is one dictionary entry, zero code changes.
- **Anti-fabrication rule built in.** The prompt explicitly instructs the model to phrase claims qualitatively rather than invent statistics, addressing the most common failure of AI-generated educational content.
- **140 wpm assumption** matches standard faceless-channel narration pace.

## Example output

`output/` is gitignored (it's where your own runs land locally). Generated samples across different niches and tones are included in `examples/`.

## Limitations (honest ones)

- **Word targets are approximate.** An 8-minute request (1,120-word target at 140 wpm) returned 853 words in testing, a 24% undershoot. The model treats length as a suggestion, not a constraint.
- **The template controls structure reliably but not voice.** Section order, open loops, and payoff placement come out correct every run. The prose still reaches for filler phrasing ("here's the kicker," "a double whammy") that a produced script would cut. Structure is solvable with prompting; voice is not.
- **Free tier limits.** Roughly 15 requests per minute and 1,500 per day. Ample for single-script runs, not for batch generation.
- **Third-party model dependency.** Behaviour changes without notice. The migration off `gemini-2.0-flash` (retired June 2026) is recorded in the commit history.
