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

**Reference files** (load when needed):
- `references/note-formats.md` — all 7 Note formats with word counts and examples
- `references/posting-rules.md` — posting windows, weekly cadence, flagship-day structure

**Sister skills to delegate to** (use the Skill tool, do not freehand the prose):
- `tcn-post` — for every X/Twitter standalone or thread draft
- `tcn-substack-notes` — for every Substack Note draft
- `tcn-text-humanizer` — for the final AI-tells pass on the assembled file. This is the TCN-calibrated humanizer (Justin's voice, punctuation philosophy, "AI hit list"). Not `humanize-writing`, which is voice-agnostic and only produces a report.

**Voice context to load before any drafting** (read once per session, then keep them in working context):
1. `/Users/justin/Documents/substack-research/Substack Research/CLAUDE.md` — wiki agent rules, themes, "Writing Voice — Prose and Narration" section at the bottom
2. `/Users/justin/Documents/substack-research/Substack Research/workspace/core/anti-ai-writing-style.md` — VOICE DNA, banned list, BIG ONE (negative parallelisms), formatting rules

If either file has been read earlier in the conversation, do not re-read — rely on what is already in context. Otherwise read both **before** drafting any prose in Mode 2.

---

## Mode 1: Check Today's Plan

1. Determine today's date. Construct the expected filename: `YYYY-MM-DD-dayN-options.md` in `workspace/notes/`.
2. To find the correct day number N, check `workspace/plans/tcn-notes-30-day-map.md` for the entry matching today's date. If no monthly plan exists, count the existing note files in `workspace/notes/` to infer N.
3. **File exists** → read it. Then check the **Status update** block at the top of the file (template defined in Step 9):
   - **Block absent, empty, or timestamped more than ~2 hours ago** → prompt the user: "What's happened since [last timestamp or 'drafting time']? Any triggers fired or fizzled?" Use the answer plus the shelf-life labels on each option to fill in (or refresh) the block — mark every Frame-forward option as safe to post, mark every Data-forward / Conditional option as safe or hold based on whether its trigger fired, and write the result to the file before summarizing. The block is the answer to "what can I post?" so populate it first; don't make the user re-derive option dependencies from prose.
   - **Block is fresh** → display it directly. That's already the answer.
   After the status update is fresh, summarize the day's Notes, X standalone recommendation, and schedule table. Ask if anything else needs updating.
4. **File missing** → say "No plan exists for today yet — drafting one now" and proceed to Mode 2 for today's date.

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

### Step 3: Look up format assignments

Read `workspace/plans/tcn-notes-30-day-map.md` and find the entry for the target date to get that day's assigned formats. If the monthly plan doesn't exist or doesn't specify formats:
- Don't repeat the same format combination used in the prior 2 days
- Include at least one Primary Source Drop per 3-day window
- Reserve Article Tease for flagship publish days (typically Fridays when an article goes live)
- Reserve Cross-Domain Connection for days when two genuinely parallel stories exist in different domains

Load `references/note-formats.md` for format definitions before drafting.

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

### Step 8: Draft engagement notes

Name 4–6 specific writers or publications who are likely posting on today's topic. For each, state what specific angle, data point, or frame from today's content would make the comment worth reading. Don't write generic "add context" notes — be specific about what the reader would learn from the comment that they couldn't get from the original post.

For restacks: describe what kind of Note to look for (the argument to restack) and the one-sentence addendum to attach.

### Step 9: Write the file

Save to `workspace/notes/YYYY-MM-DD-dayN-options.md`.

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
week: N
day: N
formats:
  - "Format 1"
  - "Format 2"
  - "Format 3"
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

**Schedule summary table** — end every plan with this table. The **Depends on** column is the key scanning surface: each row states the specific news condition the recommended option requires, so the user can map a slot to a postability decision in one glance.

```
| Time | Platform | Content | Depends on |
|------|----------|---------|------------|
```

`Depends on` cell phrasing — match the option's shelf-life label:
- Frame-forward → `no trigger needed (frame survives any outcome)`
- Data-forward → the specific direction the news must point, e.g. `walkout proceeding`, `deal announced`, `collapse confirmed`
- Conditional → the specific event that must occur by posting time, e.g. `court ruling landed by 11am`, `vote passes before 3pm window`

If a slot's recommendation is itself conditional ("Option A unless walkout confirmed, then Option B"), put the dominant case in the row and add a second row beneath it for the fallback, so each row has exactly one trigger phrase.

### Step 10: AI-tells check (final pass — required, do not skip)

Even though `tcn-post` and `tcn-substack-notes` are voice-aware, the assembled options file can still leak AI fingerprints: banned vocabulary, closed em dashes, negative parallelisms, "It's not X, it's Y" constructions, rule-of-three lists, copulative avoidance, title-case headers, dead transitions, dismissal labels without explanation.

Invoke the `tcn-text-humanizer` skill via the Skill tool — **not** `humanize-writing`. `tcn-text-humanizer` is the TCN-specific humanizer: it knows Justin's punctuation philosophy (semicolons over em dashes, parentheses for asides), his rhythm references (Hunter S. Thompson, Vonnegut, R.L. Stine), and his explicit "AI hit list" of phrases that auto-fail. It also actively rewrites the prose rather than handing back a report.

Pass `tcn-text-humanizer` the prose blocks from the just-written options file at `workspace/notes/YYYY-MM-DD-dayN-options.md`: the Note option bodies, the X option bodies, the restack addenda, and the engagement comment angles. Do not feed it the YAML frontmatter, schedule table, or section headings — those aren't voice surfaces.

For each block returned, replace the original prose in the file with the humanized version via Edit. Preserve the surrounding scaffolding (option labels like "### Option A", italicized meta-commentary, image guidance lines) — only the prose body changes.

**Hard fail conditions** — if any of these survive `tcn-text-humanizer`'s pass, fix them immediately even if the skill didn't flag them. These are the non-negotiables from `anti-ai-writing-style.md`:
- A closed em dash (`—`) used as interruption or decoration inside drafted prose. Spaced em dashes used sparingly as connectives are acceptable per Justin's punctuation philosophy; closed em dashes are not.
- Any banned word from anti-ai-writing-style.md section 3A (delve, realm, harness, unlock, leverage, robust, seamless, etc.)
- Any negative parallelism (anti-ai-writing-style.md section 3F): "This isn't X, it's Y", "Not X. Y.", "It's not about X, it's about Y", etc.
- A dismissal label as substitute for explanation (anti-ai-writing-style.md section 3H): "X is theater", "X is a press release", etc.
- Title case in a header inside drafted prose (sentence case is the rule)
- A copulative-avoidance verb: "serves as", "stands as", "represents", "marks a", "boasts a"
- Any phrase from Justin's "AI hit list" (loaded inside `tcn-text-humanizer`): "Picture this:", "Dive into…", "It's important to note…", "A testament to…", "That really hits", etc.

After fixes, update the file's `status:` field from `draft` to `voice-checked` so future check-mode reads can see the file passed the gate.

---

## Mode 3: Create Monthly Plan

Run at the start of a new month or when the user explicitly asks for a fresh 30-day content map. This is a two-step process: surface what the wiki supports, then confirm with the user before building the map.

### Step 1: Run or read the insight sweep

Check `wiki/syntheses/` for an insight-sweep file created within the past 2 weeks. If one exists, read it and extract the top 5 hooks. If not, run the INSIGHT_SWEEP workflow from CLAUDE.md: read `wiki/overview.md`, all pages in `wiki/concepts/`, all pages in `wiki/entities/` with `sources: 5` or higher, and surface the strongest editorial hooks.

The insight sweep identifies what the wiki knows deeply enough to support a flagship piece right now. Pillar pieces built on thin wiki coverage will require source acquisition mid-month, which disrupts the schedule.

### Step 2: Interview the user

Present the top 3–5 hooks and ask:

> "Here are the strongest candidates for this month's flagship pieces based on what the wiki supports right now:
>
> [list hooks with one-line descriptions]
>
> Which ones do you want to anchor the month to? And are there live events on the calendar (Fed meetings, earnings, legislative votes, economic data releases) that should shape specific weeks?"

Wait for answers before building the map.

### Step 3: Generate the 30-day map

Structure the month around the chosen flagship pieces. For each flagship:
- Assign to a Friday (unrestricted posting window)
- Seed it in the 3–5 days before with Notes that build the analytical frame without giving away the argument
- Follow it the next day with an Article Tease Note
- Leave mid-week space for live-news-reactive Notes (Contested Claims, Primary Source Drops)

Map all 30 days as a numbered list. Each entry:
```
**Item [N] — [Date] ([Day of week])**: [Platform] | [Content type] | [Format] | CTA: yes/no | [Brief note: what this seeds or establishes]
```

### Step 4: Write the file

Save to `workspace/plans/tcn-notes-30-day-map.md`. Include a "Source Hooks" section at the end listing the insight-sweep hooks that informed the flagship selections, with wiki page citations.

---

## File Paths

| File | Path |
|---|---|
| Daily plans | `workspace/notes/YYYY-MM-DD-dayN-options.md` |
| Monthly plan | `workspace/plans/tcn-notes-30-day-map.md` |
| Wiki overview | `wiki/overview.md` |
| Wiki syntheses | `wiki/syntheses/` |
| Anti-AI style | `workspace/core/anti-ai-writing-style.md` |

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
