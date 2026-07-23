"""Prompt template for ScriptGen.

The structure encoded here comes from professional scriptwriting practice:
hook in the first 15 seconds, open loop before each section, payoff before CTA.
Words-per-minute assumption: 140 (standard faceless narration pace).
"""

TONE_NOTES = {
    "conversational": "Write like you're explaining to a friend. Contractions, direct address, short sentences.",
    "authoritative": "Confident, precise, evidence-forward. No hedging. Cite the type of source for claims.",
    "storytelling": "Open with a specific scene or person. Weave facts into narrative. Callbacks to the opening.",
    "energetic": "High pace, punchy fragments, frequent direct questions to the viewer.",
}


def build_prompt(niche: str, topic: str, tone: str, minutes: int) -> str:
    target_words = minutes * 140
    return f"""You are writing a YouTube script for a faceless {niche} channel.

Topic: {topic}
Target length: {target_words} words ({minutes} minutes at 140 wpm)
Tone: {TONE_NOTES[tone]}

Follow this exact structure:

## HOOK (first 40-60 words)
Open with the single most surprising or high-stakes element of the topic.
No greetings, no "in this video". Create an open loop the viewer needs resolved.

## SETUP (~10% of script)
Establish why this matters to the viewer personally. One concrete stake.

## BODY (3-5 sections, ~70% of script)
Each section:
- Starts with a mini-hook sentence
- Delivers one clear idea with a specific example or number
- Ends with a bridge that opens the next loop
Never invent statistics. If a claim needs a number you don't have, phrase it
qualitatively instead of fabricating one.

## PAYOFF (~10%)
Resolve the loop opened in the hook. This is the moment the title promised.

## CTA (2-3 sentences max)
One action. Natural, not desperate.

Formatting rules:
- Write narration only. No camera directions, no [B-ROLL] markers.
- Short paragraphs, 1-3 sentences.
- Mark each section with its ## header so the editor can navigate.

Write the full script now."""
