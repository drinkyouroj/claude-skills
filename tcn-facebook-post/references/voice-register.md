# FB-Explainer Voice Register — Reference

The voice doc for `tcn-facebook-post`. Plain-English, warm, image-forward — calibrated for a Facebook audience scrolling between kitten pictures.

## Why FB needs its own register

Justin's Substack voice (dry, sardonic, dense, fingerprinted with closed em dashes and copulative avoidance) reads as trying-too-hard on Facebook. The X voice (compressed, edge-forward) reads as inscrutable to FB readers who don't have the analytical context. LinkedIn voice (professional, citation-heavy) reads as corporate.

FB-Explainer is a separate register. It carries Justin's instincts (which framings to surface, which AI tells to avoid) but in a voice that a non-political-junkie reader can absorb between scrolls.

## The three dials

### Warmth: high

A friend posting a thought, not an analyst publishing a take. Warmth-markers like "look," "honestly," "the thing is" are **fine on FB, banned on Substack**. Use sparingly — one per post max.

### Density: very low

One idea per post. No nested clauses. No two-part claims. If a sentence has a comma followed by another claim, it's probably too dense for FB.

### Edge: scaled by purpose

- **Awareness / Engagement:** near-zero edge. Observational. The smirk stays internal.
- **Soft funnel / Flagship CTA:** slight dry authority — "we wrote about this for a reason" — but never sardonic. No "of course," no "naturally," no "predictably."

## What survives from `workspace/core/anti-ai-writing-style.md` (hard-applies)

These rules apply in full to every FB post, regardless of length or purpose:

- **Banned-vocab list (§ 3A)** — *delve*, *navigate*, *landscape*, *tapestry*, *underscores*, *highlights*, *unpacks*, all the AI tells. Always banned.
- **Negative parallelisms (§ 3F)** — "not X, but Y" constructions banned.
- **Vocabulary cliff (§ 3I)** — FB is the **steepest cliff** in the TCN stack. Always gloss every term that requires beat-specific context. No unglossed acronyms. "CPI" becomes "the inflation report"; "the Fed" stays standalone but never appears alongside an unglossed "FOMC."
- **Closing-line abstraction (§ 3J)** — no grand wrap-ups. End on a fact or a question, not a Big Truth.

## What relaxes (FB-only)

These three Substack-voice rules are deliberately loosened for FB:

- **Closed em dashes** — Justin's Substack fingerprint. Drop entirely at caption length (≤30 words; they read as trying-too-hard in 1-2 sentences). At paragraph length, allow one maximum. Never two in the same post.
- **Copulative avoidance** — Substack voice avoids "is" verbs. FB allows them; plain English needs "is" to work. "X is bigger than Y" is fine on FB; on Substack it would be rewritten as "X exceeds Y."
- **Sardonic dismissal moves** — Substack voice tolerates "of course," "naturally," "predictably." FB doesn't. The smirk stays internal.

## Hard rule: no vague placeholder verbs

Phrases like "hit a number," "saw movement," "raised concerns," "made waves," "had a moment" are AI-filler tells. Plain English exposes them harder than analytical registers because the reader has no clausal complexity to fill in the missing fact.

**If a real specific fact (number, name, date, direct quote) isn't at hand, change the framing to one that doesn't need it.** Never paper over with abstract verbs.

This is a hard-fail in the quality bar — a post containing one of these phrases fails review even if everything else is correct.

## The Marcus check, FB-edition

The Substack stack writes for Marcus (the engaged-but-time-pressed reader who follows the beats). FB writes for a reader with the same intelligence but **zero context** on the beats Justin covers daily.

If a sentence would make that reader stop scrolling and squint, it's too dense. Rewrite.

## Length-bounded examples

### Caption (Awareness, Tuesday)

> "Interest payments on the federal debt are now bigger than the entire defense budget. Both crossed $880 billion last year. Most coverage isn't touching this."

Three sentences. 28 words. Specific numbers. No fingerprints. No CTA. Image: AI-generated split-frame showing a Treasury bond and a Pentagon-style scene.

### Caption (Engagement, Tuesday)

> "Honest question for the room: when you hear 'inflation cooling,' do you actually feel it at the grocery store? Tell me where you're at."

Two sentences. 24 words. Warmth-marker ("honest question"). Active second person. Comment-bait by design. Image: AI-generated grocery receipt closeup.

### Paragraph (Soft funnel, Thursday)

> "Writing about energy demand for Friday — the thing that keeps surprising me is how much of it comes from data centers nobody's quoting. One small Virginia county is now using more power than entire states did ten years ago. Full piece drops Friday morning."

Three sentences. 56 words. One closed em dash (allowed at paragraph length). Plain "is" verb. Specific anchor (Virginia county). Soft link forward. Image: Substack hero from Friday's draft.

### Paragraph (Flagship CTA, Friday)

> "The inflation number everyone's talking about is actually the smaller story. The bigger one is buried in the same release: services inflation isn't slowing, and that's where most of your monthly budget lives. Today's piece walks through what that means for the next six months. Full piece: [substack-url]"

Four sentences. 60 words. Slight authority. Specific anchor (services inflation). Hard link at end. Image: Friday's published Substack hero.

## Voice fallback

If `workspace/core/anti-ai-writing-style.md` is missing from the active project:

1. Flag explicitly: "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip vocabulary substitution, banned-word audit, and closing-line check.
3. Do NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions.
4. Continue with structural work (option generation, shape selection, image guidance, shelf-life labeling).
5. The daily plan's `status:` field stays `draft` rather than advancing to `voice-checked`.
