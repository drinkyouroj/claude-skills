---
name: blog-headline
description: >
  Step 3 of the blog article workflow: headline and subheadline generation from an
  approved outline. Invoke this skill when the user has an approved article outline and wants to
  move to headlines — including phrases like "write the headline", "give me headlines", "now do
  the headline", "headline options", "title this piece", or when the user approves a blog-outline
  output and asks what's next. Does NOT apply to social media posts, or drafting (that's blog-draft).
---

# Blog Headline Generator (Step 3 of the blog-pipeline)

Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else.
Loads: `identity.md`, `reader.md`, and the active preset.

## What This Skill Does

Produces 3 headline + subheadline options for a blog article, calibrated to the blog's reader persona and tested against the signal and send tests. The user selects one before drafting (`blog-draft`) begins.

Load the active profile's `voice.md` for this skill's headline-form voice and style reference. Banned vocabulary, negative parallelisms, vocabulary cliff, and closing-line abstraction live in that canonical voice file — see next section.

---

## Voice & vocabulary canonical source

This skill MUST load the active profile's `voice.md` (resolved via the resolution contract) before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule (§ 1), the banned-words list (§ 3A), dead phrases / transitions / engagement bait / hype language (§ 3B–§ 3E), the negative-parallelism rule (§ 3F), tribal-coded jargon and operational shibboleths (§ 3G), the dismissal-label rule (§ 3H), the vocabulary cliff rules including the meaning-preservation sub-principle (§ 3I), the closing-line abstraction rule (§ 3J), the broader AI writing patterns to avoid (§ 4), and the anti-overfitting guide (§ 5).

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on a copy embedded in this spec. Any short examples cited here are illustrative only — the canonical file is authoritative.

**Fallback when the voice file is missing.** If the active profile's `voice.md` is not present, this skill must:
1. Flag explicitly to the user — "no voice file found; skipping voice calibration."
2. Skip all voice-related work — no AI-hit-list cross-check on candidate headlines.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions.
4. Continue with non-voice work this skill can still do: still produce 3 headline + subheadline options using the four hook structures (Borrowed Frame, Premise + Implication, Compressed Narrative, Question That Contains Its Answer), still apply the headline-specific anti-patterns (numbered lists, power words, teaching words, vague theme headlines, question-mark overuse), still run the Signal and Send tests. Flag "voice rules pass" as not enforced in the recommendation. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The canonical voice file may note an always-gloss-on-first-use rule that is conservative; a future enhancement would vary gloss aggressiveness by which adjacent cohort each piece targets. NOT IN SCOPE this pass. When implemented, the hook-structure selection step would consume an adjacency signal — pieces targeting a wider cohort lean toward hooks that don't assume insider vocabulary; pieces targeting a denser cohort can use compressed-narrative headlines with domain shorthand.

---

## Why Headlines Are a Separate Step

The headline is not a summary of the article. It's a promise — the specific promise that earns the reader's 30 seconds of attention before they decide whether to read. A headline written after the draft tends to summarize; a headline written before the draft tends to promise. The promise is what opens the email.

The subheadline (the blog platform's deck/subtitle line) does different work: it adds enough context to turn the promise into a commitment. Together, they answer: "Why should I read this right now?"

---

## The Process

### 1. Review the Approved Outline

Before writing headlines, confirm:
- What is the dominant angle/hook?
- What structure/template is being used?
- What is the single most surprising or valuable claim in the outline?
- What would the reader persona forward to someone — what's the shareable core?

The headline should be built around the shareable core, not the topic.

### 2. Draft 3 Headline Options

**Hard length constraint**: every headline must be **under 60 characters** (including spaces, excluding the subheadline). Most blog platforms and email clients truncate longer titles in feed cards and email subject lines; over 60 reliably loses the back half of the promise where it matters most. Count characters before presenting any option — if a candidate runs long, tighten or cut before it reaches the user. This is not advisory; it is a pass/fail gate.

If `quick.platform` or `identity.md` specifies a different character ceiling for the active platform, use that platform-specific limit instead.

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
A rhetorical question where the asking is also the indictment. Use sparingly — the reader persona tends to be skeptical of question headlines.

> "If the Fed Can't See the Data, Who's Flying the Plane?"

### 3. Draft Matching Subheadlines

For each headline, write a subheadline (the blog platform's deck/subtitle line) that:
- Adds context the headline deliberately omitted
- Earns the click without overpromising or giving away the whole argument
- Is 1-2 sentences, conversational, specific
- Doesn't repeat the headline's language or frame
- **Is under 160 characters** (including spaces). This is a hard constraint — most platform deck rendering and email preview truncate longer lines, and the second sentence is where the back-half clarification often lives. Count characters before presenting any option; if a candidate runs long, tighten before the user sees it.

If `quick.platform` or `identity.md` specifies a different character ceiling for the active platform's deck line, use that platform-specific limit instead.

The subheadline is where you can name the article's scope:

> *Five supply-side forces are conspiring to keep DRAM expensive through 2027. The biggest one isn't demand — it's geopolitics.*

> *A 10-point peace plan has two versions. Only one of them mentions uranium enrichment.*

### 4. Run the Tests

For each headline + subheadline pair:

**Length check** — Headline must be under 60 characters (or the platform-specific limit from `identity.md` / `quick.platform`); subheadline must be under 160 characters (or the platform-specific limit). Report the exact count for both in every option so the user can see the budget at a glance. Any option that exceeds either ceiling must be revised before presentation — never present an over-length option and ask the user to choose; that wastes their attention on a candidate the platform will truncate. If a strong hook genuinely cannot fit under the ceiling, flag the constraint as the binding one and offer a tightened variant.

**Signal test** — Does this promise something the reader persona couldn't find easily elsewhere? If the headline could appear on three other publications in this domain, it's not specific enough.

**Send test** — Would the reader persona forward just the headline to someone? (Not the article — just the headline in a text message.) If the headline alone makes someone curious, it's working.

### 5. Make a Recommendation

State which option you'd pick and why — one sentence, anchored to the reader persona. Example:

> "Option B is strongest because the premise-implication structure mirrors how the reader persona actually processes information: fact, then 'wait, what does that mean?' The subheadline gives them just enough to commit."

---

## The Headline Hit List (Never Do This)

These patterns are specifically wrong for the reader persona this blog serves — intelligent, skeptical readers who reject clickbait:

- **Numbered list titles** ("7 Things About X") — overused and fatiguing. Reserve numbers for when the count is genuinely informational (e.g., "Five Forces" where the count IS the argument).
- **Power words** ("shocking," "amazing," "jaw-dropping," "mind-blowing") — these weaken rather than strengthen. If you have to tell the reader it's shocking, it wasn't shocking enough.
- **Teaching words** ("secrets," "tricks," "hacks," "masterclass") — feel like clickbait and damage credibility with this audience.
- **Misleading "you" framing** — only use "you" if the content genuinely addresses the reader's situation, not the writer's.
- **The journalism who/what/where/why format** — designed for opening paragraphs, not titles. Puts too much information in the wrong place.
- **AI hit-list phrases in headlines** — "Navigating," "Delving Into," "A Deep Dive," "Unpacking," "Everything You Need to Know About."
- **Vague theme headlines** ("The Future of Money," "Power and Technology") — these are topics, not promises. The reader needs to know what specific claim or insight they're getting.
- **Question marks on every headline** — one question headline per 5-6 articles maximum. Overuse signals the writer doesn't have an answer.

---

## Output Format

```
## Headline Options for: [Working Title from Outline]

**Angle/hook:** [from outline]
**Shareable core:** [the single most valuable claim, in one sentence]

---

### Option A: [Hook Structure Name]

**Headline:** [headline text] *([N] chars / 60)*
**Subheadline:** [subheadline text] *([N] chars / 160)*

*Length: [pass/fail] | Signal: [pass/fail + brief note] | Send: [pass/fail + brief note]*

---

### Option B: [Hook Structure Name]

**Headline:** [headline text] *([N] chars / 60)*
**Subheadline:** [subheadline text] *([N] chars / 160)*

*Length: [pass/fail] | Signal: [pass/fail + brief note] | Send: [pass/fail + brief note]*

---

### Option C: [Hook Structure Name]

**Headline:** [headline text] *([N] chars / 60)*
**Subheadline:** [subheadline text] *([N] chars / 160)*

*Length: [pass/fail] | Signal: [pass/fail + brief note] | Send: [pass/fail + brief note]*

---

**Recommendation:** [which option and why — one sentence, anchored to the reader persona]
```

**Stop after presenting options.** Wait for the user to select or redirect before proceeding to drafting.

---

## Reference Files

- the active profile's `voice.md` — Full voice and style reference: punctuation, rhythm, words to love/avoid, model sentences, the AI hit list
