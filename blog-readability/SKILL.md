---
name: blog-readability
description: >
  Audits a finished blog post draft for density and accessibility problems — paragraphs that run too
  long, abstract claims that never touch ground, statistics stated naked, flat paragraph rhythm,
  and sentence-level comprehension drag. Produces a prioritized report with specific rewrites for
  the worst offenders. ALWAYS invoke this skill on a blog draft when the user says the writing
  feels "dense," "hard to read," "intimidating," "inaccessible," "too dense for non-experts,"
  "information-packed but heavy," or "too much" — or asks to "make this more digestible," "loosen
  this up," "simplify the structure," "punch this up," "run a readability pass," "do an accessibility
  check," or "check if a non-expert could follow this." Also trigger when the user shares a finished
  draft and worries about reader fatigue, accessibility, or whether someone unfamiliar with the topic
  could read it. Pairs with `blog-humanizer` — this skill is the structural density audit;
  `blog-humanizer` is the lexical AI-tell pass calibrated to the author's voice (rewrites in place,
  not a report). Run `blog-readability` first when both apply (structural fixes precede word-level
  cleanup). Does NOT apply to outlines, social media posts, AI-tell hunting at the vocabulary level
  (use `blog-humanizer`), fact-checking (use `blog-fact-check`), or fixing weak openers specifically
  (use `blog-opener`). When the active preset is `fiction`, the density/comprehension audit is
  replaced by a pacing audit (see Pacing Mode below); all other presets default to density/comprehension.
---

# Blog Readability Audit (Post-Draft Density Scanner)

> Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else.
> Loads: `reader.md`, `voice.md`, and the active preset (from `profile.yaml.preset`).

## What This Skill Does

Takes a finished blog post draft and returns a structured report with three parts:

1. **Density inventory** — specific paragraphs, claims, and sentences that fail one or more readability principles, quoted with enough context that the user can locate them
2. **Severity ranking** — which problems matter most for *this* piece, given its argument and apparent reader load
3. **Revision recommendations** — concrete rewrites for the top 3–5 offenders; pattern-level guidance for the rest

The goal is to *help the user revise*, not to auto-produce a fully rewritten draft. Wholesale rewrites by an LLM tend to flatten the voice the writer has been building. The user — or a focused re-run of the drafting step on a specific section — does the final hand. This skill's job is to make the density problems legible and the revision work surgical.

---

## Preset Hook — Density/Comprehension vs. Pacing Mode

After resolving the active profile, check `profile.yaml.preset` (or any `profile.yaml.steps.readability` override):

- **Default (all presets except `fiction`):** run the full five-audit **density/comprehension** pass as described below. This is the standard mode for non-fiction, journalism, technical, and legal presets.
- **`fiction` preset:** replace Audits 1–5 with the **pacing audit** described in the fiction preset file. The pacing audit checks sentence rhythm, scene length, white space, and forward momentum rather than informational density. The output format remains the same (inventory → severity → revision), but the criteria shift from comprehension load to narrative momentum. Do NOT run the density audits on fiction drafts — they are calibrated for analytical prose and will produce false positives on scene-based writing.

If `profile.yaml.steps.readability` is explicitly set to `pacing`, use pacing mode regardless of preset.

---

## Voice & Vocabulary Canonical Source

This skill MUST load the active profile's `voice.md` before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list, banned-words list, dead phrases and hype language, AI writing patterns to avoid, and any voice-specific calibration.

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to `voice.md` at runtime, not by relying on a copy embedded in this spec. Any short examples cited here are illustrative only — `voice.md` is authoritative.

Note: this skill's primary audit dimension is *structural density*, not lexical voice. Vocabulary cliff and closing-line abstraction rules (if defined in `voice.md`) overlap the readability surface, so this skill consults `voice.md` for those specifically when a flagged passage might be a vocab-cliff or closing-line issue rather than a pure density issue.

**Fallback when `voice.md` is missing.** If `voice.md` is not present in the resolved profile:
1. Flag explicitly to the user — "no voice file found in the active profile; skipping voice calibration."
2. Skip the vocabulary cliff cross-check and the closing-line plain-language cross-check.
3. Do NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions.
4. Continue with non-voice work this skill can still do: produce the full structural density report (Audits 1–5) with quoted excerpts, severity ranking, and the top 3–5 rewrites. The lexical AI-tell audit is owned by `blog-humanizer`. Better to do less than to do harm with stale or generic guidance.

---

## Workflow Position and Source of Truth

`blog-readability` is the audit-time half of the blog pipeline's accessibility work. The generation-time half lives in the drafting step. **The active profile's `voice.md` is the source of truth for the principles being audited.** This skill audits against the same five principles rather than restating them — if the principles change in `voice.md`, this skill picks up the new bar automatically.

The five principles, in short:

1. **Paragraph length budget** — body paragraphs vary 40–100 words; dense sections rarely exceed 100 without structural reason
2. **Touch ground within three** — abstract claims touch ground (named entity, specific number, concrete scene, or one-word punch) within three sentences
3. **Statistics embed in causal chains** — numbers are never naked; they are evidence in a mechanism
4. **Reader address via "you" is permitted, sparingly** — used to convert systemic claims into human-scale experience
5. **Anaphora is permitted; AI rule-of-three is not** — deliberate parallel construction in service of rhythm is encouraged; default three-item lists are not

Companion skills:

- **`blog-draft`** generated the draft and aimed for these principles at write-time. If this audit reveals that an entire section is the problem, the cleanest fix is often re-running `blog-draft` on just that section rather than patching here.
- **`blog-humanizer`** covers the *lexical* dimension — AI vocabulary tells, voice-breaking phrases — and rewrites them in the author's voice. Run `blog-readability` first (structural) when both apply, then `blog-humanizer` (word-level).
- **`blog-opener`** covers the opener specifically. If this audit flags only the opener, defer there for the rewrite.
- **`blog-fact-check`** is a different dimension entirely (source verification). Order: density → AI tells → fact check.

---

## When to Invoke — and When Not To

**Use on:** finished blog post drafts the user is preparing to publish, or that the user describes as dense, intimidating, or hard to follow. Also use when the user explicitly asks for a readability or accessibility pass even if they haven't named what feels wrong.

**Don't use on:**
- Outlines, headlines, social posts, or other deliberately compressed artifacts — the audit thresholds are calibrated to long-form analytical prose and will surface noise on short forms
- Drafts that haven't been through the drafting step yet — running readability on raw conversation transcripts or first-pass brainstorms produces false positives
- Fiction drafts with the `general` preset active — switch to the `fiction` preset or confirm pacing mode before auditing narrative writing

---

## The Process

### Step 1 — Read the Draft Once Straight Through

Read as a reader would. Note where comprehension stalls, where attention drifts, where the eye skips ahead. Note the apparent reader load — the conceptual density of the argument, the technicality of the domain, the background the piece assumes. Consult `reader.md` to calibrate: the reader persona's sophistication level and patience signals determine what density earns its keep and what doesn't.

This calibrates severity in Step 3: a piece on derivatives pricing legitimately needs to compress more than a piece on why people don't move houses anymore.

Do not skip this pass. Running the checklist on a draft you haven't read for flow produces noisy false positives and misses problems that only show up *in motion* — places where the argument drags, not the prose.

### Step 2 — Run the Five Audits

For each principle, scan the draft and produce a list of violations. Load `references/density-patterns.md` for the detection rules, examples, and revision moves for each pattern.

**Audit 1: Paragraph Length**
Walk through each paragraph in body sections. Flag any over ~120 words. Flag any sequence of three or more paragraphs within ~15 words of each other (flat-length rhythm).

**Audit 2: Ungrounded Abstraction**
For each paragraph, identify when (if ever) it touches ground via named entity, specific number, concrete scene, or one-word punch. If three or more consecutive sentences pass without grounding, flag the paragraph and note where grounding should appear.

**Audit 3: Naked Statistics**
For each number in the draft (date, percentage, dollar figure, count), check whether it appears inside a causal chain or human consequence. Flag stats that stand alone or that appear immediately adjacent to another stat with no intervening mechanism.

**Audit 4: Flat Rhythm**
Note sections where multiple paragraphs read at the same pace — same length, same sentence count, same opening construction. Flag any section with three or more consecutive paragraphs matching on these dimensions.

**Audit 5: Sentence-Level Comprehension Drag**
Scan for sentences with three or more subordinate clauses, sentences over ~40 words that aren't doing clear structural work, and sentences that bury the main verb deep behind qualifications. Flag these for splitting or restructuring.

For each violation, record:

- **Category** — one of the five audits
- **Quoted excerpt** — 3–10 words from the offending passage so the user can search the draft
- **Location hint** — section name or paragraph number (not line numbers; prose paragraphs wrap)
- **Why it fails** — one short sentence

Be generous in what you flag, but honest about confidence. Mark borderline calls as "borderline" rather than padding the list. A noisy report is a report the user stops reading.

### Step 3 — Rank by Severity

Not all violations are equal. Rank using this priority:

1. **Comprehension-breaking** — violations severe enough that a typical reader stalls or quits. A 200-word paragraph buried in section 3. Three abstract claims in a row with no grounding. A stat dump with four numbers and no mechanism. These must be fixed.
2. **Cumulative drag** — patterns fine in isolation but exhausting when stacked. Six 80-word paragraphs in a row. Sentence after sentence of equal length. Three "this means..." openings in succession. These are fixed by varying, not eliminating.
3. **Surface drag** — single instances of long sentences or unembedded stats. Mechanical fixes; flag them but don't dwell.
4. **Borderline** — calls that could go either way depending on what the section is doing argumentatively. Note them and defer to the user.

**Calibration matters.** Consult the reader persona in `reader.md` and the blog's subject domain in `identity.md` (`quick.domain`) before grading severity. A piece targeting domain experts can carry more density than a general-audience explainer; the reader self-selected for the load.

### Step 4 — Rewrite the Top 3–5 Offenders

For the worst comprehension-breaking violations, produce an actual rewrite — not a full rewrite of the surrounding paragraph, just the fix in context, so the user can see the before/after.

Core revision moves (full pattern library in `references/density-patterns.md`):

- **For long paragraphs:** identify the secondary idea inside the paragraph and break to a new one there. The break point is often a sentence beginning with "but," "and yet," or naming a new entity.
- **For ungrounded abstraction:** add one of the four grounding moves. Prefer the one-word punch when the surrounding sentences are long and conceptual.
- **For naked statistics:** wrap the number in either (a) the mechanism that produced it or (b) the behavior change it causes. If neither answer is sharp, the number may need to come out.
- **For flat rhythm:** the fastest fix is usually to cut one or two sentences from the longest paragraph in the run and let the next paragraph stand short by comparison. Length variation does most of the rhythm work.
- **For sentence drag:** split at the first natural clause boundary, or move the main verb earlier and demote the qualifications to a follow-up sentence.

For cumulative and surface drag, give a one-line recommendation ("Three of the five paragraphs in section 4 run 90+ words; split one of them") instead of writing individual rewrites.

### Step 5 — Present the Report

Use the output format below. Keep the report scannable. A 2,000-word draft does not need a 3,000-word audit.

---

## Output Format

```markdown
# Readability Report

**Draft:** [title or first line]
**Apparent reader load:** [one sentence — how dense is this piece allowed to be given its topic and audience]
**Overall density:** [low / moderate / high / very high]
**Bottom-line take:** [one sentence — publishable as is, publishable with small fixes, or needs a structural pass]

## Top Comprehension-Breaking Violations

1. **[Audit category]** — "[quoted excerpt]" ([location])
   - Why: [one sentence]
   - Revision: [rewritten passage in context]

[2–5 of these — the worst ones]

## Cumulative Drag

- **[Pattern name]**: [count] instances ([location list]). Recommendation: [how to vary or reduce]
- ...

## Surface Drag

- [One line per item with location and fix instruction]

## Borderline — Your Call

- "[quoted excerpt]" ([location]) — [why it could go either way]
- ...

## What's Working

[Brief — 2–4 sentences on which paragraphs and passages already read cleanly. Reinforces the rhythm the user is trying to protect. Do not skip this; revision is easier when the target is named.]
```

---

## Principles to Keep in Mind

**This skill flags; it doesn't overwrite.** A fully auto-rewritten draft tends to lose the voice the user has been building. The user's hand — or a focused re-run of the drafting step on a specific section — does the final revision. The report's job is to make the problems legible and the fix specific.

**Density is not a vice in itself.** Strong long-form writing rewards information density. The failure mode this skill targets is not density per se; it's *uncalibrated* density — passages that ask the reader to hold more than they can comfortably carry. Some pieces legitimately run dense; the audit's job is to find the spots where the density wasn't earned.

**The best fix is often a cut.** Many density violations are fixed not by adding grounding but by deleting the abstract claim entirely. If a paragraph asserts three things and the reader only needs two, the third was probably the one without grounding for a reason. Deletion is a readability edit.

**Read for flow before scanning for patterns.** Running only the checklist misses the worst kind of density: passages where the *argument* drags, not the prose. A technically readable piece with a slack argument is a piece nobody finishes.

**Calibrate to audience, not to a universal threshold.** A piece on derivatives pricing for derivatives traders runs denser than a piece on housing for general readers. The thresholds in `references/density-patterns.md` are starting points, not absolutes. Adjust severity based on the blog's subject domain (`quick.domain`) and reader persona (`reader.md`).

---

## Reference Files

- `references/density-patterns.md` — Full pattern catalog for each of the five audits: detection rules, examples of violations, revision moves, and positive examples from prose that gets this right. Load when running the audit.

---

## Related Skills (with workflow order)

The natural order when running multiple post-draft passes:

1. **`blog-readability`** (this skill) — structural density audit
2. **`blog-humanizer`** — lexical AI-tell pass in the author's voice (rewrites in place)
3. **`blog-fact-check`** — source verification
4. **`blog-fact-reconcile`** — apply fact-check corrections

This order is not arbitrary: structural cuts can eliminate sentences that `blog-humanizer` would otherwise have rewritten, and rewriting density problems after fact-checking risks reintroducing unsourced claims. Density first, lexical second, sourcing last.

**`blog-opener`** is independent — if only the opener is the problem, run that instead.
