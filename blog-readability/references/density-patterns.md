# Density Patterns — Full Audit Reference

Detection rules, examples, and revision moves for each of the five readability audits in `blog-readability`. Load this when running the audit.

The five audits correspond directly to the five accessibility principles in the active profile's `voice.md` under paragraph rhythm and grounding cadence guidance. That file is the source of truth for *what the principles are*. This file is the catalog of *how to detect and fix violations* of them.

---

## Table of Contents

1. Audit 1 — Paragraph Length
2. Audit 2 — Ungrounded Abstraction
3. Audit 3 — Naked Statistics
4. Audit 4 — Flat Rhythm
5. Audit 5 — Sentence-Level Comprehension Drag
6. Cross-Audit Patterns and Order of Fixes
7. On Reader Calibration

---

## Audit 1 — Paragraph Length

**Threshold.** Flag any body paragraph over ~120 words. Flag any sequence of three or more paragraphs all within ~15 words of each other (length-flat rhythm).

**Why it matters.** Paragraph break is the most visible rhythm device in prose. Long unbroken paragraphs hide ideas; varied paragraphs cue the reader on what to slow down for and what to skim. A 150-word paragraph in dense analytical prose is a wall — the reader's eye finds nowhere to rest. Three same-length paragraphs in a row signal "the author is on autopilot" even when the writing is technically fine.

**Allowed exceptions.**
- Block quotations and their immediate surrounding context
- Multi-step examples where splitting would break the sequence
- A single piece of evidence whose force depends on uninterrupted presentation
- A deliberate "wall" paragraph that mirrors a thematic point (rare; verify it's intentional)

**Common failure modes.**
- The "everything I know about X" paragraph — author dumps all related context into one block instead of breaking at conceptual seams
- The "three reasons" paragraph — multiple distinct claims sharing a paragraph because they're "related"
- The pile-on paragraph — the author keeps adding qualifications and examples after the topic sentence has done its job
- The runaway transition — what was supposed to be a one-sentence bridge balloons into 120 words because the author kept clarifying

**Revision moves.**

1. **Find the conceptual seam.** Long paragraphs almost always contain a sentence that begins with "but," "and yet," "however," or names a new entity. That's the break point.
2. **Promote a qualification to its own paragraph.** If a paragraph ends with "though there are exceptions," the exceptions probably deserve a paragraph.
3. **Cut, don't split.** Sometimes the paragraph is long because it's saying too much, not because it needs more breaks. If three sentences in the paragraph could come out without losing the argument, cut them.
4. **Combine adjacent shorts.** If splitting a long paragraph produces two thin ones, the next short paragraph after it may absorb one cleanly.

**Positive example** (from "The Middle Class Dream"):
Paragraphs vary 38–95 words in the opening — none over 100. Short paragraphs (38–48 words) alternate with medium ones (58–95). The variation creates a staccato readability that survives high information density.

---

## Audit 2 — Ungrounded Abstraction

**Threshold.** Flag any paragraph where three or more consecutive sentences make abstract claims without touching ground (named entity, specific number, concrete scene, or one-word punch).

**Why it matters.** Abstract-on-abstract is the most common failure mode after thesis restatement. Readers can follow one ungrounded claim by trusting the writer; by the second they're skimming; by the third they're gone, even if every claim is correct. Grounding is the contract that lets the reader keep buying the abstraction.

**Detection signals.**
- Sentence starts with abstract noun: "This dynamic," "The mechanism," "Such patterns," "These forces"
- Sentence makes a systemic claim without name, number, or scene
- Sentence consists entirely of qualifications and conceptual moves
- Reader cannot answer "who/what/where/when" after reading the paragraph
- The paragraph could be cut without losing any concrete information

**Revision moves — the four grounding types.**

**1. Named entity.** Insert a specific person, company, agency, or place.
- Before: "Big tech consolidates around enterprise software."
- After: "Salesforce, Microsoft, and Adobe consolidate around enterprise software."

**2. Specific number.** Insert a date, percentage, count, dollar figure.
- Before: "Mobility has fallen sharply."
- After: "Mobility hit 11% in 2024, the lowest since 1948."

**3. Concrete scene.** Insert a place-able image the reader can hold.
- Before: "Workers face longer commutes from far-out housing."
- After: "Workers face two-hour drives from Stockton to the Bay Area job cluster."

**4. One-word punch.** Compress the abstraction into a single concrete noun.
- Pattern: "Most housing debates obsess over how many homes exist. The more revealing question is how often homes become available. Availability isn't just construction. **It's turnover.**"
- The punch is the strongest move when the surrounding sentences are long; it cleans the palate and gives the reader something specific to argue with.

**Common pitfall.** "Grounding" by adding adjectives ("a vibrant tech ecosystem," "a robust marketplace") is not grounding. Adjectives are abstraction in costume. Grounding requires nouns the reader could verify.

**When to use which grounding type.**
- Surrounding sentences are long and conceptual → use the one-word punch
- Argument is about *who* — actors, decisions, accountability → named entity
- Argument is about *scale* — magnitude, change over time → specific number
- Argument is about *experience* — what life under the system looks like → concrete scene

---

## Audit 3 — Naked Statistics

**Threshold.** Flag any numerical statistic that does not embed in a causal chain or human consequence.

**Why it matters.** Numbers are evidence, not headlines. A naked number ("Inflation hit 4.2%") gives the reader nothing to do with it. A number inside a mechanism ("For each percentage point inflation exceeds the Fed's target, housing starts decline by 12%") makes the number argumentative — it's now doing work the prose can build on. Decoration is the worst kind of density: heavy weight on the reader with no payload to justify it.

**Detection signals.**
- A sentence whose main payload is a number with no surrounding mechanism
- Two or more numbers in immediate sequence with no intervening explanation
- A "in 2024, X happened" sentence where X is a fact without a consequence
- A percentage or dollar figure where the reader can't immediately answer "so what"

**Revision moves.**

**1. Embed in mechanism.**
- Before: "Mortgage rates rose to 7%."
- After: "For each percentage point by which current mortgage rates exceed a homeowner's existing rate, the probability of sale falls by about 18.1%."

**2. Embed in behavior change.**
- Before: "Inflation hit 4.2%."
- After: "When inflation crossed 4%, household savings drew down twice as fast as the 2019 baseline."

**3. Embed in human consequence.**
- Before: "Median rent is now $1,800."
- After: "Median rent of $1,800 means a single-earner household at the median wage spends 38% of pre-tax income on rent before utilities."

**4. Cut, if neither answer is sharp.** If you can't say what mechanism produced the number or what behavior changes because of it, the number is decoration. Decoration goes.

**Allowed exceptions.**
- Direct quotations from sources that include numbers
- Footnoted citations where the number is meta-information about the source itself (e.g., "a 2023 study of 412 firms")
- A baseline number whose explicit purpose is to anchor a later comparison ("Median rent in 2014 was $X; by 2024 it was $Y" — the first number is anchoring the second's mechanism)
- Round-number historical context ("after 1980") where precision would mislead

---

## Audit 4 — Flat Rhythm

**Threshold.** Flag any section with three or more consecutive paragraphs matching on length, sentence count, or syntactic structure.

**Why it matters.** Sentence-level rhythm gets the rhythm of one paragraph; paragraph-level rhythm gets the rhythm of the whole section. Three same-shaped paragraphs in a row registers as homework even when the content is good. The reader's eye expects variation as a signal that the author is making choices rather than settling into a default.

**Detection signals.**
- Three or more paragraphs within ~15 words of each other in length
- Three or more paragraphs with the same number of sentences
- Three or more paragraphs all opening with the same construction ("This means...", "The result is...", "What this shows...")
- Three or more paragraphs all opening with abstract subjects rather than concrete ones
- A section where the writing has settled into a pattern instead of shaping a sequence

**Revision moves.**

1. **Cut to vary.** The fastest fix: cut one or two sentences from the longest paragraph in the run. The next paragraph now stands proportionally shorter.
2. **Combine or split.** Two short same-shape paragraphs can sometimes combine; one long one can split. Either move breaks the pattern.
3. **Vary the opening construction.** If three paragraphs in a row open "This means..." rewrite at least one to open with a noun or a question.
4. **Insert a one-line paragraph.** A single short sentence between two longer paragraphs is one of the most effective rhythm devices. Use sparingly — overuse becomes its own pattern.
5. **Lead with a concrete grounding move.** Replacing an abstract opening with a named entity or scene shifts the paragraph's *shape* as well as its content.

**Allowed exceptions.** Deliberate anaphora across paragraphs (rare). If the writer is intentionally stacking three paragraphs all starting "And then..." for rhetorical effect, the audit should mark this as borderline rather than flag it. Verify it's intentional — anaphora is the point only if cutting one of the three would weaken the prose.

---

## Audit 5 — Sentence-Level Comprehension Drag

**Threshold.** Flag sentences with three or more subordinate clauses, sentences over ~40 words that aren't doing clear structural work, sentences that bury the main verb deep behind qualifications.

**Why it matters.** Good long-form voice builds complexity in longer sentences and lands the point in a short one — but this only works if the longer sentences are doing complexity *well*. A 45-word sentence built from five stacked qualifications is not complex; it's diffuse. The reader's working memory has to hold each qualification until the main verb arrives, and by then the point is gone. A long sentence earns its length only when each clause does work the next clause depends on.

**Detection signals.**
- Multiple "which" or "that" clauses chained
- Main verb buried 30+ words into the sentence
- "Sentence diet" — the sentence could be split at any of several points with no loss of meaning
- A sentence where the reader has to re-read to figure out what the subject was
- Three or more commas before the main verb arrives

**Revision moves.**

1. **Split at the first natural clause boundary.** Usually after the first "which" or "and" or comma-before-conjunction. Two sentences are almost always more readable than one stuffed one.
2. **Move the main verb earlier.** If qualifications are stacked before the verb, move the verb up and demote the qualifications to a follow-up sentence.
3. **Demote parentheticals.** A long parenthetical is usually a separate idea trying to escape. Promote it to its own sentence.
4. **Cut redundant qualifications.** "Which, while not universally accepted, is generally seen as..." can usually become "Some dispute this; most..."

**Allowed exceptions.**
- The "list sentence" — a deliberate long sentence cataloguing a series of items. These work when the cataloguing is the point.
- The "build sentence" — a long sentence that's deliberately winding to build to a payoff. These work when the payoff lands; otherwise they don't.
- The "echo sentence" — a deliberately long sentence that mirrors the complexity of the thing being described. Rare; verify intent.

---

## Cross-Audit Patterns and Order of Fixes

Some passages fail multiple audits at once. The order of fixes matters:

1. **Cut first.** If the passage is failing two or three audits, the fastest path is often cutting. A paragraph that's too long, ungrounded, *and* contains a naked stat is probably a paragraph that's earning its keep marginally. Cut what doesn't serve, then re-audit.
2. **Then ground.** Once the cut version is in place, add the grounding that the remaining abstract claims need.
3. **Then rhythm.** Only after the substance is right should you tune paragraph length and rhythm.

The opposite order — tune rhythm first, then ground, then cut — produces tightly-rhythmic passages that still don't have a clear point. Substance precedes shape. Shape is what makes substance *land*; it cannot manufacture substance that wasn't there.

**Composite failure types.**
- **"Wall of think"**: long paragraph + ungrounded abstraction + flat rhythm with neighbors. Almost always benefits from aggressive cutting first.
- **"Stat dump"**: naked statistics + sentence drag (numbers piled into long sentences). Fix by extracting numbers into separate short sentences with mechanisms.
- **"Conceptual drone"**: ungrounded abstraction + sentence drag + flat rhythm. The hardest pattern to fix because the underlying issue is usually that the writer doesn't have a concrete claim — only an abstract feeling. Often needs a full section rewrite (re-run the drafting step on that section).

---

## On Reader Calibration

These audits are not absolute. A finance piece for finance readers can run denser than a general-audience explainer. The audit's severity is a function of *reader load relative to apparent audience*, not raw density.

When calibrating:

- **General audience** — lean strict. Most thresholds apply as written.
- **Domain readers** — allow more density but never excuse the basic failures (naked stats, ungrounded abstraction). Domain readers reward depth; they do not reward decoration any more than general readers do.
- **The blog's reader persona** (from `reader.md`) — use the persona's sophistication level and patience signals to calibrate how hard the reader will work for a payoff. A busy, sophisticated reader tolerates density that earns its keep and quits on density that doesn't. The bar is "did the writer make me work for a payoff that justified the work?"

When in doubt, lean toward stricter calibration. A piece that reads cleaner than its content needs to is a piece more people will finish. A piece that reads exactly as dense as its content needs to is the ideal, but hard to hit. A piece denser than its content needs to is the failure mode this audit exists to prevent.
