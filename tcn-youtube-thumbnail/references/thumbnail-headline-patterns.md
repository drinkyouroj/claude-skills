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
- **Symbols functioning as words count as one word each.** Load-bearing symbols (≠, +, ÷, ×, >, <, =, →) that stand in for a verb or relational operator count toward the word total. Purely decorative symbols (·, —, …) do not count, but are generally discouraged in thumbnail headlines and require the symbol to be doing actual rhetorical work to justify inclusion. See "Symbol headlines" below for which symbols survive thumbnail compression.
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

## Symbol headlines

Math and logic symbols can substitute for words to compress headlines further and signal "this is analysis." TCN's identity is "we read the receipts" — symbol notation is brand-coherent shorthand for that posture. Used carefully, a symbol in a headline doubles as a visual stop-element: the eye notices it before it reads it.

### When to use

- The symbol carries actual rhetorical weight (states a relationship, replaces a verb, anchors a comparison).
- Compressing to a symbol saves at least one word while preserving meaning.
- The dispatch's argument structure is a relationship between two named things (X is/isn't Y, X versus Y, X above/below Y).

### When not to use

- The symbol is decorative — it could be removed and the headline would still read the same.
- The headline already uses a number-as-word; adding a symbol on top reads as overloaded math.
- The dispatch is alarm-bell or emotional rather than analytical — symbols read as cold and dry, which can fight the wrong register.

### Symbols that survive thumbnail compression

These have weight-bearing strokes that hold up at YouTube mobile-feed scale (~240 px wide):

- `≠` — "is not / does not equal." Composite-time caveat: the diagonal slash must be 2× the cross-bar weight or it blurs into `=` and inverts the meaning. Spec the slash weight explicitly in the overlay spec.
- `+` — "and / plus / combined with." Survives compression cleanly.
- `÷` — "per / divided by." Slightly fragile but workable.
- `×` — "times / by." Reads cleanly at small sizes.
- `>` / `<` — "greater than / less than." Strong silhouettes.
- `→` — "leads to / becomes." Works as a directional connector.
- `=` — "equals / is." Works alone; pairs naturally with `≠` for series-style A/B thumbnails.

### Symbols to avoid

Thin or meaning-bearing strokes that blur out under compression:

- `≈` — the wavy lines lose definition; reads as `=` or noise.
- `≤` / `≥` — the underbar is too thin to survive thumbnail scale.
- `±` — the small vertical stroke disappears at compression.
- Any superscript or subscript (² ³ ₁ ₂) — too small to read.
- Any compound symbol made of three or more thin strokes.

### Worked example

Dispatch-004 used `≠` in the headline "Vibes ≠ Disclosure." The symbol replaces the word "aren't" (3 words → 3 words inclusive, but with maximum visual compression and a brand-coherent "we do math here" register). The composite-time directive specifies a heavy slash weight to survive mobile feed compression.

## Anti-pattern gallery

Examples of candidates that violate criteria, with the reason. Educational, not exhaustive.

- "SHOCKING Truth About Helium" — all-caps + banned word.
- "You Won't Believe What Nova Labs Did" — banned clickbait template + 8 words.
- "The Surprisingly Profitable Tapestry of Hotspots" — anti-AI-tell ("tapestry") + over-word-count + abstract.
- "An In-Depth Analysis of the Helium Network's Tokenomics" — 9 words, abstract, AI-tell shape, no curiosity gap.
- "Helium" — under word-count, no anchor.
- "Why Helium Matters" — generic, no curiosity gap, could describe any episode.

## Worked example walkthroughs

### Dispatch-004 — "You Own the Hotspot. Nova Labs Owns What It Earns."

**Cold-open** (from the narration's HOOK slide): McDonald's franchise FDD (200-page disclosure document, federally required) versus 385,000 Helium hotspot operators who got no equivalent disclosure. Punchline word: "Vibes."

**3 drafted candidates with rationales:**

1. *"Vibes ≠ Disclosure"* — Concrete Anchor + Twist + symbol headline. Anchors the cold-open's landing punchline ("Vibes") and contrasts it with the regulatory frame ("Disclosure") via the `≠` glyph. Sardonic understatement. 3 word-equivalents (≠ counts as one per the Symbol headlines section). The math notation signals "we read the receipts" — brand-coherent register before the viewer reads a word.
2. *"McDonald's Has a Receipt"* — Implied Stakes + Concrete Anchor. McDonald's is the cold-open's recognizable opening, universally legible. Twist: who *doesn't* have one? Curiosity-gap is the inversion. 4 words.
3. *"385,000 Bought Vibes"* — Concrete Anchor + Bare-Noun Provocation. Anchors the operator count from the narration's HOOK slide. The word "Vibes" does the rhetorical work. Maximally compressed at 3 words (the comma-separated number counts as one).

**Picked:** Candidate 1 — strongest visual stop-power, maximum compression, math notation as brand identity glyph. Composite-time caveat: the `≠` slash must be weighted heavily enough to survive mobile-feed compression (see Symbol headlines section).

(Add a second worked example after the second dispatch is produced.)

## How the skill uses this file

At drafting time (process step 6, SKILL.md §9), the skill:

1. Loads this file's contents into its drafting context.
2. Extracts the cold-open candidate and dispatch concept.
3. Drafts 3 candidates following the proven patterns, with the concrete-specific requirement applied if the cold-open supports it.
4. Filters candidates against the banned-word, banned-template, and anti-AI-tell lists.
5. Re-drafts any failing slot up to 2 additional attempts.
6. Surfaces the passing candidates with one-line rationales per the Gate 2 display format.
