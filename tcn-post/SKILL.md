---
name: tcn-post
description: >
  Generate social media posts and tweets for The Civic Node (drinkYourOJ) using Justin Hearn's
  voice, the Marcus reader persona, and the Civic Node viral post process. This is the correct skill
  for all Civic Node social content — it supersedes oj-tweets. ALWAYS invoke this skill when the
  user asks to write tweets, social posts, or threads for The Civic Node — including phrases like
  "write me a tweet", "post about X", "tweet about X", "give me a thread", "react to this on
  Twitter/X/LinkedIn/Facebook", "turn this into a tweet", "social post for the civic node",
  "drinkYourOJ tweet", or any request to create social media content for this brand on any platform.
  Also trigger when the user pastes a news headline, Substack article, or topic and says anything
  suggesting they want a social post. Covers single tweets, tweet options, tweet threads, and
  LinkedIn posts. Does NOT apply to full Substack articles, email newsletters, or hashtag research.
---

# The Civic Node — Social Post Generator

## What This Skill Does

Produces single tweets, tweet options, or tweet threads for The Civic Node (drinkYourOJ) that are
calibrated to go viral with Marcus — the ideal reader — by applying Justin's voice, the five viral
triggers, and the five Marcus tests before any output leaves the draft.

Load `references/viral-process.md` if you need the full five-step process with detail.
Load `references/voice-rules.md` if you need this skill's voice-rules reference (post-specific rhythm, hook structures, character-limit pressure rules). Banned vocabulary, negative-parallelism rules, vocabulary cliff, and closing-line abstraction live in the canonical voice file — see next section.

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
2. Skip all voice-related work — no vocabulary substitution, no AI-tells audit, no closing-line check.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still produce options labeled by viral trigger, hook structure, frame-forward / data-forward durability, and exact character counts; skip the voice non-negotiables enforcement and flag that gap in the meta-commentary. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The canonical file's § 1 notes the always-gloss-on-first-use rule is conservative; a future enhancement would vary gloss aggressiveness by which adjacent cohort each piece targets (monetary-policy pieces gloss crypto terms more heavily; DePIN pieces gloss monetary terms; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, the trigger-selection / angle-labeling step would consume an adjacency signal to tune which references the post can assume.

---

## The Viral Triggers (choose one per post)

Before writing anything, identify which trigger you're aiming for. Each maps to a different structure.

| Trigger | What it does | Share driver |
|---|---|---|
| **Precision Gift** | Articulates what Marcus was thinking but couldn't say | Recognition + mild embarrassment |
| **Early Warning** | Names a structural shift before it's obvious | Fear of being late |
| **Named Hypocrisy** | Names something broken with surgical dryness | Validated frustration |
| **Devastating Compression** | Reduces a complex thing to one brutal sentence | Amusement + the sentence itself |
| **Unexpected Connection** | Two domains, revealed as the same problem | Surprise → "obviously" |

Pick one. Posts that try to hit two usually miss both.

---

## Frame-Forward vs. Data-Forward (durability axis)

A second axis, applied independently of the trigger. Every X standalone option should be labeled with one of these two:

- **Frame-forward** — structurally durable. References things that have already happened or structural conditions that hold regardless of which way the news breaks. Survives any direction the story takes. Default-safe pick when the news is still developing or undetermined.
- **Data-forward** — sharper, more news-cycle-dependent. Rides a specific confirmation, deadline, or near-future outcome. Ages fast if that direction doesn't materialize. Stronger when the take is *right*; embarrassing when it isn't.

**Rule:** Every X standalone slot produces **at least one frame-forward option** as the default-safe pick. When the news is genuinely undetermined, frame-forward beats data-forward — even when the data-forward version reads sharper. A post that names a structural condition will still be true tomorrow; a post that bets on a specific resolution might not.

Lesson from real use: a 60-word standalone referencing "today's mediation" had to be tweaked when the mediation got extended. Trimming the same post to fit a 268-character cross-platform limit naturally dropped the time-fragile clause and ended up more durable than the longer original. Character pressure is a forcing function for stripping decorative specificity — usually the time-stamped kind.

---

## The Five-Step Process (condensed)

**Step 1 — Mine the spark.** Don't start writing; start listening. Find the take getting 3K likes that Marcus knows is wrong, the debate where both sides are describing symptoms but nobody named the structure, or the pattern that just got publicly confirmed.

**Step 2 — Choose the emotional architecture.** Pick your trigger (table above). This determines structure, tone, and where the floor blows out.

**Step 3 — Build the hook.** Four structures work for this voice:

- **Borrowed Frame** — Quote/screenshot/paraphrase something real. Follow it with one dry line. Never explain the gap.
- **Premise + Implication** — Two sentences. The first is real. The second is the implication nobody is saying.
- **Compressed Narrative** — A complete situation in one or two sentences, floor blows out at the end.
- **Rhetorical Question** — The question that already contains the indictment. Use sparingly.

**Step 4 — Execute and stop.** Write the post. Stop earlier than feels comfortable. If the ending needs explanation, the observation wasn't sharp enough — fix the observation, not with more words.

**Step 5 — Run the Marcus tests** (see below). Pass all five before outputting.

**Step 6 — Cross-platform character check (every X standalone).** Count exactly. Verify the draft is ≤280 (Twitter ceiling) and note whether it also fits ≤300 (Bluesky ceiling). Surface the count in the meta-commentary (e.g., "268 chars; fits Twitter and Bluesky"). If a draft is over 280, the first trim targets are time-specific operational detail — dates, mediation timelines, "today" / "this week" / "yesterday" qualifiers, named deadlines — **not** the structural frame. Character-limit pressure is a feature: trimming to fit ≤280 should first cut time-specific operational detail. If the structural frame survives the trim, the post is more durable as a result, not less.

---

## The Five Marcus Tests

Apply these internally before presenting any output. State which tests each option passes if useful.

1. **Signal test** — Does this give Marcus something he couldn't find in five minutes of searching?
2. **Shill test** — Does anything feel like promotion dressed as analysis? Check for unexamined enthusiasm, superlatives, "revolutionary."
3. **Send test** — Would Marcus forward this to one specific person he knows? (Not "some people" — one specific person.) If no, identify why: too tribal, too surface-level, too familiar, too vague.
4. **Jersey test** — Does this feel like a team jersey (tribal) or genuine analysis? If it only resonates with people who already agree, it won't spread.
5. **90-second test** — If this is conversion-oriented, is the value case legible in a single read? (Skip for pure analytical posts.)

---

## Voice Non-Negotiables

These are hard rules specific to the X / Twitter / Bluesky post form. The full banned-vocabulary list, dead phrases, negative-parallelism rule, and vocabulary cliff rules are canonical — see `workspace/core/anti-ai-writing-style.md` § 3A–§ 3J. Do not duplicate that list here; resolve specific phrases at runtime from the canonical file.

**Never:**
- Explain the joke. Ever. If it needs explanation, rewrite the observation.
- Use em dashes closed (`—word—`). Spaced em dash only, and rarely.
- Use any banned phrase from `workspace/core/anti-ai-writing-style.md` § 3A–§ 3E or any negative-parallelism construction from § 3F.
- Use the "[X] without [Y] is a press release" formula — formula dressed as insight. No matter what fills X and Y, it reads as a cliché.
- Add one more sentence after the punchline lands. When it lands, stop.
- Use ragebait. It attracts the wrong people.
- Use patterns of exactly three items in every list (the AI default — break it to two or four).

**Always:**
- The ending must earn its spot. Apply the Cover Test: cover the last sentence. If the reader already thought it from the setup, the ending is weak — upgrade it, don't remove it.
- The closer needs a **tonal drop** (casual vs. the analytical setup) AND a **micro-reframe** (one small new idea — a label, redirect, or reframe). Pure tone shift without a new idea is sarcasm without a payload.
  - ✓ "That's a franchise with a whitepaper." — tonal drop + reframes the whole incentive structure
  - ✓ "You were the loading screen." — tonal drop + reframes the worker as transitional UI state
  - ✗ "Sure." — tone only, no new idea
- Go for the second thought, not the first. The first punchline is the one everyone thinks of. Find the more specific image, the unexpected comparison.
- Specific over general: names, numbers, companies. "Salesforce charges $2K/seat" beats "enterprise software is expensive."
- Short sentences hit harder. Build complexity in longer sentences; land the point in a short one.
- **For closing lines on X posts: prefer named actors + active verbs over category labels + nominalizations.** Concrete subjects doing concrete things land harder than abstract categories performing abstract actions.
  - ✗ Avoid: "two layers of the AI supply chain are simultaneously asking who has pricing authority over the windfall."
  - ✓ Prefer: "the workers want a piece of what it brings in; the customers are paying for what it costs."
  - The first version describes a phenomenon; the second shows people acting. Marcus feels the second one.

**Profanity policy:** One use per post maximum, treated as a scarce resource, only when it hits harder than anything else.

**Emoji policy:** 0-2 max. Zero is usually right. Never decorative.

---

## The Tonal Drop + Micro-Reframe (the most important humor principle)

The laugh lives in the gap between an analytical setup and a casual, slightly bored closer. But the closer has to contain one small new idea — a label, redirect, or reframe. Without it, you've changed tone without adding anything.

Study the pattern:
- Setup: analytical, specific, building. Closer: two to five words, tossed off, almost bored — but smuggling a tiny reframe inside them.
- "Awkward business model." — labels it a business model, reframes the entire industry's incentives
- "They noticed." — adds acknowledgment, which makes the startup thesis look even more doomed
- "Consistent, I'll give them that." — mock-generous, reframes incompetence as an achievement

The cover test: cover the last line. Re-read the setup. If you already thought the ending, upgrade it.

---

## Output Format

**For a single tweet or when user asks for "a tweet":**
Always generate 3 options unless the user specifies otherwise. Label each by trigger type, angle, AND durability mode (frame-forward / data-forward). At least one option must be frame-forward.

```
## Option A: [Trigger Type] — [Brief angle label] — [frame-forward | data-forward]

[tweet text]

*[X] chars; fits Twitter (≤280) [and Bluesky (≤300) | — exceeds Bluesky]*

---

## Option B: [Trigger Type] — [Brief angle label] — [frame-forward | data-forward]

[tweet text]

*[X] chars; fits Twitter (≤280) [and Bluesky (≤300) | — exceeds Bluesky]*

---

## Option C: [Trigger Type] — [Brief angle label] — [frame-forward | data-forward]

[tweet text]

*[X] chars; fits Twitter (≤280) [and Bluesky (≤300) | — exceeds Bluesky]*
```

After the three options, briefly state which you'd pick and why — one sentence, anchored to the Marcus tests. If the news is still developing or undetermined, default to a frame-forward option and say so.

**For a thread:**
```
## Thread: [topic]

**1/** [hook — most provocative claim]

**2/** [supporting point]

**3/** [supporting point]

...

**N/** [close — implication or CTA]

---
*Tweets: [count] | Longest: [X]/280*
```

**Character counting:** Count exactly. Never estimate. 250-270 is the sweet spot; 275+ is the danger zone where the limit forces you to compromise the ending.

---

## Platform Calibration

**Twitter/X:** Maximum compression. Borrowed text preferred where available. One to three parts. Deadpan. The voice profile calls this the Benn Eifert model: quiet setup, borrowed text does the work, observation lands dry, never explain.

**LinkedIn:** Same voice, one more sentence of scaffolding. Never one-sentence-per-paragraph. Prose only.

**Substack Notes:** Can carry more analytical weight than a tweet. Good for Precision Gift and Unexpected Connection triggers. Functions best as a compressed version of a full argument — the seed before the article.

---

## Input Types

| Input | What to do |
|---|---|
| **Topic prompt** | Generate 3 options with different triggers. Label each. |
| **News headline or article** | Take a position. Don't report — say what it means and why the conventional take is wrong. |
| **Substack repurpose** | Extract the 1-2 sharpest claims. Don't summarize. Build around those. |
| **Original take** | Identify which trigger fits, apply the hook structure, execute. |

---

## Reference Files

- `references/viral-process.md` — Full five-step process with extended detail on topic mining, emotional architecture, and platform calibration
- `references/voice-rules.md` — Complete voice reference including Justin's punctuation philosophy, sentence rhythm, words he loves/hates, and the model sentences

Load these when you need more depth than the condensed versions above provide.
