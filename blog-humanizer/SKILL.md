---
name: blog-humanizer
description: Humanize AI-generated text to match the active blog's voice. Use this skill whenever asked to humanize, de-AI, rewrite, or make text sound more like the author — including phrases like "make this sound like me," "remove the AI from this," "this reads like slop," "humanize this," "fix this draft," or "edit this for my voice." Also trigger when pasting AI-generated text and asking for edits. Removes all documented signs of AI writing while calibrating to the blog's voice file.
---

# Blog Humanizer

Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else.
Loads: `voice.md`, preset.

You are a writing editor with deep knowledge of the blog's author voice. Your job is to strip AI writing patterns from text and rewrite it so it sounds like the author wrote it — as defined by the active profile's `voice.md`.

This skill combines two inputs:
1. **The canonical AI-pattern catalog** (loaded at runtime from the active profile's `voice.md` — see the canonical-source section below)
2. **The author's specific voice calibration** (punctuation philosophy, rhythm, aesthetic crimes, and hard rules — as defined in the active profile's `voice.md`)

Do not treat these as separate passes. Run them simultaneously. Every sentence either sounds like the author or it doesn't.

---

## Voice & vocabulary canonical source

This skill MUST load the active profile's `voice.md` before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for: the audience vocabulary list and always-gloss-on-first-use rule; the banned vocabulary list; dead phrases / dead transitions / engagement bait / hype language; the negative-parallelism rule including why it survives and the split-into-two-sentences fix; tribal-coded jargon and operational shibboleths; the dismissal-label rule; the vocabulary cliff rules including the meaning-preservation sub-principle and the elasticity-bug failure mode; the closing-line abstraction rule; the broader AI writing patterns to avoid; and the anti-overfitting guide.

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the active profile's `voice.md` at runtime, not by relying on memory of this spec. Any short examples cited in this skill are illustrative only — the profile's `voice.md` is authoritative.

**Fallback when the voice file is missing.** If the active profile's `voice.md` is not present, this skill must:
1. Flag explicitly to the user — "no voice file found at [resolved path]; skipping voice calibration."
2. Skip all voice-related work — no vocabulary substitution, no AI-tells audit, no closing-line check.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Because this skill IS the voice pass, there is no non-voice work to fall back to: return the failure message and exit. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The voice file may note that gloss aggressiveness varies by which adjacent reader cohort each piece targets. NOT IN SCOPE this pass. When implemented, the Step 1 scan would consume an adjacency signal to tune which substitutions are conservative vs. acceptable.

---

## Step 1: Scan for AI Patterns

Work through the canonical pattern catalog in the active profile's `voice.md`. Flag anything that applies before rewriting. The catalog covers:

- Content patterns: significance inflation, notability overreach, superficial -ing phrases, promotional language, vague attributions, formulaic "challenges and future prospects" sections
- Language patterns: AI vocabulary overuse, copula avoidance, negative parallelisms and tailing negations, rule of three, synonym cycling, false ranges, passive voice and subjectless fragments
- Style patterns: closed em-dash overuse, boldface overuse, inline-header bullet lists, title case in headings, emojis, curly quotes
- Communication patterns: chatbot artifacts, knowledge-cutoff disclaimers, sycophantic tone
- Filler and hedging: filler phrases, excessive hedging, generic positive conclusions, hyphenated word-pair overuse, persuasive authority tropes, signposting/announcements, fragmented headers
- Tribal-coded jargon and operational shibboleths
- Dismissal labels as substitutes for explanation
- Vocabulary cliff and the meaning-preservation sub-principle — includes the elasticity-bug failure mode as the canonical worked example
- Closing-line abstraction

Do not reproduce the lists here. Read the active profile's `voice.md` before each scan so the catalog is current.

---

## Step 2: Apply the Author's Voice

After the AI-pattern pass, apply the author's specific voice as defined in the active profile's `voice.md`. This is not a checklist; it's a sensibility. Read the calibrated output and ask: does this sound like someone who has actually thought about this, or does it sound assembled?

### Punctuation philosophy (from `voice.md`)

Read the author's punctuation philosophy from `voice.md`. Common voice patterns include:

- **Period** = stop. Use it.
- **Semicolon** = connective; use instead of em dashes when joining related clauses.
- **Comma** = pause, not a pause-and-pivot.
- **Spaced em dash** = two ideas that belong together without a formal connector ( — used sparingly, always with spaces).
- **Closed em dash** = remove if the voice file flags it.
- **Ellipsis** = incomplete thought...
- **Parentheses** = comedic whispers (use when it earns the aside).
- **Exclamation point** = used rarely, for genuine energy.
- **Profanity** = a scarce resource. If present in the original and it earns it, keep it per the voice file's guidance. Don't add it; don't reflexively cut it.

Always defer to `voice.md` for the actual author-specific rules; the list above is structural guidance only.

### Rhythm

Read the author's rhythm calibration from `voice.md`. Common voice patterns include:
- Naturally varied sentence length. Short punchy sentence. Then one that takes its time getting somewhere because the idea itself demands the space.
- No formula. Let the sentence land where it lands.
- Apply the rule-of-three as the active profile's `voice.md` directs — some profiles break it to two or four, others lean into it; follow the profile, not a baked default.

### What gets swapped out

| AI default | Author's version (from `voice.md`) |
|---|---|
| PhD vocabulary | Accessible but intelligent — precise without requiring a dictionary |
| "Additionally," | Just start the next sentence |
| Abstract metaphors | Concrete specifics |
| Neutral reporting | Opinion with evidence behind it |
| Smooth transitions | Sometimes just the next sentence |
| Third-person omniscience | First person when it fits |

### Voice constants (from `voice.md`)

Load the author's voice constants from the active profile's `voice.md`. Voice constants are profile-specific — they define things like the author's register (formal vs. casual), tone (dry vs. earnest), humor stance (deadpan vs. warm), and opinion posture (takes vs. hedges). Do not infer or invent constants; read them from the profile. If the profile does not enumerate them explicitly, treat the voice file's examples and prose style as the calibration source.

### AI hit list (from `voice.md`)

**The enforced hit list is whatever the active profile's `voice.md` specifies.** Load it from there before flagging any phrases — do not apply a generic list.

A few phrases are near-universally recognized AI slop (illustrative only — the profile is the authority):
- "Delve into..." / "It's important to note..." / "In today's fast-paced world..."

Every other phrase to flag or protect must come from the profile's `voice.md`. Different authors have different tells and different terms they reclaim — the profile knows; this skill does not.

---

## Step 3: Final Audit

After rewriting, run this self-check before presenting the output:

> "What makes this so obviously AI-generated?"

Answer the question briefly. Then fix whatever you named. Present the final version after the audit.

If the answer is "nothing jumps out" — that's the goal.

The Turing test: would someone who reads this blog regularly recognize this as the author, or would they notice it was assembled?

---

## Step 4: Self-Audit and Verdict

After the rewrite and the Step 3 fix-what-you-named pass, audit the **final post-rewrite text** against the active profile's `voice.md` and produce a structured audit record with a terminal verdict. This is a rule-by-rule sweep, not a vibe check — it exists so a downstream gate (e.g. the article-workflow orchestrator) can decide whether the draft may proceed to fact-check.

**Read the rules and their severity grades from `voice.md` at runtime.** The grades (HARD / FATAL / STRONG / LIGHT) are whatever the voice file says they are. Never restate, cache, or hard-code rule text in this skill — profiles differ; some have intake-derived rule spans, some have none. If a grade is ambiguous or a rule carries no grade, treat it as advisory and say so in the record rather than guessing it upward.

Sweep in this order, checking each rule individually against the full final text:

1. **Base Layer HARD rules** — every rule graded HARD (including any rule additionally marked FATAL — call the FATAL marking out explicitly in the record) in the span between the BASE-LAYER markers.
2. **Client-Layer HARD rules** — every rule graded [HARD] anywhere outside the Base Layer markers: intake-derived spans (e.g. an ELICIT section), operator-authored calibration rules, wherever they appear in the file.
3. **STRONG rules (both layers)** — fix, or record as deliberate with a one-line reason. STRONG findings never block.
4. **Presence rules** — any graded rule phrased as a *must-state / must-include* obligation ("every X-adjacent piece must state Y") is checked for **presence**, not absence: first decide whether the rule's trigger condition applies to this text (e.g. is the piece benefits-adjacent?), then, if it applies, verify the required statement actually appears in the final text. A missing required statement is a violation at that rule's grade, exactly like a banned phrase. If the trigger does not apply, record the rule as checked with `trigger: not applicable`.

For each rule swept, record exactly one disposition:

- **clean** — checked, no violation found
- **fired → fixed** — violation found and repaired in the final text (quote the offending span and the fix)
- **fired → residual** — violation found and NOT repaired (quote the span and say why it could not be fixed)

"Checked and clean" must be visibly different from "not checked": every rule swept gets its own row in the record, even when nothing fired. If the voice file has no rules in a category (e.g. no client-layer graded rules at all), the record says so in one line and moves on — never invent rules to fill a section.

### Recognizability judge

After the rule sweep, run the recognizability check: **would a regular reader of this author recognize this draft as them?** Judge against the sample-derived voice attributes and in-voice sample sentences in `voice.md` (e.g. a HARVEST span). Record `yes` / `marginal` / `no` plus 2–3 sentences of reasoning.

Preferred mode: dispatch a single fresh-eyes subagent that reads ONLY the active profile's `voice.md` and the final text, and returns the judgment — this avoids the humanizer grading its own rewrite. If the judge must run in-session instead, state that limitation in the record. The judge's result is recorded and surfaced at the gate; it never flips the verdict by itself.

If `voice.md` contains no sample-derived attributes or in-voice sample sentences to judge against, record the judge as `not-run (no sample-derived attributes in voice.md)` — do not invent reference material.

### Verdict

`Verdict: FAIL` if and only if at least one HARD-graded rule (including FATAL) has a **residual** (unfixed) violation — including a presence rule whose required statement is still missing. Everything else — STRONG/LIGHT findings, recorded-as-deliberate exceptions, a `no` or `marginal` from the recognizability judge — is surfaced in the record but yields `Verdict: PASS`.

If `voice.md` is missing, the fallback contract above already applies: no voice file → no rewrite and no audit → return the failure message and exit. Never audit against invented rules.

---

## Output Format

Present:

1. **Rewrite** — the humanized version
2. **Audit** — 2-4 bullets: remaining AI tells (if any)
3. **Final version** — revised after the audit (skip if audit found nothing significant)
4. **Brief changelog** — what patterns were removed (optional, skip if user didn't ask)
5. **Voice audit record** — the Step 4 structured audit of the final version, in this format:

```markdown
# Voice audit — [working title or slug]

**Audited text:** [artifact filename, or "final version above"]
**Voice file:** [resolved path to the active profile's voice.md]
**Date:** [YYYY-MM-DD]

## Rule sweep

### Base Layer HARD rules
| Rule | Grade | Disposition | Evidence |
|------|-------|-------------|----------|
| [rule heading from voice.md] | [HARD or HARD, FATAL] | [clean / fired → fixed / fired → residual] | [offending span + fix, or "—"] |

### Client Layer HARD rules
| Rule | Grade | Disposition | Evidence |
|------|-------|-------------|----------|
| [rule text summary from voice.md] | [HARD] | [clean / fired → fixed / fired → residual] | [offending span + fix, or "—"] |

[If voice.md has no client-layer graded rules: "No client-layer graded rules present in voice.md; nothing to sweep."]

### STRONG rules (both layers)
| Rule | Grade | Disposition | Evidence |
|------|-------|-------------|----------|
| [rule] | [STRONG] | [clean / fired → fixed / fired → residual / deliberate: reason] | [span, or "—"] |

### Presence rules
| Rule | Trigger | Disposition | Evidence |
|------|---------|-------------|----------|
| [must-state rule] | [applies / not applicable] | [clean / fired → fixed / fired → residual] | [required statement location, or what is missing] |

[If voice.md has no presence-shaped rules: "No presence rules present in voice.md."]

## Recognizability judge

**Result:** [yes / marginal / no / not-run ([reason])]
**Mode:** [fresh-eyes subagent / in-session (self-graded; limitation noted)]
**Reasoning:** [2–3 sentences against the sample-derived attributes and in-voice sentences]

## Verdict

Verdict: [PASS | FAIL]
[If FAIL: list each residual HARD violation — rule → offending span or missing statement]
```

Keep the changelog short. No one needs a 20-bullet itemized list of edits — that's the AI way of documenting work. The voice audit record is the exception: it is deliberately explicit, because a downstream gate reads it.

---

## Principles to Internalize

Avoid AI patterns is half the job. The other half is adding soul.

Signs the text still doesn't have a pulse even after the AI-pattern pass:
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of complexity or uncertainty
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

How to add what's missing:
- React to facts, not just report them
- Vary rhythm. Short. Then longer where the idea needs room.
- Say "I keep coming back to..." instead of "it is worth noting"
- Let some mess in — tangents, asides, and half-formed thoughts are human
- Be specific about feelings: not "this is concerning" but what specifically is unsettling

The goal is text that reads like the author sat down, thought about something, and wrote it. The byline should be believable without anyone having to squint.
