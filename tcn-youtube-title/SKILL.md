---
name: tcn-youtube-title
description: "Step 3 of the Civic Node YouTube production workflow — produces 3 two-part-stop YouTube title candidates for a TCN dispatch, complementary to the chosen thumbnail in-image headline (not redundant), with the 'Specific Anchor. Twist.' pattern that lands the hook before mobile-feed truncation (≤55 chars first half) and rewards the desktop view with a second-half twist. Pre- or post-record. Invoke when the user says 'write the title', 'title for this dispatch', 'make the youtube title', 'title №NNN', 'generate title options', 'what should we call this video', or has approved a youtube-narration.md/youtube-thumbnail.md and wants titles. Does NOT generate the article, narration, slideshow, thumbnail image, or description (those are separate skills), and does NOT push titles to YouTube Studio (user pastes manually or uses Test & Compare)."
---

# The Civic Node — YouTube Title (Step 3 of the YouTube Production Workflow)

## What This Skill Does

Produces a single artifact for a TCN dispatch: three two-part-stop YouTube title candidates with one-line rationales, surfaced for user pick at Gate 2. Every candidate uses the `Specific Anchor. Twist.` pattern — first half ≤55 chars to clear mobile-feed truncation, full title ≤90 chars ideal (≤100 hard ceiling, YouTube's max). The skill reads `youtube-thumbnail.md` so its candidates *complement* the chosen in-image headline rather than restating it — title and thumbnail compose into one rhetorical move on the YouTube feed, not two duplicate ones. See §6 for the pattern definition.

---

## Why a Candidate-Pick Pattern

Titles are a CTR-first decision that benefits from side-by-side comparison of *mechanisms*, not just words. The skill surfaces three candidates that all use the same structural pattern (two-part stop) but vary the rhetorical mechanism — authority-asymmetry, completion-pairing with the thumbnail, hidden-contradiction, etc. This makes the user's pick a choice about which lever moves their audience, not a choice between three random phrasings. The picked title also seeds YouTube Studio's Test & Compare feature: the user can take the chosen title as primary and (optionally) test against one or both alts.

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
tcn-youtube-title       [Step 3 — this skill]
tcn-youtube-description [Step 4 — planned]
tcn-youtube-thumbnail   [Step 5]
```

Recording is the cleavage point between upstream skills (which consume article prose) and downstream packaging skills (which consume the recorded transcript). This skill, like `tcn-youtube-thumbnail`, can run **pre- or post-record**: pre-record against the narration's cold-open for early concepting and metadata-prep alongside thumbnail design; post-record against the recorded transcript to capture any improv'd lines that landed harder than the script. Recommended order: run pre-record alongside the thumbnail skill for paired concepting, re-run post-record for the final pick.

---

## Inputs and Outputs

### Required input

- **Path to a narration file (`youtube-narration.md`) OR a recorded transcript** (`.srt` or `.txt`). The skill auto-detects: it looks for both in the supplied directory; **transcript wins if both are present** (the transcript captures the actual delivered voice, including improv'd phrasing the script doesn't have). If the user pastes contents directly, save to a temp file and proceed. Halt with an explicit message and example path if neither is found.

### Strongly recommended input

- **`youtube-thumbnail.md`** in the same directory. If present, the skill reads the chosen thumbnail in-image headline and uses it as input to the complementarity check (§7.5). If missing, the skill soft-warns ("redundancy-avoidance degraded — title may overlap with thumbnail; consider running tcn-youtube-thumbnail first") and proceeds. The title can still be drafted, but the user is responsible for visually checking redundancy at composite time.

### Optional inputs

- **Final article draft** (`10-final.md` or slug-named variant) — used only to mine concrete anchors (numbers, place names, proper nouns) not surfaced in the narration. Read silently if present, skipped if absent.
- **Steering** — free-text guidance like "lean on the McDonald's framing", "include the dollar figures", "more declarative, less curiosity gap".
- **Override headline** — user pastes their own title; skill skips Gate 2 and goes straight to the final gate.

### Primary output artifact

- **File:** `workspace/drafts/<slug>/youtube-title.md`
- **Structure:**

```markdown
# YouTube title — TCN Dispatch №NNN

**Generated:** YYYY-MM-DD
**Source:** narration | transcript
**Paired with thumbnail headline:** "<thumbnail in-image headline, or 'no thumbnail artifact found'>"

---

## Picked title

"<chosen title after Gate 2 closes>"

**Length:** NN chars (first half NN, second half NN)
**Pattern:** <mechanism name>
**Search anchors:** <proper nouns / numbers / place names used>
**Pairs with thumbnail as:** compound | completion | orthogonal-compound | none

---

## All 3 candidates

1. "<candidate 1>" (NN chars · first half NN)
   — <one-line rationale>

2. "<candidate 2>" (NN chars · first half NN)
   — <one-line rationale>

3. "<candidate 3>" (NN chars · first half NN)
   — <one-line rationale>
```

The "All 3 candidates" section persists in the artifact even after the user picks — the unused candidates are useful as alternates if the user later wants to A/B-test in YouTube Studio.

---

## Run Timing

The skill ships dual-input. Same output shape in both modes — only the source text differs.

| Concern | Pre-record (narration) | Post-record (transcript) |
|---|---|---|
| Activation | Only `youtube-narration.md` found | `.srt` or `.txt` transcript found (wins over narration) |
| Source label in artifact | `**Source:** narration` | `**Source:** transcript` |
| Cold-open extraction | Read narration's title block + first slide (HOOK) | Read first ~30 seconds of transcript |
| Refrain extraction | Read narration's Script Notes "Refrain markers" field | Mine the transcript for repeated landing phrases |
| Concrete-anchor mining | Narration body | Transcript body |
| Workflow position | Run alongside Step 5 (thumbnail) for paired pre-record concepting | Re-run for final pick |

---

## The Process

### 1. Read narration or transcript

Auto-detect in the supplied directory: transcript (`.srt` or `.txt`) wins if both exist. Halt with an explicit message and example path if neither is found.

### 2. Read the thumbnail artifact (recommended)

Look for `youtube-thumbnail.md` in the same directory. If found, extract the **Chosen headline** field — that's the in-image headline the skill must avoid duplicating. If missing, log a one-line soft warning ("redundancy-avoidance degraded; consider running tcn-youtube-thumbnail first") and proceed without the complementarity check.

### 3. Extract dispatch metadata

Pull the dispatch number from the narration's title block (or the `<slug>` directory naming convention if reading a raw transcript). If the dispatch number is missing from both sources, halt and ask the user to confirm. Do not guess.

### 4. Mine the source for concrete anchors

Extract numbers, dollar amounts, place names, proper nouns, years, and percentages from the cold-open and the dispatch concept. This is the candidate pool for the **specific anchor** half of the title. Note which anchors the thumbnail headline already uses — these are *available* for the title but lower priority (using a thumbnail-overlapping anchor weakens complementarity).

### 5. Draft 3 candidates per the two-part-stop pattern

Distill candidates per §6 below: drafting inputs (§6.1), acceptance criteria (§6.2), mechanism variety (§6.3), retry behavior (§6.4), and Gate 2 display format (§6.5). Each candidate is two halves separated by a period (or colon, if natural), with the specific anchor in the first half and the twist in the second half. The three candidates must use **different rhetorical mechanisms**, not just different words around the same mechanic.

### 6. GATE 2 — Title pick

Present:

```
Pick a title:

1. "<Candidate 1>" (NN chars · first half NN)
   — <rationale>

2. "<Candidate 2>" (NN chars · first half NN)
   — <rationale>

3. "<Candidate 3>" (NN chars · first half NN)
   — <rationale>

Or 'try again' for new options. Or paste your own.
```

Wait for response. If an override title was supplied at invocation, skip this gate.

### 7. Write the artifact file

Write `workspace/drafts/<slug>/youtube-title.md` with the picked title at the top, the full candidate list preserved below for future A/B reference, and the metadata block (source, dispatch number, paired thumbnail headline).

### 8. Final gate

Present:

```
Title artifact ready at `<path>`. Approve, redirect (e.g., 'try again', 'lean on McDonald's framing', 'more declarative', 'swap candidate 2 for something with the dollar figures', 'shorter first half'), or cancel?
```

Wait for response. Redirects re-enter Gate 2 with the new steering applied to all 3 candidates. If the user asks to swap just one candidate, re-draft only that slot.

---

## Title Drafting

YouTube titles are a distinct content genre from article headlines, social hooks, thumbnail in-image headlines, or the cold-open itself. They occupy a unique constraint: metadata text beside the thumbnail in the feed, search-indexed, truncated to ~55 chars on mobile, expandable to ~90 on desktop, hard-capped at 100. See §6.1–§6.5 in `references/title-patterns.md` for the full pattern library.

### Drafting inputs (§6.1)

When drafting candidates at process step 5, the skill has:

- The cold-open candidate (from narration) OR the first ~30 seconds of recorded transcript — the dispatch's most punchable opening.
- The dispatch concept — the broader subject, extracted from narration structure or transcript flow.
- The thumbnail in-image headline (if `youtube-thumbnail.md` is present) — for redundancy avoidance.
- The dispatch number, slug, and any user-supplied steering.
- The full contents of `references/title-patterns.md` (loaded into context at drafting time as the source of truth for two-part-stop patterns and mechanism taxonomy).

### Acceptance criteria (§6.2)

A candidate is rejected silently and re-drafted if it fails any of:

- **First half ≤55 chars** including its terminal period. This is the mobile-feed truncation budget — the hook must land before the "..." cut.
- **Total ≤100 chars** hard ceiling (YouTube's max). Warn but do not reject if 90 < total ≤ 100.
- **Word count 8–14 words total.** Hyphenated compounds count as one word; contractions count as one word; numbers count as one word regardless of digit count.
- **Sentence case only.** No all-caps words. Genuine acronyms (FCC, FAA, HIP, IoT, DAO) are exceptions.
- **Period or colon stop only** between the two halves. Em-dashes are banned (anti-AI-tell). Exclamation points are banned. Question marks are allowed only when load-bearing for a genuine curiosity gap.
- **Concrete-specific requirement.** If the source carries any number, place name, dollar amount, year, or proper noun, at least one of the three candidates MUST use it. (Variety is good — the other two can be more abstract.)
- **Inherited banned content.** Banned hype adjectives, banned clickbait templates, and anti-AI-tell tokens come from `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` by reference. Do not duplicate the lists here — read them at drafting time.
- **Title-specific bans** (additional to inherited list):
  - Both halves within 5 chars of equal length → reject (no rhythm; reads as cadenced AI output).
  - Second half merely rephrases the first → reject (redundant; spends two halves on one idea).
  - Second half is a generic moralizing tail ("Here's What That Means", "And It's Worse Than You Think", "You Won't Believe Why") → reject.
- **Complementarity-with-thumbnail check.** If `youtube-thumbnail.md` is found and the chosen thumbnail headline is known: reject candidates whose specific content overlaps >50% with the thumbnail headline (sharing 1–2 anchor words is fine; sharing the whole rhetorical move is redundant).

The banned-word and banned-template lists live in `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` (single source of truth across both skills). The title-specific bans live in `references/title-patterns.md` and can evolve there without skill-code changes.

### Mechanism variety (§6.3)

All three candidates use the two-part-stop *structure*. They differ in the *mechanism* the twist runs:

- **Authority-Asymmetry** — first half describes what the viewer bought / owns / chose; second half names who controls the economics or rules.
- **Specific Contradiction** — first half states a concrete fact; second half states an equally concrete contradicting fact. The two halves are in named, fact-checkable tension.
- **Hidden Revenue / Hidden Move** — first half describes the visible/marketed side; second half names where the actual money or power lives.
- **Completion-Pairing** — first half opens a curiosity gap whose answer is the thumbnail in-image headline. Tightest pairing of all mechanisms.
- **Personal-Implication** — first half describes the author's own action; second half delivers the consequence or reframe. (Sparingly — only when the dispatch has a real "I was wrong about X" moment.)

The three candidates should use three different mechanisms. See the mechanism taxonomy in `references/title-patterns.md` for the full set and worked examples.

### Retry behavior (§6.4)

If any of the 3 initially drafted candidates fails the acceptance criteria, internally re-draft the failing slot(s) up to 2 additional attempts before surfacing. If after 3 total attempts a slot still fails, surface the best-effort candidate with a one-line note ("could not satisfy [criterion]; consider redirecting"). The user always sees 3 candidates. Re-drafts are silent — the user does not see rejected attempts.

### Gate 2 display format (§6.5)

After successful drafting, the user sees the format shown in process step 6 above. Rationales surface *what mechanism* each candidate runs and *how it pairs with the thumbnail*, not just the words themselves. This is the user's mental model for picking — they're choosing a rhetorical lever, not a phrasing.

---

## TCN Voice Inheritance

Title voice inherits from the same corpus as the narration:

- **Justin Hearn / drinkYourOJ voice profile** — sardonic, specific, dry. Sentence case. No screaming.
- **Anti-AI-writing-style rules** — the same tell-list applied by `tcn-text-humanizer`. Cross-referenced via `thumbnail-headline-patterns.md`.
- **Marcus-reader visiting-friends register** — talking to a smart friend who happens to scroll YouTube, not shouting at a crowd.
- **7/10 Hank-Vox blend** — the same dial as the narration script. Slightly broader-audience than pure-Marcus, but Marcus would still smirk at the result.

Title and thumbnail share this voice; what differs is *what each surface optimizes for*. Thumbnail = visual stop power in 3–6 words. Title = readable specificity in 8–14 words. Same dial, different mechanic.

---

## Failure Modes

- **No narration and no transcript found** — halt with an explicit message and an example path. Do not attempt to compose from nothing.
- **Narration malformed** (no Script Notes footer, no cold-open candidate, no title block) — halt and ask the user to supply a cold-open candidate as steering, or fix the narration upstream.
- **`youtube-thumbnail.md` missing** — soft warn ("redundancy-avoidance degraded; consider running tcn-youtube-thumbnail first"). Proceed without the complementarity check. Note this in the artifact's header (`**Paired with thumbnail headline:** no thumbnail artifact found`).
- **Thumbnail artifact present but malformed** (no `Chosen headline:` field) — log a one-line warning, treat as missing, proceed.
- **Dispatch number missing from narration title block and not derivable from the slug** — halt and ask the user to confirm. Do not guess.
- **All 3 candidates fail acceptance criteria after 3 attempts each** — surface best-effort candidates with one-line notes per failure ("could not satisfy first-half ≤55 chars; second strongest candidate runs 58"). User decides whether to redirect or accept the degraded version.
- **Transcript present but garbled** (audio-typo-heavy, missing punctuation, low confidence) — proceed but note in the artifact header ("transcript quality degraded; consider verifying anchors against narration").
- **User pastes a title at invocation** — skip Gate 2 entirely; run only the acceptance criteria check and the final gate. Surface any warnings from the criteria check before the final gate so the user can decide whether their override needs revision.
- **User redirects at the final gate** — re-enter Gate 2 with the new steering. If the redirect targets a single candidate ("swap candidate 2 for something with the dollar figures"), re-draft only that slot.

---

## What This Skill Is NOT

- Not a thumbnail headline generator. That's `tcn-youtube-thumbnail`. The two skills are intentionally separated because the constraints differ (3–6 words visual stop vs. 8–14 words readable specificity).
- Not a description, tags, or chapter-timestamp generator. That's `tcn-youtube-description` (planned).
- Not an article headline generator. That's `tcn-headline` in the article workflow.
- Not a YouTube uploader or Test & Compare automator. The skill produces the artifact; the user pastes manually or sets up Test & Compare in YouTube Studio.
- Not an SEO-keyword-density optimizer. Light keyword anchoring is encouraged (proper nouns when natural), but the skill does not score candidates by keyword density or run YouTube search lookups.
- Not a series-prefix generator. Bare titles only. The thumbnail's corner identity block carries `DISPATCH №NNN`.
- Not a transcript cleaner. If the transcript is garbled, the skill notes the degradation but does not attempt to fix the source.

---

## Companion Skills

**Upstream (this skill reads from):**
- `tcn-youtube-narration` — produces the narration file the skill reads pre-record.
- Recording → transcript — produces the `.srt` or `.txt` the skill prefers post-record.
- `tcn-youtube-thumbnail` — produces the thumbnail artifact whose chosen headline informs the complementarity check.

**Sibling (planned, not built today):**
- `tcn-youtube-description` — description body, tags, chapter timestamps.

**Shared pattern library:**
- `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` — single source of truth for banned hype adjectives, banned clickbait templates, and anti-AI-tell tokens. Read at drafting time; not duplicated in this skill.

---

## Reference Files

- `references/title-patterns.md` — pattern library for §6 candidate drafting. Two-part-stop structural patterns, anchor-vs-twist mechanics, mechanism taxonomy (authority-asymmetry, specific contradiction, hidden revenue, completion-pairing, personal-implication), thumbnail-pairing modes (compound vs completion vs orthogonal), first-half char budget math, title-specific anti-pattern gallery (equal-length halves, second-half rephrase, generic moralizing tail), and worked example walkthroughs. The source of truth for title drafting — the skill reads this file at drafting time. Living document.
