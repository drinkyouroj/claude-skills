# Mining Playbook — Surfacing Candidate Backstage Moves

This is the **detection procedure** the `tcn-paid-note` skill runs at **Step 2** (design-spec §6), before it presents candidates to the writer (Step 3) and before it interviews (Step 4). Its job is to mine a finished flagship's workflow artifacts and surface **2–3 candidate analytical moves** — so the interview is a short, pointed steering conversation instead of a blank-slate "what do you remember?" recall exercise.

**This file owns the *procedure* for finding candidates. It does not own the *definition* of a conformant move.** The definition lives in the DNA doc, `workspace/paid/_template-thinking-behind-the-thinking-note.md` §3 ("the invisible move principle"). That section delegates detection here in so many words: *"How to detect candidate moves is the mining-playbook's job."* So the two files interlock — read the DNA §3 for *what* you are looking for; read this file for *where* it hides and *how* to extract it. Do not restate the format rules (furniture, word band, title formula, em-dash ban) here; those are the DNA doc's and `note-format-spec.md`'s.

Structural model: this file is to the DNA doc what a detection rulebook is to a style guide. The DNA defines the conformant output; this defines the search that feeds it.

**The single property that organizes everything below:** a paid note must feature a move that is **invisible in the published flagship** — reasoning that left no trace in the free article, because a subscriber who already read the free piece must get something they could not have reconstructed from it (DNA §1, §3). Three of the four sources below *find* invisible moves. The fourth source exists only to *subtract* the visible ones. Keep that asymmetry in mind: sources 1–3 add candidates, source 4 removes them.

---

## Acceptance contract

Given a flagship's manifest + draft versions, following this playbook must:

1. **Surface the number that changed** from the manifest's fact-check loop history (Samsung worked example: the iteration-3 `755%` division-vs-company attribution fix).
2. **Surface the sentence that almost shipped** from the draft diffs and the manifest's analytical commitments (Samsung worked example: the "same money" compression that was refused).
3. **Subtract the flagship's own confession** so it is *not* offered as a candidate (Samsung worked example: the "I read the wrong variable" Personal Code section, which is public and therefore off the list).

If, after working all four sources, no strong invisible move survives, the playbook's honest output is **"no strong note this week"** — see §"When mining comes up empty" below. Do not fabricate a move to fill the slot (DNA §3; design-spec §9).

---

## Preconditions (what must be true before mining)

- The flagship is **final** — manifest `status: ready-to-publish`, or the writer confirms (design-spec Step 0). Mining a moving target wastes effort; the diffs and the fact-check table aren't settled until the piece is done.
- You have located, in the flagship's `workspace/drafts/{slug}/` directory:
  - the **manifest** (`manifest.md`),
  - the **final draft** (highest-numbered `05-draft-vN.md`, or a `*-final.md`),
  - the **intermediate draft versions** (`05-draft-v1.md` … `05-draft-v{N-1}.md`).
- **Degraded layouts.** If the flagship has no manifest (older or flat-layout pieces), do not halt — mine the draft diffs if any draft versions are present, and otherwise fall back to interview-first (design-spec §9). Sources 1 and 3 below depend on the manifest; sources 2 and 4 depend only on drafts.

---

## The four sources

Each source is documented as: **what to read → what a candidate looks like → the Samsung worked example.** Work them in order. Sources 1–3 add candidates to the pool; source 4 removes the disqualified ones.

---

### Source 1 — Manifest fact-check loop history → *the number that changed*

**What to read.** Open `manifest.md` and find the **"Fact-check loop history"** table (the manifest section the `tcn-fact-check` ↔ `tcn-fact-reconcile` loop fills in during steps 8–9). Each row is one iteration; the columns record what was flagged before reconcile, what remained after, and the outcome. The cross-reference is the "Step progress" line for steps 8–9, which narrates the same fixes in prose.

**What a candidate looks like.** Every **flagged or corrected claim** is a candidate move. The richest ones are **precision fixes** — a number or attribution that was *defensible but not exactly right* in an early draft and got tightened once the writer sat with the primary source. These are strong candidates precisely because the *first* version is invisible: it was corrected before publish, so the free flagship shows only the final, correct number. The subscriber never saw the wrong one. That is the backstage. (Contrast a flagged claim that was simply *deleted* with no replacement — still a candidate, but usually a thinner one, because there is no "truer read" to land in beat ③.)

For each flagged row, capture: the claim, what it changed *from* and *to*, and which iteration caught it. The from→to delta is the move's beat ② (the breaking moment) and beat ③ (the corrected read) in miniature.

**Samsung worked example.** The manifest's fact-check loop history, iteration 3 (a user-requested deep re-run), records: *"1 precision flag (755% division→company)."* The Step-9 line elaborates: the iteration-3 reconcile fixed *"755% attribution + 2 sourcing upgrades,"* producing `05-draft-v5.md`. Reading the drafts confirms the delta — v1 read *"The **division's** profit had jumped 755% in a single year"*; v5 corrected it to *"**Samsung's** profit had jumped 755% **year over year**,"* because the 755% is Samsung Electronics **company-wide** for the March quarter, not a division-specific annual figure. **Candidate:** *"I attributed a 755% profit jump to the chip division; it was the whole company, for one quarter — I'd narrowed a company number to the division to make the chokepoint look more profitable than the data licensed."* This is invisible in the published flagship, which prints only the corrected "Samsung's profit had jumped 755% year over year."

---

### Source 2 — Draft v1→vN diffs → *the sentence that almost shipped*

**What to read.** Diff consecutive draft versions. A **reworked, rewritten, or cut** closer, frame, or claim is a candidate — especially a sentence that was *sharp* in an early draft and got softened, qualified, or removed. Run:

```bash
cd "workspace/drafts/<slug>"
for n in 1 2 3 4 5; do echo "=== v$n → v$((n+1)) ==="; diff <(cat 05-draft-v$n.md) <(cat 05-draft-v$((n+1)).md); done
```

(Adjust the loop bound to the actual highest version present, e.g. `for n in 1 2 3 4 5 6` if the final is `v7`. The `diff <(cat …) <(cat …)` form is used rather than bare `diff` so the output is robust to the files being read as streams; the substance is identical to a plain two-file `diff`.)

**What a candidate looks like.** Read the `<` (old) side of each hunk for a line that did real analytical work and then changed. Three shapes recur, each a candidate:

- **A cut closer or frame** — a sentence that ended a section or named the through-line, then got replaced. The most valuable kind: the *easy, shareable* version of the thesis that the writer talked themselves out of. (This is the canonical "I Almost Wrote ___" / "The Sentence I Cut" near-miss — DNA §4 exception test.)
- **A claim that got *softer*** — a flat assertion ("it lands on shareholders") rewritten into a hedged or mechanism-named version ("it eats the reinvestment that keeps a chokepoint a chokepoint"). The softening usually marks a place where the writer realized the strong version overclaimed.
- **A reordering that changes the argument** — a sentence moved from one section to another so two punches don't twin. The move is the *reason* for the move.

Cross-check the diff against the manifest's draft-notes / Notes block: a writer often records *why* a line was cut in the same breath as cutting it, which converts an ambiguous diff hunk into a confirmed analytical commitment (this is the handoff to Source 3).

**Samsung worked example.** Two complementary signals point at the same candidate:

- The v1 draft-notes block records, verbatim, the discipline as a pre-commitment: *"'Same money' claim: explicitly refused in §2."* So the writer *deliberately did not write* the easy line "the Samsung worker's bonus and your power bill are the same money."
- The v1→v2 diff shows the §2 (Protocol) profit-incidence paragraph being reworked: v1's flat *"So it lands on shareholders, and on the money that would have built the next factory. … The windfall isn't traveling down the supply chain. It's eating the reinvestment…"* is split out and relocated into its own isolated two-line paragraph (*"So the windfall lands on shareholders and on the budget for the next factory. It eats the reinvestment that keeps a chokepoint a chokepoint."*). The rework is the writer tightening exactly the place where a "the cost rolls downhill to you" claim would have been the easy, wrong version.

**Candidate:** *"My first instinct was to weld the Samsung bonus and the Ohio power bill with 'the same money.' Writing it plainly showed the dollars never meet — his bonus is division profit to shareholders; your bill is PJM's capacity-auction cost to ratepayers. The shared thread is the boom that caused both and the *leverage* that split them, not a dollar moving between them."* This sentence **never shipped** — it died in drafting — so it is fully invisible in the published flagship, which instead prints the audited version: *"his raise didn't pay for your bill, and your bill didn't fund his raise."*

> **Note on this worked example's status.** This is the move the manually-written 2026-06-10 note (`workspace/paid/2026-06-10-thinking-behind-the-thinking-windfall-thread.md`) actually featured — confirming that Source 2 + Source 3 together reproduce the human angle-selection the skill is meant to formalize (design-spec §1, §13).

---

### Source 3 — Manifest "analytical commitments" / Notes → *the discipline pre-committed to*

**What to read.** Open `manifest.md` and read the **"Notes"** section (and any "analytical commitments" baked into the seed/synthesis line). This is where the writer records, *before drafting*, the disciplines the piece will hold itself to — the compressions it will refuse, the parallels it will bound, the inferences it will flag rather than assert.

**What a candidate looks like.** A **pre-committed discipline** is a candidate when it names a tempting-but-wrong move the writer chose *not* to make. These are invisible by construction: a discipline that worked leaves no scar on the published text — the reader sees the clean final framing and has no way to know the writer fought for it. The note makes the restraint visible. Look specifically for commitments phrased as a refusal ("No X"), a bound ("X only along this axis, not that one"), or a flag ("X is inference, never asserted as fact").

A Source-3 commitment frequently **corroborates a Source-2 diff** — the diff shows the line changing, the Notes block says *why*. When they point at the same move, you have a single strong candidate with two independent pieces of evidence, not two candidates. Merge them.

**Samsung worked example.** The manifest's Notes section lists the seed's baked-in analytical commitments, including:

> **Weld = asymmetry**: same cause (AI boom), opposite directions — labor *captures* at the memory chokepoint; ratepayers/grid *absorb* at the transformer chokepoint. **No "same money" compression.**

and:

> **GAP 4 = named inference**: windfall incidence falls on shareholders/reinvestment; hyperscaler pass-through is Samsung *choosing* to use pricing power, flagged as inference, never asserted as a cost flow.

The first commitment is the **same move** Source 2 surfaced from the diff — the "same money" refusal — now confirmed as a deliberate pre-commitment rather than an accident of editing. **Merge them into one candidate** (the "same money" / asymmetry move), carrying both pieces of evidence: the manifest Notes commitment *and* the v1→v2 §2 rework. The GAP-4 commitment is a *second, distinct* candidate available from this source (the "could" verb discipline — refusing to assert the bonus is passed through to cloud customers when no source shows it), should the writer want an alternative to the "same money" move.

---

### Source 4 — The flagship's own confession section → **SUBTRACT it**

**What to read.** Scan the **final draft** for a first-person admission section — a passage where the writer openly says, *on the page in the free article*, that they got something wrong, changed their mind, or did a calculation by hand. In the TCN house structure this is often a "Personal Code" section, but it can be any visible mea-culpa ("I called this wrong," "I'd been quoting one number," "I had to add them in my head").

**What this source does (and why it is different).** Sources 1–3 *find* candidates. Source 4 *removes* them. **Any move the flagship already confesses openly is OFF the candidate list** — it is, by definition, *visible* in the published piece, so featuring it in the paid note would give a paying subscriber nothing they didn't already get free (DNA §3; design-spec §10, "Never features a move the flagship already confesses openly"). After listing candidates from Sources 1–3, run each one against the confession section: if a candidate *is* the confessed move, strike it. If a candidate merely *neighbors* the confessed move (same topic, different analytical step), keep it but steer the note's framing away from re-treading the public confession.

**Samsung worked example.** The final draft (`05-draft-v6.md`) carries a "Personal Code: I read the wrong variable" section in which the writer states publicly: *"I called this one wrong in April … I flagged the chip workers as a supply risk and watched for a walkout … Right chokepoint, wrong variable. They didn't walk out; they signed."* This "wrong variable" confession (strike-vs-contract; watching the threat instead of what the threat was for) **is public**, printed in the free flagship. **Subtract it.** It must not be offered as a candidate, and the note should steer away from it. (Note that subtracting it does *not* touch the two surviving candidates: the 755% fix and the "same money" refusal are different moves, neither of which the flagship confesses — the flagship prints the corrected 755% number with no note that it was ever the "division's," and the "same money" line never appears at all.)

---

## Candidate output shape

After working all four sources, emit the surviving candidates as a small structured list. Each candidate is:

```
{
  move:      <one sentence — the single analytical move, in the writer's "I did X; it broke; the truer read is Y" register>
  evidence:  <file + location — e.g., "manifest.md, fact-check loop history iteration 3" or "05-draft-v1.md §2 + v1→v2 diff">
  visibility: visible | invisible   <invisible in the published flagship is strongly preferred>
}
```

Rules for the list:

- **Prefer invisible.** A visible candidate (one the flagship confesses) should not normally appear at all — Source 4 strikes it. If a visible candidate survives only because nothing invisible was found, flag it as visible and tell the writer the honest situation (design-spec §9: "featuring a public confession shortchanges subscribers").
- **Cap at 2–3.** Two strong candidates beat three with a weak filler.
- **Never pad a weak third** (the editorial-honesty rule, borrowed from `tcn-flagship-cover`). If only two real moves exist, present two. If only one does, present one and say so. A padded third candidate wastes the writer's GATE-1 attention and signals false abundance.
- **Merge corroborating evidence into one candidate.** When Source 2 (a diff) and Source 3 (a Notes commitment) point at the same move, that is *one* candidate with two receipts, not two candidates. (Samsung: the "same money" diff rework + the "No 'same money' compression" Notes commitment = one candidate.)

**Samsung worked example — the assembled output.** Applying all four sources to the Samsung flagship yields exactly two strong candidates, with the public confession correctly excluded:

| # | Move (one line) | Evidence | Visibility |
|---|---|---|---|
| 1 | I welded the bonus and the power bill with "the same money"; tracing the dollars showed they never meet — the real shared thread is the boom that caused both and the leverage that split them. | `manifest.md` Notes ("No 'same money' compression") **+** `05-draft-v1.md` §2 and the v1→v2 diff (the refused easy version) | **invisible** (the line never shipped) |
| 2 | I attributed a 755% profit jump to the chip *division*; the primary source showed it was the *company*, for one *quarter* — I'd narrowed a company-wide number to make the chokepoint look more profitable than the data supported. | `manifest.md` fact-check loop history, iteration 3 ("755% division→company") **+** the v1→v5 drafts (division → Samsung / year over year) | **invisible** (only the corrected number is in print) |
| — | ~~I read the wrong variable: watched for a strike when the move was the contract.~~ | `05-draft-v6.md` "Personal Code: I read the wrong variable" | **visible → SUBTRACTED** (the flagship confesses it openly) |

This is the acceptance target: the playbook yields the "same money" and "755%" candidates and excludes "wrong variable."

---

## When mining comes up empty

Not every week leaves a backstage. Some flagships are produced frictionlessly: the fact-check loop exits clean on the first pass (no precision flags), the draft diffs show only copyedits (no cut frames, no softened claims), the manifest Notes carry no refused-compression commitments, and the only first-person admission is one the flagship already prints. When that happens:

- **Say so. Do not fabricate.** An honest "this week's production was frictionless; I did not find a strong invisible move" is a valid output (DNA §3; design-spec §9). A manufactured "and then it hit me" pivot is worse than admitting the week is thin.
- **Hand back to interview-first.** The files don't hold every move; some live only in the writer's head (design-spec §1, §6 Step 4). When mining is empty, the skill falls back to an interview-first flow — and may surface the **quiet method-note** shape (DNA §5: the Helium "I had to add them in my head" model), where the move is an unglamorous manual step the published piece never shows, rather than a dramatic correction.
- **Flag the possibility that the week lacks a strong note.** This is an allowed terminal state. A quiet method-note or an honest skip both beat dressing up a public confession as backstage access.

The litmus test for every candidate, applied before it reaches the writer: *could a subscriber have reconstructed this move from the free flagship alone?* If yes, it is not a paid-note candidate — it is Source-4 material, and it gets subtracted.

---

## One-paragraph summary (for a fresh agent)

Read the manifest's **fact-check loop history** for the number that changed (Source 1), **diff the draft versions** for the sentence that almost shipped (Source 2), and read the manifest **Notes** for the discipline pre-committed to (Source 3) — these three add candidates. Then scan the **final draft's confession section** and **subtract** any move it already admits (Source 4) — this one removes candidates. Merge corroborating evidence (a diff + a Notes commitment about the same move = one candidate). Emit 2–3 candidates as `{ move, evidence, visible|invisible }`, prefer invisible, never pad a weak third, and if nothing strong survives, say so and hand back to interview-first rather than fabricate.
