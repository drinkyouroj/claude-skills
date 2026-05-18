---
name: tcn-headline
description: >
  Step 2 of the Civic Node Substack article workflow: headline and subheadline generation from an
  approved outline. Invoke this skill when the user has an approved article outline and wants to
  move to headlines — including phrases like "write the headline", "give me headlines", "now do
  the headline", "headline options", "title this piece", or when the user approves a tcn-outline
  output and asks what's next. Does NOT apply to social media posts, wiki operations, or drafting
  (that's tcn-draft).
---

# The Civic Node — Headline Generator (Step 2 of 3)

## What This Skill Does

Produces 3 headline + subheadline options for a Civic Node Substack article, calibrated to Marcus and tested against the signal and send tests. The user selects one before drafting (tcn-draft) begins.

Load `references/voice-rules.md` for this skill's headline-form voice and style reference. Banned vocabulary, negative parallelisms, vocabulary cliff, and closing-line abstraction live in the canonical voice file — see next section.

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
2. Skip all voice-related work — no AI-hit-list cross-check on candidate headlines.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still produce 3 headline + subheadline options using the four hook structures (Borrowed Frame, Premise + Implication, Compressed Narrative, Question That Contains Its Answer), still apply the headline-specific anti-patterns (numbered lists, power words, teaching words, vague theme headlines, question-mark overuse), still run the Signal and Send tests. Flag "voice rules pass" as not enforced in the recommendation. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The canonical file's § 1 notes the always-gloss-on-first-use rule is conservative; a future enhancement would vary gloss aggressiveness by which adjacent cohort each piece targets (monetary-policy pieces gloss crypto terms more heavily; DePIN pieces gloss monetary terms; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, the hook-structure selection step would consume an adjacency signal — pieces targeting a wider cohort lean toward hooks that don't assume insider vocabulary; pieces targeting a denser cohort can use compressed-narrative headlines with domain shorthand.

---

## Why Headlines Are a Separate Step

The headline is not a summary of the article. It's a promise — the specific promise that earns Marcus's 30 seconds of attention before he decides whether to read. A headline written after the draft tends to summarize; a headline written before the draft tends to promise. The promise is what opens the email.

The subheadline (Substack deck line) does different work: it adds enough context to turn the promise into a commitment. Together, they answer: "Why should I read this right now?"

---

## The Process

### 1. Review the Approved Outline

Before writing headlines, confirm:
- What is the dominant viral trigger?
- What template is being used?
- What is the single most surprising or valuable claim in the outline?
- What would Marcus forward to someone — what's the shareable core?

The headline should be built around the shareable core, not the topic.

### 2. Draft 3 Headline Options

Each option should use a different hook structure. Pick 3 from:

**A. Borrowed Frame**
Use a recognizable reference — a quote, a familiar phrase, a cultural touchstone — and recontextualize it. The reader recognizes the frame and is surprised by where it goes.

> "The IOU That Broke the Memory Market"
> "The Fed's Inventory Management Problem"

**B. Premise + Implication**
Two-part structure: state the fact, then the implication nobody is saying. Can be done in one line with a colon or dash.

> "RAM Prices Won't Fall: Five Forces Holding the Floor"
> "The Shutdown That Blinded the Fed"

**C. Compressed Narrative**
A complete story arc in a single phrase. The headline IS the argument, compressed.

> "How Apple Bought South Korea's Memory Supply From a Hotel Lobby"
> "One Side Brought a Policy Paper to a Meme War"

**D. The Question That Contains Its Answer**
A rhetorical question where the asking is also the indictment. Use sparingly — Marcus is skeptical of question headlines.

> "If the Fed Can't See the Data, Who's Flying the Plane?"

### 3. Draft Matching Subheadlines

For each headline, write a subheadline (the Substack deck) that:
- Adds context the headline deliberately omitted
- Earns the click without overpromising or giving away the whole argument
- Is 1-2 sentences, conversational, specific
- Doesn't repeat the headline's language or frame

The subheadline is where you can name the template's scope:

> *Five supply-side forces are conspiring to keep DRAM expensive through 2027. The biggest one isn't demand — it's geopolitics.*

> *A 10-point peace plan has two versions. Only one of them mentions uranium enrichment.*

### 4. Run the Tests

For each headline + subheadline pair:

**Signal test** — Does this promise something Marcus couldn't find easily himself? If the headline could appear on three other newsletters, it's not specific enough.

**Send test** — Would Marcus forward just the headline to someone? (Not the article — just the headline in a text message.) If the headline alone makes someone curious, it's working.

### 5. Make a Recommendation

State which option you'd pick and why — one sentence, anchored to Marcus. Example:

> "Option B is strongest because the premise-implication structure mirrors how Marcus actually processes information: fact, then 'wait, what does that mean?' The subheadline gives him just enough to commit."

---

## The Headline Hit List (Never Do This)

These patterns are specifically wrong for the Substack audience Marcus represents — intelligent writer-readers who reject clickbait:

- **Numbered list titles** ("7 Things About X") — overused and fatiguing on Substack. Reserve numbers for when the count is genuinely informational (e.g., "Five Forces" where the count IS the argument).
- **Power words** ("shocking," "amazing," "jaw-dropping," "mind-blowing") — these weaken rather than strengthen. If you have to tell the reader it's shocking, it wasn't shocking enough.
- **Teaching words** ("secrets," "tricks," "hacks," "masterclass") — feel like clickbait and damage credibility with this audience.
- **Misleading "you" framing** — only use "you" if the content genuinely addresses the reader's situation, not the writer's.
- **The journalism who/what/where/why format** — designed for opening paragraphs, not titles. Puts too much information in the wrong place.
- **AI hit-list phrases in headlines** — "Navigating," "Delving Into," "A Deep Dive," "Unpacking," "Everything You Need to Know About."
- **Vague theme headlines** ("The Future of Money," "Power and Technology") — these are topics, not promises. Marcus needs to know what specific claim or insight he's getting.
- **Question marks on every headline** — one question headline per 5-6 articles maximum. Overuse signals the writer doesn't have an answer.

---

## Output Format

```
## Headline Options for: [Working Title from Outline]

**Trigger:** [from outline]
**Shareable core:** [the single most valuable claim, in one sentence]

---

### Option A: [Hook Structure Name]

**Headline:** [headline text]
**Subheadline:** [subheadline text]

*Signal: [pass/fail + brief note] | Send: [pass/fail + brief note]*

---

### Option B: [Hook Structure Name]

**Headline:** [headline text]
**Subheadline:** [subheadline text]

*Signal: [pass/fail + brief note] | Send: [pass/fail + brief note]*

---

### Option C: [Hook Structure Name]

**Headline:** [headline text]
**Subheadline:** [subheadline text]

*Signal: [pass/fail + brief note] | Send: [pass/fail + brief note]*

---

**Recommendation:** [which option and why — one sentence, anchored to Marcus]
```

**Stop after presenting options.** Wait for the user to select or redirect before proceeding to drafting.

---

## Reference Files

- `references/voice-rules.md` — Full voice and style reference: punctuation, rhythm, words to love/avoid, model sentences, the AI hit list
