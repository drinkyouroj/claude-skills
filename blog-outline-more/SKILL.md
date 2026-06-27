---
name: blog-outline-more
description: >
  Step 1b of the blog article workflow: expands a blog-outline bullet-point outline
  into a paragraph-level detailed outline with all facts laid out, argument flow mapped, and
  optional rhetorical device suggestions. ALWAYS invoke this skill when the user has an approved
  outline and wants to flesh it out before writing — including phrases like "flesh out the outline",
  "make the outline more detailed", "add more detail to the outline", "I want to write from this
  outline", "expand the outline", "detailed outline", "outline-more", or when the user has a
  blog-outline output and wants to go deeper before drafting themselves. Does NOT produce prose.
  Does NOT replace blog-draft. The user still writes every sentence.
---

# Blog Detailed Outline Generator (Step 1b)

## What This Skill Does

Takes a `blog-outline` output and expands it into a paragraph-level detailed outline — all facts
laid out in sequence, argument flow mapped move by move, and clearly-marked optional suggestions
for where analogies/metaphors/similes could land and what shape they might take.

The user still writes every word. This skill pre-loads all the raw material so they can write
in one uninterrupted pass.

Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else.
Loads: `reader.md`, `templates.md`, `voice.md`, and the active preset.

---

## Voice & vocabulary canonical source

This skill MUST load the active profile's `voice.md` before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule (§ 1), the banned-words list (§ 3A), dead phrases / transitions / engagement bait / hype language (§ 3B–§ 3E), the negative-parallelism rule (§ 3F), tribal-coded jargon and operational shibboleths (§ 3G), the dismissal-label rule (§ 3H), the vocabulary cliff rules including the meaning-preservation sub-principle (§ 3I), the closing-line abstraction rule (§ 3J), the broader AI writing patterns to avoid (§ 4), and the anti-overfitting guide (§ 5).

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the active profile's `voice.md` at runtime, not by relying on a copy embedded in this spec. Any short examples cited here are illustrative only — the `voice.md` file is authoritative.

Note: this is the detailed-outline step. There is still no prose, but the Grounding plan and Statistic framing fields (per paragraph block) anticipate how jargon will land in the draft — that's where vocabulary cliff considerations enter at this stage.

**Fallback when the voice file is missing.** If the active profile's `voice.md` is not present, this skill must:
1. Flag explicitly to the user — "no voice file found; skipping voice calibration."
2. Skip the vocabulary-cliff anticipation in Grounding plan and Statistic framing fields (leave them populated with what the user provides, but do not propose substitutions).
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions downstream (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still produce the detailed paragraph-level content blocks, rhetorical suggestions, humor location flags, opener and close approach maps, accessibility pre-check, reader-persona pre-assessment, and source gaps. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The active profile's `voice.md` may note an always-gloss-on-first-use rule; a future enhancement would vary gloss aggressiveness by which adjacent audience cohort each piece targets (domain-specialist pieces gloss general-audience terms more heavily; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, the per-paragraph Grounding plan field would consume an adjacency signal to flag which abstractions need extra grounding for the targeted cohort.

---

## Workflow Position

This is Step 1b — the last step before prose. What comes next:

- **`blog-draft`** (Step 3) writes the article from this outline, baking accessibility principles in at generation time (paragraph rhythm, grounding cadence, statistic framing, deliberate reader address — see its "Drafting for Accessibility" section).
- **`blog-readability`** runs after the draft as a structural audit for density and accessibility, against the same five principles.

The detailed outline is where those principles get *planned*, not just hoped for. Every paragraph block should already know where its abstraction touches ground and how its numbers embed in mechanism — see the Grounding plan and Statistic framing fields in the paragraph content block below. The cleaner the outline on these dimensions, the less work the downstream skills have to do, and the more likely the prose lands readably on the first pass.

---

## The Core Contract

> **The detailed outline must make the prose feel inevitable — but not write it.**

Every fact is surfaced. Every argument move is named. Every rhetorical opportunity is flagged with
a description, not a draft. The user reads the detailed outline and thinks: "I know exactly what
I'm writing. I just need to write it."

If the detailed outline contains prose, it has failed.
If the user would need to stop mid-section to look something up, it has failed.
If the user doesn't know where the jokes land, it has failed.

---

## Before You Begin

Review the incoming `blog-outline` and confirm:

1. **Structure selection** — which of the structures was chosen (from the active profile's `templates.md`), and why
2. **Angle/hook** — which of the five angles the outline targets
3. **Section structure** — how many sections, their names, word count targets
4. **Source availability** — which facts already have sources vs. need flagging
5. **Opener and close strategy** — what analogy was proposed and how the close calls back

If the incoming outline has gaps (missing sources, vague bullets, unclear argument moves), resolve
them in the detailed outline. Don't inherit the gaps.

---

## The Expansion Process

For each section in the outline, expand to a paragraph-level content map.

### Section Header Block

For each section, open with:

```
### [Section Name]: [Proposed Subheadline]
Word target: ~[X] words | Tone: [analytical / sardonic / personal / building]
Argument job: [one sentence — what does this section add that the previous section didn't establish?]
```

**Section header format — strict rules.** The proposed subheadline is not final, but it must be cast in the canonical format the draft will inherit:

- **Title case on the left of the colon** (the template section name): match the active profile's `templates.md` section names verbatim — do not invent new section names.
- **Sentence case on the right of the colon** (the actual headline that previews the section's argument): only the first word capitalized, plus any proper nouns. *Not* title case.
- **No trailing punctuation** when the right-of-colon is a single sentence or fragment.
- **Internal punctuation only when multiple sentences are needed.** When the subheadline runs as two short sentences (or a sentence followed by a punctuated fragment), use sentence-ending punctuation on each.
- **Under 12 words on the right of the colon.** Specific. Slightly provocative. Someone scanning only the headers should get the argument's shape.

**How many section headers to produce.** Match the template structure from the active profile's `templates.md`. For list/multi-signal structures, generate a header per item (plus opener and close headers) rather than a fixed count. Each item header still follows the casing/punctuation rules above.

---

### Paragraph-Level Expansion

For each paragraph within the section, produce a **content block** in this format:

```
**¶[N] — [Paragraph job: one-line description of what this paragraph does]**

Facts to deploy (in order):
- [Specific fact, data point, or quote — exact numbers, names, dates]
  Source: [URL or source description]
- [Next fact]
  Source: [...]

Argument move: [How this paragraph advances from the previous — "introduces," "complicates,"
"proves by example," "pivots to implication," "lands the thesis," etc.]

Grounding plan: [Where in this paragraph does the abstraction touch ground? Name the move — named entity, specific number, concrete scene, or one-word punch. If the paragraph is already concrete throughout, write "concrete throughout — no extra grounding needed." This field exists so `blog-readability` finds the grounding already in place rather than flagging the paragraph as ungrounded. See the active profile's `voice.md` for "Paragraph Rhythm and Grounding Cadence."]

Statistic framing: [If this paragraph contains numbers, name the mechanism, behavior change, or human consequence each number embeds in. "Mortgage rates rose to 7%" is naked; "For each percentage point mortgage rates exceed an existing rate, probability of sale falls by 18.1%" is framed. If no numbers, omit this field.]

Key sentence to land: [Not the prose — describe what the most important sentence in this
paragraph must achieve. E.g., "The sentence that collapses the official explanation."]
```

**Paragraph count guidance by section type:**
- Spark / Glitch / Definition sections (400 words): 3-4 paragraphs
- Pattern / Source Code / Mechanics sections (500-600 words): 4-6 paragraphs
- Protocol / Upgrade / Applications sections (400 words): 3-4 paragraphs
- Personal reflection sections (200-300 words): 2-3 paragraphs
- Multi-signal / list-structure items (200-300 words each): 2-3 paragraphs

---

### Rhetorical Device Suggestions

At any point in a content block where an analogy, metaphor, simile, or structural move could
strengthen the argument, add a clearly-marked optional suggestion:

```
💡 [RHETORICAL SUGGESTION — USE OR SKIP]
Type: [Analogy / Metaphor / Simile / Comparison / Historical parallel / Structural move]
Location: [Before ¶N / Opening of ¶N / Closing of ¶N / Transition between ¶N and ¶N+1]
Suggestion: [Describe the device — what two things it connects, what the bridging property is,
roughly what the shape of the move is. Do NOT write the prose. Give enough description that
the author can decide whether it works and, if so, write it themselves.]
Example shape: "[rough natural-language description of the arc — one sentence, not polished prose]"
Why it might work: [one sentence on what it would achieve for the reader — hook, credibility,
compression, humor, emotional access point before technical material, etc.]
Why it might not: [one sentence on the risk — too cute, too insider, too far from the argument]
```

These are offers, not instructions. Flag 2-4 per section maximum. More than that becomes noise.

Rhetorical suggestions are most valuable at:
- The opener (the broad-to-specific narrowing analogy)
- The transition into the densest analytical section
- The moment before the thesis lands
- The close callback to the opener
- Any humor/pressure-valve location

---

### Humor Location Flags

Where the voice rules call for a pressure valve — usually in personal reflection sections or at
the end of a dense analytical block — flag the location:

```
😬 [HUMOR LOCATION]
Situation: [What's being described — what's the heavy thing that needs releasing?]
Register: [sardonic / deadpan / self-deprecating / pointed]
Rough target: [Describe the thing the joke should land on — not the joke, the target]
Model sentence rhythm: [Reference a sentence rhythm from the active profile's `voice.md` that suits this moment]
```

---

## The Opener Section

Expand the opener strategy from the bullet outline into a full approach map:

```
### OPENER APPROACH MAP

Analogy to use: [Describe the proposed analogy fully — what is the broad thing, what is the
specific thing, what is the bridging property, how it narrows to the article's subject]

Paragraph structure:
¶1 — [What the opening image establishes and why it hooks]
¶2 — [How thesis lands — what specific sentence must exist by end of ¶2]

Reader 30-second test: [Would the reader pass this opener into the full piece? What's the hook that
earns the next 30 seconds?]

What to avoid: [Specific failure modes for this particular opener — not general rules, but
specific risks given this topic and analogy]
```

---

## The Close Section

Expand the close strategy into a full approach map:

```
### CLOSE APPROACH MAP

Callback: [How the opener analogy returns — what has changed in how we see it after the piece]
New element: [What the close adds that the body didn't already establish — the reframe, the
implication, the question worth investigating]

Cover Test: [If you cover the last paragraph and read the piece, do you already have this
ending? If yes, it's weak. What would make it stronger?]

Final sentence goal: [Describe what the last sentence must achieve — not what it says, what
it does to the reader]
```

---

## Accessibility Pre-Check

Before handing the detailed outline off to `blog-draft`, verify it has set the prose up to succeed on the five accessibility principles (audited later by `blog-readability`):

```
### ACCESSIBILITY PRE-CHECK

1. Grounding coverage — Every paragraph block names where the abstraction touches ground, or marks itself as "concrete throughout."
   [assessment — name any paragraph block still missing this]

2. Statistic framing — Every number in "Facts to deploy" has its mechanism, behavior change, or human consequence noted, not just the raw fact.
   [assessment — name any naked numbers in the outline]

3. Paragraph length intention — The paragraph count per section is appropriate to the word target (e.g., 3-4 paragraphs for 400 words ≈ 100 words each, the ceiling). If every paragraph hits the ceiling, the section will run length-flat unless the writer deliberately varies in the draft.
   [assessment — flag sections at risk of length-flat rhythm]

4. Reader address moments — If second-person "you" should make a structural claim feel human-scale, the location is named in the outline (typically the analytical section's payoff paragraph).
   [assessment — present, absent, or N/A for this piece]

5. Anaphora opportunities — If 3-4 consecutive sentences could run parallel construction for rhythmic effect, the location is flagged in the rhetorical suggestions above.
   [assessment — present, absent, or not applicable]

Verdict: [ready for blog-draft / needs accessibility planning fix before drafting]
```

The point of this check is not to write the prose; it is to make sure the *raw material* is set up so that when `blog-draft` runs, it has what it needs to draft accessibly on the first pass. Fixing accessibility at outline time is cheaper than fixing it at audit time.

---

## The Reader-Persona Pre-Assessment

Load `reader.md` from the active profile and run the five reader-persona tests against the detailed outline before presenting:

```
### READER-PERSONA PRE-ASSESSMENT

1. Signal test — Does this deliver at least one thing the reader couldn't have found easily themselves?
   [assessment — be specific about what the one thing is]

2. Patience test — Would the reader still be reading at paragraph 3?
   [assessment — name the paragraph most likely to lose them and why]

3. Depth test — Does this feel like the writer operates in the thing they're writing about?
   [assessment — what's the strongest credibility signal in the outline?]

4. Save test — Would the reader save this or forward it?
   [assessment — save or forward, and what specifically triggers it]

5. Accumulation test — Does this raise or maintain the signal floor?
   [assessment]

Verdict: [ready to write / needs X before writing]
```

---

## Source Gaps

List any claims in the detailed outline that lack a verified source:

```
### SOURCE GAPS

- [Claim that needs sourcing] — [what kind of source is needed]
- [...]

Status: [ready to write / needs source ingestion first]
```

---

## Output Format

The full detailed outline is a self-contained document structured as:

```
## Detailed Outline: [Working Title]

**Angle:** [which of the 5]
**Structure:** [which structure from templates.md]
**Timeliness:** [why now — one sentence]
**Target length:** [word count]

---

[OPENER APPROACH MAP]

---

[For each section:]
### [Section Name]: [Proposed Subheadline]
Word target: ~[X] words | Tone: [...]
Argument job: [...]

[Content blocks ¶1 through ¶N]
[Rhetorical suggestions where applicable]
[Humor location flags where applicable]

---

[CLOSE APPROACH MAP]

---

[ACCESSIBILITY PRE-CHECK]

---

[READER-PERSONA PRE-ASSESSMENT]

---

[SOURCE GAPS]
```

---

## What This Is Not

**Not a draft.** No prose. If a sentence sounds finished, it's a failure mode — restate it as a
content requirement.

**Not a replacement for the author's voice.** Rhetorical suggestions describe a move, not a voice.
The analogy described will be written by the author in their own register. The suggestion is
structural permission, not a script.

**Not optional for sources.** Every factual claim needs a source reference. Vague bullets like
"discuss Q1 results" are not detailed enough — it's "Company X posted Q1 2026 operating profit of
$X billion — [source]."

---

## Reference Files (profile-driven)

- Active profile's `templates.md` — Full structure detail: section layouts, word counts, tone notes, angle pairings
- Active profile's `reader.md` — Reader persona for long-form: what keeps them reading, what makes them save/forward
- Active profile's `voice.md` — Voice and style reference: sentence rhythm, paragraph rhythm and grounding cadence (shared source of truth for accessibility), rhetorical principles, humor, the AI hit list

## Companion Skills

- **`blog-outline`** (Step 1) — Bullet-point outline that feeds into this skill.
- **`blog-headline`** (Step 2) — Headline and subheadline generation from the outline.
- **`blog-draft`** (Step 3) — Writes the prose from this detailed outline. See its "Drafting for Accessibility" section, which this outline's Grounding plan and Statistic framing fields are designed to set up.
- **`blog-readability`** — Post-draft structural audit. The Accessibility Pre-Check above directly determines how light a touch `blog-readability` will need on the back end.
- **`blog-humanizer`** — Post-draft lexical pass for AI tells, calibrated to the active profile's voice (rewrites in place). Independent of accessibility.
- **`blog-opener`** — Standalone opener fix-pass if needed after drafting.
- **`blog-fact-check`** / **`blog-fact-reconcile`** — Source verification on the finished draft.
