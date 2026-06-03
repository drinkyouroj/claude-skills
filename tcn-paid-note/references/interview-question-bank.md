# Interview Question Bank — Steering the Note at GATE 2

This is the **interview** the `tcn-paid-note` skill runs at **Step 4** (design-spec §6), the second of the two gates. It runs **after** the writer has already picked one move at GATE 1. By the time you reach this file, the move is chosen — your job is not to find a move, it is to **extract the writing-process texture the artifacts don't hold** (what the writer was thinking, what almost shipped, the felt experience) and to **lock the four beats + the title + the closer before drafting**.

**Boundary — where this file sits in the pipeline.**

- **Detection is already done.** `mining-playbook.md` owns finding candidate moves (its four sources → the number that changed, the sentence that almost shipped, the discipline pre-committed to, minus the flagship's public confession). Do **not** re-run detection here. The interview begins with a move in hand. The single most common failure is asking the writer a question mining already answered — see "Interview discipline" below.
- **Format is owned elsewhere.** The DNA doc (`workspace/paid/_template-thinking-behind-the-thinking-note.md`) owns the *shape* of the output: the four beats (§5), the title formula and its exception (§4), the closer-aphorism pattern (§8), the quiet-method variant (§5). The frontmatter schema and furniture checklist live in `note-format-spec.md`. This file does **not** restate those rules. It turns the beats into **questions that elicit them**, and references the DNA by section for the rules themselves.

The interview produces five things the drafter then needs: the **four beats** (wrong read, breaking moment, corrected read, lesson), a **title decision** (default formula vs. the near-miss exception), and a **closer aphorism** (approved or supplied). Everything below exists to land exactly those.

---

## The four beats — default questions (ask verbatim)

The note moves through four beats in order (DNA §5). Each beat has one default question. These are the spine of every interview; the move-type openers below replace only the *first* question, then you rejoin this sequence.

**Beat ① — The wrong read**
> "What was the first/easiest version of the connection or claim — the one that would've been most shareable?"

This elicits the move's starting point: the easy, shareable version the writer began with and later left behind. It must be owned in the first person ("I started by joining them with money"), not described from the outside. If the writer answers with the *correct* read, you have the wrong end of the move — re-ask for the version that came first, before the correction.

**Beat ② — The breaking moment**
> "What specific source, number, or sentence exposed it? When did you *see* it was wrong?"

This is the load-bearing beat (DNA §5: it "must be tangible, not a mood"). Push for a **concrete pivot** — a named source, a specific number, a sentence the writer wrote down. "I realized it didn't hold up" is not an answer; "writing 'same money' in plain words and then trying to follow the dollars" is. If the writer can only give a mood, either dig for the tangible artifact behind the mood or fall to the empty-handed path below (the move may be a quiet method note, where beat ② is a disclosed technique rather than a thunderclap).

**Beat ③ — The corrected read**
> "What replaced it, and why is the replacement truer rather than just safer?"

The "truer, not safer" framing is deliberate and load-bearing (DNA §5). A note that swaps a sharp claim for a hedged one is just timid; a note that swaps a *wrong* read for a *truer* one is analysis. Make the writer name why the replacement is more correct, not merely more cautious. If the honest answer is "it's safer," the move may be weaker than it looked at GATE 1 — surface that rather than dress retreat up as insight.

**Beat ④ — The lesson**
> "State the discipline in one transferable line — the rule a reader could carry to the next piece."

This becomes the closer aphorism (DNA §8). It generalizes *this* move one level — a rule that outlives the specific story. See "Title & closer confirmation" below for how to confirm or supply it; do not leave the closer for the drafter to invent from scratch.

---

## Move-type variant openers (tuned FIRST question)

GATE 1 hands you a move of a known **type** — because the mining playbook found it through one of its four sources, each of which surfaces a different kind of move. Lead beat ① with the opener tuned to that type, then rejoin the default beat sequence (②→③→④) above. Each opener is built to **lead with what mining already found** so the writer steers rather than recalls (see "Interview discipline").

**(a) Fact-check change** — *the number that changed* (mining Source 1; the manifest's fact-check loop history).
> "Mining shows [number/attribution] changed from [old] to [new] at fact-check iteration [N]. What did the early version let you claim that the corrected one doesn't — and why was the first number tempting?"

The move here is the *delta*: what the wrong number bought the argument before it was tightened. The from→to is on the page already (lead with it); what you're extracting is the **temptation** — why the looser number felt right, which the artifact can't tell you.

**(b) Cut sentence** — *the sentence that almost shipped* (mining Source 2; the draft v1→vN diffs).
> "The diff shows you cut [sentence] between v[X] and v[Y]. Read it back to me as you first wrote it — what made it the most shareable line in the draft, and what made you not trust it?"

The move is a near-miss (this is the canonical `I Almost Wrote "___"` / `The Sentence I Cut` case — DNA §4 exception). The cut line is in the diff; don't ask *what* you cut. Ask what made it seductive and what tripped the writer's instinct against it — the felt moment of distrust the diff can't record.

**(c) Pre-committed discipline** — *the refusal/bound* (mining Source 3; the manifest's analytical commitments / Notes).
> "The manifest records you committing up front to [the refusal/bound, e.g. 'no same-money compression']. What was the tempting version you were guarding against — and has writing the piece taught you why that guardrail holds in general?"

A pre-committed discipline is invisible by construction (a guardrail that worked leaves no scar on the published text — DNA §3 via mining Source 3). The commitment is recorded; what's missing is the **tempting move it was guarding against** and the *generalizable why*. That why is often the closer.

**(d) Quiet method note** — *a method reveal with no dramatic pivot* (DNA §5 quiet-method variant; the Helium model).
> "Walk me through the step you did by hand that the published piece never shows. What does the platform/source give you by default, and what did you have to do yourself to see what was really there?"

**Do not force a "breaking moment" here.** This move-type has no thunderclap; beat ② is a *disclosed technique*, not a pivot (DNA §5: the Helium "I had to add them in my head" model). The wrong read is usually "trusting the default/headline number"; the method is the manual step; the corrected read is what the manual step revealed. If you find yourself trying to manufacture an "and then it hit me" for a method note, stop — the unglamorous manual step **is** the move.

---

## Title & closer confirmation

These two decisions must be locked before drafting (design-spec Step 4). The skill **confirms** them with the writer; it does not impose them (DNA §4: "the decision is the writer's, and the skill confirms which one fits rather than imposing it").

**Title** (DNA §4 for the rules — the `I Had the Wrong ___` default, the unit-of-the-error blank, and the near-miss exception):
> "Does `I Had the Wrong ___` fit, or is this a near-miss you caught pre-publish (use `I Almost Wrote ___`)?"

The deciding question is **did the error reach print** (DNA §4 exception test, quotable verbatim). If something *was* wrong in the published flagship, the default correction frame fits. If the writer caught it in drafting so nothing shipped wrong, the near-miss shapes (`I Almost Wrote "___"` or `The Sentence I Cut`) describe the process more honestly — though **either framing is acceptable when the writer caught it pre-publish** (the windfall note kept `I Had the Wrong Thread` despite being a near-miss). Offer the call; don't make it for them. Fill the blank with the **unit of the error** (a single analytical object — "thread," "number," "protagonist"), never a topic-word or a vibe.

**Closer** (DNA §8 for the rules — the two families):
> "Give me the closing aphorism, or approve mine: ___."

Always arrive with a proposed closer (derived from the beat-④ answer) so the writer reacts to something concrete rather than facing a blank. Choose which family to propose from (DNA §8): the **series signature** ("When the private analysis produces a correction, the published work should say so") when the move is cleanly a correction; a **fresh move-specific aphorism** when the move is a method, a near-miss, or a two-number split the signature line would undersell. The closer should feel inevitable given the body — the reader arrives at the discipline, then the line names it.

---

## Empty-handed path (when there is no crisp breaking moment)

If, after pushing on beat ②, the writer **cannot** produce a concrete pivot — no named source, no specific number, no sentence that broke the read — do **not** invent one (DNA §5: "a fabricated 'and then it hit me' is worse than an honest 'here is the unglamorous step I took'"; design-spec §9). Take one of two honest exits:

1. **Offer the quiet method-note shape** (DNA §5). Ask the method-note opener (d) above: was there an unglamorous manual step the published piece never shows — a number summed by hand, a source cross-checked off-platform, a calculation the tool doesn't do for you? If yes, the move is a method reveal, beat ② becomes a disclosed technique, and the note runs fine without a thunderclap.

2. **Flag that the week may lack a strong note.** If there is no breaking moment *and* no quiet method step, the honest output is that this week's production may have been frictionless and may not yield a strong backstage note (design-spec §9). Surface that to the writer plainly. A skipped week or an honest "no strong note this week" beats a manufactured pivot. **Never fabricate** a breaking moment to fill the slot.

---

## Interview discipline

Five rules govern *how* the interview runs, not just what it asks:

1. **One question at a time.** Ask, wait for the answer, then ask the next. Do not batch the four beats into one multi-part prompt — the writer's answer to beat ① often reshapes what you ask at beat ②.

2. **Never ask what mining already answered.** This is the cardinal rule. Mining (`mining-playbook.md`) has already surfaced the from→to of a changed number, the text of a cut sentence, the wording of a pre-committed discipline. Asking "what number changed?" when the manifest's fact-check loop history already shows it wastes the writer's attention and signals you didn't read the artifacts. **Lead with what the artifacts found**, then ask for the layer underneath. Pattern:
   > "You cut [X] between v1 and v6 — was that the move, or the deeper one underneath?"

   The artifact supplies the *what*; the interview extracts the *why it was tempting*, the *moment you saw it break*, the *felt experience* — the texture that left no trace in the files.

3. **Keep it to 3–5 questions total.** The move-type opener + the three remaining beats is already four; the title/closer confirmation can ride on the beat-④ answer or take one more turn. If you're past five questions, you're either re-asking mining or over-engineering — stop and draft.

4. **Push for the tangible at beat ②, but know when to fall back.** The breaking moment is the one beat that *must* be concrete. Dig once for the named source/number/sentence. If it isn't there, route to the empty-handed path — do not keep pushing for a pivot that doesn't exist.

5. **Confirm, don't impose, on title and closer.** Offer the title call and a proposed closer; let the writer steer both. The note is the writer's reasoning made visible; the skill's job is to elicit and lock it, not to author the verdict.

---

## Worked example — the four beats → four questions → a real note

This maps the bank onto the validation note, `workspace/paid/2026-06-10-thinking-behind-the-thinking-windfall-thread.md` (the near-miss exemplar; flagship: *Samsung's $400,000 Bonus, and the $4,000 One*). A fresh agent should be able to read the note, read this table, and see the **beats → questions → note** chain end to end.

The move arrived at GATE 2 as a **cut-sentence near-miss** (mining Source 2 + Source 3: the diff showed the "same money" line reworked out of §2, and the manifest Notes recorded "No 'same money' compression" as a pre-commitment). So the interview opened with **variant (b)**, then ran the default beats.

| Beat | Question asked | What the note shows (the answer, drafted) |
|---|---|---|
| **① Wrong read** | Opener **(b)**: "The diff shows you cut the 'same money' line — read it back as you first wrote it; what made it the most shareable line, and what made you not trust it?" | *"My first draft joined them with money. The closing line said, more or less, that the bonus and the bill come out of the same AI pot. It was the most shareable sentence in the draft."* |
| **② Breaking moment** | "What specific source, number, or sentence exposed it? When did you *see* it was wrong?" | *Writing "same money" in plain words and trying to follow the dollars.* The note: *"It was also wrong, and what showed me was writing it down in plain words. Once 'the same money' was on the page, I had to follow the dollars, and they don't meet."* Concretized with the two primary-source receipts: the bonus is [division profit to shareholders](analyst note); the bill is [PJM's $13.77B capacity-auction cost](market-monitor PDF). |
| **③ Corrected read** | "What replaced it, and why is the replacement truer rather than just safer?" | *Leverage — who can say no — not dollars.* The note: *"What the two halves actually share is the cause … the outcomes run opposite because the leverage runs opposite … the thread isn't dollars. It's the question each bottleneck asks, which is who here can say no."* Truer, not safer: "same money" *flattened* the one fact that makes the story worth telling. |
| **④ Lesson** | "State the discipline in one transferable line — the rule a reader could carry to the next piece." | *"When the parallel is real, compress it. When it isn't, name the asymmetry. The plain sentence is the test that tells you which."* |

**Title decision.** Asked: default or near-miss? This was a near-miss (the "same money" line died in drafting; nothing shipped wrong), but the writer kept the default `I Had the Wrong Thread` — allowed under DNA §4 ("either framing is acceptable when the writer caught it pre-publish"). The blank, "Thread," is the unit of the error.

**Closer decision.** A move-specific aphorism (DNA §8 family b), not the series signature — the move is a false-symmetry near-miss, and the signature correction line would have undersold the "plain sentence is the test" discipline. Confirmed, not imposed.

This is the acceptance target: handed this chosen move and move-type, a fresh agent running the openers above lands all four beats, the title call, and the closer that the human-written note actually carries.
