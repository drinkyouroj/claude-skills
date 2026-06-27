---
name: blog-outline
description: >
  Research, angle/hook + structure selection, and bullet-point outline step of the blog-article-builder pipeline.
  outline. ALWAYS invoke this skill when the user wants to start writing a blog article — including
  phrases like "write a blog post", "I want to write about X", "outline a piece about X",
  "help me write an article", "write a newsletter post", "long-form piece about X", or any request
  to produce a blog article from scratch. Also trigger when the user pastes a source document,
  editorial brief, or topic and says anything suggesting they want to turn it into an article.
  Does NOT apply to social media posts, fiction, or knowledge-base operations.
---

# Blog Article Outline Generator (Outline step of the blog-article-builder pipeline)

## What This Skill Does

Produces a researched, structured bullet-point outline for a blog article — including angle/hook + structure selection and section-by-section content mapping. The outline is the foundation; the user approves it before headlines (blog-headline) or drafting (blog-draft) begin.

Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else.
Loads: `identity.md`, `reader.md`, `templates.md`, and the active preset.

---

## Voice & vocabulary canonical source

This skill MUST load the active profile's `voice.md` before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule, the banned-words list, dead phrases / transitions / engagement bait / hype language, the negative-parallelism rule, tribal-coded jargon and operational shibboleths, the dismissal-label rule, the vocabulary cliff rules including the meaning-preservation sub-principle, the closing-line abstraction rule, the broader AI writing patterns to avoid, and the anti-overfitting guide.

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the active profile's `voice.md` at runtime, not by relying on a copy embedded in this spec. Any short examples cited here are illustrative only — the `voice.md` file is authoritative.

Note: this is the outline step, so voice rules apply lightly here — there is no prose to audit. The `voice.md` file matters at outline-time for the Opener Strategy (analogy choices that might trip a vocabulary cliff) and for the bullet content (sources cited, claims made — not the language used to describe them).

**Fallback when the voice file is missing.** If the active profile's `voice.md` is not present, this skill must:
1. Flag explicitly to the user — "no voice file found; skipping voice calibration."
2. Skip any vocabulary-cliff anticipation in the Opener Strategy.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions downstream.
4. Continue with non-voice work this skill can still do: still produce the full outline including angle/hook identification, structure selection, section-by-section bullets with sources, opener and close strategy, personal reflection angle, and source gaps. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** A future enhancement would vary gloss aggressiveness by which adjacent audience cohort each piece targets (domain-specialist pieces gloss general-audience terms more heavily; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, the structure-selection step would consume an adjacency signal — pieces targeting a wider cohort lean toward explanatory / concept-explainer structures (more vocabulary work needed); pieces targeting a denser cohort can run analytical or multi-signal structures with less inline definition.

---

## The Long-Form End State

Everything in this skill builds backward from one target:

> **The reader finishes the piece, saves it, and forwards it to one specific person they respect within 48 hours.**

The outline must set up an article that can achieve this. If the outline doesn't have the structural bones for signal, depth, and shareability, no amount of good prose in the draft will fix it.

---

## The Process

### 1. Orient — Find the Editorial Hook

Before choosing a structure, identify what makes this topic worth writing about *right now*.

Ask:
- What's the catalyst? A development in the blog's domain (`quick.domain`), a pattern confirmed, a concept the reader needs vocabulary for?
- Which of the five angles does this map to?

| Angle | What it does | Long-form application |
|---|---|---|
| **Precision Gift** | Articulates what the reader was thinking but couldn't say | The piece gives them the framework or vocabulary they were missing |
| **Early Warning** | Names a structural shift before it's obvious | The piece connects signals seen separately into a pattern |
| **Named Hypocrisy** | Names something broken with surgical dryness | The piece audits a system or institution with evidence |
| **Devastating Compression** | Reduces a complex thing to one brutal insight | The piece builds to a single devastating reframe |
| **Unexpected Connection** | Two domains, revealed as the same problem | The piece bridges topics the reader follows separately |

Pick one. Articles that try to hit multiple angles lose focus.

### 2. Research Pass — Query Available Sources

If a seed source is specified in the active profile (`profile.yaml.paths.source`):
1. Read any available index or table of contents to identify relevant pages
2. Pull source pages, entity pages, and concept pages related to the topic
3. Surface specific facts, data points, quotes, and contradictions that should anchor the argument
4. Note which sources have already been ingested vs. what gaps exist

If no source is available, identify what evidence the article needs and flag source gaps.

### 3. Choose the Structure

Load `templates.md` from the active profile and map the topic to the most appropriate content structure based on what the material calls for. The active `templates.md` lists the available structures, their sections, and the conditions under which each works best.

Default four-structure reference (the active `templates.md` may add, rename, or replace these):

| Structure | Logic | Best when |
|---|---|---|
| **Context & Implications** | Current Event → Historical Context → Future Implications | A current event has a precedent nobody is citing |
| **Problem-Analysis-Solution** | Problem → Analysis → Solutions | Something is obviously broken and the cause is structural |
| **Concept Explainer** | Definition → Mechanics → Applications | The reader needs vocabulary for something they're circling |
| **Multi-Signal Synthesis** | Multiple signals → Thesis | Several separate developments reveal one structural shift |

See the active profile's `templates.md` for section word counts, tone notes, and angle pairings.

### 4. Build the Outline

Produce a bullet-point outline following an inductive process: **inductive, not deductive.** Lay out the facts first. Let the thesis emerge from the evidence, don't impose it.

The outline must include:

**Topic & Angle**
- One-line description of the topic
- Which angle this targets
- Why this is worth writing *now* (the timeliness hook)

**Structure Selection**
- Which structure and why

**Section-by-Section Bullets**
For each section in the chosen structure:
- 4-6 bullet points of specific content: facts, data, quotes, examples, arguments
- Word count target for this section
- Tone note (analytical, sardonic, personal, building, etc.)
- Key sources to cite (with links if available)

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
- What the article needs that isn't available yet
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

**Angle:** [which of the 5]
**Structure:** [which structure from templates.md]
**Timeliness:** [why now — one sentence]
**Target length:** [word count]

---

### Section 1: [Structure section name] (~[X] words)
*Tone: [analytical / sardonic / personal / building]*

- [specific bullet]
- [specific bullet]
- [specific bullet]
- [specific bullet]
- Sources: [source], [source]

### Section 2: [Structure section name] (~[X] words)
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

## Reference Files (profile-driven)

- Active profile's `templates.md` — Full structure detail: section layouts, word counts, tone notes, angle pairings
- Active profile's `reader.md` — Reader persona: what keeps them reading, what makes them save/forward, what causes them to unsubscribe
