# tcn-youtube-description — Design Spec

**Date:** 2026-05-21
**Status:** Approved for implementation planning
**Workflow position:** Step 4 of the Civic Node YouTube production workflow
**Sibling specs:** `2026-05-20-tcn-youtube-narration-design.md`, `2026-05-20-tcn-youtube-slideshow-design.md`, `2026-05-21-tcn-youtube-thumbnail-design.md`, plus the `tcn-youtube-title` skill (no design spec on file at time of writing; reference its `SKILL.md` directly)

---

## 1. Purpose

Produce a paste-ready YouTube description for a Civic Node Dispatch video. The description is engineered as the third surface of a three-surface YouTube package (thumbnail, title, description), each running a different rhetorical mechanism, all converging on one funnel goal: drive viewers to read the full article on Substack.

The description must:

1. Hook above the fold (~first 200 chars visible before YouTube's "show more" cut) in TCN voice.
2. Tease the article's twist with a 3-5 sentence summary that mines the narration's *Cuts from the article* field.
3. Surface the Substack article URL explicitly, with a single-sentence CTA, before chapters.
4. Provide YouTube-auto-detect-format chapter timestamps (mined from a recorded transcript when present, estimated from narration WPM math otherwise).
5. Carry a constant channel link block (Substack subscribe URL + Bluesky profile URL).
6. Carry 3-5 dispatch-specific hashtags + 2 channel-evergreen hashtags, sentence-case, single line.

The skill produces a single canonical draft, presented at one final gate (approve / redirect / cancel).

---

## 2. Position in the YouTube workflow

```
Article (tcn-article-builder)
    ↓
tcn-youtube-narration         [Step 1, built]
    ↓
tcn-youtube-slideshow         [Step 2, built]
    ↓
┌─── RECORDING ───┐
    ↓
tcn-youtube-title             [Step 3, built]
tcn-youtube-description       [Step 4 — this skill]
tcn-youtube-thumbnail         [Step 5, built]
```

Like `tcn-youtube-title` and `tcn-youtube-thumbnail`, this skill is **dual-input**: it runs pre-record from `youtube-narration.md` for early concepting alongside the title and thumbnail, or post-record from a recorded transcript (`.srt` or `.txt`) for finalization. Transcript wins if both are present in the dispatch directory. The shared rationale is that recording often improvises lines that land harder than the script — those should be available to all three packaging skills.

Recommended sequencing:

- **Pre-record:** run alongside title and thumbnail for paired metadata concepting. Description's above-fold hook reads the paired title + thumbnail mechanisms (from their respective artifact metadata blocks) to enforce orthogonality.
- **Post-record:** re-run after recording to mine real timestamps for chapter markers and capture any improv'd phrases that landed.

---

## 3. Inputs and outputs

### Required input

- **Path to a narration file** (`youtube-narration.md`) **OR** a recorded transcript (`.srt` or `.txt`). The skill auto-detects in the supplied directory: transcript wins if both present. Halt with an explicit message and example path if neither is found.

### Strongly recommended inputs

- **`youtube-title.md`** in the same directory — read the picked title (for above-fold continuity: the description hook must not restate the title verbatim) and the metadata block's `**Pattern:**` field (records which mechanism the picked title runs, used to enforce the orthogonal-mechanism rule for the description hook).
- **`youtube-thumbnail.md`** in the same directory — read the chosen in-image headline and its mechanism, same orthogonality enforcement.

If either is missing: soft-warn ("orthogonal-mechanism enforcement degraded — description hook may overlap with title or thumbnail"). Proceed; note in the artifact metadata block.

### Optional inputs

- **Final article draft** (`10-final.md` or slug-named variant) — read silently if present to mine concrete anchors (numbers, dates, proper nouns) for the summary block. Skipped if absent; not required.
- **Custom Substack URL override** — if the user passes one at invocation, skip URL auto-derivation. Use the override directly.
- **Custom Bluesky URL** — defaults to `https://bsky.app/profile/thecivicnode.bsky.social`. Overrideable.
- **Steering** — free-text guidance applied at draft time and at the final gate redirect (e.g., "punchier above-fold", "more chapter granularity", "swap the article tease line", "lean on the McDonald's framing").
- **Override description** — user pastes their own description; skill skips drafting and goes straight to the final gate with a validation pass (anti-AI-tells, length budgets, hashtag count, link block present).

### Primary output artifact

- **File:** `workspace/drafts/<slug>/youtube-description.md`
- **Structure:**

```markdown
# YouTube description — TCN Dispatch №NNN

**Generated:** YYYY-MM-DD
**Source:** narration (timestamps estimated) | transcript
**Article URL:** <derived or overridden URL>
**Paired title:** "<picked title from youtube-title.md, or 'no title artifact found'>"
**Paired title mechanism:** <pattern name from title metadata, or 'unknown'>
**Paired thumbnail headline:** "<chosen headline from youtube-thumbnail.md, or 'no thumbnail artifact found'>"
**Paired thumbnail mechanism:** <pattern name from thumbnail metadata, or 'unknown'>
**Description hook mechanism:** <mechanism name — must be ∉ {paired title mechanism, paired thumbnail mechanism} when both paired artifacts are present>

---

## Paste this into YouTube

<the full description copy, exactly as it will be pasted into the YouTube Studio description field — no Markdown formatting, no bracketed placeholders, no escape sequences>

---

## Block-level breakdown (for reference)

**Above-fold hook (blocks 1):** <copy>
**Summary (block 3):** <copy>
**Article CTA (block 5):** <copy>
**Chapters (block 7):** <list>
**Channel link block (block 9):** <copy>
**Hashtags (block 11):** <copy>

**Total length:** NNNN chars (above-fold prefix NNN chars)
```

The block-level breakdown section persists for diagnostic and steering reference. The "Paste this into YouTube" section is the only block the user copies into YouTube Studio.

---

## 4. Description anatomy

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

- **2-3 short lines.** Total line length ≤200 chars including line breaks (YouTube's mobile above-fold budget; desktop is wider but mobile is the binding constraint).
- **8/10 register** — punchier than the narration's 7/10. Sentence case. No em-dashes. No exclamation points. Period-stops as default landing.
- **Rewritten fresh from the dispatch concept** — NOT a verbatim restatement of the narration's cold-open. The viewer who clicks because of this hook should get a *different* first 15 seconds than what they expected (creating "this is even better than the description suggested"). Different keywords, different rhetorical surface, same article concept.
- **Mechanism orthogonality** — runs a different mechanism than the picked title and the chosen thumbnail headline. Mechanism taxonomy is inherited from `../tcn-youtube-title/references/title-patterns.md`:
  - Authority-Asymmetry
  - Specific Contradiction
  - Hidden Revenue / Hidden Move
  - Completion-Pairing (with thumbnail) — banned for description hook (description is not a visual surface; cannot completion-pair)
  - Personal-Implication
  - Additional description-only mechanism: **Audit-Standard** (proposes a standard the subject failed; specific to TCN's editorial frame)
- **Anti-AI-tells enforced** — banned word list inherited from `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md`. The hook must pass the same banned-content gate as titles and thumbnails.

### Block 3 — Dispatch summary

- **3-5 sentences.** Target 400-700 chars. Always below the fold.
- **8/10 register.** Same voice file (`workspace/core/anti-ai-writing-style.md`) as all TCN skills.
- **Mines the narration's *Cuts from the article* field as raw material** — names what the video did NOT cover. This is the funnel mechanic that converts viewers to readers. The narration skill produces this field explicitly for this consumer (and `tcn-youtube-title` and `tcn-youtube-thumbnail`).
- **Numbers spoken aloud only in spoken-word contexts; here, write numerals.** Description copy is scanned visually; "385,000 hotspots" reads faster than "three hundred eighty-five thousand hotspots."
- **Proper-noun density** — name 3-5 indexable nouns (companies, people, votes, places, technologies) for SEO. TCN voice already does this naturally; the skill should not strain to add them.
- Anti-AI-tells enforced (same banned list).

### Block 5 — Article CTA

- **Single sentence** introducing the article URL, followed by the bare URL on the next line.
- Example: `→ Read the full piece on Substack:\nhttps://drinkyouroj.substack.com/p/<slug>`
- The `→` arrow is acceptable (Unicode arrow, not em-dash, not asterisk-marketing-bait). Other directional indicators (`>`, `>>`) are also acceptable; the skill picks one and stays consistent across dispatches.
- **Bare URLs only.** YouTube descriptions do not render markdown; `[text](url)` is shown literally. Bare URLs auto-link in the YouTube renderer.

### Block 7 — Chapters

- **Format:** YouTube's auto-detect format — `MM:SS  Label` per line, first chapter must be `0:00`, lines separated by single newlines.
- **First chapter ALWAYS `0:00`** — YouTube refuses to auto-detect chapters otherwise.
- **At least 3 chapters total** — YouTube's auto-detect minimum.
- **Maximum 10 chapters.** Beyond ~10 the chapter ribbon below the progress bar becomes unscannable.
- **One chapter per narration slide by default** — narration zone label maps deterministically to the chapter label (Hook / Thesis / The Receipt / The Twist / Tease / End all map). For combined narration slides like "THE FRAME + STAKES, Author's Debug," produce ONE chapter (using the rewritten label).
- **Viewer-rewritten labels** — producer-facing narration labels ("THE RECEIPT, Unit Economics", "THE FRAME + STAKES, Author's Debug") are rewritten into noun phrases viewers will scan. Mechanism: mine the slide's actual content, distill to a 4-8 word noun phrase, calibrate to 8/10 register (same as the rest of the description).
- **End slide always included as final chapter** — "Subscribe at drinkyouroj.substack.com" or near-equivalent. Gives skipping viewers a direct route to the channel CTA without scrubbing.
- **Spacing:** two spaces between timestamp and label in the artifact for human readability. YouTube collapses to single-space-or-tab at render time; no behavioral impact.

### Block 7 — Chapter timestamp computation

**Post-record (transcript present):**

1. Parse the `.srt` or `.txt` transcript.
2. For each narration slide, find the timestamp of the first sentence of that slide's content in the transcript (via fuzzy match on the first 4-6 words of each slide).
3. Use the matched timestamp, rounded down to whole seconds (YouTube does not honor sub-second precision in chapters).
4. If a slide cannot be located in the transcript (likely cause: heavy improv during recording), surface a one-line warning in the metadata block and fall back to estimated-from-narration timestamp for that slide only.

**Pre-record (narration only):**

1. Count words in each narration slide.
2. Use 140 wpm as the TCN-natural pace (matches the narration skill's standard).
3. Accumulate runtime slide-by-slide; emit `MM:SS` per slide start.
4. Mark the artifact metadata block's `**Source:**` field as `narration (timestamps estimated)`. The user knows to re-run post-record for final accuracy.

### Block 9 — Channel link block

Constant boilerplate across every dispatch:

```
-- THE CIVIC NODE --
Weekly. No hype.

Substack:  https://drinkyouroj.substack.com
Bluesky:   https://bsky.app/profile/thecivicnode.bsky.social
```

Skill writes this verbatim with the user-supplied Bluesky override if provided. Substack subscribe URL is also overrideable. The two-space alignment between `Substack:`/`Bluesky:` and the URLs is decorative — YouTube collapses it at render time.

### Block 11 — Hashtags

- **3-5 dispatch-specific** mined from the narration + article: prefer proper-noun anchors (companies, technologies, votes, places, named events) over abstract categories.
- **2 channel-evergreen** constant across every dispatch: `#TheCivicNode #drinkYourOJ`.
- **Sentence case enforced** — `#NovaLabs`, `#HIP143`, not `#NOVALABS` or `#novalabs`. PascalCase / camelCase for multi-word, no spaces, no punctuation (YouTube hashtags only honor `[A-Za-z0-9_]`).
- **Single line, space-separated** — YouTube parses the entire description for hashtags but only the first 3 in description order appear above the title as clickable category tags. Order matters: put the strongest dispatch-specific tag first.
- **Total count 5-7** — beyond ~7 YouTube's own guidelines treat as spam-coded and may suppress the description in search.
- Skill silently re-rolls if generated count falls outside 5-7.

### Dividers

- All section dividers use double-hyphen wrappers: `-- CHAPTERS --`, `-- THE CIVIC NODE --`.
- Em-dashes are banned (anti-AI-tell, inherited rule).
- The hyphenated form scans clean in YouTube's monospace-adjacent description renderer.

### Length budgets (paste-ready output only — excludes metadata block)

| Block | Char budget | Notes |
|---|---|---|
| [1] Hook punch | ≤200 chars total (incl. line breaks) | Mobile above-fold |
| [3] Summary | 400-700 chars | 3-5 sentences |
| [5] Article CTA | ~100 chars + URL | One sentence + bare URL line |
| [7] Chapter list | varies (~200-500 chars depending on 5-10 chapters) | One line per chapter |
| [9] Link block | ~150 chars constant | Boilerplate |
| [11] Hashtags | ~100 chars | 5-7 tags |
| **Total** | **1,500-2,500 chars target** | YouTube cap is 5,000; we run well below |

---

## 5. The process

### Step 1 — Auto-detect source

In the supplied dispatch directory, look for:

- `.srt` file (any name) — preferred transcript form
- `.txt` file (any name with "transcript" in filename) — fallback transcript form
- `youtube-narration.md` — narration source

**Transcript wins if both transcript and narration present.** If neither exists, halt with example path: `expected workspace/drafts/<slug>/youtube-narration.md or a .srt/.txt transcript in the same directory.`

### Step 2 — Read paired artifacts

In the same dispatch directory, look for:

- `youtube-title.md` — extract the picked title from the `## Picked title` section and the mechanism name from the `**Pattern:**` field.
- `youtube-thumbnail.md` — extract the `Chosen headline:` field and the chosen variant's mechanism.

If either missing: log soft warning, proceed without orthogonality enforcement, note in artifact metadata.

If artifacts present but malformed (missing the expected fields): same as missing — soft warn, proceed.

### Step 3 — Derive article URL

1. Extract the slug from the supplied directory name (e.g., `you-own-the-hotspot-nova-labs-owns-what-it-earns`).
2. Construct candidate URL: `https://drinkyouroj.substack.com/p/<slug>`.
3. Surface to user: `Detected article URL: <candidate URL>. Confirm or paste an override:`
4. If user confirms (empty response, "confirm", "yes"), use the candidate.
5. If user pastes a URL, use the override. Record in artifact metadata.
6. If slug fails sanity checks (>80 chars, contains `_`, contains uppercase, contains chars outside `[a-z0-9-]`), surface with a flag: `Derived URL doesn't match Substack slug conventions. Paste the correct URL:` and require an explicit override.

### Step 4 — Mine anchors

From the narration body (or transcript body, post-record) and the article draft (if present):

- Numbers and dollar amounts.
- Proper nouns (companies, people, technologies, votes, places).
- Years and dates.
- Quoted phrases (highest-confidence anchors).

Anchor pool feeds the summary (block 3) and hashtag selection (block 11). The above-fold hook uses anchors only when they fit the mechanism naturally — abstract hooks are also fine.

### Step 5 — Draft the above-fold hook (block 1)

Inputs:

- The dispatch concept (extracted from narration title block + thesis slide post-record, or from the transcript's thesis-equivalent passage if the cold-open analogy was abandoned during recording). Explicitly NOT from the narration's cold-open or the transcript's first 30 seconds — the hook is rewritten fresh, runs its own rhetorical move, and avoids restating what viewers heard in the spoken opener.
- The paired title mechanism (from `youtube-title.md` metadata).
- The paired thumbnail mechanism (from `youtube-thumbnail.md`).
- The anchor pool from step 4.
- Steering text from the user, if any.

Drafting:

1. Pick a mechanism from the taxonomy that is NOT used by the paired title or thumbnail.
2. Compose 2-3 short lines using the picked mechanism.
3. Validate:
   - Total length (with line breaks) ≤200 chars.
   - No banned content per `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md`.
   - No em-dashes. No exclamation points. Sentence case.
   - Not a verbatim restatement of the picked title or the thumbnail headline.
4. If validation fails: redraft up to 2 additional times. If still failing after 3 attempts total, surface the best-effort candidate with a one-line note about which criterion couldn't be satisfied.

### Step 6 — Draft the dispatch summary (block 3)

Inputs:

- The narration body (or transcript body).
- The narration's *Cuts from the article* field (the funnel raw material).
- The anchor pool from step 4.

Drafting:

1. Compose 3-5 sentences.
2. Front-load anchors and proper nouns (helps both viewer scanning and YouTube search indexing).
3. Reference what the video did NOT cover — that's the funnel mechanic.
4. End on a phrase that motivates clicking through to the article.
5. Validate: length 400-700 chars, anti-AI-tells pass, no em-dashes, no banned content.

### Step 7 — Build the chapter list (block 7)

Run the timestamp computation (post-record from transcript or pre-record from narration WPM math, per §4 block 7).

For each chapter, draft a viewer-facing label:

1. Read the narration slide's actual content (or the transcript segment for that timestamp).
2. Distill the segment's main idea into a 4-8 word noun phrase.
3. Calibrate to 8/10 register.
4. Validate: no banned content, no em-dashes, no exclamation points, sentence case.

Compose the chapter block as YouTube auto-detect format: `MM:SS  Label` per line, one chapter per line, first chapter `0:00`, last chapter is always the End-slide CTA.

### Step 8 — Assemble the channel link block (block 9)

Write the constant boilerplate. Substitute the user's Bluesky override and Substack subscribe URL override if supplied; otherwise use defaults.

### Step 9 — Generate hashtags (block 11)

1. From the anchor pool, pick 3-5 proper-noun hashtags. Prefer specific (`#HIP143`) over generic (`#Crypto`).
2. Append the 2 channel-evergreen tags: `#TheCivicNode #drinkYourOJ`.
3. Validate count is 5-7; sentence-case enforced (PascalCase / camelCase for multi-word).
4. Compose as a single line, space-separated, dispatch-specific tags first.

### Step 10 — Final gate

Present:

```
YouTube description draft complete (NNNN chars, above-fold prefix NNN chars).

[full paste-ready description]

Approve, redirect (e.g., 'punchier above-fold', 'swap the hook mechanism', 'more chapter granularity', 'add the August 2025 halving in summary', 'replace #DePIN with #Web3'), or cancel?
```

Wait for response. If override description was supplied at invocation, skip the drafting steps and go straight to validation + final gate.

Redirect handling:

- **Global steering** ("redo punchier", "more declarative throughout") → re-draft all blocks with the new steering applied.
- **Block-targeted steering** ("swap the hook", "rewrite chapter 4 label", "drop #DePIN") → re-draft only the affected block(s). Don't re-roll the rest.
- **URL override** ("use this URL instead") → swap the article URL block, regenerate metadata, no other changes.

### Step 11 — Write the artifact

Write `workspace/drafts/<slug>/youtube-description.md` with:

- Metadata block (source, article URL, paired artifacts and mechanisms, hook mechanism).
- The paste-ready description under `## Paste this into YouTube`.
- The block-level breakdown for reference.

Then surface a one-line confirmation: `Wrote youtube-description.md. Paste into YouTube Studio description field.`

---

## 6. Voice & shared references

### Voice file

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice, vocabulary, substitution, or AI-tells decision. Same canonical file used by `tcn-youtube-narration`, `tcn-youtube-title`, and `tcn-youtube-thumbnail`. The skill does not maintain a duplicate copy.

**Fallback when the canonical file is missing:** apply the same degraded-mode pattern used by sibling skills:

1. Flag to the user: "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip voice-aware work (anti-AI-tells cross-check, banned-vocabulary substitutions).
3. Do NOT fall back to generic register from training data — that risks shipping wrong substitutions (elasticity-bug failure mode documented in `tcn-headline`).
4. Continue with non-voice work: still derive URL, still compute chapter timestamps, still assemble link block + hashtags, still apply the orthogonal-mechanism rule against the paired artifacts. Flag the artifact's metadata block to indicate voice calibration was skipped.

### Shared reference libraries (read, not duplicated)

- `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` — banned hype adjectives, banned clickbait templates, anti-AI-tells. Read at drafting time for all banned-content checks in blocks [1] (hook), [3] (summary), and [7] (chapter labels).
- `../tcn-youtube-title/references/title-patterns.md` — mechanism taxonomy (Authority-Asymmetry / Specific Contradiction / Hidden Revenue / Completion-Pairing / Personal-Implication). Read at drafting time for hook mechanism selection. Description skill adds one description-only mechanism (Audit-Standard) directly in its own reference file.

### Skill-local reference

- `references/description-anatomy.md` — block-by-block specs (above-fold char budget math, chapter format rules, hashtag selection logic, link block boilerplate, divider conventions, hyphen-divider rule, the Audit-Standard mechanism definition). Living document. Read at drafting time for all anatomy-related decisions.

---

## 7. Failure modes

- **No narration and no transcript found** — halt with explicit message and example path. Do not attempt to compose from nothing.
- **Narration malformed** (missing title block, missing Script Notes footer, missing *Cuts from the article* field) — halt for missing title block (can't get dispatch number); soft-warn for missing *Cuts from the article* and proceed with degraded summary quality (summary will be tighter, less funnel-y, but still publishable).
- **Slug doesn't match Substack conventions** (>80 chars, underscores, uppercase, chars outside `[a-z0-9-]`) — surface the constructed URL with a flag and require explicit override.
- **`youtube-title.md` missing or malformed** — soft warn ("orthogonal-mechanism enforcement degraded"); proceed without the orthogonality rule for the hook.
- **`youtube-thumbnail.md` missing or malformed** — same soft warn, same degraded path.
- **Transcript present but `.srt` timestamps malformed** — fall back to narration-estimate mode for chapters and note in artifact metadata (`Source: narration (timestamps estimated; transcript parsing failed)`).
- **Transcript present but slide content can't be located via fuzzy match** (likely cause: heavy improv during recording) — for that slide only, fall back to narration-estimate timestamp and surface a one-line warning in metadata block.
- **Above-fold hook exceeds 200-char budget after 3 redraft attempts** — surface the best-effort candidate with a one-line note in metadata (`above-fold prefix NNN chars; exceeds 200-char mobile budget by NN chars; consider redirecting`).
- **Hashtag count drifts outside 5-7 range** — silently re-roll selection until in range; never surface a count-violating draft.
- **Article URL confirmation rejected by user, override empty** — surface again with the original candidate and a friendlier prompt; do not assume the empty response means accept (this is an active-confirmation gate, not a passive one).
- **User pastes a description at invocation** — skip drafting; run validation pass (length budgets, banned-content, hashtag count, link block presence, article URL present); surface warnings; gate as override-accepted.
- **User redirects at final gate** — apply steering and re-draft only the affected block(s). Don't re-roll the whole artifact unless the redirect is global ("redo everything punchier").

---

## 8. What this skill is NOT

- Not a title generator. That's `tcn-youtube-title`.
- Not a thumbnail prompt generator. That's `tcn-youtube-thumbnail`.
- Not a slideshow prompt generator. That's `tcn-youtube-slideshow`.
- Not a narration script generator. That's `tcn-youtube-narration`.
- Not an article generator. That's the `tcn-article-builder` ecosystem.
- Not a YouTube uploader / YouTube Studio API client. The user pastes the artifact manually into the Studio description field.
- Not a YouTube tags-field generator. The separate metadata "tags" field has been deprecated for search ranking by YouTube itself; we lean on description-body hashtags + proper-noun density instead.
- Not a transcript cleaner. If the `.srt` is garbled, the skill notes degraded quality and falls back where possible; it does not attempt to fix the source.
- Not an article URL HTTP validator. Auto-derivation + user confirmation is the gate; live-checking adds fragility for marginal value.
- Not a multi-language translator. English-only output; matches the rest of the TCN content.

---

## 9. Companion skills

**Upstream (this skill reads from):**

- `tcn-youtube-narration` — primary input (the `youtube-narration.md` file with its Script Notes footer and *Cuts from the article* field).
- Recording → transcript — `.srt` or `.txt` preferred post-record.
- `tcn-youtube-title` — paired artifact, picked title + mechanism (for orthogonal-hook enforcement and above-fold non-restatement).
- `tcn-youtube-thumbnail` — paired artifact, chosen headline + mechanism (for orthogonal-hook enforcement).
- Final article draft (`10-final.md`) — optional, mined for SEO anchors only.

**Sibling skills (do not consume each other directly):**

- `tcn-youtube-slideshow` — produces the slide deck for the video. No direct interaction with this skill.

**Shared canonical sources:**

- `workspace/core/anti-ai-writing-style.md` — voice file.
- `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` — banned content + anti-AI-tells (single source of truth across thumbnail, title, description).
- `../tcn-youtube-title/references/title-patterns.md` — mechanism taxonomy.

---

## 10. Reference files

- `references/description-anatomy.md` — the skill's living, authoritative anatomy doc. Block-by-block specs, length budgets, chapter format rules, hashtag selection logic, link-block boilerplate, divider conventions, the Audit-Standard description-only mechanism definition, worked examples (one full Dispatch 004 worked example walking from narration to final description). The source of truth for draft-time decisions. Read at every draft, not duplicated in the SKILL.md.

---

## 11. Open questions / things the implementation plan should resolve

(Captured here because the brainstorm went straight to design without surfacing them in conversation. Implementation planning should resolve them; none block the spec from being approved.)

1. **`.srt` fuzzy-matching threshold** — what edit distance qualifies as "I found this slide's opener in the transcript"? Need to pick a default and document it in `references/description-anatomy.md`.
2. **Channel-evergreen hashtag list** — committed to `#TheCivicNode #drinkYourOJ` in this spec. If a third evergreen tag emerges as channel identity matures (e.g., `#CivicTech`, `#DePIN` if Justin's coverage stabilizes around that), the list updates in `references/description-anatomy.md` without a SKILL.md change.
3. **Bluesky URL changes** — currently `https://bsky.app/profile/thecivicnode.bsky.social`. If Justin moves handles, the default updates in `references/description-anatomy.md`.
4. **Long-form pre-record artifact lifecycle** — pre-record artifact is built off estimated timestamps; post-record re-run is recommended. Should the skill silently overwrite the pre-record artifact when re-run post-record, or version-tag (`youtube-description-v1.md`, `youtube-description-v2.md`)? Recommendation: silent overwrite, matching the title-skill pattern; document the recommendation in the SKILL.md.
5. **Audit-Standard mechanism definition** — needs to be written out with 2-3 worked examples in `references/description-anatomy.md`. The mechanism is: hook proposes a known industry/regulatory standard the subject failed to meet (e.g., "Buy a McDonald's franchise and you get a 200-page disclosure document. Helium operators got vibes."). Distinct from Specific-Contradiction (which doesn't anchor to an external standard) and Authority-Asymmetry (which doesn't propose what the standard *should* have been).
