---
name: tcn-paid-note
description: "Writes the weekly 'Thinking Behind the Thinking' paid backstage note for The Civic Node — a ~365–490 word (240 floor) first-person process essay that exposes ONE analytical move from behind that week's flagship article. Mines the flagship's manifest, draft-version diffs, and fact-check history for candidate moves, then interviews Justin to steer the angle before drafting to the locked format. Invoke when Justin says 'write the paid note', 'this week's paid article', 'paid piece', 'backstage note', 'thinking behind the thinking', 'the process note for [flagship]', or points at a finished flagship and asks for its paid companion. Does NOT write the flagship (tcn-draft / tcn-article-builder), the paid cover (manual template / future tcn-paid-cover), social posts (tcn-post), or Substack Notes (tcn-substack-notes)."
---

# The Civic Node — "Thinking Behind the Thinking" Paid Note

## What This Skill Does

Produces a saved, finished backstage note for a week's flagship TCN article — the paid "Thinking Behind the Thinking" companion. The skill **extracts the backstage**; it does not summarize the draft. It loads the locked prose DNA from `workspace/paid/_template-thinking-behind-the-thinking-note.md`, reads the finished flagship and its workflow exhaust (manifest, draft-version diffs, fact-check history), mines that exhaust for 2–3 candidate analytical moves, lets the writer pick one, interviews the writer to extract what the files can't hold, drafts to the locked format, and saves the note to `workspace/paid/YYYY-MM-DD-thinking-behind-the-thinking-{slug}.md`. The saved file is the deliverable — a note that exists only in the chat is not finished.

---

## Why Interview, Not Summarize

`tcn-flagship-cover` compresses what is *already visible* in the finished article. A paid note's raw material is the **opposite**: the move that left no trace in the published text — the number that changed before publish, the sentence that almost shipped and got cut, the parallel that was the original thesis until the dollars were traced and it fell apart. A subscriber already read the free flagship; the note's contract is to show them a move they could **not** have reconstructed from it.

That material lives in two places, and neither is the published prose. Part of it is the **workflow exhaust** — the manifest's fact-check loop history, the v1→vN draft diffs, the manifest's recorded analytical commitments — which the skill mines mechanically. The rest lives in **the writer's head**: why the wrong version was tempting, the moment it broke, the felt experience of distrusting a line. Mining cannot reach that; only the interview can. So mining makes the interview short and pointed (steering, not blank-slate recall), and the interview is load-bearing, not decorative.

---

## Where This Sits

| Surface | Skill |
|---|---|
| Paid "Thinking Behind the Thinking" note prose | **this skill** |
| The flagship article it sits behind | `tcn-draft` / `tcn-article-builder` (this skill reads the finished flagship; it never writes one) |
| The paid-note cover image | manual template available now at `workspace/paid/_template-thinking-behind-the-thinking-cover.md` — locked composition, four variable substitutions; future `tcn-paid-cover` will automate it. This skill **offers** the cover as a handoff but does not generate it. |
| Flagship Substack covers | `tcn-flagship-cover` (different system, different DNA) |
| Substack Notes | `tcn-substack-notes` |
| X / LinkedIn / Facebook social posts | `tcn-post` |
| Image generation itself | out of scope entirely |

This skill = **paid note prose only**.

---

## Inputs and Outputs

### Required input

- A reference to the **finished flagship**: a file path, a slug, or a piece title that maps to a slug. The skill resolves this in Step 1 and verifies it is final in Step 0.

### Optional inputs

- **Steering** — free-text guidance on which move to feature ("do the 755% one," "the cut sentence, not the number").
- **Pre-confirmed frontmatter** — the writer supplies `pillar` / `published` / `source_url` up front; the skill still echoes them back for confirmation.

### Primary output artifact

- **File:** `workspace/paid/YYYY-MM-DD-thinking-behind-the-thinking-{slug}.md` (the date is the note's `published` date — the flagship date + 5 days, Fri → Wed).
- **Frontmatter:** every field in the DNA doc § 9, validated against [`references/note-format-spec.md`](references/note-format-spec.md) § 1 before saving.
- **Body:** the locked furniture skeleton (title repeat, italic subtitle, `Process note —` line, closing refrain) wrapping a first-person essay of **365–490 words (target), 240 hard floor** (a 240–364 note is allowed only when the move is genuinely tight — the validation layer warns but does not block), with 2–4 flagship-sourced primary links and zero body em dashes.

---

## The Process

Seven steps, three gates (GATE 1 = candidate pick; GATE 2 = the interview; GATE 3 = draft approval).

### 0. Preconditions

Verify both before doing anything else:

- The flagship is **final** — its manifest reads `status: ready-to-publish`, or the user explicitly confirms it is done. Mining a moving target wastes effort; the diffs and the fact-check table aren't settled until the piece is.
- The DNA doc exists at `workspace/paid/_template-thinking-behind-the-thinking-note.md`.

If either is missing, **halt and ask** — do not guess. The DNA doc is the format spec the skill enforces; the skill cannot operate without it.

### 1. Locate the flagship + load context

Resolve the flagship file in this order, first match wins:

1. **Explicit path** from the user.
2. **Newest `workspace/drafts/{slug}/`** whose `manifest.md` reads `status: ready-to-publish`.
3. **Ambiguous** (multiple `ready-to-publish` candidates, or a title not a slug) → list candidates, ask which.

If nothing matches, halt and ask for the path. Then read in full: the **final draft** (highest `05-draft-vN.md`, or a `*-final.md`), the **manifest**, the **DNA doc**, and the **existing exemplar notes**. Enumerate the notes by their **dated form** and exclude templates and covers — the broad `*-thinking-behind-the-thinking-*.md` glob wrongly matches the DNA doc and the cover files:

```bash
ls workspace/paid/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-thinking-behind-the-thinking-*.md \
  | grep -v -- '-cover'
```

Never hardcode the installment count — the series grows weekly. If `workspace/core/anti-ai-writing-style.md` exists, load it too (the house voice governs the note's prose).

### 2. Mine for candidate moves

Run the detection procedure in [`references/mining-playbook.md`](references/mining-playbook.md). Four sources, worked in order: the manifest's **fact-check loop history** (*the number that changed*), the **draft v1→vN diffs** (*the sentence that almost shipped*), the manifest's **analytical commitments / Notes** (*the discipline pre-committed to*) — these three *add* candidates — and the flagship's own **confession section** (the playbook's fourth source — "Source 4"), which exists only to *subtract* the moves the published piece already admits openly. Merge corroborating evidence (a diff + a Notes commitment about the same move = one candidate). Prefer invisible moves.

**Degraded layout:** if the flagship has no manifest (older / flat-layout), do not halt — mine the draft diffs if present, else fall back to interview-first.

### 3. Present candidates → writer picks — GATE 1

Present the surviving 2–3 candidates via `AskUserQuestion`, each as `{ one-line move, evidence (artifact + location), visible/invisible }`. The writer responds: **pick one**, **"different move"** (re-mine with steering), or **"combine."** **Never pad a weak third candidate** — editorial honesty over feature completeness (the rule borrowed from `tcn-flagship-cover`). If mining surfaced only one strong move, present one and say so. If the only candidate is the flagship's public confession, flag it and ask for an off-the-page move (featuring a public confession shortchanges subscribers).

### 4. Interview to steer — GATE 2 (the heart)

Run the interview in [`references/interview-question-bank.md`](references/interview-question-bank.md): 3–5 targeted questions, **one at a time**, leading with the move-type opener (fact-check change / cut sentence / pre-committed discipline / quiet method note) then rejoining the four beats (wrong read → breaking moment → corrected read → lesson). **Cardinal rule: never ask what mining already answered** — lead with the artifact's *what*, extract the *why it was tempting* and the *moment it broke*. Push once for a concrete pivot at the breaking-moment beat; if none exists, route to the quiet method-note shape or flag that the week may lack a strong note — do **not** manufacture false drama. Confirm (don't impose) the title-formula instance and a proposed closer aphorism — `AskUserQuestion` works here too.

### 5. Draft to the locked format

Compose against the DNA doc: the four furniture lines (§6), the four beats (§5), **365–490 body words (target), 240 hard floor** (a 240–364 note is allowed only when the move is genuinely tight), **zero em dashes in the body** (the locked `Process note —` furniture line is the only one), 2–4 primary-source links reused from the flagship's own sourcing, and the founding-tier refrain at the close. Derive the frontmatter (DNA §9) and **confirm `pillar`, `published`, and `source_url`** with the writer — no field is silently assumed. Run the pre-save checks in [`references/note-format-spec.md`](references/note-format-spec.md) (§§1–3: frontmatter, furniture, body em-dash / word-count / link gates) before presenting.

### 6. Present draft → revise — GATE 3

Show the full drafted note. The writer responds: **approve**, **revise specific lines** (the series iterates at the line level), or **"wrong move, restart at Step 3."** Apply line edits in place and re-run the body gates after any change that could affect them.

### 7. Save + hand off

Write the note to `workspace/paid/YYYY-MM-DD-thinking-behind-the-thinking-{slug}.md`. Stamp `created` / `updated` to today and set an accurate `word_count` at this step (not estimated earlier). **Re-run the `note-format-spec.md` pre-save gate one final time** — a failing furniture or body em-dash check blocks the save. Then report the path back with a one-line summary of the featured move (so the conversation log captures the decision), and **offer the cover as the next step** (manual template now; future `tcn-paid-cover`).

**No saved file = the note is not finished**, regardless of whether the writer has seen it in the chat. The artifact is the deliverable.

---

## What This Skill NEVER Does

- **Generate the cover image or the cover prompt.** Scope is note prose only; the skill offers the cover handoff and stops.
- **Write a flagship article.** That's `tcn-draft` / `tcn-article-builder`. This skill reads the finished flagship; it never authors one.
- **Write Substack Notes** (`tcn-substack-notes`) or social posts (`tcn-post`).
- **Fabricate a backstage move** to fill an empty week. An honest "no strong note this week" or a quiet method-note beats a manufactured "and then it hit me."
- **Feature a move the flagship already confesses openly.** A move visible in the free piece gives the paying subscriber nothing — Source 4 of the mining playbook subtracts it.
- **Pad to a third weak candidate.** Two strong moves beat three with filler.
- **Put an em dash in the body.** The locked `Process note —` furniture line is the only em dash permitted; the body proper has none (use semicolons, periods, parentheses, commas).
- **Skip Step 7.** The saved file is the deliverable.

---

## Failure Modes

| Situation | Behavior |
|---|---|
| Flagship not found / not final | Halt, ask for the path. Don't guess. |
| Multiple `ready-to-publish` candidates | List them, ask which. |
| DNA template doc missing | Halt with the path — the skill can't operate without the format spec. |
| **Mining finds no strong move** (frictionless production) | Don't fabricate. Say so, fall back to interview-first, flag that the week may lack a strong note. |
| **Only candidate is the flagship's public confession** | Flag it; ask for an off-the-page move (featuring a public confession shortchanges subscribers). |
| Flagship has no manifest (older / flat-layout) | Degrade: mine draft diffs if present, else interview-first. Don't halt. |
| No cinematic breaking moment | Allowed — offer the quiet method-note shape (the Helium model). Don't force false drama. |
| Writer rejects all candidates | Re-mine with steering, or go interview-first. |

---

## Reference Files

- [`references/mining-playbook.md`](references/mining-playbook.md) — the detection procedure for Step 2. The four sources where backstage moves hide (fact-check history, draft diffs, manifest Notes — these add candidates; the flagship's confession — this subtracts them), with detection heuristics, the candidate output shape, and the Samsung worked example end to end. Owns *finding* the move.
- [`references/interview-question-bank.md`](references/interview-question-bank.md) — the steering interview for Step 4. The four beats turned into questions, move-type variant openers, the title/closer confirmation, the empty-handed path, and the five interview-discipline rules (chief among them: never ask what mining already answered). Owns *eliciting* the texture.
- [`references/note-format-spec.md`](references/note-format-spec.md) — the pre-save validation checklist for Steps 5 and 7. The frontmatter schema, the four-furniture-line checklist, and the body gates (em-dash scan, word-count band, primary-link count) as mechanical checks. Owns *verifying* the draft. The format authority itself is the DNA doc.

---

## Companion Systems

**Upstream** (this skill reads from):

- `tcn-article-builder` (orchestrator) — produces the finished flagship **and its manifest**, which together are this skill's required input and its mining substrate. The richness of the note depends on the manifest's fact-check loop history and draft-version trail surviving intact.

**Shared source-of-truth doc:**

- `workspace/paid/_template-thinking-behind-the-thinking-note.md` — the locked prose DNA: series purpose, the single-move rule, the invisible-move principle, the title formula and its exception, the four beats, the furniture lines, body rules, the closer-aphorism pattern, the frontmatter spec, and the exemplar gallery. The skill loads it every run and references it rather than duplicating its content, so format updates propagate without skill edits.

**Sibling** (separate, do not invoke this skill for it):

- `tcn-paid-cover` (future) — automates the locked paid-note cover template. Until it exists, the cover stays manual; this skill offers the handoff at Step 7 but never generates the cover.
