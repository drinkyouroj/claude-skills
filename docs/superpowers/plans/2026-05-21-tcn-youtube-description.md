# tcn-youtube-description Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `tcn-youtube-description` skill per the spec at [docs/superpowers/specs/2026-05-21-tcn-youtube-description-design.md](../specs/2026-05-21-tcn-youtube-description-design.md). Skill produces paste-ready YouTube descriptions (trailer-funnel anatomy, viewer-rewritten chapters, auto-derived Substack URL, dual-input narration/transcript) for Civic Node Dispatch videos. Deployable in time for the Dispatch 004 packaging pass.

**Architecture:** Markdown-based Claude Code skill mirroring the structural conventions of `tcn-youtube-narration`, `tcn-youtube-slideshow`, `tcn-youtube-title`, and `tcn-youtube-thumbnail`. Source-of-truth at `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/`, runtime symlink at `~/.claude/skills/tcn-youtube-description/`. One `SKILL.md` plus one substantive reference file (`references/description-anatomy.md`). Reads shared reference libraries from sibling skills (`tcn-youtube-title/references/title-patterns.md` for mechanism taxonomy, `tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` for banned content) — does not duplicate.

**Tech Stack:** Markdown, YAML frontmatter, Bash for filesystem ops + symlink, git for atomic commits per task. No external dependencies or MCP tools required at runtime. Validation against the on-disk Dispatch 004 narration + slideshow + title + thumbnail artifacts as the smoke test corpus.

**Spec coverage map:**
- §1 (purpose) → SKILL.md body section "What this skill does" (Task 2)
- §2 (position in workflow) → SKILL.md body section "Position in the YouTube workflow" (Task 2)
- §3 (inputs and outputs) → SKILL.md body section "Inputs and outputs" + frontmatter triggers (Task 2)
- §4 (anatomy) → SKILL.md body section "Description anatomy" + `references/description-anatomy.md` (Tasks 3, 6)
- §5 (the process) → SKILL.md body section "The process" (Task 4)
- §6 (voice & shared references) → SKILL.md body section "Voice & shared references" (Task 5)
- §7 (failure modes) → SKILL.md body section "Failure modes" (Task 5)
- §8 (what this skill is NOT) → SKILL.md body section "What this skill is NOT" (Task 5)
- §9 (companion skills) → SKILL.md body section "Companion skills" (Task 5)
- §10 (reference files) → SKILL.md body section "Reference files" + Task 6
- §11 (open questions) → tracked in spec only; relevant decisions land in `references/description-anatomy.md` (Task 6)

---

## Task 1: Set up skill directory + runtime symlink

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/`
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/references/`
- Symlink: `~/.claude/skills/tcn-youtube-description/` → top-level source

- [ ] **Step 1: Create source directory + references subdirectory**

```bash
mkdir -p /Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/references
```

Expected: two new directories on disk. No output is a success.

- [ ] **Step 2: Verify the runtime symlink target does not already exist**

```bash
ls ~/.claude/skills/tcn-youtube-description 2>/dev/null || echo "OK_NOT_EXISTS"
```

Expected: `OK_NOT_EXISTS`. If a non-symlink directory exists at that path, halt and ask the user — do not overwrite.

- [ ] **Step 3: Create the runtime symlink**

```bash
ln -sf /Users/justin/CascadeProjects/claude-skills/tcn-youtube-description ~/.claude/skills/tcn-youtube-description && readlink ~/.claude/skills/tcn-youtube-description
```

Expected output: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description`

- [ ] **Step 4: No commit yet** — directory has no files. First commit lands in Task 2.

---

## Task 2: Write SKILL.md frontmatter + identity sections

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md`

Writes the YAML frontmatter and the top half of the SKILL.md: "What This Skill Does," "Voice & vocabulary canonical source," "Position in the YouTube Workflow," "Inputs and Outputs," and "Run Timing." Mirrors the structural conventions of the four sibling skills.

- [ ] **Step 1: Write the frontmatter**

Open `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md` and write the YAML frontmatter. The `description` field is single-line, lists invocation phrases, says what the skill does NOT cover, and references sibling skills by name. Match the verbosity of `tcn-youtube-title`'s frontmatter.

```markdown
---
name: tcn-youtube-description
description: "Step 4 of the Civic Node YouTube production workflow — produces a paste-ready YouTube description for a TCN dispatch with above-the-fold hook, dispatch summary, Substack article CTA, viewer-rewritten chapter timestamps, channel link block (Substack + Bluesky), and dispatch-specific hashtags. Trailer-funnel anatomy that mines the narration's 'cuts from the article' field to drive Substack click-through. Dual-input: pre-record reads youtube-narration.md (chapter timestamps estimated from slide pacing); post-record reads .srt/.txt transcript (exact timestamps win if both present). Auto-derives the Substack article URL from the workspace slug with a confirmation gate. Invoke when the user says 'write the description', 'youtube description for this dispatch', 'make the description', 'description for №NNN', 'generate description', 'what should go in the youtube description', or has approved a youtube-narration.md / youtube-title.md / youtube-thumbnail.md and wants the description. Does NOT generate the article, narration, slideshow, title, or thumbnail (those are separate skills), and does NOT upload the description to YouTube Studio (user pastes manually)."
---
```

- [ ] **Step 2: Write the "What This Skill Does" section**

Below the frontmatter, write the section. Single paragraph; states the surface (paste-ready description), the structure (trailer-funnel with 11 blocks), the dual-input pattern (narration pre-record OR transcript post-record), and the orthogonal-mechanism rule against paired title/thumbnail artifacts. Reference spec §1 for content.

```markdown
# The Civic Node — YouTube Description (Step 4 of the YouTube Production Workflow)

## What This Skill Does

Produces a single paste-ready YouTube description for a TCN dispatch, structured as a trailer-funnel that mines the narration's *Cuts from the article* field to drive Substack click-through rather than retention on YouTube alone. The description has 11 ordered blocks: above-fold hook (≤200 chars), blank, 3-5 sentence summary, blank, single-sentence article CTA + bare URL, blank, chapter list (viewer-rewritten labels, MM:SS timestamps), blank, channel link block (Substack + Bluesky boilerplate), blank, and 5-7 hashtags (3-5 dispatch-specific + 2 channel-evergreen). The skill is dual-input — pre-record reads `youtube-narration.md`; post-record reads a `.srt` or `.txt` transcript (transcript wins if both present). The above-fold hook runs an orthogonal rhetorical mechanism to the paired title and thumbnail headlines: if `youtube-title.md` and `youtube-thumbnail.md` are present, the skill enforces three different mechanisms across the three YouTube surfaces.
```

- [ ] **Step 3: Write the "Voice & vocabulary canonical source" section**

Copy the exact pattern from `tcn-youtube-narration/SKILL.md` (lines 14-31 of that file). Adapt only the skill name. The fallback-when-missing language must be identical (per the "elasticity-bug failure mode" reference).

```markdown
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
```

- [ ] **Step 4: Write the "Position in the YouTube Workflow" section**

Match the ASCII workflow diagram from `tcn-youtube-title/SKILL.md`. Mark this skill as Step 4 (the diagram already lists it as planned in sibling skills — confirm consistency).

```markdown
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
```

- [ ] **Step 5: Write the "Inputs and Outputs" section**

Match the structure used by `tcn-youtube-title/SKILL.md` (Required / Strongly recommended / Optional / Primary output artifact / Gate prompt). The Strongly Recommended block lists BOTH `youtube-title.md` and `youtube-thumbnail.md` for orthogonal-mechanism enforcement. The output artifact template lives in spec §3.

Provide the section in full per spec §3. Include the exact metadata block format with all paired-artifact fields. Include the "Paste this into YouTube" section header and the "Block-level breakdown" section header. End the section with the final gate prompt format.

```markdown
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

\`\`\`markdown
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
\`\`\`

### Gate prompt presented to user

> YouTube description draft complete (~NNNN chars, above-fold prefix NNN chars). Approve, redirect (e.g., 'punchier above-fold', 'swap the hook mechanism', 'more chapter granularity', 'replace #DePIN with #Web3'), or cancel?

**Stop after presenting the draft.** Wait for user approval or redirect before doing anything else.
```

(Note: in the actual SKILL.md the inner backticked-markdown block should use 4-backtick fences for the outer to allow the 3-backtick inner block. Adjust during paste.)

- [ ] **Step 6: Write the "Run Timing" section**

Copy the run-timing table format from `tcn-youtube-title/SKILL.md` lines 97-108. Adapt the column content for description-specific concerns (chapter timestamps replace cold-open extraction).

```markdown
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
```

- [ ] **Step 7: Verify the file is syntactically clean markdown**

```bash
head -100 /Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md
```

Expected: see the frontmatter (delimited by `---`), then the first section headers. No partial code blocks. No trailing `---` orphan.

- [ ] **Step 8: Commit**

```bash
git add tcn-youtube-description/SKILL.md && git commit -m "feat(tcn-youtube-description): scaffold skill with frontmatter and identity sections"
```

---

## Task 3: Write the Description Anatomy section

**Files:**
- Modify: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md` (append the anatomy section)

The most content-dense section. Walks through all 11 blocks of the description, length budgets, divider conventions, chapter timestamp computation. Spec §4 is the authoritative source.

- [ ] **Step 1: Append the section header and block-ordering ASCII diagram**

```markdown
---

## Description Anatomy

### Block ordering (top to bottom)

\`\`\`
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
\`\`\`
```

- [ ] **Step 2: Append the Block 1 (Hook punch) subsection**

Reference spec §4 block 1. Include the orthogonal-mechanism rule, the "rewritten fresh" rule (not from narration cold-open, not from transcript first 30 seconds), the 200-char budget, banned content, and the explicit ban on Completion-Pairing as a description-hook mechanism (description is not a visual surface).

```markdown
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
```

- [ ] **Step 3: Append the Block 3 (Dispatch summary) subsection**

Reference spec §4 block 3. Include the *Cuts from the article* funnel-mining rule, the 400-700 char target, the proper-noun density guidance, and the "numerals not words" deviation from spoken-word style.

```markdown
### Block 3 — Dispatch summary

- **3-5 sentences.** Target 400-700 chars. Below the fold.
- **8/10 register.** Voice file enforced.
- **Mines the narration's *Cuts from the article* field as raw material** — names what the video did NOT cover. This is the funnel mechanic that converts viewers to readers.
- **Numerals, not words.** Description copy is scanned visually; "385,000 hotspots" reads faster than "three hundred eighty-five thousand hotspots." (Opposite of the spoken-word rule in the narration skill.)
- **Proper-noun density** — name 3-5 indexable nouns (companies, people, votes, places, technologies) for SEO. TCN voice already does this naturally; the skill should not strain to add them.
- Anti-AI-tells enforced.
```

- [ ] **Step 4: Append the Block 5 (Article CTA) subsection**

```markdown
### Block 5 — Article CTA

- **Single sentence** introducing the article URL, followed by the bare URL on the next line.
- Example: `→ Read the full piece on Substack:` \n `https://drinkyouroj.substack.com/p/<slug>`
- The `→` arrow is acceptable (Unicode arrow, not em-dash, not asterisk-marketing-bait). `>` or `>>` are also acceptable; the skill picks one and stays consistent across dispatches.
- **Bare URLs only.** YouTube descriptions do not render markdown; `[text](url)` is shown literally.
```

- [ ] **Step 5: Append the Block 7 (Chapters) subsection**

Reference spec §4 blocks 7 and the chapter-timestamp-computation block. Include the YouTube auto-detect format requirements (first chapter `0:00`, minimum 3, maximum 10), the viewer-rewritten label rule, and the "End slide always included" rule.

```markdown
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
```

- [ ] **Step 6: Append the Block 9 (Channel link block) subsection**

```markdown
### Block 9 — Channel link block

Constant boilerplate across every dispatch:

\`\`\`
-- THE CIVIC NODE --
Weekly. No hype.

Substack:  https://drinkyouroj.substack.com
Bluesky:   https://bsky.app/profile/thecivicnode.bsky.social
\`\`\`

Skill writes this verbatim. User-supplied Substack and Bluesky overrides replace the defaults.
```

- [ ] **Step 7: Append the Block 11 (Hashtags) subsection**

```markdown
### Block 11 — Hashtags

- **3-5 dispatch-specific** mined from the narration + article: prefer proper-noun anchors (companies, technologies, votes, places, named events) over abstract categories.
- **2 channel-evergreen** constant across every dispatch: `#TheCivicNode #drinkYourOJ`.
- **Sentence case enforced** — `#NovaLabs`, `#HIP143`, not `#NOVALABS` or `#novalabs`. PascalCase / camelCase for multi-word, no spaces, no punctuation (YouTube hashtags only honor `[A-Za-z0-9_]`).
- **Single line, space-separated.** YouTube shows only the first 3 in description order as clickable category tags above the title; put the strongest dispatch-specific tag first.
- **Total count 5-7** — beyond ~7 YouTube treats as spam-coded.
- Skill silently re-rolls if count falls outside 5-7.
```

- [ ] **Step 8: Append the Dividers and Length Budgets subsections**

```markdown
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
```

- [ ] **Step 9: Verify section reads coherently**

```bash
grep -n "^### Block" /Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md
```

Expected: 6 lines, one each for `### Block 1`, `### Block 3`, `### Block 5`, `### Block 7`, `### Block 9`, `### Block 11`. (Blocks 2, 4, 6, 8, 10 are blank-line spacers and not subsection-headed.)

- [ ] **Step 10: Commit**

```bash
git add tcn-youtube-description/SKILL.md && git commit -m "feat(tcn-youtube-description): add description anatomy section (11 blocks, length budgets, dividers)"
```

---

## Task 4: Write the Process section

**Files:**
- Modify: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md`

Eleven numbered process steps walking from input detection through artifact write. Spec §5 is authoritative.

- [ ] **Step 1: Append the section header**

```markdown
---

## The Process
```

- [ ] **Step 2: Append Steps 1-3 (input detection, paired artifact reads, URL derivation)**

```markdown
### 1. Auto-detect source

In the supplied dispatch directory, look for:

- `.srt` file (any name) — preferred transcript form
- `.txt` file (any name with "transcript" in filename) — fallback transcript form
- `youtube-narration.md` — narration source

**Transcript wins if both transcript and narration present.** If neither exists, halt with example path: `expected workspace/drafts/<slug>/youtube-narration.md or a .srt/.txt transcript in the same directory.`

### 2. Read paired artifacts

In the same dispatch directory, look for:

- `youtube-title.md` — extract the picked title from the `## Picked title` section and the mechanism name from the `**Pattern:**` field.
- `youtube-thumbnail.md` — extract the `Chosen headline:` field and the chosen variant's mechanism.

If either missing or malformed (missing expected fields): log soft warning ("orthogonal-mechanism enforcement degraded"), proceed without orthogonality enforcement, note in artifact metadata.

### 3. Derive article URL

1. Extract the slug from the supplied directory name (e.g., `you-own-the-hotspot-nova-labs-owns-what-it-earns`).
2. Construct candidate URL: `https://drinkyouroj.substack.com/p/<slug>`.
3. Surface to user: `Detected article URL: <candidate URL>. Confirm or paste an override:`
4. If user confirms (empty response, "confirm", "yes"), use the candidate.
5. If user pastes a URL, use the override. Record in artifact metadata.
6. If slug fails sanity checks (>80 chars, contains `_`, contains uppercase, contains chars outside `[a-z0-9-]`), surface with a flag: `Derived URL doesn't match Substack slug conventions. Paste the correct URL:` and require an explicit override.
```

- [ ] **Step 3: Append Steps 4-5 (anchor mining, hook drafting)**

```markdown
### 4. Mine anchors

From the narration body (or transcript body, post-record) and the article draft (if present):

- Numbers and dollar amounts.
- Proper nouns (companies, people, technologies, votes, places).
- Years and dates.
- Quoted phrases (highest-confidence anchors).

Anchor pool feeds the summary (block 3) and hashtag selection (block 11). The above-fold hook uses anchors only when they fit the mechanism naturally.

### 5. Draft the above-fold hook (block 1)

Inputs:

- The dispatch concept (extracted from narration title block + thesis slide post-record, or from the transcript's thesis-equivalent passage if the cold-open analogy was abandoned during recording). Explicitly NOT from the narration's cold-open or the transcript's first 30 seconds.
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
```

- [ ] **Step 4: Append Steps 6-7 (summary drafting, chapter list)**

```markdown
### 6. Draft the dispatch summary (block 3)

Inputs:

- The narration body (or transcript body).
- The narration's *Cuts from the article* field.
- The anchor pool from step 4.

Drafting:

1. Compose 3-5 sentences.
2. Front-load anchors and proper nouns (helps viewer scanning and YouTube search indexing).
3. Reference what the video did NOT cover — that's the funnel mechanic.
4. End on a phrase that motivates clicking through to the article.
5. Validate: length 400-700 chars, anti-AI-tells pass, no em-dashes, no banned content.

### 7. Build the chapter list (block 7)

Run the timestamp computation (post-record from transcript or pre-record from narration WPM math, per the Description Anatomy section's Block 7 spec).

For each chapter, draft a viewer-facing label:

1. Read the narration slide's actual content (or the transcript segment for that timestamp).
2. Distill the segment's main idea into a 4-8 word noun phrase.
3. Calibrate to 8/10 register.
4. Validate: no banned content, no em-dashes, no exclamation points, sentence case.

Compose the chapter block as YouTube auto-detect format: `MM:SS  Label` per line, first chapter `0:00`, last chapter is the End-slide CTA.
```

- [ ] **Step 5: Append Steps 8-11 (link block, hashtags, final gate, artifact write)**

```markdown
### 8. Assemble the channel link block (block 9)

Write the constant boilerplate. Substitute user-supplied Bluesky and Substack overrides if provided; otherwise use the defaults from `references/description-anatomy.md`.

### 9. Generate hashtags (block 11)

1. From the anchor pool, pick 3-5 proper-noun hashtags. Prefer specific (`#HIP143`) over generic (`#Crypto`).
2. Append the 2 channel-evergreen tags: `#TheCivicNode #drinkYourOJ`.
3. Validate count is 5-7; sentence-case enforced.
4. Compose as a single line, space-separated, dispatch-specific tags first.

### 10. Final gate

Present:

\`\`\`
YouTube description draft complete (NNNN chars, above-fold prefix NNN chars).

[full paste-ready description]

Approve, redirect (e.g., 'punchier above-fold', 'swap the hook mechanism', 'more chapter granularity', 'add the August 2025 halving in summary', 'replace #DePIN with #Web3'), or cancel?
\`\`\`

Wait for response. If override description was supplied at invocation, skip drafting steps 5-9 and go straight to validation + final gate.

Redirect handling:

- **Global steering** ("redo punchier", "more declarative throughout") → re-draft all blocks.
- **Block-targeted steering** ("swap the hook", "rewrite chapter 4 label", "drop #DePIN") → re-draft only affected block(s).
- **URL override** ("use this URL instead") → swap the article URL block, regenerate metadata, no other changes.

### 11. Write the artifact

Write `workspace/drafts/<slug>/youtube-description.md` with:

- Metadata block (source, article URL, paired artifacts and mechanisms, hook mechanism).
- The paste-ready description under `## Paste this into YouTube`.
- The block-level breakdown for reference.

Surface a one-line confirmation: `Wrote youtube-description.md. Paste into YouTube Studio description field.`
```

- [ ] **Step 6: Verify section ordering**

```bash
grep -n "^### [0-9]\+\." /Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md
```

Expected: 11 lines, `### 1.` through `### 11.` in order.

- [ ] **Step 7: Commit**

```bash
git add tcn-youtube-description/SKILL.md && git commit -m "feat(tcn-youtube-description): add 11-step process section"
```

---

## Task 5: Write the Failure Modes, What This Skill Is NOT, Companion Skills, and Reference Files sections

**Files:**
- Modify: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md`

Tail sections of the SKILL.md. Mirror the conventions of `tcn-youtube-title/SKILL.md` lines 239-282. Spec §7, §8, §9, §10 are the authoritative sources.

- [ ] **Step 1: Append the Failure Modes section**

Map each spec §7 bullet to a SKILL.md bullet, preserving wording.

```markdown
---

## Failure Modes

- **No narration and no transcript found** — halt with explicit message and example path. Do not attempt to compose from nothing.
- **Narration malformed** (missing title block, missing Script Notes footer, missing *Cuts from the article* field) — halt for missing title block (can't get dispatch number); soft-warn for missing *Cuts from the article* and proceed with degraded summary quality.
- **Slug doesn't match Substack conventions** (>80 chars, underscores, uppercase, chars outside `[a-z0-9-]`) — surface the constructed URL with a flag and require explicit override.
- **`youtube-title.md` missing or malformed** — soft warn ("orthogonal-mechanism enforcement degraded"); proceed without the orthogonality rule for the hook.
- **`youtube-thumbnail.md` missing or malformed** — same soft warn, same degraded path.
- **Transcript present but `.srt` timestamps malformed** — fall back to narration-estimate mode for chapters and note in artifact metadata.
- **Transcript present but slide content can't be located via fuzzy match** — for that slide only, fall back to narration-estimate timestamp and surface a one-line warning in metadata.
- **Above-fold hook exceeds 200-char budget after 3 redraft attempts** — surface the best-effort candidate with a one-line note in metadata.
- **Hashtag count drifts outside 5-7 range** — silently re-roll selection; never surface a count-violating draft.
- **Article URL confirmation rejected by user, override empty** — surface again with the original candidate; do not assume empty response means accept.
- **User pastes a description at invocation** — skip drafting; run validation pass; surface warnings; gate as override-accepted.
- **User redirects at final gate** — apply steering and re-draft only affected block(s) unless redirect is global.
```

- [ ] **Step 2: Append the "What This Skill Is NOT" section**

```markdown
---

## What This Skill Is NOT

- Not a title generator. That's `tcn-youtube-title`.
- Not a thumbnail prompt generator. That's `tcn-youtube-thumbnail`.
- Not a slideshow prompt generator. That's `tcn-youtube-slideshow`.
- Not a narration script generator. That's `tcn-youtube-narration`.
- Not an article generator. That's the `tcn-article-builder` ecosystem.
- Not a YouTube uploader / YouTube Studio API client. User pastes the artifact manually.
- Not a YouTube tags-field generator. The separate metadata "tags" field is deprecated for search ranking; the skill leans on description-body hashtags + proper-noun density instead.
- Not a transcript cleaner. If the `.srt` is garbled, the skill notes degraded quality and falls back where possible; it does not attempt to fix the source.
- Not an article URL HTTP validator. Auto-derivation + user confirmation is the gate.
- Not a multi-language translator. English-only output.
```

- [ ] **Step 3: Append the Companion Skills section**

```markdown
---

## Companion Skills

**Upstream (this skill reads from):**
- `tcn-youtube-narration` — produces the `youtube-narration.md` with the Script Notes footer and *Cuts from the article* field.
- Recording → transcript — `.srt` or `.txt` preferred post-record.
- `tcn-youtube-title` — paired artifact, picked title + mechanism (for orthogonal-hook enforcement).
- `tcn-youtube-thumbnail` — paired artifact, chosen headline + mechanism (for orthogonal-hook enforcement).
- Final article draft (`10-final.md`) — optional, mined for SEO anchors.

**Sibling (do not consume directly):**
- `tcn-youtube-slideshow` — produces the slide deck for the video. No direct interaction with this skill.

**Shared canonical sources (read at runtime, not duplicated):**
- `workspace/core/anti-ai-writing-style.md` — voice file.
- `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` — banned content + anti-AI-tells.
- `../tcn-youtube-title/references/title-patterns.md` — mechanism taxonomy.
```

- [ ] **Step 4: Append the Reference Files section**

```markdown
---

## Reference Files

- `references/description-anatomy.md` — block-by-block specs (above-fold char budget math, chapter format rules, hashtag selection logic, link block boilerplate, divider conventions, the Audit-Standard description-only mechanism definition, one full Dispatch 004 worked example walking from narration to final description). The source of truth for draft-time decisions. Read at every draft, not duplicated in this SKILL.md. Living document.
```

- [ ] **Step 5: Verify all required sections present**

```bash
grep -n "^## " /Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md
```

Expected: in order — `## What This Skill Does`, `## Voice & vocabulary canonical source`, `## Position in the YouTube Workflow`, `## Inputs and Outputs`, `## Run Timing`, `## Description Anatomy`, `## The Process`, `## Failure Modes`, `## What This Skill Is NOT`, `## Companion Skills`, `## Reference Files`.

- [ ] **Step 6: Commit**

```bash
git add tcn-youtube-description/SKILL.md && git commit -m "feat(tcn-youtube-description): add failure modes, companion skills, and reference files sections"
```

---

## Task 6: Write `references/description-anatomy.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/references/description-anatomy.md`

The substantive new reference file. Three things go here that don't belong in the SKILL.md: (1) the Audit-Standard mechanism definition with worked examples; (2) channel-evergreen hashtag list as a single source of truth; (3) one full Dispatch 004 worked example walking from narration to final description. The SKILL.md references this file at drafting time.

- [ ] **Step 1: Write the file header and Audit-Standard mechanism definition**

```markdown
# description-anatomy.md

Living reference for `tcn-youtube-description`. Block-by-block decision rules, the Audit-Standard mechanism definition, channel-evergreen hashtag canon, and one full worked example. The SKILL.md references this file at drafting time.

---

## The Audit-Standard mechanism (description-only)

A sixth mechanism specific to the description hook surface, added to the five inherited from `../tcn-youtube-title/references/title-patterns.md`.

**Definition.** The hook proposes a known industry, regulatory, or institutional standard that the subject failed to meet. The first half names the standard; the second half names the gap.

**Why description-only?** Audit-Standard hooks need ~20-40 words to land — too long for a title (10-14 words) and too text-heavy for a thumbnail (3-6 words). The description's above-fold budget (200 chars / ~30-40 words) is the right surface for it.

**Distinct from:**
- **Specific Contradiction** — Audit-Standard anchors to an *external* standard the reader can verify (federal law, industry convention, regulatory floor). Specific Contradiction just states two contradicting facts without naming a standard.
- **Authority-Asymmetry** — Audit-Standard proposes what the standard *should have been*; Authority-Asymmetry just names who controls what.

**Worked examples:**

1. **Helium / Dispatch 004 (the canonical example).**
   - Hook: "Federal law requires McDonald's franchisees get a 200-page disclosure. Helium hotspot buyers got vibes."
   - Standard named: federal franchise disclosure (FTC Franchise Rule).
   - Gap named: zero disclosure for a $949 hardware buy-in with 10-20 year payback.

2. **Generic Fed-policy example.**
   - Hook: "Every Fed Chair since Volcker has briefed Congress quarterly. This one updated a blog."
   - Standard named: post-Volcker Fed communications convention.
   - Gap named: institutional-communications floor missed.

3. **Generic DePIN example.**
   - Hook: "Public companies file annual reports under penalty of perjury. This token project files vibes on Discord."
   - Standard named: SEC public-company disclosure regime.
   - Gap named: voluntary-but-marketed-as-rigorous reporting.

**When to use:** Justin's editorial frame is repeatedly "what disclosure / what audit / what standard would have caught this?" Audit-Standard surfaces that frame directly above the fold. Use when the dispatch's thesis is fundamentally about a missing institutional floor.

**When NOT to use:** if the dispatch is a debugging post-mortem (Personal-Implication fits better), a revenue-concentration receipt (Hidden Revenue fits better), or a "who controls X" piece (Authority-Asymmetry fits better).
```

- [ ] **Step 2: Append the channel-evergreen hashtag canon**

```markdown
---

## Channel-evergreen hashtag canon

The two constant tags appended to every dispatch's hashtag block:

- `#TheCivicNode`
- `#drinkYourOJ`

**Stability commitment.** These tags should NOT change without a deliberate channel-identity decision. The reason they exist as evergreens is to build channel-level discoverability over time — tags that appear on every dispatch accumulate weight in YouTube's hashtag-clustering signal.

**If a third evergreen is added** (e.g., as Justin's coverage stabilizes around a domain), append to this list with the date of the decision and the dispatch number where it first appeared. Do not retroactively edit prior artifacts.

**Format rules** (apply to dispatch-specific tags too):
- Sentence case for single-word: `#Helium`, `#Bluesky`.
- PascalCase / camelCase for multi-word: `#TheCivicNode`, `#NovaLabs`, `#HIP143`, `#drinkYourOJ`.
- No spaces, no punctuation. YouTube hashtags honor `[A-Za-z0-9_]` only.
- Lowercase numbers and letters are fine; ALL-CAPS is banned.
```

- [ ] **Step 3: Append channel link block boilerplate canon**

```markdown
---

## Channel link block canon

Default Substack URL: `https://drinkyouroj.substack.com`
Default Bluesky URL: `https://bsky.app/profile/thecivicnode.bsky.social`

Both are overrideable per-invocation. Update this canon if Justin moves handles.

Default boilerplate text:

\`\`\`
-- THE CIVIC NODE --
Weekly. No hype.

Substack:  https://drinkyouroj.substack.com
Bluesky:   https://bsky.app/profile/thecivicnode.bsky.social
\`\`\`

The two-space alignment between `Substack:`/`Bluesky:` and the URLs is decorative. YouTube collapses to single-space at render time.
```

- [ ] **Step 4: Append the fuzzy-match threshold rule for transcript chapter timestamps**

```markdown
---

## Transcript fuzzy-match threshold (chapter timestamps)

When mining `.srt` for chapter timestamps post-record, fuzzy-match the first 4-6 words of each narration slide's opener against the transcript text. Recommended thresholds:

- **High confidence (use timestamp):** Levenshtein ratio ≥ 0.85 OR exact word-sequence match.
- **Medium confidence (use timestamp + warning):** Levenshtein ratio 0.7-0.85. Surface a one-line metadata note: `slide N matched at medium confidence; verify timestamp`.
- **Low confidence (fall back to narration estimate):** Levenshtein ratio < 0.7. Use narration WPM math for that slide; surface metadata note: `slide N not located in transcript; using estimated timestamp`.

This threshold tolerates light improv during recording while catching genuinely abandoned passages (which deserve user attention before publishing).
```

- [ ] **Step 5: Append the Dispatch 004 worked example**

```markdown
---

## Worked example — Dispatch 004 ("You Own the Hotspot")

Input narration: `workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md` (8 slides, 5:11 runtime, 727 words at 140 wpm).

Paired title (hypothetical): "Buy a Helium hotspot. Nova Labs sets the price." (Authority-Asymmetry mechanism)
Paired thumbnail headline (hypothetical): "Vibes ≠ Disclosure" (Specific-Contradiction mechanism)

**Orthogonal mechanism choice for description hook:** title runs Authority-Asymmetry, thumbnail runs Specific-Contradiction. Description hook must run something else. **Audit-Standard fits the dispatch concept best** — the article's whole frame is "the four disclosures Helium operators should have received."

**Block 1 (hook punch):**

\`\`\`
Federal law requires McDonald's franchisees get a 200-page disclosure.
385,000 Helium hotspot buyers got vibes.
\`\`\`

(150 chars total. Audit-Standard mechanism. Bare numeral "385,000" not spelled out, matching description-vs-narration rule.)

**Block 3 (summary):**

\`\`\`
After the August 2025 halving, a Helium hotspot earns $4-$8/month. The hardware costs $949. The pricing that determines the payback is set by Nova Labs, the same company that voted itself 26% of the HIP-143 ballot that handed it pricing authority. The piece on Substack walks the four disclosures Helium operators should have received, the HIP-148 vote that traded subscriber rewards for gift cards, and the Datagram debug that broke the author's own counter-example.
\`\`\`

(498 chars. Front-loads anchors: $4-$8, $949, 26%, HIP-143, HIP-148, Datagram. References cuts from the article. Ends on a click-motivator.)

**Block 5 (article CTA):**

\`\`\`
→ Read the full piece on Substack:
https://drinkyouroj.substack.com/p/you-own-the-hotspot-nova-labs-owns-what-it-earns
\`\`\`

**Block 7 (chapters, pre-record estimate at 140 wpm):**

\`\`\`
-- CHAPTERS --
0:00  The McDonald's standard
0:38  What Helium operators bought
1:09  The unit math after the halving
2:01  How the pricing vote extended itself
2:54  Who actually controlled the vote
3:47  The audit standard that catches this
4:34  What the article covers that this video doesn't
5:02  Subscribe at drinkyouroj.substack.com
\`\`\`

(Eight chapters, one per narration slide. End slide included. Viewer-rewritten labels at 8/10 register.)

**Block 9 (channel link block):** canon boilerplate, no changes.

**Block 11 (hashtags):**

\`\`\`
#Helium #DePIN #NovaLabs #HIP143 #HIP148 #TheCivicNode #drinkYourOJ
\`\`\`

(7 tags: 5 dispatch-specific proper nouns + 2 channel-evergreens. Sentence-case PascalCase. Dispatch-specific tags first.)

**Total assembled description: ~1,650 chars** including dividers and blank lines. Well within the 1,500-2,500 target.

**Metadata block written to artifact:**

\`\`\`
**Generated:** 2026-05-21
**Source:** narration (timestamps estimated)
**Article URL:** https://drinkyouroj.substack.com/p/you-own-the-hotspot-nova-labs-owns-what-it-earns
**Paired title:** "Buy a Helium hotspot. Nova Labs sets the price."
**Paired title mechanism:** Authority-Asymmetry
**Paired thumbnail headline:** "Vibes ≠ Disclosure"
**Paired thumbnail mechanism:** Specific-Contradiction
**Description hook mechanism:** Audit-Standard
\`\`\`
```

- [ ] **Step 6: Verify file is well-formed**

```bash
wc -l /Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/references/description-anatomy.md
grep -n "^## " /Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/references/description-anatomy.md
```

Expected line count: ~150-200 lines. Expected sections: `## The Audit-Standard mechanism`, `## Channel-evergreen hashtag canon`, `## Channel link block canon`, `## Transcript fuzzy-match threshold`, `## Worked example — Dispatch 004`.

- [ ] **Step 7: Commit**

```bash
git add tcn-youtube-description/references/description-anatomy.md && git commit -m "feat(tcn-youtube-description): add description-anatomy reference (Audit-Standard mechanism + Dispatch 004 worked example)"
```

---

## Task 7: Smoke test — invoke the skill against Dispatch 004

**Files:**
- Read: `/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md`
- Read: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md`
- Read: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/references/description-anatomy.md`

Manual coherence check. The agent walks through the skill's documented process against the on-disk Dispatch 004 narration and verifies each step's output would match the documented behavior. No actual artifact is written in this task — purely a behavior-trace.

- [ ] **Step 1: Read all three files into context**

Open the narration, SKILL.md, and references/description-anatomy.md.

- [ ] **Step 2: Walk through Process Step 1 (auto-detect source)**

Verify: does the supplied directory contain `youtube-narration.md`? Yes. Are there `.srt` or `.txt` transcripts? Check via `ls` — if no transcript, source = narration. Confirm the skill would correctly default to narration mode.

```bash
ls "/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/" | grep -iE '\.(srt|txt)$'
```

Expected: no transcript files (Dispatch 004 has not been recorded yet). Skill would run in pre-record mode.

- [ ] **Step 3: Walk through Process Step 2 (paired artifacts)**

Check for `youtube-title.md` and `youtube-thumbnail.md` in the same directory.

```bash
ls "/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/" | grep -E '(title|thumbnail)\.md$'
```

If either is missing, confirm the skill would log soft warnings and proceed with degraded orthogonality. If both are present, confirm the skill would extract mechanisms. Either outcome is acceptable for smoke-test purposes — verify the documented behavior matches.

- [ ] **Step 4: Walk through Process Step 3 (URL derivation)**

The slug is `you-own-the-hotspot-nova-labs-owns-what-it-earns`. Apply sanity checks:
- Length: 49 chars (≤80 ✓)
- Underscores: no ✓
- Uppercase: no ✓
- Chars in `[a-z0-9-]`: yes ✓

Constructed URL: `https://drinkyouroj.substack.com/p/you-own-the-hotspot-nova-labs-owns-what-it-earns` — matches the user-provided URL exactly. Skill would surface confirmation gate; user would confirm.

- [ ] **Step 5: Walk through Process Steps 4-9 against the narration content**

For each block (1, 3, 5, 7, 9, 11), verify the documented drafting logic produces output that matches the worked example in `references/description-anatomy.md`. If the worked example matches the documented process, this is a structural pass.

Specifically check:
- Block 1: Audit-Standard mechanism applied? (worked example: yes ✓)
- Block 3: mines *Cuts from the article*? (narration has the field at lines 187-195 ✓)
- Block 5: bare URL + arrow prefix? (worked example: yes ✓)
- Block 7: 8 chapters at 140 wpm estimated timestamps? (worked example: yes ✓, end-slide included)
- Block 9: canon boilerplate? (yes ✓)
- Block 11: 5-7 hashtags with channel evergreens? (worked example: 7 tags ✓)

- [ ] **Step 6: Verify length budget**

The worked example claims ~1,650 chars total. Verify this matches the per-block budgets in the SKILL.md (sum: 150 + 498 + ~150 + ~350 + ~150 + ~75 = ~1,373 chars, plus dividers and blank lines = ~1,500-1,700 chars).

Expected: budget aligns with claim.

- [ ] **Step 7: Report any divergences to the user**

If any of steps 2-6 reveal a divergence between the documented behavior and what the worked example would actually produce, flag to the user. If everything aligns, report: `Smoke test passed: Dispatch 004 narration traces cleanly through all 11 process steps; SKILL.md behavior matches references/description-anatomy.md worked example.`

- [ ] **Step 8: No commit** — smoke test is read-only.

---

## Task 8: Final review + capture remaining open questions

**Files:**
- Modify (if needed): `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md`
- Modify (if needed): `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/references/description-anatomy.md`

Final read-through. Catch typos, broken section references, dead links. Make sure cross-skill reference paths are correct.

- [ ] **Step 1: Verify all cross-skill reference paths resolve**

```bash
ls /Users/justin/CascadeProjects/claude-skills/tcn-youtube-title/references/title-patterns.md
ls /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md
```

Expected: both files exist. If either is missing (the title-patterns.md file was committed in dispatch 004's session per the activity log; the thumbnail-headline-patterns.md is in the git status as M), confirm with a `git show HEAD:<path>` if not currently committed.

- [ ] **Step 2: Verify SKILL.md is end-to-end coherent**

Read the full SKILL.md top to bottom. Check for:
- Broken `### Block N` references between sections.
- Inconsistent terminology (e.g., "hook punch" vs "hook line" vs "above-fold hook" — pick one and stay consistent; the spec uses "hook punch" in §4 and "above-fold hook" in §5).
- Missing companion-skill references in the description frontmatter description field.

Apply edits inline if any issues found.

- [ ] **Step 3: Verify the runtime symlink resolves**

```bash
ls -la ~/.claude/skills/tcn-youtube-description/SKILL.md
```

Expected: shows the symlink target as `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-description/SKILL.md`. If broken, repair with `ln -sf`.

- [ ] **Step 4: Final commit**

If any inline fixes were applied in Step 2:

```bash
git add tcn-youtube-description/ && git commit -m "fix(tcn-youtube-description): final review consistency pass"
```

If no fixes needed, skip the commit.

- [ ] **Step 5: Surface remaining open questions from spec §11 to the user**

Re-read spec §11. For each open question:
1. `.srt` fuzzy-matching threshold → resolved in `references/description-anatomy.md` (Task 6 Step 4) ✓
2. Channel-evergreen hashtag list → resolved in `references/description-anatomy.md` (Task 6 Step 2) ✓
3. Bluesky URL default → resolved in `references/description-anatomy.md` (Task 6 Step 3) ✓
4. Pre-record vs post-record artifact lifecycle → not resolved; flag to user
5. Audit-Standard mechanism definition → resolved in `references/description-anatomy.md` (Task 6 Step 1) ✓

Surface to user: `Implementation complete. One spec open-question remains unresolved by the build: pre-record vs post-record artifact lifecycle (silent overwrite vs versioned files). Recommend silent overwrite to match title skill pattern. Want this documented in SKILL.md, or leave it implicit?`

Wait for user response before declaring the task fully done.

---

## Self-review

After writing this plan, I checked it against the spec:

**Spec coverage:**
- §1 (purpose) → Task 2 Step 2 ✓
- §2 (workflow position) → Task 2 Step 4 ✓
- §3 (inputs/outputs) → Task 2 Step 5 ✓
- §4 (anatomy) → Task 3 (all 11 blocks + length budgets + dividers) ✓
- §5 (process) → Task 4 (all 11 steps) ✓
- §6 (voice & shared refs) → Task 2 Step 3 + Task 5 Step 3 ✓
- §7 (failure modes) → Task 5 Step 1 ✓
- §8 (what skill is NOT) → Task 5 Step 2 ✓
- §9 (companion skills) → Task 5 Step 3 ✓
- §10 (reference files) → Task 5 Step 4 + Task 6 ✓
- §11 (open questions) → Task 6 (4 of 5 resolved) + Task 8 Step 5 (surface remaining one) ✓

**Placeholder scan:** no TBDs, no "implement later", no "similar to Task N." Each step shows the actual content the engineer needs to write.

**Type / terminology consistency:** the spec uses "hook punch" in §4 block 1 and "above-fold hook" in §5 step 5. Task 8 Step 2 explicitly catches this and resolves to one term. Plan uses "above-fold hook" in process steps to match spec §5 wording.

**One drift caught:** spec §3 metadata block references "Paired title" and "Paired thumbnail headline" fields. Plan Task 2 Step 5 reproduces these correctly. ✓
