---
name: tcn-opener
description: >
  Drafts or evaluates the opening paragraph(s) of a Civic Node article. Invoke when the user
  wants to punch up a weak opener, draft an opener before or separately from the full article,
  or when a voice assessment flags the opener as the weak point — including phrases like
  "fix the opener", "punch up the beginning", "the opener is weak", "draft an opener for this",
  "help with the hook", "the opening doesn't land", or "let's work on the intro". Does NOT apply
  to social media posts (that's tcn-post), full article drafts (tcn-draft), or wiki operations.
---

# The Civic Node — Opener Skill

## What This Skill Does

Drafts or evaluates the opening paragraph(s) of a TCN article. Operates in two modes:

- **Generate** — produce 2 opener variants for a piece with an approved outline
- **Evaluate** — assess an existing opener, diagnose its failure mode, suggest specific fixes

The opener is the most leveraged paragraph in the piece. A weak opener sends Marcus away before the argument starts. A strong one creates a reader who will follow wherever the piece goes.

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

**Fallback when the canonical file is missing.** If `workspace/core/anti-ai-writing-style.md` is not present in the current project, this skill must:
1. Flag explicitly to the user — "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip all voice-related work — no vocabulary substitution, no AI-tells check on the opener.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still produce opener variants from the technique menu (lighthouse, expectation-subversion, mid-action drop, counterintuitive fact, uncomfortable truth, tight paradox question), still document the opener-close contract, still run the seven-check evaluation for structural items (engage from word one, broad enough, narrow speed, thesis by paragraph 2, contract creation, patience test); flag "voice rules pass" as not enforced in the output. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The canonical file's § 1 notes the always-gloss-on-first-use rule is conservative; a future enhancement would vary gloss aggressiveness by which adjacent cohort each piece targets (monetary-policy pieces gloss crypto terms more heavily; DePIN pieces gloss monetary terms; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, the technique-selection step (specifically which broad hook to reach for) would consume an adjacency signal — pieces targeting a wider cohort lean toward the lighthouse with a more universal broad-end; pieces targeting a denser cohort can carry more domain-specific opening images.

---

## The Lighthouse Model

Justin opens with an **analogy that narrows from broad to specific**. The lighthouse attracts ships that weren't looking for it.

The opener's job is to attract readers who don't yet know they care about the specific topic. It does this in two phases:

**Phase 1 — The broad hook.** Something the reader already has a relationship with. A counterintuitive fact. A familiar paradox. A scene they can place themselves in. The broad hook operates at a level above the specific topic — not "DRAM prices" but "what happens when a market loses the ability to self-correct."

**Phase 2 — The narrow.** The broad hook reveals why it matters *here*, for *this* argument. The narrowing must feel inevitable, not forced. If the reader can see the pivot coming from sentence one, the broad hook wasn't broad enough.

**Thesis lands by paragraph 2.** The opener earns the reader's attention; paragraph 2 tells them what they're here for. The reader should know the argument before the third paragraph begins.

---

## The Technique Menu

Six opener approaches that work in Justin's voice. The lighthouse is the default — the others are variations or alternatives when the piece calls for something different.

### 1. The Analogy That Narrows (the lighthouse)
**What it is:** Open with something broadly accessible; narrow to the specific thesis.
**Best for:** Concept Decoders, Unexpected Connections, pieces where the reader might not know they care about the topic yet.
**How to use it:** Find the *human-scale* version of the argument — the pattern underneath the specific case — and open there. Then narrow: "That's what's happening with [specific topic] right now."
**Requires:** Identifying what the broad version of this story is. If you can't name it in one sentence, the analogy isn't ready.

### 2. The Expectation-Subversion
**What it is:** State what should be true according to every model or assumption. Then show it isn't.
**Best for:** Pattern Reports, paradox-driven pieces, Early Warning triggers.
**Structure:** `[What the model predicts.] [What actually happened.] [This piece explains why.]`
**TCN example:** "By every standard model of supply and demand, DDR5 should be trending toward $200 by now. It's at $400."
**Note:** Don't use this if the whole piece is the expectation-subversion — it works as a hook, not as a structure substitute.

### 3. The Mid-Action Drop
**What it is:** Drop the reader into something already happening — no setup, no context. The reader is inside the moment before they understand the stakes.
**Best for:** Origin Stories, Triple Connections opening on a specific event, news-peg pieces.
**How to use it:** Find the scene with the highest narrative compression. Not "In early 2025, negotiations began..." but "On January 14, a purchasing executive boarded a flight to Seoul carrying a non-binding letter and an open question."
**Why it works:** Immediate, specific, no throat-clearing. Obligations of setup reversed — the reader follows because they're already inside.

### 4. The Counterintuitive Fact
**What it is:** Lead with a statistic or finding that contradicts what the reader would expect. Let the fact speak; don't editorialize.
**Best for:** Early Warning, Named Hypocrisy, data-heavy pieces.
**How to use it:** Find the number or fact in your research that surprised you most. Lead with that, dry, no commentary. The reader's own cognitive dissonance does the work.
**Rule:** The fact must be the actual surprising thing, not a setup fact. If the reader's first reaction isn't "wait, really?" — find a different fact.

### 5. The Uncomfortable Truth Stated Plainly
**What it is:** Say the thing that everyone is dancing around, without hedging.
**Best for:** System Audits, Named Hypocrisy, pieces where the mainstream framing is wrong.
**How to use it:** Identify the thing the piece proves that nobody says out loud. Open with that, stated flatly. No qualifications, no softening.
**TCN example:** "Three companies control 90% of the world's DRAM production. Two of them are on the same peninsula. One shipping lane carries their primary process gas. This was always going to happen."
**Voice check:** Must be backed by the piece's evidence. An uncomfortable truth that turns out to be wrong collapses the credibility of everything that follows.

### 6. The Tight Paradox Question
**What it is:** A single, minimal question that sets up a logical impossibility or counterintuitive situation.
**Best for:** Pieces where the central tension is a genuine paradox.
**Rule:** One question only. Multiple questions stacked at the opener is a content farm pattern.
**The question must be answerable** by the piece — it creates a promise that must be paid.
**TCN example:** "Why would a war in the Middle East affect your RAM?"
**Anti-pattern:** "Have you ever wondered..." — banned. The question should be specific, not an invitation.

---

## Anti-Techniques: What Doesn't Work

These are opener-form failure modes, kept in this skill because each one has a reason it specifically fails *as an opener* (not just as prose). For the broader banned-phrase catalog (any context, not just openers), see `workspace/core/anti-ai-writing-style.md` § 3A–§ 3E and § 4. Phrases listed here that also appear in the canonical file are not contradicting it — they're flagged here for their opener-specific failure mode; the canonical file is authoritative on the phrase ban itself.

| Don't | Why |
|---|---|
| "In today's rapidly changing..." | Throat-clearing. Instant death. |
| "Have you ever wondered..." | Banned AI phrase. Cliché content-farm hook. |
| "Picture this:" / "Imagine you're..." | Banned. Too cheesy; signals generic content. |
| "I've been thinking about..." | Explicitly banned from voice rules. |
| Famous quotes as openers | Performative. Feels borrowed, not owned. |
| Multiple questions stacked | Content farm pattern. One question only, if any. |
| "Today I'll show you how to..." | Wrong register for analysis. |
| State-of-the-world preamble | Throat-clearing in a trench coat. Cut it. |
| Personal anecdote about the writer's day | Belongs in Personal Reflection, not the opener. Too slow to narrow. |
| "It's important to note..." | Banned AI phrase. |

---

## Template-Specific Guidance

Each template calls for a different opener approach:

**Pattern Report** (multiple signals → thesis)
The opener must name the convergence before the body explains each signal. Don't tease — tell. The power is that the reader knows all five forces exist before encountering any one of them; the body then delivers on each.
→ Best technique: Expectation-Subversion, then name the forces.

**System Audit** (problem → analysis → solutions)
Open by identifying the broken thing plainly. Don't build to the diagnosis — state it. The analysis earns its credibility by proving what the opener asserted.
→ Best technique: Uncomfortable Truth, Counterintuitive Fact.

**Triple Connection** (current event → historical context → future implications)
Open on the current event with maximum specificity. Dates, names, the exact thing that happened. The historical context comes in the body — the opener is the news peg.
→ Best technique: Mid-Action Drop, Counterintuitive Fact.

**Concept Decoder** (definition → mechanics → applications)
The reader doesn't yet know they need this vocabulary. The opener's broad hook must attract them before they understand why. The analogy is critical here.
→ Best technique: Analogy That Narrows (lighthouse — default).

---

## The Opener-Close Contract

Every opener creates a debt the close must pay. The image, phrase, or tension introduced in the opener needs to return in the close — transformed by what the argument established between them.

When generating an opener, always document:

> **Contract:** [The specific image / fact / tension / question the opener introduces that the close must return to]

If the close can't call back to the opener, the opener is wrong — not the close.

This is also a diagnostic tool when evaluating an existing opener: ask whether the close has something to call back to. If the opener is throat-clearing, the close has nothing to hold.

---

## The Process

### Generate Mode

1. **Read the outline** — specifically the Opener Strategy section and the template/trigger.
2. **Identify the template** → use the template-specific guidance above to narrow the technique options.
3. **Find the broad entry point** — what is the human-scale version of this argument? What does the reader already have a relationship with that this piece connects to?
4. **Draft 2 variants** using different techniques from the menu. Label each by technique name.
5. **Document the opener-close contract** for each variant.
6. **Run the evaluation checklist** against both before presenting.
7. **Present both** — let the user choose or direct toward a hybrid.

### Evaluate Mode

Run the opener through these seven checks. For any check that fails, name the failure mode and suggest a specific fix.

1. **Engage from word one?** No throat-clearing. The first sentence should be in motion.
2. **Broad enough?** Could a non-specialist recognize the broad hook without knowing the specific topic?
3. **Narrows within 2-3 sentences?** The pivot from broad to specific must be crisp, not slow.
4. **Thesis by paragraph 2?** The reader should know the argument before paragraph 3.
5. **Passes voice rules?** Check the anti-technique list. Check for AI hit-list phrases.
6. **Creates a contract?** Does the opener introduce something the close can return to, transformed?
7. **Would Marcus keep reading?** Apply the patience test specifically to the first 100 words.

---

## Output Format

### Generate Mode

```
## Opener Variants: [Article Title]

**Template:** [which] | **Trigger:** [which] | **Technique selected:** [which]

---

### Variant A — [Technique Name]

[Opener text — full paragraph(s), Substack-ready markdown]

**Contract:** [what image/fact/tension the close must return to]

---

### Variant B — [Technique Name]

[Opener text — full paragraph(s), Substack-ready markdown]

**Contract:** [what image/fact/tension the close must return to]

---

**Recommendation:** [which variant and why — one sentence]
**Voice notes:** [any concerns about tone, em dash count, AI phrases — or "none"]
```

### Evaluate Mode

```
## Opener Assessment: [Article Title]

**Technique used (as written):** [identify which, if any]
**Overall:** [passes / needs work / fails]

### Checklist

| Check | Result | Notes |
|---|---|---|
| Engage from word one | ✓ / ✗ | [observation] |
| Broad enough | ✓ / ✗ | [observation] |
| Narrows within 2-3 sentences | ✓ / ✗ | [observation] |
| Thesis by paragraph 2 | ✓ / ✗ | [observation] |
| Passes voice rules | ✓ / ✗ | [specific violations if any] |
| Creates a contract | ✓ / ✗ | [what the close would return to] |
| Marcus keeps reading | ✓ / ✗ | [observation] |

### Failure Modes
[For each failed check: specific diagnosis and specific fix — not generic advice]

### Suggested Revision
[Optional: if the opener needs significant work, provide a revised version]
```

---

## Voice Quick-Reference

The full voice reference is at `../tcn-draft/references/voice-rules.md`. Opener-specific reminders:

- **No em dashes in the opener if possible.** The opener should flow; em dashes interrupt. Semicolons connect.
- **Short sentences hit harder.** Build complexity in longer sentences; land the point in a short one. The opener's landing sentence should be short.
- **Specific over general.** Names, numbers, dates. "On March 2, 2026" beats "In early 2026."
- **The opener is not the place for humor.** The sardonic pressure valve belongs in body sections. The opener is the hook; the joke comes after trust is established.
- **Don't explain the broad hook.** If the analogy needs explaining before it narrows, it isn't working. Find a broader point of entry.
