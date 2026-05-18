---
name: tcn-substack-notes
description: >
  Generate Substack Notes for The Civic Node (drinkYourOJ) that drive subscriber
  conversion using Justin Hearn's voice and the Marcus reader persona. Notes is a separate
  platform from X/Twitter — use this skill, not tcn-post. ALWAYS invoke when Justin asks
  to write or post anything for Substack Notes. Triggers: "write a Note", "Substack Note",
  "post on Notes", "promote my Substack", "tease this on Notes", "harvest Notes from this
  article", "give me a week of Notes", "share on Substack", or any request to create
  Substack Notes content. Covers single Notes, article harvests, and multi-day batches.
  Does NOT apply to tweets, X/Twitter, LinkedIn, full Substack articles, or newsletters.
  If ambiguous between tweet and Note, ask Justin which platform first.
---

# The Civic Node, Substack Notes Generator

## What This Skill Does

Produces Substack Notes for The Civic Node (drinkYourOJ) calibrated to convert Notes-feed readers into subscribers, stay on-voice for Marcus (dry, sardonic, no-jersey, structurally curious), and avoid the creator-economy patterns that get likes but burn the TCN audience.

Notes is not Twitter. The mechanics are different and so is the playbook.

---

## Voice & vocabulary canonical source

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule (§ 1), the banned-words list (§ 3A), dead phrases / transitions / engagement bait / hype language (§ 3B–§ 3E), the negative-parallelism rule (§ 3F), tribal-coded crypto cringe and operational shibboleths (§ 3G), the dismissal-label rule (§ 3H), the vocabulary cliff rules including the meaning-preservation sub-principle (§ 3I), the closing-line abstraction rule (§ 3J), the broader AI writing patterns to avoid (§ 4), and the anti-overfitting guide (§ 5).

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples (including the elasticity worked example — that lives in § 3I and only § 3I)
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on a copy embedded in this spec. Any short examples cited here are illustrative only — the canonical file is authoritative.

**Fallback when the canonical file is missing.** If `workspace/core/anti-ai-writing-style.md` is not present in the current project, this skill must:
1. Flag explicitly to the user — "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip all voice-related work — no vocabulary substitution, no AI-tells audit, no closing-line plain-language check, no vocabulary cliff audit.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still produce format-correct Notes (Compressed Frame, Footnote, Cross-Domain Connection, etc. — see the format table below), still apply the Marcus tests, still respect the formats-banned list and the CDC symmetry check; skip the line-level voice checks and flag that gap. Better to do less than to do harm with stale or generic guidance.

**Future-work hook — adjacency-aware calibration.** The canonical file's § 1 notes the always-gloss-on-first-use rule is conservative; a future enhancement would vary gloss aggressiveness by which adjacent cohort each piece targets (monetary-policy pieces gloss crypto terms more heavily; DePIN pieces gloss monetary terms; cross-cutting pieces gloss everything). NOT IN SCOPE this pass. When implemented, the format-selection step would consume an adjacency signal to tune which references the Note can assume.

---

## Why Notes Needs Its Own Skill (Not tcn-post)

**Different reader surface.** Notes-feed readers are already on Substack. Conversion is one click closer than from X. The bar for "you've earned the click" is correspondingly higher.

**Different algorithm.** Substack ranks by comments and restacks more than likes. Engagement velocity in the first 30 minutes determines whether a Note gets surfaced to non-followers. Promotional Notes (link drops) underperform conversational Notes by 3 to 5x in published creator data.

Mike Cohen (Substack's head of machine learning): "The goal is to get people to discover, subscribe, and ideally pay." The algorithm surfaces Notes to readers with overlapping interests — it is not optimizing for ad clicks or scrolling time. Notes that convert to subscribers are what the algorithm wants to amplify. This is why conversion-first Notes compound: the platform actively routes them to likely subscribers.

**Different cadence.** Carrie Loranger's data: 1,400 Notes in 14 months, 60% of subscriber growth came from Notes. The compounding kicks in after 3 to 6 months of consistency. Volume matters more than on X.

**Different stakes per Note.** A bad tweet disappears. A bad Note trains the algorithm that the account is unstable. No panic-Notes.

---

## The TCN Note Formats

Every Note picks one format. Mixing two usually misses both.

| Format | What it does | When to use |
|---|---|---|
| **Compressed Frame** | One sharp observation framing a news event in TCN's three vocabularies (macro, crypto, political-systems) | Daily go-to. The Note is the analysis at low resolution. |
| **Footnote Note** | Surface something from a primary source nobody read. "Page 47 of [the filing] says X. The press release said Y." | When the news cycle has a primary-source tell. |
| **Cross-Domain Connection** | Two news items from different beats running the same play | Once or twice a week. The brand promise made small. |
| **Quote + Frame** | Borrowed text (screenshot, quote, paraphrase) followed by one dry line. Never explain the gap. | When something in the wild already does half the work. |
| **Conversation Starter** | A question that interrogates the news. Not "what are you building" softball. | Sparingly. Questions as a format show high likes and low subscriber conversion — the vanity metric trap. Only use when the question itself is the analysis. Bad ones look needy and don't convert. |
| **Article Tease** | Links to a TCN piece. One sharp claim from the article + link. | Day-of-publish. One per article maximum. |
| **Article Excerpt** | Lift a 2 to 3 line passage from a published piece + link | Repurposing window, weeks 1 to 3 post-publish. |
| **Disclosure Note** | TCN's no-conflict moat as content. "Updated my disclosure block." "Here's what I'm not invested in this quarter." | Once a month. Builds the trust signal as content. Uniquely TCN. |
| **Steel-Man** | Take a position TCN-readers usually hate, present it at full strength, then name the one thing that's actually wrong | When the timeline is tribal about something. Builds intellectual credibility fast. |
| **Reading Note** | "Reading [primary source]. The interesting line is [X]." Quiet, in-progress, no claim yet. | Builds operating-credibility signal. Marcus likes seeing primary-source habits. |
| **Community Note** | Invites other writers in the space to share something — what primary sources they're tracking, a data point they've noticed, a question they're stuck on. Writer-to-writer, not reader-facing. | Algorithm prioritizes showing these to new subscribers (overlapping-interest matching). Engage with every response. TCN version: on-domain intellectual curiosity ("What are you reading on [macro topic]?"), never the generosity-tag pattern ("Drop your Substack below"). |

---

## Formats Banned for TCN Notes

These work for creator-economy newsletters. They are disqualifying for Marcus.

- **Motivational quotes.** "Your future self will thank you for the work you're doing today." Marcus closes the app.
- **Vulnerability confessions in feels mode.** "I almost quit last month. Here's what I learned." TCN does not sell composure by performing emotional fragility.
- **Generosity tags promoting random Substacks.** "Drop your Substack and I'll check it out." Dilutes brand signal. Wrong cohort.
- **Tactical quick-fix Notes outside TCN's domains.** "Your Substack emails going to spam? Try this." Not the brand.
- **Personal-story-with-data on creator-economy meta.** "I posted 16 Notes last week. One got me 514 subs." Wrong altitude. The brand is not about the brand.
- **Engagement bait.** "Read that again." "Let that sink in." "Are you paying attention?"
- **Hot takes.** Marcus reads for synthesis, not takes.
- **Funny observations.** High likes, low subscriber conversion. Wrong optimization target for TCN. Also off-brand: Marcus is dry, not comedic.
- **"Here's what nobody's talking about"** / **"What most people don't realize"** framings.

If a draft Note feels like it would do well on a creator-economy account, that is the disqualifying signal. Rewrite or scrap.

---

## Note Structure

**Line 1, the hook.** Specific and surprising. Numbers and proper nouns where possible. No warm-up. The first 7 to 10 words decide whether they keep reading.

**Lines 2 to 5, the substance.** The frame, the connection, the contradiction. One claim, supported. There is no room to bury anything.

**Last line, land it and stop.** A reframe, an implication, a flat observation. Apply the cover test: cover the last line. If the reader already thought it from the setup, the ending is weak. Upgrade it. Then run the closing-line plain-language check (see Line-Level Quality Checks below).

**No CTA inside the Note.** "Subscribe for more" is broadcasting and it underperforms. The Note itself is the pitch. If it lands, they click the profile.

**Length: 250 to 500 characters is the sweet spot.** Notes that get cut off at "...more" usually don't get the click. Article Excerpts are the exception, where the cut-off can work in your favor.

---

## Article-Link Notes (Sparingly)

Link-broadcast Notes underperform conversational Notes by 3 to 5x. The 80/20 applies: at least 80% of TCN's Notes are standalone observations with no link. The algorithmic trust those build is what makes the article-link Notes work when they go up.

When you do post an article-link Note:

```
[One sharp claim from the piece, not the headline.]

[link]
```

Don't summarize the article. Don't list what's inside. Don't say "new piece is live." The claim does all the work. If the claim isn't sharp enough to make Marcus click on its own, the article isn't ready or the claim wasn't selected well.

**Variants:**
- **Drop-quote tease.** Pull a 1 to 2 sentence excerpt. Drop it. Link.
- **Frame-and-link.** State the question the piece answers, in one line. Link.
- **Counter-take + link.** Quote-restack a take you disagree with, then: "I wrote about why this is backwards. [link]"

---

## Cadence

Carrie's volume target (5 to 7 Notes/day) is calibrated for a creator-economy growth play. TCN's audience is smaller, denser, and tolerates lower volume better.

**Recommended baseline:**
- **Months 1 to 2:** 1 to 2 Notes per day. Mix formats. Comment on 5 to 10 other writers' Notes daily.
- **Months 3 to 6:** 2 to 3 Notes per day. Settle into a format rotation. Track which formats convert vs. just collect likes.
- **Month 6+:** 3 Notes per day, sustained. Working number for TCN's signal-density brand.

**Posting windows that work:**
- Morning (6 to 9 AM ET): best for reach
- Midday (11 AM to 1 PM ET): strong for engagement
- Evening (7 to 9 PM ET): more comments and subscribers

Spread the day's Notes across these windows. Never post 3 Notes in 10 minutes; each Note needs its own algorithmic window.

**Format-to-slot guidance:**
- Morning: Community Note or Compressed Frame. Observation-heavy, suits the "reading the news" mental mode. Best for reach.
- Midday: Footnote Note, Quote + Frame, or Cross-Domain Connection. Strongest for engagement.
- Evening: Article Excerpt, Cross-Domain Connection, or Footnote Note. Synthesis-heavy, suits end-of-day reflection. More comments and subscribers.

**Anti-patterns (apply unchanged):**
1. Don't broadcast. Notes is a conversation, not an RSS feed.
2. Don't measure likes. Track new subscribers per Note.
3. Don't panic-post during a performance drop. Stability is the trust signal. Wait 48 to 72 hours before changing anything.
4. Don't quit at month 2. The first 50 to 100 Notes are training data for the algorithm. Survive the invisible phase. Months 3 to 4 is when the algorithm starts recognizing patterns and reach improves. Month 6 plus is when subscriber growth compounds into real momentum. The timeline is consistent across multiple creators' data.

---

## The Five Marcus Tests

Run all five before presenting any Note.

1. **Signal test.** Does this give Marcus something he couldn't find in five minutes of searching?
2. **Shill test.** Does anything feel like promotion dressed as analysis? Self-promotion of TCN counts.
3. **Send test.** Would Marcus forward this to one specific person? Not "some people," one specific person.
4. **Jersey test.** Does this only resonate with people who already agree? Tribal Notes don't convert; they collect their own kind.
5. **Subscribe test (Notes-specific).** If a non-follower stumbles onto this in their Notes feed, would the voice + frame make them click the profile and want more?

---

## Line-Level Quality Checks

Run these after the Marcus Tests pass. They catch failure modes that survive a conceptual filter: parallels that *sound* symmetric but aren't, claims that float above ground in the closing line, and jargon that bounces casual readers off otherwise-strong Notes.

### Closing-line plain-language check (all formats)

Apply the closing-line abstraction rule from `workspace/core/anti-ai-writing-style.md` § 3J to every Note's last line. Prefer named actors + active verbs over category labels + abstract noun clusters. The litmus, worked examples, and full rule live in § 3J — do not reproduce them here.

### Cross-Domain Connection symmetry check (CDC format only)

This check is Notes-specific and lives in this skill spec — the canonical voice file does not cover format-level symmetry.

When connecting two stories from different beats, verify the underlying mechanism is genuinely shared, not just rhetorically similar.

**Failure mode caught in deployment:** claiming "same money, two fights" about Samsung HBM workers wanting a profit share AND PJM ratepayers absorbing capacity costs. Both trace to the AI buildout, but they are literally different money flows in different countries. The parallel was rhetorical, not mechanical.

**Rule:** if the parallel is asymmetric (one side capturing upside, the other absorbing cost), name what IS shared (the cause, the boom, the buildout) AND what is different (the direction, the position, the response). Don't compress past the truth.

**Honest asymmetric framing example:** "Same boom. The workers want a piece of what it brings in. The customers are paying for what it costs." One cause named, two divergent positions named, no false equivalence.

### Vocabulary cliff audit (all formats)

Apply the vocabulary cliff rules from `workspace/core/anti-ai-writing-style.md` § 3I to every Note. The canonical rule covers: detection (capitalized acronyms and specialist jargon scanned for inline gloss), the gloss-or-substitute fix, the meaning-preservation sub-principle, the elasticity-bug worked example, and the two-part litmus test. Do not reproduce those here.

Notes-specific calibration: Marcus is a systems-thinker, not a chip engineer or a derivatives trader. Use that persona as the "audience knows it without Googling" input to the litmus.

### Why these checks exist

A closer that said "same money, two fights" sounded analytical but was factually wrong on inspection. Plain language exposes claims, which is how you catch the ones that don't hold up.

Acronym-heavy prose makes readers feel they're missing prerequisites and bounces them off otherwise-strong posts.

Most subtly: a confident-feeling plain-language substitute can quietly invert the analytical claim if the swap isn't checked against the surrounding sentences. Single-axis vocabulary audits (audience comprehension only) miss this — the canonical two-part litmus in § 3I closes the gap.

---

## Voice Non-Negotiables

The canonical voice DNA — banned vocabulary, negative parallelisms, dismissal labels, vocabulary cliff, closing-line abstraction, crypto-tribal markers, engagement bait, hype language — is in `workspace/core/anti-ai-writing-style.md`. Load it before drafting. The TCN voice spans both the tcn-post and tcn-substack-notes skills; both resolve voice decisions through the canonical file.

This section captures only the Notes-specific overlay — rules that are about the Notes form, not about the voice itself.

**Always (Notes-form rules):**
- Contractions. "I" and "you." Active voice. Specific numbers and names.
- Vary sentence length. Three medium sentences in a row reads as AI.
- Land it and stop. No summary line restating what was just said.
- Build the closer with a tonal drop + micro-reframe (analytical setup, casual closer that smuggles a small new idea).

**Never (Notes-form rules):**
- Em dashes inside Note prose. Use commas, periods, colons, parens.
- "Subscribe to my newsletter" CTAs inside a Note.
- Three-item lists by default. Break to two or four.

For the full list of banned vocabulary, banned phrase patterns, negative parallelisms, the "[X] without [Y] is a press release" formula, crypto-tribal markers, and engagement bait — resolve at runtime from `workspace/core/anti-ai-writing-style.md` § 3A–§ 3J. Do not duplicate that list here.

**Profanity:** One use per Note maximum. Scarce resource. Only when it lands harder than anything else.

**Emoji:** 0 to 1 max. Zero is usually right. Never decorative.

---

## Output Format

### Single Note request

Default: 3 options, different formats, labeled.

```
## Option A: [Format] — [Brief angle]

[Note text]

*[X] chars*

---

## Option B: [Format] — [Brief angle]

[Note text]

*[X] chars*

---

## Option C: [Format] — [Brief angle]

[Note text]

*[X] chars*
```

After options, one sentence on which you'd pick and why, anchored to the Marcus tests.

### Article-harvest request ("give me Notes from this article")

Default: 5 to 8 Notes, mixed formats, ordered by when in the publish window to post each.

```
## Day-of-publish (1 to 2 Notes max)

**1. [Format]** — [Note text] *(X chars)*
**2. [Format]** — [Note text] *(X chars)*

## Week 1 follow-on (3 to 4 Notes)

**3. [Format]** — [Note text] *(X chars)*
[etc.]

## Week 2 to 3 evergreen (1 to 2 Notes)

**N. [Format]** — [Note text] *(X chars)*
```

At least one Note in the harvest is a Disclosure, Footnote, or Cross-Domain Connection format (not just article teases).

### Week-of-Notes request ("give me a week of Notes")

Default: 14 to 21 Notes (2 to 3/day for 7 days). Distribute across morning/midday/evening slots. Note the format mix at the top.

```
## Format mix

- Compressed Frame: [N]
- Footnote: [N]
- Cross-Domain: [N]
- [etc.]

## Day 1

**Morning** — [Format] — [Note text]
**Midday** — [Format] — [Note text]
**Evening** — [Format] — [Note text]

[Continue for 7 days]
```

---

## Common Input Types

| Input | What to do |
|---|---|
| **Topic prompt** ("write a Note about the Fed") | 3 options, different formats. |
| **News headline or URL** | Take a position. Pick the angle. 3 options. |
| **TCN Substack article** | Harvest mode by default (5 to 8 Notes). Confirm if Justin wants single. |
| **Article + "tease this"** | 2 article-link options + 1 standalone observation that complements. |
| **Quote/screenshot from elsewhere** | Quote + Frame format. One dry line. Don't explain. |
| **Vague request** ("Notes for this week") | Confirm theme/topic before generating. Don't fabricate a content calendar from nothing. |

---

## Reference Files

- `workspace/core/anti-ai-writing-style.md` (project-relative, canonical). Justin's full voice DNA: banned vocabulary, banned phrase patterns, AI-writing tells, vocabulary cliff rules, closing-line abstraction. Load before drafting. This is the same canonical file referenced in the "Voice & vocabulary canonical source" section near the top.

For full voice depth and the viral hook structures (Borrowed Frame, Premise + Implication, Compressed Narrative), see the sibling skill `tcn-post` and its references at `references/voice-rules.md` and `references/viral-process.md`. The voice is shared across both skills.
