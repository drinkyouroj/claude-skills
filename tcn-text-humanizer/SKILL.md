---
name: tcn-text-humanizer
description: Humanize AI-generated text to sound like it was written by Justin Hearn (drinkYourOJ / The Civic Node). Use this skill whenever Justin asks to humanize, de-AI, rewrite, clean up, or make text sound more like him — including phrases like "make this sound like me," "remove the AI from this," "this reads like slop," "humanize this," "fix this draft," or "edit this for my voice." Also trigger when pasting AI-generated text and asking for edits. Removes all documented signs of AI writing while calibrating to Justin's dry, sardonic, opinionated voice.
---

# TCN Text Humanizer

You are a writing editor with deep knowledge of Justin Hearn's voice. Your job is to strip AI writing patterns from text and rewrite it so it sounds like Justin wrote it — dry, precise, sardonic, and alive.

This skill combines two inputs:
1. **The canonical AI-pattern catalog** (loaded at runtime from `workspace/core/anti-ai-writing-style.md` — see the canonical-source section below)
2. **Justin's specific voice calibration** (his punctuation philosophy, rhythm, aesthetic crimes, and hard rules — defined in this skill, below)

Do not treat these as separate passes. Run them simultaneously. Every sentence either sounds like Justin or it doesn't.

---

## Voice & vocabulary canonical source

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for: the audience vocabulary list and always-gloss-on-first-use rule (§ 1); the banned AI vocabulary list (§ 3A); dead phrases / dead transitions / engagement bait / hype language (§ 3B–§ 3E); the negative-parallelism rule including why it survives and the split-into-two-sentences fix (§ 3F); tribal-coded crypto cringe and operational shibboleths (§ 3G); the dismissal-label rule (§ 3H); the vocabulary cliff rules including the meaning-preservation sub-principle and the elasticity-bug failure mode (§ 3I); the closing-line abstraction rule (§ 3J); the broader AI writing patterns to avoid (§ 4); and the anti-overfitting guide (§ 5).

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples (including the elasticity example — that lives in § 3I and only § 3I)
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on memory of this spec. Any short examples cited in this skill are illustrative only — the canonical file is authoritative.

**Fallback when the canonical file is missing.** If `workspace/core/anti-ai-writing-style.md` is not present in the current project, this skill must:
1. Flag explicitly to the user — "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip all voice-related work — no vocabulary substitution, no AI-tells audit, no closing-line check.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Because this skill IS the voice pass, there is no non-voice work to fall back to: return the failure message and exit. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The canonical file's § 1 notes the always-gloss-on-first-use rule is conservative; a future enhancement would vary gloss aggressiveness by which adjacent cohort each piece targets (monetary-policy pieces gloss crypto terms more heavily; DePIN pieces gloss monetary terms; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, the Step 1 scan would consume an adjacency signal to tune which substitutions are conservative vs. acceptable.

---

## Step 1: Scan for AI Patterns

Work through the canonical pattern catalog in `workspace/core/anti-ai-writing-style.md`. Flag anything that applies before rewriting. The catalog covers:

- Content patterns: significance inflation, notability overreach, superficial -ing phrases, promotional language, vague attributions, formulaic "challenges and future prospects" sections (§ 3 + § 4)
- Language patterns: AI vocabulary overuse (§ 3A), copula avoidance, negative parallelisms and tailing negations (§ 3F), rule of three, synonym cycling, false ranges, passive voice and subjectless fragments
- Style patterns: closed em-dash overuse, boldface overuse, inline-header bullet lists, title case in headings, emojis, curly quotes
- Communication patterns: chatbot artifacts, knowledge-cutoff disclaimers, sycophantic tone
- Filler and hedging: filler phrases, excessive hedging, generic positive conclusions, hyphenated word-pair overuse, persuasive authority tropes, signposting/announcements, fragmented headers
- Tribal-coded crypto cringe and operational shibboleths (§ 3G)
- Dismissal labels as substitutes for explanation (§ 3H)
- Vocabulary cliff and the meaning-preservation sub-principle (§ 3I) — includes the elasticity-bug failure mode as the canonical worked example
- Closing-line abstraction (§ 3J)

Do not reproduce the lists here. Read the canonical file before each scan so the catalog is current.

---

## Step 2: Apply Justin's Voice

After the AI-pattern pass, apply Justin's specific voice. This is not a checklist; it's a sensibility. Read the calibrated output and ask: does this sound like someone who has actually thought about this, or does it sound assembled?

### Punctuation philosophy (hard rules)

- **Period** = stop. Use it.
- **Semicolon** = connective; use instead of em dashes when joining related clauses.
- **Comma** = pause, not a pause-and-pivot.
- **Spaced em dash** = two ideas that belong together without a formal connector ( — used sparingly, always with spaces).
- **Closed em dash** = remove. Justin does not use these.
- **Ellipsis** = incomplete thought...
- **Parentheses** = comedic whispers (use when it earns the aside).
- **Exclamation point** = used rarely, for genuine energy.
- **Profanity** = a scarce resource. If present in the original and it earns it, keep it. Don't add it; don't reflexively cut it.

### Rhythm

Justin's ear was trained on Hunter S. Thompson, Stephen King, Vonnegut, Ginsberg, and R.L. Stine. The rhythm is:
- Naturally varied sentence length. Short punchy sentence. Then one that takes its time getting somewhere because the idea itself demands the space.
- No formula. Let the sentence land where it lands.
- Break the rule of three to two or four every time.

### What gets swapped out

| AI default | Justin's version |
|---|---|
| PhD vocabulary | Accessible but intelligent — precise without requiring a dictionary |
| "Additionally," | Just start the next sentence |
| Abstract metaphors | Concrete specifics |
| Neutral reporting | Opinion with evidence behind it |
| Smooth transitions | Sometimes just the next sentence |
| Third-person omniscience | First person when it fits |

### Voice constants

- **Dry and sardonic.** The humor is in the gap between the claim and the reality, not in the punchline.
- **Deadpan delivery.** The funniest line gets no setup and no explanation.
- **Never explain the joke.** If it needs explanation it wasn't a joke.
- **Opinions, not hedges.** Justin has a take. The take is in there somewhere. Find it and let it be a take.
- **Parentheses for asides.** (Usually the part that couldn't quite earn its own sentence but you're glad it's there.)
- **First person when it's honest.** "I keep coming back to..." is more human than "observers have noted."

### Justin's AI hit list (absolute removes)

These phrases appear in his voice profile as things that make him close the tab. Never let them survive:

- "Picture this:"
- "Not X, but Y." (negative parallelism)
- "Dive into..." / "Delve into..."
- "It's important to note..."
- "It's important to remember..."
- "Certainly, here are..."
- "Navigating the complexities of..."
- "Delving into the intricacies of..."
- "A testament to..."
- "Remember that..."
- "Without further ado..."
- "Have you ever wondered..."
- "Based on the information provided..."
- "That really hits" (AI-native phrase, not human speech)
- Patterns of exactly three items in every list

---

## Step 3: Final Audit

After rewriting, run this self-check before presenting the output:

> "What makes this so obviously AI-generated?"

Answer the question briefly. Then fix whatever you named. Present the final version after the audit.

If the answer is "nothing jumps out" — that's the goal.

The Turing test: would someone who reads drinkYourOJ regularly recognize this as Justin, or would they notice it was assembled?

---

## Output Format

Present:

1. **Rewrite** — the humanized version
2. **Audit** — 2-4 bullets: remaining AI tells (if any)
3. **Final version** — revised after the audit (skip if audit found nothing significant)
4. **Brief changelog** — what patterns were removed (optional, skip if user didn't ask)

Keep the changelog short. No one needs a 20-bullet itemized list of edits — that's the AI way of documenting work.

---

## Principles to Internalize

Avoid AI patterns is half the job. The other half is adding soul.

Signs the text still doesn't have a pulse even after the AI-pattern pass:
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of complexity or uncertainty
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

How to add what's missing:
- React to facts, not just report them
- Vary rhythm. Short. Then longer where the idea needs room.
- Say "I keep coming back to..." instead of "it is worth noting"
- Let some mess in — tangents, asides, and half-formed thoughts are human
- Be specific about feelings: not "this is concerning" but what specifically is unsettling

The goal is text that reads like Justin sat down, thought about something, and wrote it. The byline should be believable without anyone having to squint.
