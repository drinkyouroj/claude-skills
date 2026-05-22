# tcn-facebook-post — Design Spec

**Date:** 2026-05-21
**Status:** Approved for implementation planning
**Workflow position:** New sister skill invoked by `tcn-content-plan` (Mode 2, new Step 7.5) for daily Facebook posts.
**Sibling skills:** `tcn-content-plan` (orchestrator), `tcn-post` (X copy), `tcn-substack-notes` (Substack Notes), `tcn-text-humanizer` (Substack/X voice pass — explicitly does NOT touch FB prose), `ai-image-prompts-skill` (image prompt generation for caption-shape posts).

---

## 1. Purpose

Add a daily Facebook post to The Civic Node's content stack. One FB post per day, seven days a week. Content engineered for FB's audience and feed dynamics — plain English, image-forward, low cognitive load — while still surfacing The Civic Node brand and (on Fridays) driving Substack click-through.

The FB post must:

1. Match the day's **purpose** (one of: Awareness / Engagement / Soft funnel / Flagship CTA) drawn from a weekday rotation or a monthly-plan override.
2. Take the **shape** that flows from purpose (caption ≤30 words OR paragraph 50-80 words).
3. Carry a concrete **image guidance** instruction (AI prompt, Substack hero URL, or screenshot recommendation — never "find an image").
4. Carry a **shelf-life label** (Safe / News-dependent) so the daily plan's Status block can decide what's postable at re-check time.
5. Be drafted in **FB-Explainer voice** — plain English, warm register, vocabulary cliff fully glossed, Justin-fingerprint moves dialed back per length.

The skill produces 2-3 options per slot plus a one-sentence recommendation, mirroring how `tcn-post` and `tcn-substack-notes` work.

---

## 2. Position in the content stack

```
tcn-content-plan (orchestrator)
    ├── Step 5: tcn-post           → X standalone or thread
    ├── Step 6: tcn-substack-notes → Substack Notes (2-3 slots)
    ├── Step 7: LinkedIn repost    → flagship days only (freehand inside orchestrator)
    └── Step 7.5: tcn-facebook-post → daily FB post  [THIS SKILL]
```

Dispatch order:
- **Funnel + Flagship days** (default: Thu, Fri, Sun): Step 7.5 runs **sequentially after** Steps 5 and 7 — needs the X copy and/or article tagline to reframe.
- **Awareness + Engagement days** (default: Mon, Tue, Wed, Sat): Step 7.5 runs **in parallel with** Steps 5 and 6 — content derives independently from live news.

---

## 3. The new skill: structure and ownership

### 3.1 Directory layout

```
tcn-facebook-post/
├── SKILL.md
├── CLAUDE.md                          # session-history pointer, minimal
└── references/
    ├── purpose-table.md               # canonical purpose × shape × image × voice matrix
    └── voice-register.md              # FB-Explainer voice doc
```

### 3.2 Skill ownership boundary

**Owned by `tcn-facebook-post`:**
- FB-Explainer voice rules
- Purpose → shape mapping (caption vs. paragraph)
- Purpose → image-source mapping (AI vs. Substack hero vs. screenshot vs. stock fallback)
- Option generation (2-3 options per slot)
- Shelf-life labeling (Safe / News-dependent — simplified two-state system, NOT the three-state Frame-forward/Data-forward/Conditional used elsewhere)
- Image prompt drafting (delegates to `ai-image-prompts-skill` when AI-generated; constructs the prompt text itself for handoff)
- Quality bars per shape (caption ≤30 words; paragraph 50-80 words; image guidance concrete, not vague)

**NOT owned by this skill:**
- The weekday rotation lookup (lives in `tcn-content-plan` as a default; `tcn-facebook-post` receives purpose as input)
- The monthly-plan override key (`tcn-content-plan` reads `facebook_purpose:` from the 30-day map)
- The X copy, Substack Note copy, or LinkedIn copy
- The schedule table or Status block formatting (`tcn-content-plan` owns the daily plan file structure)
- Voice-passes on other surfaces — `tcn-text-humanizer` handles X/Notes; this skill is self-contained on voice

### 3.3 Inputs

The orchestrator invokes `tcn-facebook-post` with:

1. **`purpose`** — one of: `Awareness`, `Engagement`, `Soft funnel`, `Flagship CTA`
2. **`source_material`** — conditional on purpose:
   - **Funnel/Flagship:** the day's X standalone option text + flagship article URL + flagship article tagline (when available)
   - **Awareness/Engagement:** today's live news (from Step 1 of Mode 2) + FRESH list (from Step 2 duplication audit)
3. **`spent_list`** — what other surfaces already said this week (avoid echoes)
4. **`flagship_url`** — present only on Flagship CTA and Soft funnel days
5. **`date`** — today's date for the schedule slot

### 3.4 Outputs

A markdown block containing:

```markdown
**Purpose:** [label]
**Shape:** [Caption | Paragraph]
**Posting time:** [HH:MM ET]  ← derived from purpose + day-of-week (see § 6)

### Option A — [Safe | News-dependent]
[FB post prose]

**Image:** [concrete instruction — AI prompt / Substack hero URL / screenshot recommendation]

### Option B — [Safe | News-dependent]
[...]

### Option C — [Safe | News-dependent]
[...]

**Recommendation:** [one sentence — default option + conditional logic if any option is News-dependent]
```

---

## 4. The purpose table

Canonical at `tcn-facebook-post/references/purpose-table.md`. Mirrored in summary form here for the spec; the file is the source of truth.

| Purpose | Shape | Image source | Voice notes | CTA rule |
|---|---|---|---|---|
| **Awareness** | Caption (≤30 words) | AI-generated (via `ai-image-prompts-skill`) | Soft, observational. Drop closed em dashes entirely. One warmth-marker max ("honestly," / "look," / "the thing is"). No edge. | No link |
| **Engagement** | Caption (≤30 words) | AI-generated | Question-framing or "tell me in the comments" pattern. Active second person OK. Designed for FB algorithm comment-signal. | No link |
| **Soft funnel** | Paragraph (50-80 words) | Substack article hero from the older piece referenced (URL specified in monthly plan's `Brief note` cell, or surfaced by `tcn-content-plan` Step 1 prompt when no monthly entry) — AI-generated fallback only if no usable hero exists | Slight authority. 1 closed em dash max. Plain-English summary of the older piece's argument. | Soft link: "wrote about this back in [month] — [link]" |
| **Flagship CTA** | Paragraph (50-80 words) | Substack article hero (today's piece) | Slight authority. Plain-English tagline of the flagship's argument. No "predictably," "naturally," "of course." | Hard link at end: "Full piece: [link]" |

### 4.1 Weekday rotation (default)

| Day | Purpose | Rationale |
|---|---|---|
| Mon | Awareness | Week opens soft — plain observation about weekend or week ahead. |
| Tue | Engagement | Tuesday FB engagement historically strong; comment signal early in the week. |
| Wed | Awareness | Mid-week observation. Wednesday is also paid Substack note day — deliberately not funneling so the two don't compete. |
| Thu | Soft funnel | Tease Friday's flagship — "writing about X for Friday." |
| Fri | Flagship CTA | Article link + plain-English tagline. Hard funnel. |
| Sat | Awareness | Weekend FB usage high but cognitive load low. |
| Sun | Soft funnel | Resurface older Substack piece relevant to the week's news. |

Lives in `tcn-facebook-post/references/purpose-table.md` as an appendix. Referenced (not duplicated) by `tcn-content-plan/references/posting-rules.md`.

### 4.2 Monthly-plan override

The 30-day map (`workspace/plans/tcn-notes-30-day-map.md`) entries gain an optional `FB: [Purpose]` cell:

```
**Item [N] — [Date] ([Day of week])**: [Platforms] | [Note formats] | FB: [Purpose] | CTA: yes/no | [Brief note]
```

If `FB:` is absent, `tcn-content-plan` defaults to the weekday rotation table. Same pattern as how `formats:` already works.

---

## 5. FB-Explainer voice register

Canonical at `tcn-facebook-post/references/voice-register.md`. Summary:

### 5.1 The three dials

- **Warmth: high.** A friend posting a thought, not an analyst publishing a take. "Look," / "honestly," / "the thing is" — warmth-markers are fine on FB, banned on Substack.
- **Density: very low.** One idea per post. No nested clauses. No two-part claims.
- **Edge: scaled by purpose.** Awareness/Engagement = near-zero edge; Soft funnel/Flagship CTA = slight dry authority, never sardonic.

### 5.2 What survives from `workspace/core/anti-ai-writing-style.md` (hard-applies)

- **Banned-vocab list (§ 3A)** — *delve*, *navigate*, *landscape*, *tapestry*, etc. Always banned.
- **Negative parallelisms (§ 3F)** — "not X, but Y" banned.
- **Vocabulary cliff (§ 3I)** — FB is the **steepest cliff** in the stack. Always gloss. No unglossed acronyms or insider terms.
- **Closing-line abstraction (§ 3J)** — no grand wrap-ups. End on a fact or question.

### 5.3 What relaxes (FB-only)

- **Closed em dashes** — drop entirely at caption length (≤30 words; they read as trying-too-hard in 1-2 sentences). At paragraph length, allow one maximum. Never two.
- **Copulative avoidance** — Substack voice avoids "is" verbs. FB allows them; plain English needs "is" to work.
- **Sardonic dismissal moves** — no "of course," "naturally," "predictably" framings on FB. Smirk stays internal.

### 5.4 Hard rule: no vague placeholder verbs

Phrases like "hit a number," "saw movement," "raised concerns," "made waves," "had a moment" are AI-filler tells. Plain English exposes them harder than analytical registers because the reader has no clausal complexity to fill in the missing fact. If a real specific fact (number, name, date, direct quote) isn't at hand, change the framing to one that doesn't need it. Never paper over with abstract verbs.

### 5.5 The Marcus check, FB-edition

The Substack stack writes for Marcus (engaged-but-time-pressed reader). FB writes for a reader with the same intelligence but zero context on the beats Justin covers daily. If a sentence would make that reader stop scrolling and squint, it's too dense.

### 5.6 Length-bounded examples

> **Caption (Awareness, Tue):** "Interest payments on the federal debt are now bigger than the entire defense budget. Both crossed $880 billion last year. Most coverage isn't touching this."

> **Paragraph (Soft funnel, Thu):** "Writing about energy demand for Friday — the thing that keeps surprising me is how much of it comes from data centers nobody's quoting. One small Virginia county is now using more power than entire states did ten years ago. Full piece drops Friday morning."

### 5.7 Voice-file fallback

If `workspace/core/anti-ai-writing-style.md` is missing from the active project, `tcn-facebook-post` follows the same fallback as the rest of the TCN stack:
1. Flag explicitly: "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip vocabulary substitution, banned-word audit, and closing-line check.
3. Do NOT apply generic vocabulary heuristics from training data.
4. Continue with the structural work (option generation, shape selection, image guidance, shelf-life labeling).
5. The daily plan's `status:` field stays `draft` rather than advancing to `voice-checked`.

---

## 6. Integration into `tcn-content-plan`

### 6.1 Mode 2 step changes

| Step | Action | Change |
|---|---|---|
| 3 | Look up format assignments | **Extended** — also reads `FB:` cell from monthly plan; falls back to weekday rotation if absent. Sets `facebook_purpose` in frontmatter. |
| 5 | Draft X standalone (`tcn-post`) | unchanged |
| 6 | Draft Notes (`tcn-substack-notes`) | unchanged |
| 7 | Draft LinkedIn (flagship only) | unchanged |
| **7.5 (NEW)** | **Draft FB post (`tcn-facebook-post`)** | **new step** — see § 6.2 for dispatch logic |
| 8 | Draft engagement notes | unchanged |
| 9 | Write the file | **Extended** — new `## Facebook` section between `## LinkedIn` and `## Engagement`; FB row in schedule table; FB rows surface in Status block |
| 10 | AI-tells check (`tcn-text-humanizer`) | **Extended** — FB prose blocks are NOT passed to the humanizer (different voice register would get over-corrected). FB prose IS audited against the canonical `anti-ai-writing-style.md` hard rules (§ 3A, § 3F, § 3I, § 3J) inline. |

### 6.2 Step 7.5 dispatch logic

Pseudocode:

```
purpose = frontmatter.facebook_purpose  (set in Step 3)

if purpose in ["Soft funnel", "Flagship CTA"]:
    # Sequential — needs upstream X output to reframe from
    wait_for(step_5_output)        # X standalone copy
    # Note: does NOT wait for step_7 (LinkedIn). Article URL and tagline
    # come from the monthly plan, not from LinkedIn output.
    invoke tcn-facebook-post with:
        purpose, source_material=x_copy + article_tagline, spent_list, flagship_url
else:  # Awareness or Engagement
    # Parallel — independent content
    invoke tcn-facebook-post with:
        purpose, source_material=live_news + fresh_list, spent_list
        (no flagship_url passed)
```

### 6.3 Posting times

Default windows per purpose (overridable in monthly plan):

| Purpose | Default posting time |
|---|---|
| Awareness | 09:00 ET |
| Engagement | 09:00 ET (high engagement window) |
| Soft funnel | 09:00 ET |
| Flagship CTA | 11:00 ET-13:00 ET (must be after article publishes) |

Fallback: 19:00-21:00 ET if morning slot missed. The fallback is informational — Mode 2 always writes the morning slot to the schedule table; Mode 1 re-check surfaces the fallback recommendation if the morning slot passed without posting.

### 6.4 Schedule table integration

Fits the existing 4-column format without adding columns. Purpose lives inline in the Content cell:

```
| Time | Platform | Content | Depends on |
| 09:00 ET | Facebook | Caption (Awareness): [option A summary] | Safe |
```

### 6.5 Status block integration

- FB options labeled `Safe` drop into the existing "Safe to post" table alongside X and Notes.
- FB options labeled `News-dependent` drop into the existing "Hold" list.
- No new columns. Block stays under the 10-line target.

### 6.6 Daily plan file structure

New section between `## LinkedIn` (when present) and `## Engagement`:

```markdown
## Facebook

**Purpose:** [Awareness | Engagement | Soft funnel | Flagship CTA]
**Shape:** [Caption | Paragraph]
**Posting time:** [HH:MM ET]

### Option A — [Safe | News-dependent]
[FB post prose]

**Image:** [concrete instruction]

### Option B — [shelf-life]
[...]

### Option C — [shelf-life]
[...]

**Recommendation:** [default + conditional logic]
```

### 6.7 Frontmatter addition

New field, required once this skill ships:

```yaml
facebook_purpose: "Awareness"  # Awareness | Engagement | Soft funnel | Flagship CTA
```

Placement: after `formats:`, before `status:`. Quoted-string per the YAML formatting rules already in `tcn-content-plan/SKILL.md` § Step 9.

---

## 7. Posting rules updates

Additions to `tcn-content-plan/references/posting-rules.md`:

### 7.1 Platform Windows table — new row

| Platform | When to post |
|---|---|
| Facebook | Daily, 09:00-10:00 ET typical (or 19:00-21:00 ET fallback). Flagship days shift to 11:00-13:00 ET (must be after article publishes). |

### 7.2 New section — Facebook Rules

After "X Standalone Rules":

```
## Facebook Rules

- 1 post per day, 7 days a week (no weekend reduction).
- Purpose follows weekday rotation by default (see tcn-facebook-post/references/purpose-table.md § appendix).
- Monthly plan can override via FB: cell in the 30-day map entry.
- Shape and image source flow from purpose; never freehand — delegate to tcn-facebook-post.
- Hard restriction: never post the FB CTA before the flagship article is live on Fridays. Out-of-order publishing breaks the funnel.
```

---

## 8. Mode 1 and Mode 3 changes

### 8.1 Mode 1 (Check Today's Plan)

- After reading the existing daily plan file, check whether `## Facebook` section exists. If absent (file pre-dates this skill), surface: "This plan was drafted before FB support shipped — no FB content for today. Run /create-daily to regenerate, or accept the gap."
- The Mode 1 summary includes the FB row's recommendation as its own line alongside X and Notes summaries.
- The Status update block prompt at re-check time covers FB triggers alongside X and Notes triggers.

### 8.2 Mode 3 (Create Monthly Plan)

- After flagship hooks are picked (Mode 3 Step 2), assign FB purposes to each of the 30 days using the weekday rotation default; write each into the `FB:` cell of the entry.
- During the user interview, after presenting flagship picks, ask: "Any weeks where the FB rotation should shift? E.g., a week with two flagships might need a second hard-funnel day, or a quiet news week might lean more on Engagement posts." User's adjustments rewrite specific cells.
- The monthly plan's "Source Hooks" section gets a parallel "FB Cadence Note" section if non-default purposes were assigned, explaining the reasoning.

---

## 9. Edge cases

1. **`ai-image-prompts-skill` not available** — fall back to plain stock-photo search-query suggestion. Surface a one-liner: "AI image generation not available; using stock-photo search query instead."
2. **Flagship article hero image not available** — fall back to AI-generated for that FB post; surface the gap so Justin knows to update before posting.
3. **`anti-ai-writing-style.md` missing** — voice fallback per § 5.7. File's `status:` stays `draft`.
4. **News breaks against today's FB option after drafting** — News-dependent options move to Hold list at re-check time. If all FB options are News-dependent and triggers haven't fired, recommendation defaults to "hold the FB post today" rather than forcing a stale post.
5. **Flagship article URL not yet known at draft time** (article still being written Friday morning) — `tcn-facebook-post` produces options with `[ARTICLE_URL_PENDING]` placeholder; surfaces a hard reminder in the recommendation that the URL must be inserted before posting.
6. **Pre-existing daily plan files without `facebook_purpose:`** — Mode 1 surfaces the gap (see § 8.1). No automatic backfill; user explicitly regenerates if they want FB content for an old day.
7. **Weekday rotation says Awareness, but the live news is huge and Substack-relevant** — `tcn-content-plan` Step 3 should detect this gap. If live news strongly indicates funnel opportunity, the orchestrator can prompt: "Today's rotation is Awareness, but the news pulls toward funnel. Override to Soft funnel?" User confirms; the override flows through.

---

## 10. Quality bar additions

Extend the existing list at the bottom of `tcn-content-plan/SKILL.md`:

A daily plan works when (FB additions in **bold**, existing criteria preserved):
- ...all existing criteria...
- **FB copy was drafted by `tcn-facebook-post`, not freehanded in `tcn-content-plan`**
- **The FB option matches the day's purpose-table.md shape (caption ≤30 words OR paragraph 50-80 words)**
- **The FB image guidance is concrete: an AI prompt, a specific Substack URL for the hero, or a screenshot recommendation — never "find an image"**
- **The FB option carries a Safe or News-dependent label and appears in the schedule table + Status block**
- **No vague placeholder verbs ("hit a number," "saw movement," etc.) — hard fail**
- **Vocabulary cliff: every FB post is glossable to a reader with zero context on the beat**
- **Flagship CTA posts include the actual article URL, not a placeholder** (or, if URL pending, the recommendation flags the gap prominently)

---

## 11. Out of scope

- Posting automation (this skill produces content; Justin or future tooling posts manually).
- FB analytics integration (no metrics tracked back; engagement analysis is manual).
- Instagram cross-posting (different platform, different surface; would be a separate sister skill if ever wanted).
- Multi-image FB posts (single image per post; carousels not supported in v1).
- FB-thread-style "comment from author for reach" pattern (mentioned as a design alternative but rejected for operational simplicity in v1).
- LinkedIn voice changes (existing pattern unchanged; LinkedIn voice still freehanded in `tcn-content-plan` Step 7).
- Replacing the X/Notes shelf-life label taxonomy with the simplified FB two-state system (the three-state taxonomy stays for X and Notes; FB's two-state is a deliberate divergence justified by FB's different time-physics).
