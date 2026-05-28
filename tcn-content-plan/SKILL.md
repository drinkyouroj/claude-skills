---
name: tcn-content-plan
description: >
  Use this skill whenever the user asks to check, create, or generate a content plan for
  The Civic Node (TCN) Substack newsletter. Trigger on: "check today's plan", "what's the
  plan for today", "create the content plan for [date]", "day N plan", "monthly plan",
  "30-day map", "what should I post", "draft the notes for today", or any request to produce
  X standalone options, Substack Note copy, or engagement guidance for a specific day.
  Also triggers for start-of-month planning requests. Use this skill even if the user
  doesn't name it explicitly — if they're asking about TCN daily or monthly content
  structure in any form, this is the right skill.
---

# TCN Content Plan Skill

Handles three modes. Identify which one the user is requesting and jump straight to it.

| User intent | Mode |
|---|---|
| "Check today's plan" / "what's the plan" / no date | **Mode 1: Check** |
| "Create the plan for [date]" / "day N" / explicit date | **Mode 2: Create Daily Plan** |
| "Monthly plan" / "30-day map" / "start of month" | **Mode 3: Create Monthly Plan** |

---

## Voice & vocabulary canonical source

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule (§ 1), the banned-words list (§ 3A), dead phrases / transitions / engagement bait / hype language (§ 3B–§ 3E), the negative-parallelism rule (§ 3F), tribal-coded crypto cringe and operational shibboleths (§ 3G), the dismissal-label rule (§ 3H), the vocabulary cliff rules including the meaning-preservation sub-principle (§ 3I), the closing-line abstraction rule (§ 3J), the broader AI writing patterns to avoid (§ 4), and the anti-overfitting guide (§ 5).

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on a copy embedded in this spec. Any examples cited here for illustration only must include a pointer back to the canonical file as authoritative.

**Fallback when the canonical file is missing.** If `workspace/core/anti-ai-writing-style.md` is not present in the current project, this skill must:
1. Flag explicitly to the user — "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip all voice-related work — no vocabulary substitution, no AI-tells audit, no closing-line check, no Step 10 humanize pass.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: produce the structural plan for Modes 1, 2, and 3 (status block, shelf-life labels, schedule table, format assignments, duplication audit, source citations) and surface drafts from sister skills as-is; mark the file's `status:` as `draft` rather than `voice-checked`. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The canonical file's § 1 notes the always-gloss-on-first-use rule is conservative; a future enhancement would vary gloss aggressiveness by which adjacent cohort each piece targets (monetary-policy pieces gloss crypto terms more heavily; DePIN pieces gloss monetary terms; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, Steps 5 and 6 would pass an adjacency label to `tcn-post` and `tcn-substack-notes` so they can tune gloss aggressiveness per option.

---

**Reference files** (load when needed):
- `references/note-formats.md` — all 7 Note formats with word counts and examples
- `references/posting-rules.md` — posting windows, weekly cadence, flagship-day structure
- `references/pillars.md` — the 5 stable editorial pillars and rotation rules (consumed by Mode 3 renewal flow)

**Sister skills to delegate to** (use the Skill tool, do not freehand the prose):
- `tcn-post` — for every X/Twitter standalone or thread draft
- `tcn-substack-notes` — for every Substack Note draft
- `tcn-text-humanizer` — for the final AI-tells pass on the assembled file. Justin's voice, punctuation philosophy, and rhythm references live in that skill spec; banned vocabulary, negative parallelisms, vocabulary cliff, and closing-line rules live in the canonical `workspace/core/anti-ai-writing-style.md`. Not `humanize-writing`, which is voice-agnostic and only produces a report.

**Voice context to load before any drafting** (read once per session, then keep them in working context):
1. `/Users/justin/Documents/substack-research/Substack Research/CLAUDE.md` — wiki agent rules, themes, "Writing Voice — Prose and Narration" section at the bottom
2. `workspace/core/anti-ai-writing-style.md` (project-relative) — VOICE DNA, banned list, negative parallelisms, vocabulary cliff, closing-line abstraction, formatting rules. This is the canonical source named in the section above.

If either file has been read earlier in the conversation, do not re-read — rely on what is already in context. Otherwise read both **before** drafting any prose in Mode 2.

---

## Mode 1: Check Today's Plan

### Step 0: Runway check (do this first, before anything else)

Determine the active monthly plan: `workspace/plans/30-day-content-plan-{YYYY-MM}.md` where `YYYY-MM` is today's calendar month (e.g., `30-day-content-plan-2026-06.md` for June 2026).

Read its frontmatter `expires_at:` field. Compute `days_remaining = expires_at - today`.

Check whether a WIP shortlist exists at `workspace/plans/.next-month-shortlist-WIP.md`. If yes, read its `target_month:` to confirm it's for the upcoming month.

Check the active plan's `created:` field. If `created == today`, skip the runway warning entirely (Mode 3 already ran today; don't nag).

Emit at most one runway message per Mode 1 invocation, per this table:

| Days remaining | WIP exists? | Message |
|---|---|---|
| ≥ 8 | n/a | (no message) |
| 7 | no | "Heads up — 7 days left in the [Month] plan. Want to start the next-month conversation soon?" |
| 7 | yes | (no message — already in motion) |
| 5 | no | "5 days left in the [Month] plan. Reasonable time to start Pass 1 of the next-month conversation. Start now, or finish today's check first?" |
| 5 | yes | "WIP shortlist exists from [WIP last_updated date], ready to resume Pass 2 when you are." |
| 3 | no | "3 days left in the [Month] plan and no shortlist WIP exists. Strongly recommend starting now — type 'next month' and I'll move into Mode 3." |
| 3 | yes | (no message — resumption already surfaced at 5d, don't double-nag) |
| 1 | n/a | "Tomorrow is [first day of next month] and there's no [next month] plan yet. Today's check will proceed, but if we don't draft the new plan today, tomorrow's Mode 1 falls back to weekday-default Note formats and FB purpose (no flagship anchor)." |
| 0 or negative | n/a | "We're in [current month] and there's no [current month] plan. Drafting daily plans against weekday-default Note formats and FB purpose until you run Mode 3 for the new month." |

After emitting the message (if any), proceed to Step 1.

### Step 1: Build today's daily plan path

Determine today's date and weekday. Construct the expected filename: `YYYY-MM-DD-{lowercase_weekday}-options.md` in `workspace/notes/` (e.g., `2026-05-15-friday-options.md`). The weekday is lowercase and spelled in full — `friday`, not `Friday`, not `fri`.

### Step 2: Determine day number N

Read the `day:` frontmatter field from each existing note file in `workspace/notes/` and take the max + 1 as today's N. The day number is a continuous counter across the whole notes archive and is no longer carried in the monthly plan. Do not try to parse N from filenames — filenames use the lowercase weekday, not the day number.

### Step 3: Branch on daily file existence

**File exists** → read it. Then check the **Status update** block at the top of the file (template defined in Mode 2 Step 9):

- **Block absent, empty, or timestamped more than ~2 hours ago** → prompt the user: "What's happened since [last timestamp or 'drafting time']? Any triggers fired or fizzled?" Use the answer plus the shelf-life labels on each option to fill in (or refresh) the block — mark every Frame-forward option as safe to post, mark every Data-forward / Conditional option as safe or hold based on whether its trigger fired, and write the result to the file before summarizing. The block is the answer to "what can I post?" so populate it first; don't make the user re-derive option dependencies from prose.
- **Block is fresh** → display it directly. That's already the answer.

After the status update is fresh, summarize the day's Notes, X standalone recommendation, **FB post recommendation**, and schedule table. Ask if anything else needs updating.

**FB-specific check:** if the file lacks a `## Facebook` section (was drafted before this skill shipped), surface: "This plan was drafted before FB support shipped — no FB content for today. Run /create-daily to regenerate, or accept the gap." Do not auto-regenerate; let the user decide.

**File missing** → say "No plan exists for today yet — drafting one now" and proceed to Mode 2 for today's date.

---

## Mode 2: Create Daily Plan

Follow all steps in order. Don't skip the live news prompt or the duplication audit — those two steps determine what the Notes can and can't say.

### Step 1: Prompt for live news

Ask before drafting anything:

> "What's happening today that's worth anchoring the Notes to? Any data releases, votes, decisions, or stories that just broke? (Say 'nothing specific' and I'll work from the monthly plan.)"

Note angles depend on what's happening. A Framework Hand on CPI data and a Framework Hand on a Fed vote are completely different pieces. Getting live context first prevents drafting Notes that feel detached from the news cycle.

### Step 2: Duplication audit

Read all note files in `workspace/notes/` from the past 14 days (or all files for the current month if fewer). For each file, extract:
- **Data points cited**: specific numbers, statistics, source names, ratios
- **Analytical frames used**: cross-domain connections, contested claims, specific mechanisms named
- **X standalone angles**: topics and framing used in prior standalones

Build the SPENT list — everything that appeared in any prior Note and must not be repeated today. Then identify what's FRESH: new data from live news, new sources not yet cited, new analytical moves not yet made. This audit is the single most important quality control step. Repeating content from prior days is the most common failure mode.

### Step 3: Look up format assignments and FB purpose

**Monthly plan filename:** `workspace/plans/30-day-content-plan-{YYYY-MM}.md` where `YYYY-MM` is the target date's calendar month.

**Note formats:** If the monthly plan exists, find the row in its `## Daily Operational Map` table that matches the target date and read the "Notes formats" column (comma-separated list of 1–3 format names). If the plan doesn't exist, doesn't have a Daily Operational Map, or the row is blank, fall back to:
- Don't repeat the same format combination used in the prior 2 days
- Include at least one Primary Source Drop per 3-day window
- Reserve Article Tease for flagship publish days (typically Fridays when an article goes live)
- Reserve Cross-Domain Connection for days when two genuinely parallel stories exist in different domains

Load `references/note-formats.md` for format definitions before drafting.

**Facebook purpose:** From the same Daily Operational Map row, read the `FB purpose` column. If present, use its value (one of: `Awareness`, `Engagement`, `Soft funnel`, `Flagship CTA`). If absent or the monthly plan doesn't exist, fall back to the weekday rotation:

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

### Step 4: Determine week, cadence, and flagship status

**Week number**: `ceil(day_number / 7)`. Day 1–7 = Week 1, Day 8–14 = Week 2, etc.

**Notes per day**:
- Week 1: 1–2 Notes
- Week 2+: 3 Notes

**Engagement target**: see `references/posting-rules.md`.

**Flagship day** = Friday AND the monthly plan lists a flagship article publishing this week. Flagship days have a different structure — see `references/posting-rules.md`.

### Step 4b: Shelf-life rule (read before drafting)

**Schedule note**: Time-sensitive content has two layers — the **durable analytical frame** (the argument or pattern that survives any outcome) and the **perishable operational claim** (the news-cycle hook the post is anchored to). The post's life is determined by the shorter of the two; a strong frame welded to a stale claim dies with the claim. Surface that split at the option level so future-you doesn't have to re-derive it at posting time.

Every option produced in Step 5 and Step 6 must carry one of three shelf-life labels, written inline next to the option header:

- **Frame-forward** — durable across multiple outcomes. References things that have already happened (vote cast, demand published, data already reported, statement on the record). Survives whether the predicted event lands or not. This is the default-safe pick.
- **Data-forward** — depends on a specific news cycle pointing the same direction (collapse confirmed, walkout proceeding, deal announced, ruling landed). Lives or dies with that direction.
- **Conditional** — tied to a specific event that may or may not happen by posting time (court ruling, vote outcome, mediation result). Becomes unpostable if the event flips or fails to occur on schedule.

**Every slot must produce at least one Frame-forward option as the default-safe pick.** The other 1–2 options can be Data-forward or Conditional to capture the upside when a trigger fires — but the slot must never depend on a trigger firing in order to post at all.

Each option's shelf-life label feeds two downstream artifacts in this file:
1. The **Depends on** cell in the schedule summary table (Step 9) — written as the specific trigger phrase ("walkout confirmation", "court ruling landed by 11am", "no trigger needed").
2. The **Status update** block (Step 9) — at re-check time, the labels determine which options are safe to post and which are on hold.

### Step 5: Draft the X standalone (delegate to `tcn-post`)

Invoke the `tcn-post` skill via the Skill tool. Pass it:
- Today's live news (from Step 1)
- The SPENT/FRESH lists (from Step 2)
- The shelf-life rule (from Step 4b) — `tcn-post` must label each option
- The instruction: "Draft 2–3 X standalone options for today, no CTA, ≤50 words each, self-contained, different angles (raw data / analytical frame / narrative). Cite source in the post itself. **Tag each option with a shelf-life label — Frame-forward, Data-forward, or Conditional — and the specific news trigger it depends on (e.g., 'walkout confirmation', 'no trigger needed').** At least one option must be Frame-forward so the slot is postable regardless of how the news breaks."

Do not freehand the X copy in this skill. `tcn-post` owns the X voice, hook rules, and Civic Node viral-post process. Capture its output verbatim under the "X STANDALONE" section of the plan file.

On flagship days, ask `tcn-post` for a 10-post X thread instead of standalones (see `references/posting-rules.md` for thread structure). The thread as a whole carries one shelf-life label; if any single post inside it is Conditional, the thread inherits the Conditional rating.

After receiving the draft, add a one-sentence recommendation that names the conditional logic explicitly — e.g., "Use Option A (Frame-forward) by default; switch to Option B (Data-forward) if the walkout is confirmed before the posting window." `tcn-post` returns options; the plan picks and states the dependency in plain English.

### Step 6: Draft the Notes (delegate to `tcn-substack-notes`)

For each Note slot assigned to this day, invoke the `tcn-substack-notes` skill via the Skill tool. Pass it:
- The assigned format (Framework Hand, Primary Source Drop, etc.) — load the format definition from `references/note-formats.md` first and include the key constraints in the request
- The SPENT/FRESH lists (from Step 2) — `tcn-substack-notes` must avoid the SPENT items
- The live news context (from Step 1) and the source citation it should anchor to
- The shelf-life rule (from Step 4b) — `tcn-substack-notes` must label each option
- The instruction: "Draft 2–3 options for one Note in [format]. Each option must hit the word count, name the source, deliver what the format promises, and respect the FRESH/SPENT split. **Tag each option with a shelf-life label — Frame-forward, Data-forward, or Conditional — and the specific news trigger it depends on.** At least one option per slot must be Frame-forward so the slot is postable regardless of how the news breaks."

Do not freehand the Note prose in this skill. `tcn-substack-notes` owns Justin's Substack voice, the Marcus reader persona, the conversion-driving frame, and the format-specific quality bars. Capture its output verbatim under each Note's heading.

After receiving each draft, add: image/screenshot guidance (needed or not, and which one), and a one-sentence recommendation that names the conditional logic explicitly — e.g., "Default to Option A (Frame-forward, no trigger needed); use Option C (Conditional) only if the court ruling lands before noon."

**Format-quality contract** — when invoking `tcn-substack-notes`, repeat these constraints from `references/note-formats.md` in the request so they don't drift:
- A Primary Source Drop that editorializes has failed its format
- A Framework Hand that only presents data and draws no analytical move has failed its format
- An Operator Observation that doesn't speak in first-person operational specifics has failed its format

### Step 7: Draft LinkedIn repost (flagship days only)

300–400 words. Professional register — no newsletter voice, no first-person analytical asides. Cite every figure. End with the article link. No CTA language.

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

### Step 8: Draft engagement notes

Name 4–6 specific writers or publications who are likely posting on today's topic. For each, state what specific angle, data point, or frame from today's content would make the comment worth reading. Don't write generic "add context" notes — be specific about what the reader would learn from the comment that they couldn't get from the original post.

For restacks: describe what kind of Note to look for (the argument to restack) and the one-sentence addendum to attach.

### Step 9: Write the file

Save to `workspace/notes/YYYY-MM-DD-{lowercase_weekday}-options.md` (e.g., `2026-05-15-friday-options.md`). The day number lives in the frontmatter and the title block, not the filename — the weekday in the filename makes operationally important patterns visible at a glance (Friday = flagship publish day, weekend = restricted posting window).

**YAML formatting rules** (Obsidian uses a strict parser — violating these makes the file render with a broken frontmatter block):

1. **Wrap every list item value in double quotes.** Any unquoted string that contains `:` followed by a space, an apostrophe, a comma followed by space, `#`, `&`, `*`, `[`, `]`, `{`, `}`, `|`, `>`, `%`, `@`, `` ` ``, or a leading `-`/`?` will break the parser. Quoting unconditionally is simpler than auditing for unsafe characters.
2. **Use `|` block scalars for any value longer than one line.** Block-scalar content does not need internal escaping — colons, dashes, apostrophes all pass through literally. This is the right choice for the SPENT/FRESH narrative blocks.
3. **`formats` must be a YAML list, not a comma-joined string.** Use either block style (one item per line with `-`) or flow style (`[A, B, C]`). Never write `formats: A, B, C` — that parses as a single string.
4. **Escape any literal `"` inside a double-quoted value as `\"`.**
5. **Indent list items two spaces under their key.** Indent continuation lines of a block scalar two spaces beyond the key.

Required frontmatter template:

```yaml
---
date: YYYY-MM-DD
weekday: lowercase_weekday   # full name, lowercase — e.g., friday, saturday
week: N
day: N
formats:
  - "Format 1"
  - "Format 2"
  - "Format 3"
facebook_purpose: "Awareness"  # one of: Awareness, Engagement, Soft funnel, Flagship CTA
status: draft
live_news:
  - "First live news item. Colons, apostrophes, em dashes all safe inside the quotes."
  - "Second item: data release, vote, decision, or breaking story."
duplication_audit:
  spent_this_week: |
    Use a literal block scalar for the SPENT list. Semicolon-separated phrases work
    well here because the parser doesn't try to interpret any of the punctuation.
    Example: Hormuz 191/3,000 crossings; April CPI energy +3.8% MoM + Hormuz
    mechanism; rate tool doesn't reach supply shocks; instrument > independence.
  fresh_today: |
    Same format. List the new data, sources, and analytical moves this day
    introduces for the first time.
---
```

On flagship days, append a `flagship_prep:` block — also as a block scalar:

```yaml
flagship_prep: |
  Draft: workspace/drafts/[slug].md
  Needs humanize pass before midnight tonight.
  Fix [specific framing issue] before publish.
```

**Before writing**, sanity-check the YAML by mentally parsing each value: if you removed the quotes, would the parser still treat it as one string? If not, the quotes are doing real work and must stay.

**Status update block (template — leave the body empty at drafting time)**

Place this section directly under the YAML frontmatter, before any other content. At drafting time, write the heading and leave the body fields empty (or write the literal placeholders below). The block gets filled in at the day's first re-check — manual prompt like "what can I post?" or via `/loop` monitoring — and answers the posting question in roughly 10 seconds without re-reading the rest of the file. Do not try to predict the news state at drafting time; the point of the block is to capture state at posting time.

```markdown
## Status update — [HH:MM ET, day of week] (empty until first re-check)

**News state since drafting:**
- [what changed — vote happened, deal collapsed, hearing scheduled, walkout proceeded]
- [what is still pending — which expected trigger has not fired yet]

**Safe to post today:**

| Slot | Option | Why this survives any outcome |
|------|--------|-------------------------------|
| [HH:MM, platform] | [A/B/C, label] | [one sentence — names the durable claim that holds regardless of the pending trigger] |

**Hold (trigger has not fired):**
- [Slot, option letter] — waiting on [specific news condition]
- [Slot, option letter] — waiting on [specific news condition]
```

The block is short on purpose. If it grows past ~10 lines you're rewriting the plan instead of indexing it; cut back to the safe/hold split.

**FB rows in the Status block:** FB options labeled `Safe` go in the Safe-to-post table alongside X and Notes. FB options labeled `News-dependent` go in the Hold list with the trigger phrase. Same scanning surface, no new columns.

**Facebook section template** — place this section after `## LinkedIn` (if present, on flagship days) and before `## Engagement`:

```markdown
## Facebook

[paste the markdown block returned by tcn-facebook-post verbatim]
```

The block already contains the `**Purpose:**` / `**Shape:**` / `**Posting time:**` header, the option subsections (`### Option A` etc.), the image guidance, and the recommendation. Do not reformat.

**Schedule summary table** — end every plan with this table. The **Depends on** column is the key scanning surface: each row states the specific news condition the recommended option requires, so the user can map a slot to a postability decision in one glance.

```
| Time | Platform | Content | Depends on |
|------|----------|---------|------------|
```

The FB row uses the same 4-column structure with purpose inline in the Content cell:

```
| 09:00 ET | Facebook | Caption (Awareness): [option A summary] | Safe |
```

For Flagship CTA days, the time is post-publish (e.g., `11:30 ET`).

`Depends on` cell phrasing — match the option's shelf-life label:
- Frame-forward → `no trigger needed (frame survives any outcome)`
- Data-forward → the specific direction the news must point, e.g. `walkout proceeding`, `deal announced`, `collapse confirmed`
- Conditional → the specific event that must occur by posting time, e.g. `court ruling landed by 11am`, `vote passes before 3pm window`

If a slot's recommendation is itself conditional ("Option A unless walkout confirmed, then Option B"), put the dominant case in the row and add a second row beneath it for the fallback, so each row has exactly one trigger phrase.

### Step 10: AI-tells check (final pass — required, do not skip)

Even though `tcn-post` and `tcn-substack-notes` are voice-aware, the assembled options file can still leak AI fingerprints. Invoke the `tcn-text-humanizer` skill via the Skill tool — **not** `humanize-writing`. `tcn-text-humanizer` is the TCN-specific humanizer: it loads Justin's voice calibration from its own spec (punctuation philosophy, rhythm references) and the universal AI-pattern catalog from `workspace/core/anti-ai-writing-style.md`. It actively rewrites the prose rather than handing back a report.

Pass `tcn-text-humanizer` the prose blocks from the just-written options file at `workspace/notes/YYYY-MM-DD-{lowercase_weekday}-options.md`: the Note option bodies, the X option bodies, the restack addenda, and the engagement comment angles. Do not feed it the YAML frontmatter, schedule table, or section headings — those aren't voice surfaces.

**FB prose is explicitly NOT passed to `tcn-text-humanizer`.** The humanizer is calibrated for Justin's Substack voice (closed em dashes, copulative avoidance, specific rhythm). Running it over FB-Explainer prose would over-correct the plain-English register back into Substack voice. The FB section must be audited separately — see the hard-fail conditions below.

For each block returned, replace the original prose in the file with the humanized version via Edit. Preserve the surrounding scaffolding (option labels like "### Option A", italicized meta-commentary, image guidance lines) — only the prose body changes.

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

Do not duplicate the lists here. If a check needs to verify a specific term or phrase, read the canonical file. If any item fires, fix immediately even if the skill didn't flag it.

After fixes, update the file's `status:` field from `draft` to `voice-checked` so future check-mode reads can see the file passed the gate. If the canonical file was missing (fallback case), leave `status: draft` and surface the missing-file note in the status update block.

---

## Mode 3: Create Monthly Plan

Run when the user explicitly asks for a fresh 30-day content map, or when Mode 1's runway escalation prompts the user to start the next-month conversation and they accept.

Load `references/pillars.md` before doing anything else — the 5 pillars and the rotation rules govern flagship selection.

### Step A: Determine target month and check for existing state

Determine the **target month**: the calendar month the new plan will cover.
- If today is in the same calendar month as the active plan's `month:` field, the target is the *next* calendar month.
- If there's no active plan, or the active plan's `month:` is already in the past, the target is the current calendar month.
- If the user explicitly named a target ("plan for July"), use that.

Check for a WIP shortlist file at `workspace/plans/.next-month-shortlist-WIP.md`:

| WIP state | Action |
|---|---|
| No WIP file | Proceed to Step B. |
| WIP exists, `target_month` matches | Read its `state:` field. Jump directly to the right pass: `pass-0-in-progress` → resume Step C; `pass-1-in-progress` → resume Step D from the first unmarked candidate; `pass-2-in-progress` → resume Step E from the first un-walked candidate; `ready-to-generate` → confirm with user, then go to Step F. |
| WIP exists, `target_month` does not match | Ask: "WIP exists for [old target month] but we'd be planning [new target]. Discard the old WIP and start fresh, or resume the old one?" Branch on answer. |

Check for a prior plan: scan `workspace/plans/` for files matching `30-day-content-plan-YYYY-MM.md` and find the most recent. This is the **prior plan**.

| Prior plan state | Branch |
|---|---|
| Exists (renewal case) | Proceed through Steps B → C → D → E → F → G. |
| Does not exist (first-ever case) | Skip to **Step F-first-time** at the end of this mode. |

### Step B: Compute candidate sets (silent — no user interaction)

Read the prior plan in full. Extract:
- Its `flagships:` frontmatter list (or, if absent, parse the Spine table)
- Its `source_hooks:` block (or, if absent, the Source Hooks section)
- Its `month:` field for the prior month's date window

Read these inputs in parallel:
- `published/` — every file with publish date in the trailing 60 days (slugs + frontmatter titles)
- `wiki/syntheses/` — all files; also all `wiki/concepts/` and `wiki/entities/` pages modified since the prior plan's `created:` date (use `git log --since=<date> --diff-filter=AM wiki/` if available; else mtime comparison)
- `wiki/syntheses/` — `Insight Sweep — *` and `insight-sweep-*` files regardless of date (used in Step B.2 escalation if fired)

Compute three lists:

1. **Wiki delta** — wiki pages added since the prior plan's `created:` date, or expanded by ≥30% (size or new section). One-line hook per page from the page's frontmatter `query:` or first heading.
2. **Unused eligible** — wiki pages with `sources: 5+` that are NOT named as flagship anchors in the active plan OR any of the prior 3 archived plans. Read each candidate archived plan's `flagships:` frontmatter list (or Spine table fallback) to compute "named as flagship anchor."
3. **Recently published exclusion** — slugs + topic phrases extracted from `published/` filenames and frontmatter titles for the trailing 60 days.

Candidate pool = `union(wiki_delta, unused_eligible) MINUS recently_published`.

**News-state annotation pass.** For each surviving candidate, run a web search: `"[candidate topic phrase]" news last 30 days`. Capture top 3–5 results (outlet + angle + date) and label the candidate:

- **COLD** — no major-outlet coverage in 30 days
- **WARM** — 1–2 significant pieces, conversation has not saturated
- **HOT** — 3+ significant pieces, mainstream conversation is active

Store the label plus a one-line prose summary on each candidate. If a search fails (network, rate limit), label `SEARCH_FAILED` and surface to the user before Step D.

**Step B.2: Single-topic dominance escalation.** After news-state annotation, check whether the wiki delta is dominated by a single topic cluster (any one of: ≥70% of delta candidates reference the same concept/entity page; ≥70% share their primary cited source; ≥70% of hook descriptions share the same dominant noun phrase).

If single-topic dominance fires, check:
- Most recent insight sweep date (`wiki/syntheses/insight-sweep-*` or `Insight Sweep — *.md` — max mtime)
- Count of files in `raw/` with mtime after the most recent insight sweep

Then branch:

| Sweep age | Raw/ activity | Surface to user |
|---|---|---|
| Stale (>7 days) | n/a | "Wiki delta is dominated by [topic cluster]. Last insight sweep was [N days ago]. Want me to run a fresh insight sweep before we continue Pass 1?" |
| Fresh (≤7 days) | High (≥10 new raw/ files) | "Wiki delta is narrow and dominated by [topic cluster]. The last insight sweep is recent ([N days ago]) but [M] new files have landed in raw/ since then. Suggest: ingest the new raw/ batch into the wiki first, then re-run the insight sweep, then resume here. Proceed with ingestion?" |
| Fresh (≤7 days) | Low | "Wiki delta is narrow and dominated by [topic cluster]. Recent insight sweep already reflects current raw/ material. Options: (a) proceed with the narrow pool — pick one strong angle from the cluster, (b) defer renewal a week to give raw/ time to grow, (c) lower the source-count bar on 'unused eligible' to surface deeper-tail candidates. Which?" |

Branch on user direction. If user chooses to run a sweep or ingest, do so, then re-enter Step B from the top with the broadened input. Otherwise proceed to Step C.

### Step C: Pass 0 — Carryover from prior plan

Cross-reference the prior plan's `flagships:` list against `published/` filenames within the prior plan's date window. Match by slug similarity and frontmatter title similarity. Compute a best-guess `shipped` / `didn't ship` split.

Present:

> "From the [Prior Month] plan, here's what I think shipped vs. didn't — please confirm:
>
> **Shipped (found in published/):**
> - [Flagship name] → matched to `YYYY-MM-DD-slug.md`
>
> **Didn't ship (no match in published/):**
> - [Flagship name] → original rationale: [pulled from prior plan's Source Hooks]
>
> For each didn't-ship: carry forward to [Target Month], defer to later, or drop entirely?"

Wait for answers. Write all decisions to the WIP file at `workspace/plans/.next-month-shortlist-WIP.md`, setting `state: pass-1-in-progress` once Pass 0 closes.

### Step D: Pass 1 — Broad keep/cut/maybe

Present the candidate pool with news-state annotations, in this order:

```
## Carryover (from Pass 0)
- [Flagship name] — your rationale: [pass-0 answer]

## Wiki delta (new or expanded since prior plan)
- [Page] — added/expanded YYYY-MM-DD, sources: N, hook: [one-line]
  News state (last 30d): [COLD/WARM/HOT] — [prose summary of outlets + angles]

## Unused eligible (high source coverage, not yet a flagship)
- [Page] — sources: N, last touched YYYY-MM-DD, hook: [one-line]
  News state (last 30d): [...]

## Recently published (excluded — shown for reference)
- YYYY-MM-DD-slug.md
- ...
```

Ask:

> "Mark each candidate as **keep**, **cut**, or **maybe**. We'll deep-dive the keep+maybe pile in Pass 2."

Wait for answer. Record marks to the WIP file. Set `state: pass-2-in-progress` and proceed.

### Step E: Pass 2 — Walk the shortlist

For each keep + maybe candidate, in order, present:

> "**[Candidate name]**
> Wiki support: [list of supporting pages with source counts]
> Operator angle: [what your operator credibility uniquely adds — pulled from the wiki page's `operator_observation:` field if present, else inferred from the page's frontmatter, else asked of you]
> Nearby published: [any `published/` piece in the trailing 60 days touching the adjacent topic, with overlap-risk note]
> Calendar context: [WebSearch result for the candidate's topic + the target Friday window — overlap with FOMC dates, data releases, earnings, hearings, votes that could affect attention. Mandatory — if search fails, write 'search failed; manually verify before deciding']
>
> Flagship (Friday anchor), seed Note (Tuesday/Thursday warm-up), or defer?"

The web search is **not optional**. If it returns nothing relevant, the line reads "no event-window pressure surfaced in search."

Wait for answer per candidate. Record to WIP. Block further "Flagship" decisions once `fridays_in_target_month` flagship slots are filled — surface: "All N flagship slots filled — remaining decisions are seed Note vs. defer."

After all candidates walked, run an **independent month calendar sweep**:

WebSearch:
- FOMC meeting dates in target month (Federal Reserve calendar)
- BLS major data releases for target month (CPI, jobs report, PCE)
- Congressional / Supreme Court major calendar items
- Major earnings landmarks if target month is in earnings season
- Election deadlines or political calendar items relevant to TCN beats

Present digest organized by week:

> "Here's the [Target Month] calendar I'm seeing — anything I missed, or context you want to add to specific weeks?
>
> **Week 1 (Jun 1–7)** — [events with dates]
> **Week 2 (Jun 8–14)** — [events with dates]
> ...
>
> What should shift?"

The framing is "what should shift?", not "are there events I should know about?" — your input augments a complete-feeling baseline.

Apply shifts (reassign Friday flagships, add seed-Note triggers, add posting-window notes). Set `state: ready-to-generate` and proceed.

### Step F: Generate the 30-day map

Compose the target month's plan file at `workspace/plans/30-day-content-plan-{YYYY-MM}.md` using the template in the **Plan template** section below.

**Validate before writing:**
- Frontmatter parses as YAML
- `flagships:` list has entries matching `fridays_in_target_month`
- `pillar_order:` contains valid pillar numbers (1–5)
- Every flagship date falls within the target month
- The chosen pillar order does not repeat the Friday-1 pillar from the prior plan (per `references/pillars.md` rotation rule 3)
- The closer slot (typically the last Friday) is not the same pillar that closed the prior plan (rotation rule 2)

If any validation fails, surface the specific failure and halt. Do NOT delete the WIP file.

On validation pass: write the file. Then delete `workspace/plans/.next-month-shortlist-WIP.md`.

### Step G: Confirm with the user

Print a summary:

> "Plan for [Target Month] written to `workspace/plans/30-day-content-plan-{YYYY-MM}.md`.
>
> Flagships (one per Friday):
> - [Date, pillar, title]
> ...
>
> Pillar order: [list]
> Closer: [last Friday's flagship + pillar]
>
> WIP shortlist deleted. Ready to use."

### Step F-first-time: Simpler flow when no prior plan exists

Used only when `workspace/plans/` has no archived `30-day-content-plan-YYYY-MM.md` files.

1. Run the INSIGHT_SWEEP workflow from the substack-research `CLAUDE.md`: read `wiki/overview.md`, all `wiki/concepts/`, all `wiki/entities/` with `sources: 5+`. Surface the top 5 hooks.
2. Ask: "Here are the strongest candidates for this month's flagship pieces based on what the wiki supports right now: [list with one-line descriptions]. Which ones do you want to anchor the month to?"
3. Run the independent month calendar sweep from Step E (without the per-candidate web search — there's no shortlist to walk).
4. Write the plan file using the template in **Plan template** below. Mark `source_hooks.generated_from: "first-time"` in the frontmatter.

### Plan template

```yaml
---
title: "30-Day Content Plan — [Month YYYY]"
month: YYYY-MM
type: synthesis
tags: [content-plan, editorial-calendar, substack, twitter, linkedin, facebook]
created: YYYY-MM-DD
expires_at: YYYY-MM-DD              # last day of the month
prior_plan: "30-day-content-plan-YYYY-MM.md"   # null if first-time
sources: N
query: "..."

pillar_order:
  - N    # Pillar number from references/pillars.md
  # ...

flagships:
  - date: YYYY-MM-DD
    pillar: N
    title: "..."
    wiki_anchor: "wiki/.../..."
  # ...

source_hooks:
  generated_from: "renewal"          # or "first-time"
  carryover_from_prior:
    - "..."
  wiki_delta_added:
    - "..."
  unused_eligible_pulled:
    - "..."
  news_state_at_generation:
    "[Page title]": "COLD"
    "[Page title]": "HOT — Bloomberg + FT + Reuters"
---

# 30-Day Content Plan — [Month YYYY]

## Revision Log
[Running notes on cuts/recasts/replacements with reasoning. Empty at generation; appended as the month progresses.]

## Spine
[Friday | Issue | Pillar table — one row per flagship Friday]

## Weekly Rhythm + Time Budget + Hook Methodology
[As in prior plans]

## The Calendar
[# | Date | Platform | Pillar | Format | Topic/Angle | Hook A | Hook B | Hook C | CTA | Purpose]

## Daily Operational Map
[| Date | Weekday | Notes formats (1-3) | FB purpose |]

## Pillar Coverage Audit
[Per-pillar accounting of which issues hit each]

## Purpose Mix
[Authority / Growth / Connection percentages]

## FB Cadence Note
[Only if non-default FB rotation used; explains the shift]

## Source Hooks
[Insight-sweep + wiki-delta + unused-eligible hooks with wiki page citations]

## What This Plan Deliberately Does Not Include
[Anti-patterns the plan respects]
```

### Renewal flow guardrails (anti-patterns — must not happen)

1. **Never silently auto-promote carryover items.** Every carryover appears in Pass 0; user confirms each. The skill does not decide that something carries.
2. **Never overwrite an existing plan file without user confirmation.** If `30-day-content-plan-{target_month}.md` already exists at write time, halt and surface: "A plan for [target_month] already exists. Replace, append, or abort?"
3. **Never skip the news-state web search for shortlisted candidates.** If web search fails for a candidate, the annotation reads "search failed — manually verify before deciding." Never silently present without context.
4. **Never auto-filter candidates by news_state HOT.** The label is annotation only; editorial decision belongs to the user.
5. **Never write to archived plan files.** Once a plan moves out of the active month, it is read-only. The renewal flow reads `prior_plan` for carryover; that is the only access.
6. **Never delete the WIP file before plan validation passes.** Cleanup is the last step, gated on validation.
7. **Never let Mode 1's runway warning fire on a day Mode 3 has already been run.** Cooldown until the new plan's `created:` date passes (already enforced by Mode 1 Step 0).
8. **Never invent more flagship slots than the target month has Fridays.** `fridays_in_target_month` is a hard cap.
9. **Never run Pass 2 without Pass 1 complete.** State machine enforced via the WIP `state:` field.
10. **Never present a candidate that's in the recently-published exclusion list as a "keep" recommendation.** Recently-published is a hard filter on the candidate pool.

---

## File Paths

| File | Path |
|---|---|
| Daily plans | `workspace/notes/YYYY-MM-DD-{lowercase_weekday}-options.md` |
| Monthly plan (active + archives) | `workspace/plans/30-day-content-plan-{YYYY-MM}.md` |
| Renewal WIP shortlist | `workspace/plans/.next-month-shortlist-WIP.md` |
| Archived dead artifacts | `workspace/plans/_archive/` |
| Wiki overview | `wiki/overview.md` |
| Wiki syntheses | `wiki/syntheses/` |
| Raw research material | `raw/` |
| Anti-AI style | `workspace/core/anti-ai-writing-style.md` |
| Pillars reference | `references/pillars.md` (this skill) |

---

## Quality bar

A daily plan works when:
- The YAML frontmatter parses cleanly in Obsidian (list items quoted, multi-line content uses `|` block scalars, `formats` is a real list)
- Notes were drafted by the `tcn-substack-notes` skill and X copy by `tcn-post`, not freehanded inside this skill
- Every Note uses content not in the SPENT list — verifiable by checking the prior files
- Each Note has 2–3 options with actual prose, not outlines
- **Every option carries a shelf-life label (Frame-forward, Data-forward, or Conditional) and a specific dependency phrase** — labels are not optional and not generic
- **Every slot has at least one Frame-forward option** so the slot is postable regardless of how the news breaks
- The recommendation for each slot names the conditional logic explicitly — "Option A by default; B if X" — not just "option A is good"
- The SPENT list is specific (cites data points and frames, not just topics) so it prevents future duplication
- Notes feel distinct from each other — they don't make the same analytical move in different words
- **The schedule summary table has a populated `Depends on` column** — every row states the specific trigger or "no trigger needed"
- **An empty Status update block exists at the top of the file**, ready to be filled in at the first re-check
- The `tcn-text-humanizer` check ran and the file's `status:` is `voice-checked` — no closed em dashes, no banned vocab, no negative parallelisms, no "AI hit list" phrases in the drafted prose
- **FB copy was drafted by `tcn-facebook-post`, not freehanded in this skill**
- **The FB option matches the day's purpose-table.md shape** (caption ≤30 words OR paragraph 50-80 words; outside range = hard fail)
- **The FB image guidance is concrete:** an AI prompt, a specific Substack URL for the hero, or a screenshot recommendation — never "find an image"
- **The FB option carries a Safe or News-dependent label** and appears in the schedule table + Status block
- **No vague placeholder verbs** ("hit a number," "saw movement," etc.) — hard fail
- **Vocabulary cliff fully glossed:** every FB post is glossable to a reader with zero context on the beat
- **Flagship CTA posts include the actual article URL**, not a placeholder (or, if URL pending, the recommendation flags the gap prominently)

A monthly plan works when:
- The file is named `30-day-content-plan-{YYYY-MM}.md` with `YYYY-MM` matching the `month:` frontmatter field
- Frontmatter includes `month`, `created`, `expires_at`, `pillar_order`, `flagships`, `source_hooks`, `prior_plan` (null for first-time) — and they parse as valid YAML
- The `flagships:` list has length `== fridays_in_target_month`
- Every flagship date falls within the target month
- `pillar_order:` contains valid pillar numbers (1–5) per `references/pillars.md`
- The Friday-1 pillar does not repeat the prior plan's Friday-1 pillar (rotation rule 3)
- The closer pillar does not repeat the prior plan's closer pillar (rotation rule 2)
- The body includes all required sections: Revision Log, Spine, Weekly Rhythm, The Calendar, Daily Operational Map, Pillar Coverage Audit, Purpose Mix, Source Hooks, What This Plan Deliberately Does Not Include
- The Daily Operational Map has a row for every date in the target month (`fridays_in_target_month` flagship Fridays inclusive; flagship-Friday rows note "see Calendar")
- The `source_hooks.news_state_at_generation:` field has an entry for every shortlist candidate that became a flagship
- If renewal: the WIP shortlist file was deleted as the final step (no orphan WIP after a successful generation)
- If renewal: every "carryover" flagship has a documented original rationale in the Source Hooks section
