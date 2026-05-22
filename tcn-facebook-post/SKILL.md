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

```markdown
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
```

Always produce 2-3 options. Single-option output is a quality-bar failure.

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
