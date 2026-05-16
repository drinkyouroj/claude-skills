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

---

## Mode 1: Check Today's Plan

1. Determine today's date. Construct the expected filename: `YYYY-MM-DD-dayN-options.md` in `workspace/notes/`.
2. To find the correct day number N, check `workspace/plans/tcn-notes-30-day-map.md` for the entry matching today's date. If no monthly plan exists, count the existing note files in `workspace/notes/` to infer N.
3. **File exists** → read it and display its full contents. Summarize the day's Notes, X standalone recommendation, and schedule table. Ask if anything needs updating.
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

### Step 5: Draft the X standalone

Post anytime, no CTA. Draft 2–3 options using different angles (raw data, analytical frame, narrative). Each option: ≤50 words, self-contained, no link. Include a recommendation that specifies which option to use and when.

On flagship days, draft a 10-post X thread instead (see `references/posting-rules.md`).

### Step 6: Draft the Notes

For each Note format assigned to this day, write 2–3 options with full prose copy — not scaffolds or outlines, actual text ready to post. Each option must:

- **Be FRESH** — no data, frame, or claim from the SPENT list
- **Hit the word count target** — see `references/note-formats.md`
- **Cite the source** — name it in the Note text
- **Deliver what the format promises** — read the format definition before drafting; a Primary Source Drop that editorializes has failed its format; a Framework Hand that only presents data and draws no analytical move has failed its format

After the options for each Note, add: image/screenshot guidance (needed or not, and which one) and a one-sentence recommendation specifying which option to use and why.

### Step 7: Draft LinkedIn repost (flagship days only)

300–400 words. Professional register — no newsletter voice, no first-person analytical asides. Cite every figure. End with the article link. No CTA language.

### Step 8: Draft engagement notes

Name 4–6 specific writers or publications who are likely posting on today's topic. For each, state what specific angle, data point, or frame from today's content would make the comment worth reading. Don't write generic "add context" notes — be specific about what the reader would learn from the comment that they couldn't get from the original post.

For restacks: describe what kind of Note to look for (the argument to restack) and the one-sentence addendum to attach.

### Step 9: Write the file

Save to `workspace/notes/YYYY-MM-DD-dayN-options.md`. Required frontmatter:

```yaml
---
date: YYYY-MM-DD
week: N
day: N
formats: [Format1, Format2, Format3]
status: draft
live_news:
  - [live news items from Step 1]
duplication_audit:
  - SPENT this week (do not repeat): [specific data points, frames, sources — not just topics]
  - FRESH today: [what this day introduces for the first time]
---
```

Add `flagship_prep:` block on flagship days (humanize checklist, framing fixes to make before publish).

End every plan with a schedule summary table:

```
| Time | Platform | Content |
|------|----------|---------|
```

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
- Every Note uses content not in the SPENT list — verifiable by checking the prior files
- Each Note has 2–3 options with actual prose, not outlines
- The recommendation for each Note tells the user which option to use and why — not just "option A is good"
- The SPENT list is specific (cites data points and frames, not just topics) so it prevents future duplication
- Notes feel distinct from each other — they don't make the same analytical move in different words
- The schedule table gives a complete picture of the day at a glance
