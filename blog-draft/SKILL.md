---
name: blog-draft
description: >
  Full section-by-section draft step of the blog-article-builder pipeline: from an approved
  outline and headline. Invoke this skill when the user has approved both an outline (blog-outline)
  and a headline (blog-headline) and wants to write the article — including phrases like "write the
  draft", "now draft it", "let's write the piece", "draft the article", "write it up", or when the
  user approves a headline and asks what's next. Does NOT apply to social media posts (that's
  blog-post, if available), outlines (blog-outline), headlines (blog-headline), fiction, or
  knowledge-base operations.
---

# Blog Article Draft Generator

## What This Skill Does

Produces a full blog article draft — section by section, in the blog's author voice, from an approved outline and headline. The draft is presented for the user's review and editing.

Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else.
Loads: `voice.md`, `reader.md`, `templates.md`, and the active preset.

Load the active profile's `voice.md` for this skill's draft-specific voice and rhythm reference (paragraph rhythm and grounding cadence, draft-form punctuation, model sentences). Banned vocabulary, negative parallelisms, vocabulary cliff, and closing-line abstraction live in the canonical voice file — see next section.
Load the active profile's `templates.md` for section structures, word counts, and tone notes.

---

## Voice & vocabulary canonical source

This skill MUST load the active profile's `voice.md` before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule, the banned-words list, dead phrases / transitions / engagement bait / hype language, the negative-parallelism rule, tribal-coded jargon and operational shibboleths, the dismissal-label rule, the vocabulary cliff rules including the meaning-preservation sub-principle, the closing-line abstraction rule, the broader AI writing patterns to avoid, and the anti-overfitting guide. See the relevant sections of the active profile's `voice.md` for all of these.

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on a copy embedded in this spec. Any short examples cited here are illustrative only — the canonical file is authoritative.

**Fallback when the canonical file is missing.** If the active profile's `voice.md` is not present, this skill must:
1. Flag explicitly to the user — "no voice file found at [profile path]/voice.md; skipping voice calibration."
2. Skip all voice-related work — no vocabulary substitution, no AI-tells audit, no closing-line check.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions.
4. Continue with non-voice work this skill can still do: still draft the structural sections (opener, body sections per template, personal reflection, close), still apply the Drafting for Accessibility principles, still cite sources inline, still pass through reader-persona tests. Skip the voice rules pass and note the gap in the draft's "Draft notes" block. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The active profile's `voice.md` may note an always-gloss-on-first-use rule that is conservative; a future enhancement would vary gloss aggressiveness by which adjacent reader cohort each piece targets. NOT IN SCOPE this pass. When implemented, the per-section tone note in the outline would feed an adjacency signal here so the draft tunes which jargon needs gloss vs. plain-language swap.

---

## Workflow Position and Companion Skills

`blog-draft` is one of two skills that share responsibility for prose accessibility in the blog workflow:

- **`blog-draft` (this skill)** generates the draft and bakes accessibility principles in from the start — paragraph rhythm, grounding cadence, statistic framing, deliberate reader address. These are generation-time choices that are easier to make once than to fix later.
- **`blog-readability` (audit pass)** runs after the draft and audits the same accessibility principles structurally — flagging paragraphs that ran too long, abstract claims that never touched ground, statistics stated naked, flat rhythm, and sentence-level comprehension drag.

The two are intentionally aimed at the same target from different angles. `blog-draft` aims for the principle during generation; `blog-readability` enforces it on the back end. The principles are stated once in detail — here under "Drafting for Accessibility" and in the active profile's `voice.md` under "Paragraph Rhythm and Grounding Cadence." `blog-readability` audits against the same source of truth rather than restating it. If a principle changes, update it in the profile's `voice.md` and `blog-readability` will pick up the new bar on its next audit.

`blog-humanizer` is a separate, lexical-level pass (AI tells, voice-breaking vocabulary) calibrated to the blog's author voice — it rewrites in place rather than producing a report. When both apply, run `blog-readability` first (structural fixes) and `blog-humanizer` second (word-level cleanup).

---

## The Long-Form End State

Every sentence in this draft must serve one target:

> **The reader persona (see `reader.md`) finishes the piece, saves it, and forwards it to one specific person they respect within 48 hours.**

Write conversationally — like the blog's author emailing a specific smart person they respect. Not a brand, not a bot, not a thought leader performing thought leadership. The writing is reaching out. It should feel like contact.

---

## Before You Write a Single Word

Review:
1. The approved outline — every bullet point, source reference, and section note
2. The approved headline and subheadline — the promise the draft must deliver on
3. The angle/hook — this determines tone and structural emphasis throughout
4. **A locked opener, if one was supplied** — see "Locked-opener input contract" below

Confirm the opener strategy and close strategy from the outline. These are the two ends of the piece; everything between them must connect.

---

## Locked-opener input contract

When this skill is invoked as part of the `blog-article-builder` workflow (or any pipeline that ran `blog-opener` before `blog-draft`), the caller supplies a **locked opener** — the opener variant the user already approved at a separate step. The locked opener is supplied in the invocation prompt under an explicit heading like:

> Locked opener (use verbatim — do not regenerate):
> ```
> <opener paragraph(s)>
> ```

When a locked opener is present:

1. **Use it verbatim** as the article's opening paragraph(s). Do not rewrite, condense, or re-pace it. The user already evaluated and approved this opener separately.
2. **Build the rest of the draft around it.** Treat the locked opener as fixed scaffolding the rest of the piece must connect to. The body sections must advance from where the locked opener leaves off; the close must call back to whatever image, fact, tension, or question the locked opener established (the opener-close contract from `blog-opener` ships with the locked opener — honor it).
3. **Do not run the "The Opener" generation rules below for this draft.** Those rules describe how to generate an opener from outline strategy; they don't apply when one is supplied.

When no locked opener is supplied (standalone single-step use of `blog-draft`), follow the outline's opener strategy and generate the opener inline using the rules in the "The Opener" subsection below. This is the original behavior — the locked-opener contract is additive, not breaking.

---

## The Drafting Process

### Write Section by Section

Follow the outline's section order. For each section:

1. **Check the tone note** from the outline (analytical, sardonic, personal, building)
2. **Hit the word count target** — within 10%. Going long dilutes; going short underdelivers
3. **Advance the argument** — each section must add something the previous section didn't establish. Restating the thesis in different words is the single most common failure mode in long-form
4. **Cite sources inline** — footnote links for data claims, hyperlinks for direct references. More citations is always better than fewer. The citations are for reader trust
5. **Cross-link to relevant reference pages** where relevant (if publishing from a linked vault or knowledge base)

### The Opener

**Skip this subsection if a locked opener was supplied** (see "Locked-opener input contract" above). When a locked opener is present, use it verbatim and do not regenerate.

When no locked opener is supplied: the opener is the most important paragraph in the piece. The blog author's voice (per `voice.md`) opens with a specific image or analogy that narrows from broad to specific — the lighthouse that attracts the ship.

Rules:
- Engage from the first word. No throat-clearing ("In today's rapidly changing..." is instant death)
- The analogy or image should be broadly accessible — something the reader persona and a non-specialist both recognize
- Narrow quickly to the specific topic
- **Thesis must land by paragraph 2.** The reader should know what this piece is arguing before the third paragraph begins
- The opener is also a structural investment: the close will call back to it

### The Body Sections

Follow the template structure from the outline. Each section has its own character; refer to the active profile's `templates.md` for section definitions and tone notes per section type.

### Section Subheadlines

Every section heading gets a subheadline — a short phrase after the template section name that previews the section's specific argument. Format: `## [Section Name from templates.md]: [Specific Section Argument]`

The subheadlines serve two purposes:
1. **Skimmability** — someone scanning only the headers should get the argument's shape
2. **Patience renewal** — each subheadline gives the reader persona a reason to keep reading into the next section

The subheadline is not a summary of the section. It's a promise — the same way the article headline promises the piece. Keep them short (under 12 words), specific, and slightly provocative.

---

**Analytical sections** (per the active profile's `templates.md` — typical: background/context sections, mechanics/how-it-works sections):
- Longest sections. Build complexity in longer sentences; land the point in a short one
- Primary sources over secondary. Data over assertion
- The "charitable reading then audit" move: present the official explanation fairly, then show why it's insufficient
- Specific over general: names, numbers, companies. "Salesforce charges $2K/seat" beats "enterprise software is expensive"

**Action sections** (per the active profile's `templates.md` — typical: implications, applications, what-to-do sections):
- Shorter. More direct. Forward-looking but grounded
- Implications, not predictions. What the evidence suggests, not what you guarantee
- Connect to the blog's core domain (per `identity.md`): who this affects, and what readers can do about it

**Personal reflection sections** (per the active profile's `templates.md` — typical: author-voice, first-person, human-element sections):
- First person. Less analytical, more human
- The anecdote serves the argument — it's illustration, not memoir
- Humor works best here as a pressure valve on heavy pieces
- Vulnerable but not confessional. Emotional exposure is fine; professional liability is not
- Can be shorter than other sections — 200-300 words is enough

### Inline Source Links

Every factual claim — data points, quotes, dates, dollar figures, percentages — gets an inline hyperlink. This is non-negotiable. The reader persona follows source links. One unsourced claim on something they can check destroys credibility across the entire piece.

**Do not use footnotes.** Sources are embedded as inline links on a few key words within the sentence that states the claim. When the draft is pasted into the blog's publishing platform, the links carry over directly — no manual footnote conversion needed.

**Format:** Choose 2-4 words in the sentence that naturally describe the source or the claim, and link them to the source URL. The linked words should read naturally in the sentence — the reader shouldn't notice the link is there unless they want to verify.

**Examples:**
- "Quarterly revenue [rose 38% year-over-year](https://url) in the most recent filing."
- "The committee [met behind closed doors](https://url) twice before the vote."
- "The company reported [a record operating profit](https://url) — its highest in eight quarters."

**Rules:**
- One link per claim. Don't double-link the same fact from two places in the sentence.
- Link the most specific words — the data point or the action, not generic words like "according to" or "reports say."
- Every link must point to a real, verifiable URL from the source material or from verified external reporting. Never use generic domain links.
- If a claim can't be sourced to a specific URL, flag it in draft notes as needing verification rather than linking to nothing.

### The Close

The close is the second most important paragraph. Two requirements:

1. **Callback to the opener** — restate the opening image or analogy in the light of what the piece established. The same image, transformed by the argument
2. **Leave the reader pondering** — the close adds one more thing. Not a conclusion they already drew from the setup; a reframe, an implication, or a question worth investigating

Apply the Cover Test: cover the last paragraph. Re-read the piece. If you already thought the ending from reading the body, the ending is weak — upgrade it.

The **tonal drop + micro-reframe** applies here too. The close can shift register (from analytical to personal, from precise to casual) but must carry a new idea inside the shift. Tone change without payload is sarcasm without a point.

---

## Drafting for Accessibility

These five principles shape readability from the moment a sentence is written. They are the generation-time half of the accessibility work — `blog-readability` (post-draft audit) checks the same five principles structurally on the finished draft. See the active profile's `voice.md` under "Paragraph Rhythm and Grounding Cadence" for the full explanation; this section is the working summary.

The reason these matter: the blog's reader persona (per `reader.md`) tolerates and rewards density, but only when the density is earned. Uncalibrated density — paragraphs that go on, abstractions that don't touch ground, numbers that don't argue anything — is the difference between a piece the reader saves and a piece they close at paragraph three even though every claim is correct.

### 1. Paragraph Length Budget

Body paragraphs vary roughly between 40 and 100 words. In dense analytical sections, no paragraph runs longer than ~100 words without a structural reason (a block quote, a multi-step example, a piece of evidence that loses force if split). Mix short and long deliberately — a 40-word paragraph hits harder when it follows a 90-word one. Three same-length paragraphs in a row flatten the rhythm and register as homework even if every sentence is correct.

### 2. Touch Ground Within Three

Every abstract claim, conceptual move, or system-level statement touches ground within three sentences via one of:
- A named entity (person, company, agency, place)
- A specific number (date, percentage, dollar figure, count)
- A concrete scene the reader can picture
- A one-word punch that compresses the abstraction back to street level

Pattern: "Most housing debates obsess over how many homes exist. The more revealing question is how often homes become available. Availability isn't just construction. **It's turnover.**" Three sentences of abstraction, then a one-word punch that collapses the concept into something concrete enough to argue with.

Abstract-on-abstract is the single most common failure mode after thesis restatement. The reader can follow one ungrounded claim; by the second, they're skimming.

### 3. Statistics Embed in a Causal Chain

Numbers never get stated naked. Every statistic embeds in a mechanism, consequence, or behavior change — the number is *evidence in an argument*, not the headline. Compare:

- Weak: "Mortgage rates rose to 7%."
- Strong: "For each percentage point by which current mortgage rates exceed a homeowner's existing rate, the probability of sale falls by about 18.1%."

The fix when a number feels orphaned: ask what mechanism it's evidence for, or what behavior changes because of it. If neither answer is sharp, the number probably doesn't belong.

### 4. Reader Address via "You" — Sparingly

"You" is permitted when a structural claim benefits from being felt at human scale. The construction places the reader inside the system the piece is describing: "You can't move closer to the job cluster, so you commute longer. You can't save enough for a down payment while rent eats the margin..." Not casual address — a universalizing move that converts an abstract claim into something the reader can picture themselves inside.

Constraints:
- Never opens the piece with "you" — that reads as a textbook or a self-help post
- Reserve for moments where the alternative is pure third-person abstraction
- "I" still appears only in personal reflection sections (per `templates.md`); "we" remains off-limits (it presumes shared identity with the reader, which the blog does not assert)

### 5. Anaphora Is Permitted; AI Rule-of-Three Is Not

The voice rule against "exactly three items in lists" targets the *AI default* — three parallel items inside a sentence because the model couldn't decide where to stop. *Deliberate anaphora* — three or four sentences in a row starting with the same construction, doing rhythmic or argumentative work — is different and is encouraged when the piece calls for it.

Example of anaphora doing real work: four consecutive sentences beginning "You can't..." that build structural pressure on the reader, each one closing a different exit from a trapped situation.

Test: if the parallelism does rhythmic or argumentative work no other construction could do as well, keep it. If it exists because three felt like the right number of examples, cut to two or expand to four.

---

## Voice Rules (Draft-Form Overlay — see active profile's `voice.md` for full depth)

The canonical voice DNA — banned vocabulary, AI hit-list phrases, negative parallelisms, dismissal labels, vocabulary cliff, closing-line abstraction — lives in the active profile's `voice.md`. Load it before drafting. The rules below are draft-form-specific only.

### Hard Rules (draft-form-specific)

**Never:**
- Explain the joke. If it needs explanation, fix the delivery.
- Use em dashes closed (`—word—`). Spaced em dash only, and rarely.
- Use the "[X] without [Y] is a press release" formula — formula dressed as insight. No matter what fills the variables, it reads as a cliché.
- Add one more sentence after the punchline lands.
- Use ragebait or engagement farming patterns.
- Default to three-item lists inside a single sentence (use two or four — but deliberate anaphora across three or four sentences is encouraged when it does rhythmic work; see "Drafting for Accessibility" above).
- Use therapy-speak unironically: "holding space," "toxic positivity," "somatic," "processing."
- Use PhD-level vocabulary without earning the difficulty.

For banned individual words, banned phrases, and the broader AI-pattern catalog: resolve at runtime from the active profile's `voice.md`. Do not duplicate that list here.

**Always:**
- Semicolons connect; em dashes are rare and spaced.
- Parentheses are comedic whispers.
- Profanity is a scarce resource — one use per piece maximum, only when it hits harder than anything else.
- Short sentences hit harder. Build complexity in longer sentences; land the point in a short one.
- Go for the second thought, not the first. The first punchline is the one everyone thinks of.
- Specific over general: names, numbers, companies, dates.
- Humor to ease tension on heavy pieces — the sardonic edge is a pressure valve, not decoration.

### The Litmus Test

Before finalizing:

> "Does this sound like something the blog's author (per `voice.md`) would say to a specific smart person they respect — or does it sound like something written for an algorithm?"

If the latter, cut until it's the former. Less content, more compression.

---

## The Five Long-Form Reader-Persona Tests

Run these against the complete draft before presenting (reader persona defined in `reader.md`):

1. **Signal test** — Does this deliver at least one thing the reader persona couldn't have found easily themselves?

2. **Patience test** — Would the reader persona still be reading at paragraph 3? Is the argument advancing, not restating?

3. **Depth test** — Does this feel like the writer operates in the thing they're writing about? Operational credibility, not credential-signaling.

4. **Save test** — Would the reader persona save this to reference later, or forward it to one specific person they respect?

5. **Accumulation test** — Does this contribute to the "slightly ahead of them" pattern? Does it raise or maintain the signal floor?

If the draft fails any test, identify which section is the weak point and fix it before presenting.

---

## Output Format

Present the draft as clean, platform-ready markdown (formatted for the blog's publishing platform per `quick.platform`):

```markdown
# [Approved Headline]

## [Approved Subheadline]

[Opener — the specific image or analogy that narrows]

[Thesis — by paragraph 2]

---

## [Template Section Name from templates.md]: [Section Subheadline]

[Section content]

---

## [Template Section Name from templates.md]: [Section Subheadline]

[Section content]

[Continue for all sections including personal reflection]

---

[Close — callback + reframe]
```

After the draft, include a brief note:

```
---

**Draft notes:**
- Word count: [X]
- Template: [which — per templates.md]
- Angle/hook: [which]
- Reader-persona tests: [pass/fail summary — flag any concerns]
- Inline source links: [count]
- Unsourced claims: [any that need verification, or "none"]
```

---

## What Makes a Strong Blog Draft Different from Generic Newsletter Prose

Generic newsletter prose:
- Opens with throat-clearing or "state of the world" preamble
- Uses hedging language to avoid commitment ("it seems," "one might argue")
- Summarizes rather than argues
- Ends with a vague call to reflection

A strong blog draft (calibrated to this profile):
- Opens with a specific image that hooks before the reader knows why
- Takes a position and defends it with evidence
- Advances the argument every paragraph — no restating in new words
- Ends with a reframe that makes the reader reconsider something they thought was settled
- Sounds like a specific person talking, not a brand publishing

The difference is conviction backed by evidence, delivered with personality. That's what keeps the reader persona reading.

---

## Profile Files Loaded

- **`voice.md`** — Full voice reference: punctuation philosophy, sentence rhythm, paragraph rhythm and grounding cadence, words to love/avoid, model sentences, the AI hit list, humor principles
- **`reader.md`** — Reader persona profile: who the reader is, what they know, what earns their trust, what loses it
- **`templates.md`** — Full template detail: section structures, word counts, tone notes per section, angle/hook-template pairings

## Companion Skills

- **`blog-readability`** — Post-draft accessibility audit. Runs the same five principles in "Drafting for Accessibility" above as a structural check on the finished draft. Use after `blog-draft` and before publishing whenever the writing feels dense or hard to follow.
- **`blog-humanizer`** — Post-draft lexical pass for AI tells, calibrated to the blog's author voice (active rewriter, not a report). Run after `blog-readability` when both apply (structural fixes precede word-level cleanup).
- **`blog-opener`** — Standalone opener fix-pass when the opening paragraph is the weak point.
- **`blog-fact-check`** / **`blog-fact-reconcile`** — Source verification and correction application. Independent dimension from voice and readability.
