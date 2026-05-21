# Thumbnail Headline Patterns

Source of truth for the headline drafting step (Gate 2) in `tcn-youtube-thumbnail`. The skill reads this file at drafting time to surface 3 candidate thumbnail headlines that pass the acceptance criteria in SKILL.md §9.2.

Edit this file directly when banned-word lists, structural patterns, or anti-pattern observations need to evolve. No skill-code changes required.

## Voice anchors

Thumbnail headlines extend TCN's existing voice corpus:
- Inherits from `justin-hearn-voice-profile.md` (drinkYourOJ voice).
- Inherits from the anti-AI-writing-style rules used in `tcn-text-humanizer`.
- Constrained to the Marcus-reader visiting-friends register — talking to a smart friend, not shouting at a crowd.
- Sentence case. No screaming.
- Declarative or genuine curiosity-gap. Never clickbait-shaped.
- Sardonic and specific. Specificity = trust.

## Word-count discipline

- 3–6 words inclusive. Hyphenated compounds count as one word. Contractions count as one word. Numbers count as one word regardless of digit count.
- 3 words: punchy, works when you have a strong anchor noun.
- 4–5 words: the sweet spot for most dispatches.
- 6 words: only when every word earns its place.

## Banned hype adjectives (case-insensitive)

Any candidate containing any of these is rejected:

- SHOCKING
- AMAZING
- INSANE
- EXPOSED
- REVEALED
- UNBELIEVABLE
- MASSIVE
- ULTIMATE
- EPIC
- INCREDIBLE
- MIND-BLOWING
- GAME-CHANGING

Add new entries as future dispatches surface them. Keep the list explicit — no fuzzy matching.

## Banned clickbait templates

Any candidate matching these shapes is rejected:

- "This One Trick…" / "This Simple Trick…"
- "What They Don't Want You To Know"
- "You Won't Believe…"
- "Here's Why…" (when leading)
- "The Truth About…" (generic — fine when specific)
- "Doctors Hate This…" / any "[Group] Hate This…"
- "Number N Will Shock You"

## Anti-AI-tell tokens

Reject any candidate containing:

- em-dashes (—)
- "delve" / "delving"
- "tapestry"
- "navigate the landscape" / "the landscape of"
- "in the realm of"
- "it's worth noting"
- Any token flagged by the `tcn-text-humanizer` skill's tell list (cross-reference, don't duplicate)

## Concrete-specific requirement

If the cold-open contains any of:
- A number ($499, 11%, 23 cities)
- A place name (Helium, Austin, Reykjavík)
- A dollar amount
- A year (2024, 1996)
- A proper noun (Nova Labs, FAA, HIP-143)

…then at least ONE of the three candidates MUST use it. The other two candidates can be more abstract for variety. The point is to anchor the headline in a fact-check-able specific so the curiosity gap is earned, not invented.

## Proven structural patterns

Each pattern with worked example(s).

### Concrete Anchor + Twist

Lead with a specific named thing, then a twist that creates the curiosity gap.

- "You Own the Hotspot" — dispatch-004. Anchor: the thing the viewer paid for. Twist: implied "but…"
- "Nova Labs Owns It" — dispatch-004 alt. Anchor: named entity. Twist: contradicts what the viewer just spent $499 expecting.

### Implied Stakes

State the fact; let the stakes hang in the air. No exclamation needed.

- "The FAA Already Knows"
- "Reykjavík Tried This First"

### Direct Address

Speak to the viewer. "You" or "Your" anchors the headline.

- "Why You're Funding This"
- "Your Hotspot, Their Token"

### Specific Contradiction

Two facts in tension. Concrete on both sides.

- "$499 to Mine WiFi"
- "Public Money, Private Profit"

### Bare-Noun Provocation

One or two nouns. Pure provocation through the noun choice.

- "The Hotspot Tax"
- "The Helium Receipt"
- "The Quiet Default"

## Anti-pattern gallery

Examples of candidates that violate criteria, with the reason. Educational, not exhaustive.

- "SHOCKING Truth About Helium" — all-caps + banned word.
- "You Won't Believe What Nova Labs Did" — banned clickbait template + 8 words.
- "The Surprisingly Profitable Tapestry of Hotspots" — anti-AI-tell ("tapestry") + over-word-count + abstract.
- "An In-Depth Analysis of the Helium Network's Tokenomics" — 9 words, abstract, AI-tell shape, no curiosity gap.
- "Helium" — under word-count, no anchor.
- "Why Helium Matters" — generic, no curiosity gap, could describe any episode.

## Worked example walkthroughs

### Dispatch-004 — "You Own the Hotspot"

**Cold-open candidate:** "I bought a $499 hotspot to mine WiFi tokens. Nova Labs owns what it earns."

**3 drafted candidates with rationales:**

1. *"You Own the Hotspot"* — Direct Address + Concrete Anchor + Twist. Anchors "you" + the hardware noun. The "but…" hangs implied.
2. *"$499 to Mine WiFi"* — Specific Contradiction. Anchors dollar amount. Tension: spending money to mine something that should be free.
3. *"Nova Labs Owns It"* — Implied Stakes + named entity. The "it" is load-bearing — viewer has to click to find out what.

**Picked:** Candidate 1 — strongest curiosity gap, direct-address pulls viewer in, the implied twist is the gap.

(Add a second worked example after the second dispatch is produced. Until then, the dispatch-004 walkthrough alone is sufficient.)

## How the skill uses this file

At drafting time (process step 6, SKILL.md §9), the skill:

1. Loads this file's contents into its drafting context.
2. Extracts the cold-open candidate and dispatch concept.
3. Drafts 3 candidates following the proven patterns, with the concrete-specific requirement applied if the cold-open supports it.
4. Filters candidates against the banned-word, banned-template, and anti-AI-tell lists.
5. Re-drafts any failing slot up to 2 additional attempts.
6. Surfaces the passing candidates with one-line rationales per the Gate 2 display format.
