---
name: tcn-outline
description: >
  Step 1 of the Civic Node Substack article workflow: research, template selection, and bullet-point
  outline. ALWAYS invoke this skill when the user wants to start writing a Substack article for
  The Civic Node — including phrases like "write a substack post", "I want to write about X",
  "outline a piece about X", "help me write an article", "write a newsletter post", "long-form piece
  about X", "article for TCN", "piece for drinkYourOJ", or any request to produce a Civic Node
  article from scratch. Also trigger when the user pastes a synthesis page, editorial brief, or
  topic and says anything suggesting they want to turn it into an article. Does NOT apply to social
  media posts (that's tcn-post), fiction, or wiki operations.
---

# The Civic Node — Article Outline Generator (Step 1 of 3)

## What This Skill Does

Produces a researched, structured bullet-point outline for a Substack article — including template selection, viral trigger identification, and section-by-section content mapping. The outline is the foundation; the user approves it before headlines (tcn-headline) or drafting (tcn-draft) begin.

Load `references/article-templates.md` for full template detail.
Load `references/marcus-long-form.md` for the long-form reader persona.

---

## Voice & vocabulary canonical source

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule (§ 1), the banned-words list (§ 3A), dead phrases / transitions / engagement bait / hype language (§ 3B–§ 3E), the negative-parallelism rule (§ 3F), tribal-coded crypto cringe and operational shibboleths (§ 3G), the dismissal-label rule (§ 3H), the vocabulary cliff rules including the meaning-preservation sub-principle (§ 3I), the closing-line abstraction rule (§ 3J), the broader AI writing patterns to avoid (§ 4), and the anti-overfitting guide (§ 5).

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on a copy embedded in this spec. Any short examples cited here are illustrative only — the canonical file is authoritative.

Note: this is the outline step, so voice rules apply lightly here — there is no prose to audit. The canonical file matters at outline-time for the Opener Strategy (analogy choices that might trip a vocabulary cliff) and for the bullet content (sources cited, claims made — not the language used to describe them).

**Fallback when the canonical file is missing.** If `workspace/core/anti-ai-writing-style.md` is not present in the current project, this skill must:
1. Flag explicitly to the user — "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip any vocabulary-cliff anticipation in the Opener Strategy.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions downstream (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still produce the full outline including viral trigger identification, template selection (Triple Connection / System Audit / Concept Decoder / Pattern Report), section-by-section bullets with sources, opener and close strategy, personal reflection angle, and source gaps. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The canonical file's § 1 notes the always-gloss-on-first-use rule is conservative; a future enhancement would vary gloss aggressiveness by which adjacent cohort each piece targets (monetary-policy pieces gloss crypto terms more heavily; DePIN pieces gloss monetary terms; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, the template-selection step would consume an adjacency signal — pieces targeting a wider cohort lean toward Concept Decoders (more vocabulary work needed); pieces targeting a denser cohort can run System Audit or Pattern Report with less inline definition.

---

## The Long-Form End State

Everything in this skill builds backward from one target:

> **Marcus finishes the piece, saves it, and forwards it to one specific person he respects within 48 hours.**

The outline must set up an article that can achieve this. If the outline doesn't have the structural bones for signal, depth, and shareability, no amount of good prose in the draft will fix it.

---

## The Process

### 1. Orient — Find the Editorial Hook

Before choosing a template, identify what makes this topic worth writing about *right now*.

Ask:
- What's the spark? A news event, a pattern confirmed, a concept Marcus needs vocabulary for?
- Which of the five viral triggers does this map to?

| Trigger | What it does | Long-form application |
|---|---|---|
| **Precision Gift** | Articulates what Marcus was thinking but couldn't say | The piece gives him the framework or vocabulary he was missing |
| **Early Warning** | Names a structural shift before it's obvious | The piece connects signals he's seen separately into a pattern |
| **Named Hypocrisy** | Names something broken with surgical dryness | The piece audits a system or institution with evidence |
| **Devastating Compression** | Reduces a complex thing to one brutal insight | The piece builds to a single devastating reframe |
| **Unexpected Connection** | Two domains, revealed as the same problem | The piece bridges topics Marcus follows separately |

Pick one. Articles that try to hit multiple triggers lose focus.

### 2. Research Pass — Query the Wiki

If working in the Substack Research vault:
1. Read `wiki/index.md` to identify relevant pages
2. Pull source pages, entity pages, and concept pages related to the topic
3. Surface specific facts, data points, quotes, and contradictions that should anchor the argument
4. Note which sources have already been ingested vs. what gaps exist

If no wiki is available, identify what evidence the article needs and flag source gaps.

### 3. Choose the Template

Map the topic to one of the four templates based on what the material calls for:

| Template | Structure | Best when |
|---|---|---|
| **Triple Connection** | Current Event -> Historical Context -> Future Implications | A current event has a precedent nobody is citing |
| **System Audit** | Problem -> Analysis -> Solutions | Something is obviously broken and the cause is structural |
| **Concept Decoder** | Definition -> Mechanics -> Applications | Marcus needs vocabulary for something he's circling |
| **Pattern Report** | Multiple signals -> Thesis | Several separate developments reveal one structural shift |

See `references/article-templates.md` for section word counts and tone notes.

### 4. Build the Outline

Produce a bullet-point outline following Justin's actual process: **inductive, not deductive.** Lay out the facts first. Let the thesis emerge from the evidence, don't impose it.

The outline must include:

**Topic & Trigger**
- One-line description of the topic
- Which viral trigger this targets
- Why this is worth writing *now* (the timeliness hook)

**Template Selection**
- Which template and why

**Section-by-Section Bullets**
For each section in the chosen template:
- 4-6 bullet points of specific content: facts, data, quotes, examples, arguments
- Word count target for this section
- Tone note (analytical, sardonic, personal, building, etc.)
- Key sources to cite (with wiki links if available)

**Opener Strategy**
- Proposed analogy that narrows from broad to specific
- How the thesis lands by paragraph 2

**Close Strategy**
- How the close calls back to the opener
- What the reader is left pondering — not a conclusion they already drew

**Personal Reflection Angle**
- What personal experience connects to this topic
- How the anecdote serves the argument (illustration, not destination)

**Source Gaps**
- What the article needs that the wiki doesn't have yet
- Whether the article can be written now or needs additional source ingestion

### 5. Stop and Present

Present the outline clearly. **Do not proceed to headlines or drafting.** The user approves, redirects, or adds before the next step.

---

## What a Good Outline Looks Like

A good outline makes the article feel almost inevitable — the structure is visible, the evidence is laid out, and the only remaining work is prose. A reader who saw only the outline would understand the argument.

A bad outline is vague bullets that could apply to any article ("discuss the implications," "provide historical context"). Every bullet should be specific enough that someone else could write the section from it.

---

## Output Format

```
## Article Outline: [Working Title]

**Trigger:** [which of the 5]
**Template:** [which of the 4]
**Timeliness:** [why now — one sentence]
**Target length:** [word count]

---

### Section 1: [Template section name] (~[X] words)
*Tone: [analytical / sardonic / personal / building]*

- [specific bullet]
- [specific bullet]
- [specific bullet]
- [specific bullet]
- Sources: [[wiki page]], [[wiki page]]

### Section 2: [Template section name] (~[X] words)
*Tone: [tone note]*

- [specific bullet]
- ...

[repeat for all sections]

---

### Opener Strategy
- Analogy: [proposed broad-to-specific analogy]
- Thesis lands by: [how/where]

### Close Strategy
- Callback: [how the opener returns]
- Reader leaves with: [the pondering question or reframe]

### Personal Reflection
- Angle: [what connects personally]
- Serves the argument by: [how]

### Source Gaps
- [what's missing, if anything]
- Status: [ready to draft / needs source ingestion first]
```

---

## Reference Files

- `references/article-templates.md` — Full template detail: section structures, word counts, tone notes, trigger pairings
- `references/marcus-long-form.md` — Marcus persona for long-form: what keeps him reading, what makes him save/forward, what causes him to unsubscribe
