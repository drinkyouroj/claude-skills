# tcn-facebook-post Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new sister skill `tcn-facebook-post` that produces one Facebook post per day for The Civic Node, integrated into the existing `tcn-content-plan` orchestrator with weekday-rotating purpose, purpose-driven shape and image source, and a Flagship-CTA link on Friday article-publish days.

**Architecture:** New sister skill at `/Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/` mirroring the structure of `tcn-post` and `tcn-substack-notes`. Two canonical reference files (`purpose-table.md`, `voice-register.md`). Integration into `tcn-content-plan` via one extended step (Step 3, purpose lookup), one new step (Step 7.5, dispatch), and edits to Steps 9, 10, Mode 1, Mode 3, plus the posting-rules reference. No code — all markdown. Verification is grep/wc on the resulting files plus reading each commit diff.

**Tech Stack:** Markdown files (Obsidian-compatible). No build, no tests, no runtime — these are skill specifications. Verification = textual checks on the written files.

**Spec reference:** [docs/superpowers/specs/2026-05-21-tcn-facebook-post-design.md](../specs/2026-05-21-tcn-facebook-post-design.md)

---

## File Structure

**Files to create:**
- `tcn-facebook-post/SKILL.md` — main skill spec (frontmatter, identity, inputs/outputs, process, voice, shelf-life, image guidance, quality bar)
- `tcn-facebook-post/CLAUDE.md` — minimal session-history pointer (mirrors other TCN skills)
- `tcn-facebook-post/references/purpose-table.md` — canonical purpose × shape × image × voice × CTA matrix + weekday rotation appendix
- `tcn-facebook-post/references/voice-register.md` — FB-Explainer voice register doc with examples

**Files to modify:**
- `tcn-content-plan/SKILL.md` — Step 3 extension, new Step 7.5, Step 9 file-structure changes, Step 10 audit changes, frontmatter additions, schedule table, Status block, Mode 1, Mode 3, quality bar
- `tcn-content-plan/references/posting-rules.md` — new Facebook row in Platform Windows table; new Facebook Rules section

**Each file changes together with its companion test (verification step). Each task = one atomic commit.**

---

## Task 1: Scaffold `tcn-facebook-post` directory and SKILL.md frontmatter

**Files:**
- Create: `tcn-facebook-post/SKILL.md`
- Create: `tcn-facebook-post/CLAUDE.md`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/references
```

- [ ] **Step 2: Write SKILL.md with frontmatter and identity section**

Write to `/Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/SKILL.md`:

```markdown
---
name: tcn-facebook-post
description: >
  Draft a daily Facebook post for The Civic Node (TCN) — one post per day, plain-English
  voice, image-forward, image-required on caption-shape posts. Sister skill invoked by
  tcn-content-plan Step 7.5. Use this skill whenever the user (or the orchestrator) asks
  for "the FB post", "facebook copy", "today's facebook post", "draft the FB for [date]",
  "facebook caption", "facebook paragraph", or any TCN Facebook content. Also use when the
  orchestrator delegates Step 7.5 of Mode 2 with a purpose label. Produces 2-3 options per
  slot, each tagged Safe / News-dependent, each with concrete image guidance (AI prompt,
  Substack hero URL, or screenshot recommendation). Does NOT own the weekday rotation
  (tcn-content-plan does), does NOT own the monthly-plan override (tcn-content-plan does),
  does NOT replace tcn-post or tcn-substack-notes (those run on different surfaces).
---

# tcn-facebook-post

The Facebook drafting skill for The Civic Node. One FB post per day, seven days a week. Plain-English voice, low cognitive load, image-forward — calibrated for an audience used to scrolling kitten pictures, not parsing analytical takes.

This skill is invoked by `tcn-content-plan` Step 7.5 in Mode 2 (Create Daily Plan). It can also be invoked directly if the user just wants today's FB post without a full daily plan.

## What this skill owns

- FB-Explainer voice rules (see `references/voice-register.md`)
- Purpose → shape mapping (caption vs. paragraph)
- Purpose → image-source mapping (see `references/purpose-table.md`)
- Option generation (2-3 options per slot)
- Shelf-life labeling (Safe / News-dependent — two-state, NOT the three-state Frame-forward/Data-forward/Conditional used for X and Notes)
- Image prompt drafting (delegates to `ai-image-prompts-skill` for AI-generated; constructs prompt text directly)

## What this skill does NOT own

- The weekday rotation lookup (`tcn-content-plan` owns)
- The monthly-plan `FB:` override (`tcn-content-plan` reads this from the 30-day map)
- The X copy, Substack Note copy, or LinkedIn copy
- The schedule table or Status block formatting (`tcn-content-plan` owns the daily plan file)
- Voice-passes on other surfaces — `tcn-text-humanizer` handles X/Notes; this skill is self-contained on voice
```

- [ ] **Step 3: Write CLAUDE.md**

Write to `/Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/CLAUDE.md`:

```markdown
# tcn-facebook-post — Session History

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->
```

- [ ] **Step 4: Verify files landed and frontmatter is valid**

Run:
```bash
ls -la /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/
head -20 /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/SKILL.md
```

Expected: directory exists with SKILL.md, CLAUDE.md, and references/ subdirectory; SKILL.md frontmatter starts with `---` and contains `name: tcn-facebook-post`.

- [ ] **Step 5: Commit**

```bash
git add tcn-facebook-post/SKILL.md tcn-facebook-post/CLAUDE.md
git commit -m "feat(tcn-facebook-post): scaffold skill with frontmatter and identity"
```

---

## Task 2: Write `references/purpose-table.md`

**Files:**
- Create: `tcn-facebook-post/references/purpose-table.md`

- [ ] **Step 1: Write the purpose table reference file**

Write to `/Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/references/purpose-table.md`:

```markdown
# Facebook Purpose Table — Reference

Canonical mapping for FB post purpose → shape → image source → voice notes → CTA rule. This is the single source of truth referenced by `tcn-facebook-post/SKILL.md` and `tcn-content-plan/references/posting-rules.md`.

## The four purposes

| Purpose | Shape | Image source | Voice notes | CTA rule |
|---|---|---|---|---|
| **Awareness** | Caption (≤30 words) | AI-generated (via `ai-image-prompts-skill`) | Soft, observational. Drop closed em dashes entirely. One warmth-marker max ("honestly," / "look," / "the thing is"). No edge. | No link |
| **Engagement** | Caption (≤30 words) | AI-generated | Question-framing or "tell me in the comments" pattern. Active second person OK. Designed for FB algorithm comment-signal. | No link |
| **Soft funnel** | Paragraph (50-80 words) | Substack article hero from the older piece referenced (URL specified in monthly plan's `Brief note` cell, or surfaced by `tcn-content-plan` Step 1 prompt when no monthly entry) — AI-generated fallback only if no usable hero exists | Slight authority. 1 closed em dash max. Plain-English summary of the older piece's argument. | Soft link: "wrote about this back in [month] — [link]" |
| **Flagship CTA** | Paragraph (50-80 words) | Substack article hero (today's piece) | Slight authority. Plain-English tagline of the flagship's argument. No "predictably," "naturally," "of course." | Hard link at end: "Full piece: [link]" |

## Shape rules

### Caption (Awareness, Engagement)

- ≤30 words total
- Image is **required** — no caption ships without an image
- Closed em dashes: forbidden (read as trying-too-hard at this length)
- Sentences: 1-3 short ones
- No CTA, no link
- One warmth-marker max ("honestly," / "look," / "the thing is")

### Paragraph (Soft funnel, Flagship CTA)

- 50-80 words total (hard fail outside this range)
- Image is recommended (Substack hero preferred); not strictly required if no hero exists
- Closed em dashes: max 1 per post
- Sentences: 2-4
- CTA placement: end of post, on its own line for Flagship CTA; inline for Soft funnel

## Image source rules

### AI-generated (Awareness, Engagement)

Invoke `ai-image-prompts-skill` to draft the prompt. The prompt must:
- Be ≤80 words
- Reference the post's subject concretely (numbers visible, scene specific)
- Avoid generic stock-photo language ("business people in a meeting," "abstract concept of growth")
- Be safe for Facebook's content policies (no political party logos, no copyrighted figures by name without context)

### Substack hero (Soft funnel, Flagship CTA)

- Flagship CTA: the article's published hero image, fetched from the published article URL
- Soft funnel: the older referenced piece's hero, URL specified in monthly plan
- If hero image not available, fall back to AI-generated (surface the gap in the recommendation)

### Stock-photo fallback

Triggered only if:
- `ai-image-prompts-skill` is not available
- Substack hero not retrievable

Format: a one-line search-query suggestion ("freeway gridlock at dusk, no logos") that Justin pastes into Unsplash/Pexels.

## Weekday rotation (default)

Used by `tcn-content-plan` Step 3 when the monthly plan's `FB:` cell is absent.

| Day | Purpose | Rationale |
|---|---|---|
| Monday | Awareness | Week opens soft — plain observation about weekend or week ahead. |
| Tuesday | Engagement | Tuesday FB engagement historically strong; comment signal early in the week. |
| Wednesday | Awareness | Mid-week observation. Wednesday is also paid Substack note day — deliberately not funneling so the two don't compete. |
| Thursday | Soft funnel | Tease Friday's flagship — "writing about X for Friday." |
| Friday | Flagship CTA | Article link + plain-English tagline. Hard funnel. |
| Saturday | Awareness | Weekend FB usage high but cognitive load low. |
| Sunday | Soft funnel | Resurface older Substack piece relevant to the week's news. |

## Posting time defaults

| Purpose | Default posting time | Fallback |
|---|---|---|
| Awareness | 09:00 ET | 19:00-21:00 ET |
| Engagement | 09:00 ET (high engagement window) | 19:00-21:00 ET |
| Soft funnel | 09:00 ET | 19:00-21:00 ET |
| Flagship CTA | 11:00-13:00 ET (must be after article publishes) | Same-day evening if AM missed |

Hard rule: never post Flagship CTA before the article is live. Out-of-order publishing breaks the funnel.
```

- [ ] **Step 2: Verify the file landed and the rotation table is complete**

Run:
```bash
grep -c '^| ' /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/references/purpose-table.md
```

Expected: at least 25 table rows (4 purposes × 2 tables + 7 weekdays + 4 posting times + headers ≈ 27).

- [ ] **Step 3: Commit**

```bash
git add tcn-facebook-post/references/purpose-table.md
git commit -m "feat(tcn-facebook-post): add purpose-table reference (purpose matrix + weekday rotation + posting times)"
```

---

## Task 3: Write `references/voice-register.md`

**Files:**
- Create: `tcn-facebook-post/references/voice-register.md`

- [ ] **Step 1: Write the voice register reference file**

Write to `/Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/references/voice-register.md`:

```markdown
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
```

- [ ] **Step 2: Verify the file landed and the examples are complete**

Run:
```bash
grep -c '^> ' /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/references/voice-register.md
```

Expected: 4 example blockquotes (one per shape × purpose example).

- [ ] **Step 3: Commit**

```bash
git add tcn-facebook-post/references/voice-register.md
git commit -m "feat(tcn-facebook-post): add voice-register reference (FB-Explainer register + examples + fallback)"
```

---

## Task 4: Add inputs, outputs, and dispatch logic to SKILL.md

**Files:**
- Modify: `tcn-facebook-post/SKILL.md` (append sections)

- [ ] **Step 1: Append the Inputs section**

Read the current SKILL.md, then append after the existing "What this skill does NOT own" section:

```markdown

---

## Inputs

When invoked by `tcn-content-plan` Step 7.5, this skill receives:

1. **`purpose`** — one of: `Awareness`, `Engagement`, `Soft funnel`, `Flagship CTA`. Required. The orchestrator derives this from the day's `facebook_purpose:` frontmatter (set in Step 3 of Mode 2).
2. **`source_material`** — conditional on purpose:
   - **Funnel/Flagship:** the day's X standalone option text (from Step 5 output) + flagship article URL + flagship article tagline (when available)
   - **Awareness/Engagement:** today's live news (from Step 1 of Mode 2) + FRESH list (from Step 2 duplication audit)
3. **`spent_list`** — the SPENT list from Step 2 of Mode 2. Required. Used to avoid echoing what other surfaces already said.
4. **`flagship_url`** — present only on Flagship CTA and Soft funnel days. The full URL of the article being linked.
5. **`date`** — today's date (YYYY-MM-DD) for the schedule slot.

When invoked directly (not via the orchestrator), prompt the user for any missing inputs before drafting.

## Outputs

A markdown block in the following structure, returned to the orchestrator for insertion into the daily plan file under `## Facebook`:

\`\`\`markdown
**Purpose:** [Awareness | Engagement | Soft funnel | Flagship CTA]
**Shape:** [Caption | Paragraph]
**Posting time:** [HH:MM ET]

### Option A — [Safe | News-dependent]
[FB post prose]

**Image:** [concrete instruction — AI prompt text, Substack hero URL, or screenshot recommendation]

### Option B — [Safe | News-dependent]
[FB post prose]

**Image:** [concrete instruction]

### Option C — [Safe | News-dependent]
[FB post prose]

**Image:** [concrete instruction]

**Recommendation:** [one sentence — default option + conditional logic if any option is News-dependent]
\`\`\`

Always produce 2-3 options. Single-option output is a quality-bar failure.
```

- [ ] **Step 2: Verify the appended sections parse**

Run:
```bash
grep -E '^## (Inputs|Outputs)' /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/SKILL.md
```

Expected: both `## Inputs` and `## Outputs` headers present.

- [ ] **Step 3: Commit**

```bash
git add tcn-facebook-post/SKILL.md
git commit -m "feat(tcn-facebook-post): add inputs and outputs sections to SKILL.md"
```

---

## Task 5: Add the process steps to SKILL.md

**Files:**
- Modify: `tcn-facebook-post/SKILL.md` (append the Process section)

- [ ] **Step 1: Append the Process section**

Append after the Outputs section:

```markdown

---

## Process

Follow these steps in order. Do not skip the voice loading or the duplication check — those determine what the options can and can't say.

### Step 1: Load voice context

If `workspace/core/anti-ai-writing-style.md` is present in the active project's root, read it once. This is the canonical source for banned vocabulary, negative parallelisms, vocabulary cliff, and closing-line rules. Keep it in working context for the duration of this skill invocation.

If the file is missing, apply the voice fallback per `references/voice-register.md` § Voice fallback. Do NOT proceed with vocabulary-substitution heuristics from training data.

Also read `references/voice-register.md` and `references/purpose-table.md` if not already loaded.

### Step 2: Look up shape, image source, and CTA rule

Use the `purpose` input to look up the row in `references/purpose-table.md`:
- `shape` — Caption (≤30 words) or Paragraph (50-80 words)
- `image_source` — AI-generated / Substack hero / fallback
- `cta_rule` — No link / Soft link / Hard link
- `voice_notes` — purpose-specific voice notes (e.g., "drop closed em dashes entirely" for Awareness captions)

### Step 3: Derive the angle

Conditional on purpose:

**Funnel/Flagship days** — read the X standalone copy from `source_material`. Identify the single sharpest claim or framing. Restate it in FB-Explainer voice: drop the X compression, drop the analytical fingerprints, expand to a plain-English sentence a non-political-junkie can absorb. The FB post is NOT a copy of the X post; it's a re-voicing of the same anchor claim for a different reader.

**Awareness/Engagement days** — read the live news and FRESH list from `source_material`. Find one specific fact (number, name, date, quote) that's plain-language interesting on its own — something a friend at a barbecue might bring up. The FB post is not a take; it's an observation. For Engagement, frame it as a question or invite a response.

In both cases, audit against the `spent_list`: if the angle echoes what X or Notes already said this week, find a different angle.

### Step 4: Draft 2-3 options

For each option:
1. Write the prose at the target word count (caption ≤30 words / paragraph 50-80 words). Hard fail outside range.
2. Apply the voice rules from `voice-register.md`:
   - Hard rules (banned vocab, negative parallelisms, vocabulary cliff, closing-line, no vague placeholder verbs)
   - Length-relaxed rules (closed em dashes per length; copulative-avoidance off; sardonic moves off)
3. Determine the shelf-life label:
   - **Safe** — postable today regardless of how the news breaks. Default for Awareness, most Engagement, most Soft funnel.
   - **News-dependent** — depends on a specific event happening before posting time (court ruling, vote outcome, deal announcement). Note the specific dependency inline.
4. Construct image guidance:
   - **AI-generated:** invoke `ai-image-prompts-skill` with the option's anchor concept; capture its returned prompt as the image guidance text. If `ai-image-prompts-skill` is unavailable, output a stock-photo search-query suggestion and surface the gap.
   - **Substack hero (Flagship CTA):** if `flagship_url` is provided, output `Use Substack hero from [flagship_url]`. If URL is `[ARTICLE_URL_PENDING]`, output the same with a hard reminder that the URL must be inserted before posting.
   - **Substack hero (Soft funnel):** output `Use Substack hero from [older-piece-url]` where the URL comes from the monthly plan's `Brief note` cell. If absent, fall back to AI-generated and surface the gap.

Aim for genuine variation across options — different angles, not different word choices on the same angle.

### Step 5: Write the recommendation

One sentence that names the default option and any conditional logic. Examples:

- All Safe: `"Default to Option A (Frame-forward Soft); B and C are alternates if the framing in A feels off."`
- Mixed shelf-life: `"Default to Option A (Safe); switch to Option B (News-dependent on ruling at 11am) if the court releases its decision before posting time."`

If all options are News-dependent and the trigger may not fire, the recommendation defaults to: `"Hold the FB post today if no trigger fires before the posting window."`

### Step 6: Assemble and return

Format the output per the Outputs section. Return as a markdown block. The orchestrator handles file insertion.
```

- [ ] **Step 2: Verify the Process section is well-formed**

Run:
```bash
grep -E '^### Step [1-6]' /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/SKILL.md
```

Expected: six step headers (Step 1 through Step 6).

- [ ] **Step 3: Commit**

```bash
git add tcn-facebook-post/SKILL.md
git commit -m "feat(tcn-facebook-post): add 6-step process section to SKILL.md"
```

---

## Task 6: Add the quality bar to SKILL.md

**Files:**
- Modify: `tcn-facebook-post/SKILL.md` (append Quality bar section)

- [ ] **Step 1: Append the Quality bar section**

Append after the Process section:

```markdown

---

## Quality bar

An FB post option works when:

- **Shape match:** caption ≤30 words OR paragraph 50-80 words. Outside range = hard fail.
- **Image guidance is concrete:** an actual AI prompt, a specific URL, or a specific screenshot recommendation. "Find an image" = hard fail.
- **Shelf-life label present:** Safe or News-dependent, with a specific dependency phrase if News-dependent.
- **No vague placeholder verbs:** "hit a number," "saw movement," "raised concerns," "made waves," "had a moment" = hard fail. See `references/voice-register.md` § Hard rule.
- **No banned vocabulary** from `workspace/core/anti-ai-writing-style.md` § 3A (when the file is present).
- **No negative parallelisms** ("not X, but Y" constructions).
- **Vocabulary cliff fully glossed:** every term requiring beat-specific context is glossed inline. No unglossed acronyms.
- **No closing-line abstraction:** end on a fact or question, not a Big Truth.
- **Closed em dashes per length:** zero at caption length; max one at paragraph length.
- **Voice-marker discipline:** captions allow one warmth-marker ("honestly," / "look," / "the thing is") max. Paragraphs allow zero.
- **Specific anchor present:** a number, name, date, or direct quote. Posts without one tend to read as AI-filler.
- **CTA matches purpose:** Awareness/Engagement = no link; Soft funnel = inline soft link; Flagship CTA = hard link on its own line at end.
- **Two or three options provided, not one.** Single-option output is a quality-bar failure.
- **Recommendation names conditional logic explicitly** if any option is News-dependent.

## Failure modes to watch for

- **The "translation tax" failure** (Funnel/Flagship days): rewriting the X post into plain English by just substituting simpler words. Real FB rewrite drops the analytical compression entirely and writes from scratch for a different reader.
- **The "wikipedia voice" failure** (Awareness days): writing flat factual statements with no warmth. FB-Explainer is plain but not dry. One warmth-marker per caption fixes this.
- **The "Substack leak" failure** (any day): closed em dashes, "of course," "naturally," copulative avoidance bleeding through from the canonical voice file. Re-check against `voice-register.md` § What relaxes.
- **The "stock photo abstraction" failure** (caption days): AI image prompts that describe abstract concepts ("inflation visualization") instead of concrete scenes. Concrete scenes with specific anchors (a grocery receipt, a Treasury bond, a Virginia data center) outperform.
- **The "click-bait CTA" failure** (Flagship CTA days): writing "you won't believe what we found" or "must-read" framings to drive clicks. These read as low-trust and tank reach. Plain-English tagline > engagement bait.
```

- [ ] **Step 2: Verify the quality bar list is comprehensive**

Run:
```bash
grep -c '^- \*\*' /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/SKILL.md
```

Expected: at least 14 bolded bullets (covering shape, image, shelf-life, vague verbs, banned vocab, negative parallelisms, vocabulary cliff, closing-line, em dashes, warmth markers, anchor, CTA, options count, recommendation).

- [ ] **Step 3: Commit**

```bash
git add tcn-facebook-post/SKILL.md
git commit -m "feat(tcn-facebook-post): add quality bar and failure modes to SKILL.md"
```

---

## Task 7: Wire `tcn-facebook-post` into `tcn-content-plan` Step 3 (purpose lookup)

**Files:**
- Modify: `tcn-content-plan/SKILL.md` (extend Step 3 of Mode 2)

- [ ] **Step 1: Read the current Step 3 section**

Run:
```bash
grep -n "Step 3:" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Note the line range of Step 3.

- [ ] **Step 2: Edit Step 3 to add FB purpose lookup**

Use Edit to replace the existing Step 3 section. Find:

```markdown
### Step 3: Look up format assignments

Read `workspace/plans/tcn-notes-30-day-map.md` and find the entry for the target date to get that day's assigned formats. If the monthly plan doesn't exist or doesn't specify formats:
- Don't repeat the same format combination used in the prior 2 days
- Include at least one Primary Source Drop per 3-day window
- Reserve Article Tease for flagship publish days (typically Fridays when an article goes live)
- Reserve Cross-Domain Connection for days when two genuinely parallel stories exist in different domains

Load `references/note-formats.md` for format definitions before drafting.
```

Replace with:

```markdown
### Step 3: Look up format assignments and FB purpose

**Note formats:** Read `workspace/plans/tcn-notes-30-day-map.md` and find the entry for the target date to get that day's assigned formats. If the monthly plan doesn't exist or doesn't specify formats:
- Don't repeat the same format combination used in the prior 2 days
- Include at least one Primary Source Drop per 3-day window
- Reserve Article Tease for flagship publish days (typically Fridays when an article goes live)
- Reserve Cross-Domain Connection for days when two genuinely parallel stories exist in different domains

Load `references/note-formats.md` for format definitions before drafting.

**Facebook purpose:** From the same monthly plan entry, read the `FB:` cell. If present, use its value (one of: `Awareness`, `Engagement`, `Soft funnel`, `Flagship CTA`). If absent or the monthly plan doesn't exist, fall back to the weekday rotation:

| Day | Default purpose |
|---|---|
| Monday | Awareness |
| Tuesday | Engagement |
| Wednesday | Awareness |
| Thursday | Soft funnel |
| Friday | Flagship CTA |
| Saturday | Awareness |
| Sunday | Soft funnel |

(Canonical table with rationale lives in `tcn-facebook-post/references/purpose-table.md` § Weekday rotation.)

Set `facebook_purpose:` in the daily plan frontmatter to the determined value.

**Override prompt:** If the weekday rotation says Awareness or Engagement but the live news from Step 1 strongly suggests funnel opportunity (a flagship-relevant story breaking), surface to the user: `"Today's rotation is [Awareness/Engagement], but the live news pulls toward funnel. Override to Soft funnel? (y/n)"`. If yes, set `facebook_purpose: "Soft funnel"`.
```

- [ ] **Step 3: Verify Step 3 now references FB**

Run:
```bash
grep -A 2 "Facebook purpose:" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Expected: the new "Facebook purpose:" subsection appears, followed by the lookup logic.

- [ ] **Step 4: Commit**

```bash
git add tcn-content-plan/SKILL.md
git commit -m "feat(tcn-content-plan): extend Step 3 with Facebook purpose lookup and weekday rotation fallback"
```

---

## Task 8: Add Step 7.5 (FB drafting) to `tcn-content-plan`

**Files:**
- Modify: `tcn-content-plan/SKILL.md` (insert new Step 7.5 between Step 7 and Step 8)

- [ ] **Step 1: Locate the insertion point**

Run:
```bash
grep -n "^### Step [78]" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Note the line numbers for Step 7 and Step 8.

- [ ] **Step 2: Insert Step 7.5 before Step 8**

Use Edit to insert before `### Step 8: Draft engagement notes`:

```markdown
### Step 7.5: Draft the Facebook post (delegate to `tcn-facebook-post`)

Invoke the `tcn-facebook-post` skill via the Skill tool. The dispatch depends on the day's `facebook_purpose:` value:

**Funnel/Flagship days** (`Soft funnel` or `Flagship CTA`) — sequential dispatch: wait for Step 5 output (X standalone copy) before invoking. Pass:
- `purpose` — from frontmatter
- `source_material` — the X standalone option text from Step 5 + the flagship article URL + the flagship article tagline (if available)
- `spent_list` — from Step 2
- `flagship_url` — the article URL (for Flagship CTA, today's article; for Soft funnel, the older referenced piece from the monthly plan)
- `date` — today's date

**Awareness/Engagement days** (`Awareness` or `Engagement`) — parallel dispatch: invoke alongside Steps 5 and 6 (no upstream dependency). Pass:
- `purpose` — from frontmatter
- `source_material` — today's live news (Step 1) + FRESH list (Step 2)
- `spent_list` — from Step 2
- `date` — today's date
- Do NOT pass `flagship_url`

Capture the returned markdown block verbatim under the `## Facebook` section of the plan file (Step 9 covers the file structure).

Do not freehand the FB copy in this skill. `tcn-facebook-post` owns the FB-Explainer voice, the purpose → shape mapping, the image guidance, and the shelf-life labeling.

**Posting time:** the returned `**Posting time:**` line drives the schedule table row in Step 9. If Flagship CTA, the time MUST be after the article publishes — verify before writing the schedule table; if the article isn't yet live at draft time, use a placeholder posting window like `11:00-13:00 ET (after publish)` and surface the dependency in the recommendation.
```

- [ ] **Step 3: Verify Step 7.5 landed in the correct position**

Run:
```bash
grep -E '^### Step (7|7\.5|8)' /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Expected: Step 7, then Step 7.5, then Step 8 in order.

- [ ] **Step 4: Commit**

```bash
git add tcn-content-plan/SKILL.md
git commit -m "feat(tcn-content-plan): add Step 7.5 to delegate FB drafting to tcn-facebook-post"
```

---

## Task 9: Update Step 9 (file structure) in `tcn-content-plan`

**Files:**
- Modify: `tcn-content-plan/SKILL.md` (extend Step 9 with FB frontmatter field, FB section template, schedule table FB row, Status block FB integration)

- [ ] **Step 1: Add `facebook_purpose:` to the frontmatter template**

Find the YAML frontmatter template in Step 9:

```yaml
formats:
  - "Format 1"
  - "Format 2"
  - "Format 3"
status: draft
```

Replace with:

```yaml
formats:
  - "Format 1"
  - "Format 2"
  - "Format 3"
facebook_purpose: "Awareness"  # one of: Awareness, Engagement, Soft funnel, Flagship CTA
status: draft
```

- [ ] **Step 2: Add the `## Facebook` section template**

Append a new subsection to Step 9 (after the Status update block template, before the Schedule summary table):

```markdown
**Facebook section template** — place this section after `## LinkedIn` (if present, on flagship days) and before `## Engagement`:

\`\`\`markdown
## Facebook

[paste the markdown block returned by tcn-facebook-post verbatim]
\`\`\`

The block already contains the `**Purpose:**` / `**Shape:**` / `**Posting time:**` header, the option subsections (`### Option A` etc.), the image guidance, and the recommendation. Do not reformat.
```

- [ ] **Step 3: Update the schedule summary table example**

Find the schedule table example in Step 9:

```
| Time | Platform | Content | Depends on |
|------|----------|---------|------------|
```

Add an example FB row note immediately after:

```markdown

The FB row uses the same 4-column structure with purpose inline in the Content cell:

\`\`\`
| 09:00 ET | Facebook | Caption (Awareness): [option A summary] | Safe |
\`\`\`

For Flagship CTA days, the time is post-publish (e.g., `11:30 ET`).
```

- [ ] **Step 4: Update the Status update block to cover FB**

Find the Status update block template section. Update the descriptive paragraph above the template (NOT the template fields themselves — those stay generic). Find:

```markdown
The block is short on purpose. If it grows past ~10 lines you're rewriting the plan instead of indexing it; cut back to the safe/hold split.
```

Replace with:

```markdown
The block is short on purpose. If it grows past ~10 lines you're rewriting the plan instead of indexing it; cut back to the safe/hold split.

**FB rows in the Status block:** FB options labeled `Safe` go in the Safe-to-post table alongside X and Notes. FB options labeled `News-dependent` go in the Hold list with the trigger phrase. Same scanning surface, no new columns.
```

- [ ] **Step 5: Verify all four edits landed**

Run:
```bash
grep -c "facebook_purpose" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
grep -c "## Facebook" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
grep -c "FB rows in the Status" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Expected: `facebook_purpose` appears at least twice (frontmatter + override prompt); `## Facebook` appears at least once; `FB rows in the Status` appears once.

- [ ] **Step 6: Commit**

```bash
git add tcn-content-plan/SKILL.md
git commit -m "feat(tcn-content-plan): update Step 9 with FB frontmatter field, section template, schedule row, and Status block integration"
```

---

## Task 10: Update Step 10 (AI-tells check) in `tcn-content-plan`

**Files:**
- Modify: `tcn-content-plan/SKILL.md` (extend Step 10 with FB handling)

- [ ] **Step 1: Find and edit the tcn-text-humanizer payload list**

Find:

```markdown
Pass `tcn-text-humanizer` the prose blocks from the just-written options file at `workspace/notes/YYYY-MM-DD-{lowercase_weekday}-options.md`: the Note option bodies, the X option bodies, the restack addenda, and the engagement comment angles. Do not feed it the YAML frontmatter, schedule table, or section headings — those aren't voice surfaces.
```

Replace with:

```markdown
Pass `tcn-text-humanizer` the prose blocks from the just-written options file at `workspace/notes/YYYY-MM-DD-{lowercase_weekday}-options.md`: the Note option bodies, the X option bodies, the restack addenda, and the engagement comment angles. Do not feed it the YAML frontmatter, schedule table, or section headings — those aren't voice surfaces.

**FB prose is explicitly NOT passed to `tcn-text-humanizer`.** The humanizer is calibrated for Justin's Substack voice (closed em dashes, copulative avoidance, specific rhythm). Running it over FB-Explainer prose would over-correct the plain-English register back into Substack voice. The FB section must be audited separately — see the hard-fail conditions below.
```

- [ ] **Step 2: Add FB to the hard-fail audit list**

Find the "Hard fail conditions" list near the end of Step 10:

```markdown
**Hard fail conditions.** After `tcn-text-humanizer`'s pass, audit the assembled file against the canonical catalog in `workspace/core/anti-ai-writing-style.md`:
- Banned vocabulary — § 3A
- Negative parallelisms — § 3F
- Dismissal labels — § 3H
- Vocabulary cliff and meaning-preservation — § 3I
- Closing-line abstraction — § 3J
- Plus per-skill voice non-negotiables from `tcn-text-humanizer` (closed em dashes, copulative-avoidance verbs, sentence-case headers, Justin's TCN-specific hit-list phrases)
```

Replace with:

```markdown
**Hard fail conditions.** After `tcn-text-humanizer`'s pass, audit the assembled file against the canonical catalog in `workspace/core/anti-ai-writing-style.md`. This audit covers ALL prose surfaces in the file, including the FB section (which skipped the humanizer):
- Banned vocabulary — § 3A
- Negative parallelisms — § 3F
- Dismissal labels — § 3H
- Vocabulary cliff and meaning-preservation — § 3I
- Closing-line abstraction — § 3J
- Plus per-skill voice non-negotiables from `tcn-text-humanizer` (closed em dashes, copulative-avoidance verbs, sentence-case headers, Justin's TCN-specific hit-list phrases) — these apply to X, Notes, restacks, and engagement copy ONLY. They do NOT apply to FB prose, which has its own register (see `tcn-facebook-post/references/voice-register.md`).
- **FB-specific hard fails (audit the `## Facebook` section against these):**
  - No vague placeholder verbs ("hit a number," "saw movement," "raised concerns," "made waves," "had a moment")
  - Caption length ≤30 words; paragraph length 50-80 words (hard fail outside range)
  - Closed em dashes: zero at caption length; max 1 at paragraph length
  - Image guidance is concrete (AI prompt text, Substack URL, or screenshot recommendation — never "find an image")
```

- [ ] **Step 3: Verify both edits**

Run:
```bash
grep -c "FB prose is explicitly NOT" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
grep -c "FB-specific hard fails" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Expected: both phrases appear exactly once.

- [ ] **Step 4: Commit**

```bash
git add tcn-content-plan/SKILL.md
git commit -m "feat(tcn-content-plan): update Step 10 to skip FB prose in humanizer pass, add FB-specific hard-fail audit"
```

---

## Task 11: Update Mode 1 (Check Today's Plan) in `tcn-content-plan`

**Files:**
- Modify: `tcn-content-plan/SKILL.md` (extend Mode 1)

- [ ] **Step 1: Find Mode 1 and extend its file-existence handling**

Find:

```markdown
3. **File exists** → read it. Then check the **Status update** block at the top of the file (template defined in Step 9):
```

Add a new sub-step after the existing "File exists" handling, before "File missing". Find the bullet structure under "File exists" and append:

```markdown
   After the status update is fresh, summarize the day's Notes, X standalone recommendation, **FB post recommendation**, and schedule table. Ask if anything else needs updating.

   **FB-specific check:** if the file lacks a `## Facebook` section (was drafted before this skill shipped), surface: "This plan was drafted before FB support shipped — no FB content for today. Run /create-daily to regenerate, or accept the gap." Do not auto-regenerate; let the user decide.
```

(Find the existing "After the status update is fresh, summarize the day's Notes, X standalone recommendation, and schedule table. Ask if anything else needs updating." line and replace it with the version above that includes `**FB post recommendation**` plus the new sub-step.)

- [ ] **Step 2: Verify**

Run:
```bash
grep -c "FB post recommendation" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
grep -c "drafted before FB support shipped" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Expected: both phrases appear once each.

- [ ] **Step 3: Commit**

```bash
git add tcn-content-plan/SKILL.md
git commit -m "feat(tcn-content-plan): extend Mode 1 to surface FB recommendation and handle pre-FB files"
```

---

## Task 12: Update Mode 3 (Create Monthly Plan) in `tcn-content-plan`

**Files:**
- Modify: `tcn-content-plan/SKILL.md` (extend Mode 3)

- [ ] **Step 1: Find Mode 3 Step 3 (Generate the 30-day map)**

Locate the entry format example in Mode 3 Step 3:

```
**Item [N] — [Date] ([Day of week])**: [Platform] | [Content type] | [Format] | CTA: yes/no | [Brief note: what this seeds or establishes]
```

Replace with:

```
**Item [N] — [Date] ([Day of week])**: [Platforms] | [Note formats] | FB: [Purpose] | CTA: yes/no | [Brief note: what this seeds or establishes]
```

- [ ] **Step 2: Add FB purpose assignment instructions**

After the entry format example, add:

```markdown

**FB purpose assignment:** Assign each day's `FB:` cell using the weekday rotation default (see `tcn-facebook-post/references/purpose-table.md` § Weekday rotation). The default mapping is:

- Mon, Wed, Sat → Awareness
- Tue → Engagement
- Thu, Sun → Soft funnel
- Fri → Flagship CTA

After auto-assigning, ask the user: `"Any weeks where the FB rotation should shift? E.g., a week with two flagships might need a second hard-funnel day, or a quiet news week might lean more on Engagement posts."` Adjust specific cells based on the answer.

For Soft funnel days, also assign the older Substack article URL that will be linked. The URL belongs in the `Brief note` cell.
```

- [ ] **Step 3: Add the FB Cadence Note section to Mode 3 Step 4**

Find Mode 3 Step 4 (Write the file):

```markdown
### Step 4: Write the file

Save to `workspace/plans/tcn-notes-30-day-map.md`. Include a "Source Hooks" section at the end listing the insight-sweep hooks that informed the flagship selections, with wiki page citations.
```

Replace with:

```markdown
### Step 4: Write the file

Save to `workspace/plans/tcn-notes-30-day-map.md`. Include a "Source Hooks" section at the end listing the insight-sweep hooks that informed the flagship selections, with wiki page citations.

If any FB purposes were assigned non-default values, append an **FB Cadence Note** section after Source Hooks explaining the reasoning. Example:

\`\`\`markdown
## FB Cadence Note

Week 2 (Days 8-14) has two flagships (Tue + Fri). Tue's typical Engagement is shifted to Soft funnel to tease Tuesday's flagship, then back to standard rotation Wed onward. Week 3 reverts to default.
\`\`\`

If all FB purposes are default, omit the section.
```

- [ ] **Step 4: Verify**

Run:
```bash
grep -c "FB: \[Purpose\]" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
grep -c "FB Cadence Note" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Expected: `FB: [Purpose]` appears at least once; `FB Cadence Note` appears at least once.

- [ ] **Step 5: Commit**

```bash
git add tcn-content-plan/SKILL.md
git commit -m "feat(tcn-content-plan): extend Mode 3 with FB purpose assignment and cadence note section"
```

---

## Task 13: Add FB additions to the `tcn-content-plan` quality bar

**Files:**
- Modify: `tcn-content-plan/SKILL.md` (extend the Quality bar list at the bottom)

- [ ] **Step 1: Find the existing quality bar list**

Locate the last bullet of the existing list:

```markdown
- The `tcn-text-humanizer` check ran and the file's `status:` is `voice-checked` — no closed em dashes, no banned vocab, no negative parallelisms, no "AI hit list" phrases in the drafted prose
```

- [ ] **Step 2: Append FB-specific bullets**

Add after the last bullet:

```markdown
- **FB copy was drafted by `tcn-facebook-post`, not freehanded in this skill**
- **The FB option matches the day's purpose-table.md shape** (caption ≤30 words OR paragraph 50-80 words; outside range = hard fail)
- **The FB image guidance is concrete:** an AI prompt, a specific Substack URL for the hero, or a screenshot recommendation — never "find an image"
- **The FB option carries a Safe or News-dependent label** and appears in the schedule table + Status block
- **No vague placeholder verbs** ("hit a number," "saw movement," etc.) — hard fail
- **Vocabulary cliff fully glossed:** every FB post is glossable to a reader with zero context on the beat
- **Flagship CTA posts include the actual article URL**, not a placeholder (or, if URL pending, the recommendation flags the gap prominently)
```

- [ ] **Step 3: Verify**

Run:
```bash
grep -c "FB copy was drafted by" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
grep -c "vague placeholder verbs" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Expected: both phrases appear exactly once.

- [ ] **Step 4: Commit**

```bash
git add tcn-content-plan/SKILL.md
git commit -m "feat(tcn-content-plan): add FB-specific bullets to quality bar"
```

---

## Task 14: Update `posting-rules.md` with Facebook windows and rules

**Files:**
- Modify: `tcn-content-plan/references/posting-rules.md`

- [ ] **Step 1: Add Facebook to the Platform Windows table**

Find:

```markdown
| Platform | When to post |
|---|---|
| Substack Notes | Weekdays: 3–10 PM ET. Weekend: 8–11 PM ET only. |
| X (Twitter) | Anytime — no window restriction. |
| LinkedIn | Weekday afternoons preferred. No hard rule. |
| Flagship article | Friday AM — unrestricted. |
| Paid ("thinking behind the thinking") note | Wednesday, no specific window. |
```

Replace with:

```markdown
| Platform | When to post |
|---|---|
| Substack Notes | Weekdays: 3–10 PM ET. Weekend: 8–11 PM ET only. |
| X (Twitter) | Anytime — no window restriction. |
| LinkedIn | Weekday afternoons preferred. No hard rule. |
| Facebook | Daily, 09:00-10:00 ET typical (or 19:00-21:00 ET fallback). Flagship days shift to 11:00-13:00 ET (must be after article publishes). |
| Flagship article | Friday AM — unrestricted. |
| Paid ("thinking behind the thinking") note | Wednesday, no specific window. |
```

- [ ] **Step 2: Add a "Facebook Rules" section after "X Standalone Rules"**

Find the section header:

```markdown
## X Standalone Rules
```

Find the end of that section (the last bullet of X Standalone Rules) and immediately after, before the next section, insert:

```markdown

---

## Facebook Rules

- 1 post per day, 7 days a week (no weekend reduction — FB doesn't have Substack's audience-fatigue dynamic).
- Purpose follows weekday rotation by default (see `tcn-facebook-post/references/purpose-table.md` § Weekday rotation):
  - Mon, Wed, Sat → Awareness
  - Tue → Engagement
  - Thu, Sun → Soft funnel
  - Fri → Flagship CTA
- Monthly plan can override via the `FB:` cell in the 30-day map entry.
- Shape and image source flow from purpose (caption + AI image vs. paragraph + Substack hero); never freehand — delegate to `tcn-facebook-post`.
- Hard restriction: never post the FB Flagship CTA before the article is live on Fridays. Out-of-order publishing breaks the funnel.
- Voice: FB-Explainer register (separate from Substack/X/LinkedIn). See `tcn-facebook-post/references/voice-register.md`.

```

- [ ] **Step 3: Verify**

Run:
```bash
grep -c "^| Facebook " /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/references/posting-rules.md
grep -c "^## Facebook Rules" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/references/posting-rules.md
```

Expected: Facebook row in Platform Windows appears once; Facebook Rules section header appears once.

- [ ] **Step 4: Commit**

```bash
git add tcn-content-plan/references/posting-rules.md
git commit -m "feat(tcn-content-plan): add Facebook to platform windows table and new Facebook Rules section"
```

---

## Task 15: Add a worked example to `tcn-facebook-post`

**Files:**
- Create: `tcn-facebook-post/references/worked-example.md`

- [ ] **Step 1: Write the worked example**

Write to `/Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/references/worked-example.md`:

```markdown
# Worked Example — tcn-facebook-post

Two complete invocations end-to-end, showing inputs, dispatch, and final output. Used as a sanity check during skill development and as a reference for future tuning.

## Example 1: Tuesday Awareness day

### Inputs

- `purpose`: `Awareness`
- `source_material`: 
  - Live news: "Treasury Department released FY2024 final figures; interest payments on federal debt = $881B, defense outlays = $880B"
  - FRESH list: "Treasury FY2024 final figures, interest-vs-defense crossover, services inflation Q1 data"
- `spent_list`: "Hormuz crossings 191/3000; April CPI energy +3.8% MoM; rate tool doesn't reach supply shocks"
- `date`: 2026-05-19

### Skill process

1. **Voice context loaded:** workspace/core/anti-ai-writing-style.md present, in working context.
2. **Lookup:** `purpose: Awareness` → shape: Caption (≤30 words), image_source: AI-generated, cta_rule: No link, voice_notes: drop closed em dashes, one warmth-marker max, no edge.
3. **Angle derivation:** Awareness day, audience is the general FB reader. Specific anchor from live news: interest payments now exceed defense budget, both >$880B. Plain-language interesting on its own; nothing in spent_list overlaps.
4. **Draft 3 options:**

### Output

\`\`\`markdown
**Purpose:** Awareness
**Shape:** Caption
**Posting time:** 09:00 ET

### Option A — Safe
Interest payments on the federal debt are now bigger than the entire defense budget. Both crossed $880 billion last year. Most coverage isn't touching this.

**Image:** AI prompt: "Split-frame photograph, left half shows a stack of physical Treasury bond certificates on a desk, right half shows the Pentagon building exterior from below at golden hour. Equal weight to both halves. Documentary photography style, no logos, no text."

### Option B — Safe
The U.S. is now spending more on interest payments for the debt than on the entire military. First time in modern history. Honestly worth paying attention to.

**Image:** AI prompt: "Close-up overhead shot of a calculator displaying $881,000,000,000 on its screen, sitting on top of a folded American flag. Documentary photography, natural light, no other objects in frame."

### Option C — Safe
Quick reality check: the federal government now spends more paying interest on the debt than it does on defense. $881B vs $880B last year.

**Image:** AI prompt: "Two simple stacked piles of cash visible in a clean overhead photograph. Left pile labeled with a small handwritten card reading 'INTEREST', right pile labeled 'DEFENSE'. Both piles roughly equal in size. Natural daylight, white background."

**Recommendation:** Default to Option A (cleanest framing, strongest specific anchor). Option B if a slightly warmer "honestly" tone fits the week's mood. Option C if the previous day's posts have been heavier; this one lands lighter.
\`\`\`

---

## Example 2: Friday Flagship CTA day

### Inputs

- `purpose`: `Flagship CTA`
- `source_material`:
  - X standalone copy (from Step 5 output): "Services inflation didn't slow in Q1. Goods deflation is masking that. The Fed's 2% target is being missed in the part of the economy that actually drives household budgets. (BLS Q1 release)"
  - Flagship article URL: `https://thecivicnode.substack.com/p/services-inflation-q1-2026`
  - Flagship article tagline (from article frontmatter): "Why the headline inflation number is hiding the real story for most households"
- `spent_list`: "Headline CPI 2.3% YoY April; goods deflation -0.4%; Fed dot plot December 2025; services inflation glossed earlier this week (Tue Note)"
- `flagship_url`: `https://thecivicnode.substack.com/p/services-inflation-q1-2026`
- `date`: 2026-05-22

### Skill process

1. **Voice context loaded.**
2. **Lookup:** `purpose: Flagship CTA` → shape: Paragraph (50-80 words), image_source: Substack hero (today's piece), cta_rule: Hard link at end, voice_notes: slight authority, plain-English tagline, no "predictably/naturally/of course."
3. **Angle derivation:** Funnel day. Restate the X claim in FB-Explainer voice — drop "Fed's 2% target is being missed" (too technical) and "BLS Q1 release" (citation is fine on X, redundant on FB). Plain-English: the headline number is misleading; the part most household budgets actually feel (services) isn't slowing.
4. **Draft 3 options:**

### Output

\`\`\`markdown
**Purpose:** Flagship CTA
**Shape:** Paragraph
**Posting time:** 11:30 ET (after article publishes)

### Option A — Safe
The inflation number everyone's talking about is actually the smaller story. The bigger one is buried in the same release: services inflation isn't slowing, and that's where most of your monthly budget lives. Today's piece walks through what that means for the next six months.

Full piece: https://thecivicnode.substack.com/p/services-inflation-q1-2026

**Image:** Use Substack hero from https://thecivicnode.substack.com/p/services-inflation-q1-2026

### Option B — Safe
Here's the thing about this week's inflation report: the part that's slowing is goods (TVs, cars, appliances). The part that's NOT slowing is services (rent, healthcare, childcare) — and that's the part you feel every month. Friday's piece pulls that apart.

Full piece: https://thecivicnode.substack.com/p/services-inflation-q1-2026

**Image:** Use Substack hero from https://thecivicnode.substack.com/p/services-inflation-q1-2026

### Option C — Safe
The April inflation number looked like good news. Underneath it, the part of inflation most households actually feel (services — rent, healthcare, childcare) is still running well above the Fed's target. Worth understanding why before the next rate decision.

Full piece: https://thecivicnode.substack.com/p/services-inflation-q1-2026

**Image:** Use Substack hero from https://thecivicnode.substack.com/p/services-inflation-q1-2026

**Recommendation:** Default to Option A (cleanest narrative arc — "what you think it is vs. what it actually is"). Option B if the previous week's posts already covered the goods/services split; this one reinforces. Option C if the Fed meeting context matters more this week than the household-budget angle.
\`\`\`

## Self-checks against the quality bar

For Example 1 (Tuesday Awareness):
- ✅ All 3 options ≤30 words (A: 26, B: 26, C: 25)
- ✅ No closed em dashes (caption length)
- ✅ Specific anchors (interest payments $881B, defense $880B)
- ✅ One warmth-marker in B ("honestly"); zero in A and C
- ✅ No banned vocab, no vague placeholder verbs
- ✅ All image guidance concrete (AI prompts with specific scene)
- ✅ All Safe (no news triggers required)
- ✅ No link (matches Awareness CTA rule)

For Example 2 (Friday Flagship CTA):
- ✅ All 3 options within 50-80 words (A: 56, B: 55, C: 52)
- ✅ One closed em dash in B ("services — rent, healthcare, childcare"); zero in A and C — within paragraph allowance
- ✅ Specific anchors (services inflation, six months, rent/healthcare/childcare)
- ✅ Hard link on its own line at end
- ✅ No banned vocab, no vague placeholder verbs, no "of course/naturally/predictably"
- ✅ Substack hero image source specified
- ✅ All Safe (article is live by posting time)
```

- [ ] **Step 2: Verify the worked example covers both shape types**

Run:
```bash
grep -E "^### Option [ABC] — " /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/references/worked-example.md
```

Expected: 6 option headers (3 for Example 1, 3 for Example 2).

- [ ] **Step 3: Commit**

```bash
git add tcn-facebook-post/references/worked-example.md
git commit -m "feat(tcn-facebook-post): add worked example (Tue Awareness caption + Fri Flagship CTA paragraph)"
```

---

## Task 16: Final integration check + documentation cross-references

**Files:**
- Modify: `tcn-facebook-post/SKILL.md` (add Reference files section and Sister skills section)

- [ ] **Step 1: Append Reference files and Sister skills sections to SKILL.md**

Append at the end of `/Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/SKILL.md`:

```markdown

---

## Reference files

Load these when needed:

- `references/purpose-table.md` — canonical purpose × shape × image × voice × CTA matrix; weekday rotation appendix; posting time defaults
- `references/voice-register.md` — FB-Explainer voice doc (three dials, what survives from canonical voice file, what relaxes, hard rules, Marcus-FB check, length-bounded examples, voice fallback)
- `references/worked-example.md` — two complete invocations end-to-end (Tue Awareness + Fri Flagship CTA)

## Sister skills (do not freehand the prose; delegate)

- `ai-image-prompts-skill` — invoked for AI-generated image prompts on Awareness and Engagement days. If unavailable, fall back to a stock-photo search-query suggestion and surface the gap.

## Skills this is invoked by

- `tcn-content-plan` Step 7.5 (Mode 2) — primary integration. Receives the markdown block from this skill and inserts it under the daily plan file's `## Facebook` section.

## Voice authority

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice decision. That file is the single source of truth for banned vocabulary (§ 3A), negative parallelisms (§ 3F), dismissal labels (§ 3H), vocabulary cliff and meaning-preservation (§ 3I), and closing-line abstraction (§ 3J).

This skill MUST NOT maintain a duplicate copy of any of the above. `references/voice-register.md` documents which canonical rules **relax** for FB-Explainer; it does not override the hard rules.

If the canonical file is missing, follow the fallback in `references/voice-register.md` § Voice fallback.
```

- [ ] **Step 2: Run a full skill audit**

Run:
```bash
# Required sections present in SKILL.md
grep -E '^## ' /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/SKILL.md

# Reference files all present
ls /Users/justin/CascadeProjects/claude-skills/tcn-facebook-post/references/

# Posting rules cross-reference
grep "tcn-facebook-post" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/references/posting-rules.md

# Step 7.5 cross-reference
grep "tcn-facebook-post" /Users/justin/CascadeProjects/claude-skills/tcn-content-plan/SKILL.md
```

Expected:
- SKILL.md has at minimum: "What this skill owns", "What this skill does NOT own", "Inputs", "Outputs", "Process", "Quality bar", "Failure modes to watch for", "Reference files", "Sister skills", "Skills this is invoked by", "Voice authority"
- references/ directory contains: purpose-table.md, voice-register.md, worked-example.md
- posting-rules.md contains references to tcn-facebook-post
- tcn-content-plan/SKILL.md contains references to tcn-facebook-post (Step 3, Step 7.5, Step 10, quality bar)

- [ ] **Step 3: Commit**

```bash
git add tcn-facebook-post/SKILL.md
git commit -m "feat(tcn-facebook-post): add reference files index, sister skills, and voice authority sections"
```

---

## Self-Review

Running the writing-plans self-review now (placeholder scan, spec coverage, type consistency).

### Spec coverage check

Walking through each section of the spec at [docs/superpowers/specs/2026-05-21-tcn-facebook-post-design.md](../specs/2026-05-21-tcn-facebook-post-design.md):

| Spec section | Implementing task(s) |
|---|---|
| § 1 Purpose | Task 1 (identity), Task 4 (inputs/outputs) |
| § 2 Position in stack | Task 8 (Step 7.5 dispatch logic captures position) |
| § 3.1 Directory layout | Task 1 (creates directory), Tasks 2/3/15 (references), Task 1 (CLAUDE.md) |
| § 3.2 Ownership boundary | Task 1 ("What this skill owns / does NOT own") |
| § 3.3 Inputs | Task 4 (Inputs section) |
| § 3.4 Outputs | Task 4 (Outputs section) |
| § 4 Purpose table | Task 2 (purpose-table.md) |
| § 4.1 Weekday rotation | Task 2 (rotation appendix), Task 7 (orchestrator default) |
| § 4.2 Monthly-plan override | Task 7 (Step 3 lookup), Task 12 (Mode 3 assignment) |
| § 5 Voice register | Task 3 (voice-register.md), Task 5 (Process Step 1 loading) |
| § 5.1-5.6 Voice dials, rules, examples | Task 3 (all covered in voice-register.md) |
| § 5.7 Voice fallback | Task 3 (Voice fallback section), Task 5 (Process Step 1 fallback handling) |
| § 6.1 Mode 2 step changes | Tasks 7, 8, 9, 10 |
| § 6.2 Step 7.5 dispatch logic | Task 8 |
| § 6.3 Posting times | Task 2 (purpose-table.md posting times), Task 8 (Step 7.5 surfaces them) |
| § 6.4 Schedule table | Task 9 (Step 9 schedule table example) |
| § 6.5 Status block | Task 9 (FB rows in Status block) |
| § 6.6 Daily plan file structure | Task 9 (Facebook section template) |
| § 6.7 Frontmatter addition | Task 9 (facebook_purpose: in YAML) |
| § 7 Posting rules updates | Task 14 |
| § 8.1 Mode 1 changes | Task 11 |
| § 8.2 Mode 3 changes | Task 12 |
| § 9 Edge cases | Tasks 5 (process handles them), 8 (URL pending), 11 (pre-FB files), 7 (override prompt) |
| § 10 Quality bar additions | Tasks 6 (skill's own bar), 13 (orchestrator's bar) |
| § 11 Out of scope | (no implementation needed — informational) |

All spec sections have implementing tasks. No gaps.

### Placeholder scan

Searched plan for forbidden patterns: TBD, TODO, "implement later," "add appropriate error handling," "similar to Task N." None found. All code/markdown blocks contain complete content. All commands have exact expected output.

### Type consistency

Cross-checking key strings used across tasks:

- `facebook_purpose:` (frontmatter field) — used identically in Task 7 (Step 3 sets it), Task 9 (frontmatter template), Task 13 (quality bar mentions). ✓
- `FB:` (monthly plan cell) — used identically in Task 7 (Step 3 reads it), Task 12 (Mode 3 writes it), Task 14 (posting rules describes it). ✓
- `Awareness | Engagement | Soft funnel | Flagship CTA` — purpose values consistent across Tasks 2, 4, 7, 9, 12. ✓
- `Safe | News-dependent` — shelf-life labels consistent across Tasks 2, 4, 5, 6, 9, 10. ✓
- `tcn-facebook-post` — skill name consistent across Tasks 1-16. ✓
- `references/purpose-table.md` / `references/voice-register.md` / `references/worked-example.md` — file paths consistent across Tasks 2, 3, 5, 14, 15, 16. ✓

No type/name inconsistencies found.

---

## Plan complete

Plan saved to `docs/superpowers/plans/2026-05-21-tcn-facebook-post.md`.

**16 atomic tasks**, each producing one git commit. Estimated total: 4-6 hours of focused work depending on review pacing.

Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
