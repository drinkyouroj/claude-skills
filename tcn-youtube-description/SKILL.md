---
name: tcn-youtube-description
description: "Step 4 of the Civic Node YouTube production workflow — produces a paste-ready YouTube description for a TCN dispatch with above-the-fold hook, dispatch summary, Substack article CTA, viewer-rewritten chapter timestamps, channel link block (Substack + Bluesky), and dispatch-specific hashtags. Trailer-funnel anatomy that mines the narration's 'cuts from the article' field to drive Substack click-through. Dual-input: pre-record reads youtube-narration.md (chapter timestamps estimated from slide pacing); post-record reads .srt/.txt transcript (exact timestamps win if both present). Auto-derives the Substack article URL from the workspace slug with a confirmation gate. Invoke when the user says 'write the description', 'youtube description for this dispatch', 'make the description', 'description for №NNN', 'generate description', 'what should go in the youtube description', or has approved a youtube-narration.md / youtube-title.md / youtube-thumbnail.md and wants the description. Does NOT generate the article, narration, slideshow, title, or thumbnail (those are separate skills), and does NOT upload the description to YouTube Studio (user pastes manually)."
---

# The Civic Node — YouTube Description (Step 4 of the YouTube Production Workflow)

## What This Skill Does

Produces a single paste-ready YouTube description for a TCN dispatch, structured as a trailer-funnel that mines the narration's *Cuts from the article* field to drive Substack click-through rather than retention on YouTube alone. The description has 11 ordered blocks: above-fold hook (≤200 chars), blank, 3-5 sentence summary, blank, single-sentence article CTA + bare URL, blank, chapter list (viewer-rewritten labels, MM:SS timestamps), blank, channel link block (Substack + Bluesky boilerplate), blank, and 5-7 hashtags (3-5 dispatch-specific + 2 channel-evergreen). The skill is dual-input — pre-record reads `youtube-narration.md`; post-record reads a `.srt` or `.txt` transcript (transcript wins if both present). The above-fold hook runs an orthogonal rhetorical mechanism to the paired title and thumbnail headlines: if `youtube-title.md` and `youtube-thumbnail.md` are present, the skill enforces three different mechanisms across the three YouTube surfaces.

---

## Voice & vocabulary canonical source

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule, the banned-words list, dead phrases / transitions / engagement bait / hype language, the negative-parallelism rule, tribal-coded crypto cringe and operational shibboleths, the dismissal-label rule, the vocabulary cliff rules including the meaning-preservation sub-principle, the closing-line abstraction rule, the broader AI writing patterns to avoid, and the anti-overfitting guide.

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on a copy embedded in this spec.

**Fallback when the canonical file is missing.** If `workspace/core/anti-ai-writing-style.md` is not present in the current project, this skill must:
1. Flag explicitly to the user — "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip all voice-related work — no AI-hit-list cross-check on candidate description copy.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still derive the article URL, still compute chapter timestamps from the narration or transcript, still assemble the link block + hashtags, still apply the orthogonal-mechanism rule against paired artifacts. Flag "voice rules pass" as not enforced in the artifact metadata.

---

## Position in the YouTube Workflow

```
Article (tcn-article-builder)
    ↓
tcn-youtube-narration   [Step 1]
    ↓
tcn-youtube-slideshow   [Step 2]
    ↓
┌─── RECORDING ───┐
    ↓
tcn-youtube-title       [Step 3]
tcn-youtube-description [Step 4 — this skill]
tcn-youtube-thumbnail   [Step 5]
```

Recording is the cleavage point between upstream skills (which consume article prose) and downstream packaging skills (which consume the recorded transcript). This skill, like `tcn-youtube-title` and `tcn-youtube-thumbnail`, can run **pre- or post-record**: pre-record against the narration for early concepting and metadata-prep alongside the title and thumbnail; post-record against the recorded transcript to mine exact chapter timestamps and capture any improv'd phrases. Recommended order: run pre-record alongside title and thumbnail for paired concepting, re-run post-record for final chapter accuracy.

---

## Inputs and Outputs

### Required input

- **Path to a narration file (`youtube-narration.md`) OR a recorded transcript** (`.srt` or `.txt`). The skill auto-detects in the supplied directory: transcript wins if both present. If the user pastes content directly, save to a temp file and proceed. Halt with an explicit message and example path if neither is found.

### Strongly recommended inputs

- **`youtube-title.md`** in the same directory — extract the picked title and the mechanism name from the `**Pattern:**` field. Used for orthogonal-hook enforcement: the description hook must run a different mechanism than the picked title. If missing, soft warn ("orthogonal-mechanism enforcement degraded — description hook may overlap with title") and proceed.
- **`youtube-thumbnail.md`** in the same directory — extract the chosen headline and its mechanism. Same orthogonality enforcement. Same soft-warn fallback.

### Optional inputs

- **Final article draft** (`10-final.md` or slug-named variant) — used silently to mine concrete anchors for the summary block. Skipped if absent.
- **Custom Substack URL override** — bypasses URL auto-derivation.
- **Custom Bluesky URL** — defaults to `https://bsky.app/profile/thecivicnode.bsky.social`, overrideable.
- **Steering** — free-text guidance like "punchier above-fold", "more chapter granularity", "swap the article tease line".
- **Override description** — user pastes their own description; skill skips drafting and goes straight to the final gate with validation pass only.

### Primary output artifact

- **File:** `workspace/drafts/<slug>/youtube-description.md`
- **Structure:**

````markdown
# YouTube description — TCN Dispatch №NNN

**Generated:** YYYY-MM-DD
**Source:** narration (timestamps estimated) | transcript
**Article URL:** <derived or overridden URL>
**Paired title:** "<picked title from youtube-title.md, or 'no title artifact found'>"
**Paired title mechanism:** <pattern name, or 'unknown'>
**Paired thumbnail headline:** "<chosen headline from youtube-thumbnail.md, or 'no thumbnail artifact found'>"
**Paired thumbnail mechanism:** <pattern name, or 'unknown'>
**Description hook mechanism:** <mechanism name — must be ∉ {paired title mechanism, paired thumbnail mechanism} when both paired artifacts are present>

---

## Paste this into YouTube

<the full description copy, exactly as it will be pasted into the YouTube Studio description field — no Markdown formatting, no bracketed placeholders, no escape sequences>

---

## Block-level breakdown (for reference)

**Above-fold hook (block 1):** <copy>
**Summary (block 3):** <copy>
**Article CTA (block 5):** <copy>
**Chapters (block 7):** <list>
**Channel link block (block 9):** <copy>
**Hashtags (block 11):** <copy>

**Total length:** NNNN chars (above-fold prefix NNN chars)
````

### Gate prompt presented to user

> YouTube description draft complete (~NNNN chars, above-fold prefix NNN chars). Approve, redirect (e.g., 'punchier above-fold', 'swap the hook mechanism', 'more chapter granularity', 'replace #DePIN with #Web3'), or cancel?

**Stop after presenting the draft.** Wait for user approval or redirect before doing anything else.

---

## Run Timing

The skill ships dual-input. Same output shape in both modes — only the timestamp source and freshness differ.

| Concern | Pre-record (narration) | Post-record (transcript) |
|---|---|---|
| Activation | Only `youtube-narration.md` found | `.srt` or `.txt` transcript found (wins over narration) |
| Source label in artifact | `**Source:** narration (timestamps estimated)` | `**Source:** transcript` |
| Chapter timestamps | Estimated from slide word count ÷ 140 wpm, accumulated | Mined from `.srt` via fuzzy match on each slide's opener |
| Hook drafting | Drafted from narration thesis + paired title/thumbnail mechanisms | Drafted from transcript thesis-equivalent passage + paired mechanisms |
| Anchor mining | Narration body + article draft (if present) | Transcript body + article draft (if present) |
| Workflow position | Run alongside Step 3 (title) and Step 5 (thumbnail) for paired pre-record concepting | Re-run for final chapter accuracy |

---

## Description Anatomy

### Block ordering (top to bottom)

```
┌─────────────────────────────────────────────────────────────┐
│  ABOVE THE FOLD (~200 chars — visible before "show more")   │
└─────────────────────────────────────────────────────────────┘

[1] HOOK PUNCH (2-3 short lines, 8/10 register)

┌─────────────────────────────────────────────────────────────┐
│  BELOW THE FOLD                                             │
└─────────────────────────────────────────────────────────────┘

[2] BLANK LINE

[3] DISPATCH SUMMARY (3-5 sentences, 8/10 register)

[4] BLANK LINE

[5] ARTICLE CTA (single sentence + bare URL on next line)

[6] BLANK LINE

[7] CHAPTERS HEADER + LIST
    -- CHAPTERS --
    0:00  <viewer-rewritten chapter label>
    ...

[8] BLANK LINE

[9] CHANNEL LINK BLOCK
    -- THE CIVIC NODE --
    Weekly. No hype.

    Substack:  https://drinkyouroj.substack.com
    Bluesky:   https://bsky.app/profile/thecivicnode.bsky.social

[10] BLANK LINE

[11] HASHTAGS (3-5 dispatch-specific + 2 channel-evergreen, single line, space-separated)
```

### Block 1 — Hook punch (above the fold)

- **2-3 short lines.** Total length ≤200 chars including line breaks (mobile above-fold budget).
- **8/10 register** — punchier than the narration's 7/10. Sentence case. No em-dashes. No exclamation points. Period stops as default landing.
- **Rewritten fresh from the dispatch concept** — NOT a verbatim restatement of the narration's cold-open or the transcript's first 30 seconds. The viewer who clicks because of this hook should get a different first 15 seconds than what they expected.
- **Mechanism orthogonality** — runs a different mechanism than the picked title and the chosen thumbnail headline. Mechanism taxonomy inherited from `../tcn-youtube-title/references/title-patterns.md`:
  - Authority-Asymmetry
  - Specific Contradiction
  - Hidden Revenue / Hidden Move
  - Personal-Implication
  - **Audit-Standard** (description-only mechanism — see `references/description-anatomy.md`)
  - Completion-Pairing is **banned** for description hook (description is not a visual surface; cannot completion-pair with the thumbnail).
- **Anti-AI-tells enforced** — banned word list inherited from `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md`. Same banned-content gate as titles and thumbnails.

### Block 3 — Dispatch summary

- **3-5 sentences.** Target 400-700 chars. Below the fold.
- **8/10 register.** Voice file enforced.
- **Mines the narration's *Cuts from the article* field as raw material** — names what the video did NOT cover. This is the funnel mechanic that converts viewers to readers.
- **Numerals, not words.** Description copy is scanned visually; "385,000 hotspots" reads faster than "three hundred eighty-five thousand hotspots." (Opposite of the spoken-word rule in the narration skill.)
- **Proper-noun density** — name 3-5 indexable nouns (companies, people, votes, places, technologies) for SEO. TCN voice already does this naturally; the skill should not strain to add them.
- Anti-AI-tells enforced.

### Block 5 — Article CTA

- **Single sentence** introducing the article URL, followed by the bare URL on the next line.
- Example: `→ Read the full piece on Substack:` \n `https://drinkyouroj.substack.com/p/<slug>`
- The `→` arrow is acceptable (Unicode arrow, not em-dash, not asterisk-marketing-bait). `>` or `>>` are also acceptable; the skill picks one and stays consistent across dispatches.
- **Bare URLs only.** YouTube descriptions do not render markdown; `[text](url)` is shown literally.

### Block 7 — Chapters

- **Format:** YouTube auto-detect format — `MM:SS  Label` per line, single newlines between chapters.
- **First chapter ALWAYS `0:00`** — YouTube refuses to auto-detect chapters otherwise.
- **At least 3 chapters total** — YouTube's auto-detect minimum.
- **Maximum 10 chapters.** Beyond that the chapter ribbon becomes unscannable.
- **One chapter per narration slide by default.** Combined narration slides (e.g., "THE FRAME + STAKES, Author's Debug") produce ONE chapter with a single rewritten label.
- **Viewer-rewritten labels** — producer-facing narration labels rewritten into noun phrases. Distill each slide's actual content into a 4-8 word noun phrase at 8/10 register.
- **End slide always included as final chapter** — gives skipping viewers a direct route to the channel CTA.
- **Spacing:** two spaces between timestamp and label for human readability. YouTube collapses to single-space at render time.

### Chapter timestamp computation

**Post-record (transcript present):**

1. Parse the `.srt` or `.txt` transcript.
2. For each narration slide, find the timestamp of the first sentence of that slide's content in the transcript via fuzzy match on the first 4-6 words of each slide's opener.
3. Use the matched timestamp, rounded down to whole seconds.
4. If a slide cannot be located (likely cause: heavy improv during recording), surface a one-line warning in metadata and fall back to estimated-from-narration timestamp for that slide only.

**Pre-record (narration only):**

1. Count words per narration slide.
2. Use 140 wpm as the TCN-natural pace (matches the narration skill's standard).
3. Accumulate runtime slide-by-slide; emit `MM:SS` per slide start.
4. Mark the artifact metadata block's `**Source:**` field as `narration (timestamps estimated)`.

### Block 9 — Channel link block

Constant boilerplate across every dispatch:

```
-- THE CIVIC NODE --
Weekly. No hype.

Substack:  https://drinkyouroj.substack.com
Bluesky:   https://bsky.app/profile/thecivicnode.bsky.social
```

Skill writes this verbatim. User-supplied Substack and Bluesky overrides replace the defaults.

### Block 11 — Hashtags

- **3-5 dispatch-specific** mined from the narration + article: prefer proper-noun anchors (companies, technologies, votes, places, named events) over abstract categories.
- **2 channel-evergreen** constant across every dispatch: `#TheCivicNode #drinkYourOJ`.
- **Sentence case enforced** — `#NovaLabs`, `#HIP143`, not `#NOVALABS` or `#novalabs`. PascalCase / camelCase for multi-word, no spaces, no punctuation (YouTube hashtags only honor `[A-Za-z0-9_]`).
- **Single line, space-separated.** YouTube shows only the first 3 in description order as clickable category tags above the title; put the strongest dispatch-specific tag first.
- **Total count 5-7** — beyond ~7 YouTube treats as spam-coded.
- Skill silently re-rolls if count falls outside 5-7.

### Dividers

- All section dividers use double-hyphen wrappers: `-- CHAPTERS --`, `-- THE CIVIC NODE --`.
- Em-dashes are banned (anti-AI-tell, inherited rule).
- Hyphenated form scans clean in YouTube's monospace-adjacent description renderer.

### Length budgets (paste-ready output only — excludes metadata block)

| Block | Char budget | Notes |
|---|---|---|
| [1] Hook punch | ≤200 chars (incl. line breaks) | Mobile above-fold |
| [3] Summary | 400-700 chars | 3-5 sentences |
| [5] Article CTA | ~100 chars + URL | One sentence + bare URL line |
| [7] Chapter list | varies (~200-500 chars depending on 5-10 chapters) | One line per chapter |
| [9] Link block | ~150 chars constant | Boilerplate |
| [11] Hashtags | ~100 chars | 5-7 tags |
| **Total** | **1,500-2,500 chars target** | YouTube cap is 5,000 |
