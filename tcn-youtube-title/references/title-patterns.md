# Title Patterns

Source of truth for the title drafting step (process step 5, Gate 2) in `tcn-youtube-title`. The skill reads this file at drafting time to surface 3 candidate two-part-stop titles that pass the acceptance criteria in SKILL.md §6.2.

Edit this file directly when banned-list refinements, structural patterns, or anti-pattern observations need to evolve. No skill-code changes required.

## Why a Separate File from Thumbnail Headlines

Thumbnail in-image headlines (`../../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md`) and YouTube titles are two different rhetorical objects:

- **Thumbnail headline** lives *inside* the image. 3–6 words. Visual stop-element. Read in a fraction of a second of scrolling.
- **Title** lives *beside* the thumbnail in the feed. 8–14 words. Search-indexed metadata. Truncated to ~55 chars on mobile, expandable to ~90 on desktop, hard-capped at 100.

The voice anchors are identical. The structural patterns are not. This file owns the title patterns; it cross-links to the thumbnail patterns file for the shared voice/bans content.

## Inheritance from thumbnail-headline-patterns.md

Read at drafting time, do not duplicate:

- **Voice anchors** — Justin Hearn / drinkYourOJ voice. Sentence case. Sardonic, specific, declarative-or-curiosity-gap, never clickbait-shaped. Marcus-reader visiting-friends register.
- **Banned hype adjectives** — SHOCKING, AMAZING, INSANE, EXPOSED, REVEALED, UNBELIEVABLE, MASSIVE, ULTIMATE, EPIC, INCREDIBLE, MIND-BLOWING, GAME-CHANGING. Case-insensitive match.
- **Banned clickbait templates** — "This One Trick…", "What They Don't Want…", "You Won't Believe…", "Here's Why…" (when leading), "The Truth About…" (generic), "Doctors Hate This…", "Number N Will Shock You".
- **Anti-AI-tell tokens** — em-dashes (—), "delve" / "delving", "tapestry", "navigate the landscape", "in the realm of", "it's worth noting", plus any token flagged by the `tcn-text-humanizer` skill's tell list.

If a token or template needs to be banned for *thumbnail headlines too*, edit the shared file. If a ban is *title-specific*, edit this file's "Title-specific bans" section.

## Length budget math

YouTube title constraints (current as of skill creation, verify periodically):

- **Hard ceiling:** 100 characters. YouTube rejects longer titles at the API layer.
- **Soft ceiling:** 90 characters. Above this, the title gets visually truncated in YouTube Studio's preview, the watch-page sidebar, and embedded-share contexts. Warn but allow.
- **Mobile feed truncation:** ~55 characters before the "..." cut. This is the hard rule for the first half of a two-part-stop title — the hook must land before the cut.
- **Desktop feed truncation:** ~70 characters before the "..." cut on standard widths; full title shown on wide layouts.
- **Search results page:** truncation varies by viewport; mobile-safe assumption (~55 chars) generalizes.

### First-half budget: ≤55 chars including its terminal period

Why 55 and not 60: YouTube's mobile feed truncation point varies slightly by device width (iPhone SE / mid-Android narrower than Pixel Pro / iPhone Pro Max). The 55-char ceiling guarantees the first half lands on the narrowest mainstream device. The 5-char buffer also leaves room for the period itself plus a single space if YouTube ever shifts the cut.

### Second-half budget: total title 35–55 chars after the first half

This works out to 35 chars when the first half is at its maximum (55), or 55 chars when the first half is shorter (35–40). The second half should be substantial enough to deliver a payoff on desktop expand — single-word twists tend to read as cheap, while phrases ≥4 words let the twist breathe.

### Word count: 8–14 words total

Below 8 words, the two halves typically lack the rhythm and specificity the pattern needs. Above 14 words, the title runs over the 90-char soft ceiling and starts truncating in YouTube Studio preview.

## Punctuation rules

- **Period (default)** between the two halves. Reads as two distinct beats. E.g., `385,000 People Bought a Franchise. Nova Labs Owns the Pricing.`
- **Colon allowed** when the second half *literally defines or extends* the first. E.g., `The Helium Receipt: $949 for a 10-Year Payoff.` The colon must be earned by a literal definition relationship — using it as a generic "here's the twist" connector reads as listicle-shaped.
- **Em-dashes banned** between halves and anywhere else in the title. The em-dash is the strongest single AI-tell token in modern LLM output. Use a period instead.
- **Exclamation points banned.** No exceptions. Voice is dry, not yelling.
- **Question marks allowed sparingly** and only when load-bearing for a genuine curiosity gap, not a rhetorical question. Most dispatches will not use one.

## Two-part-stop structural patterns

The structural shape is always `[Specific Anchor]. [Twist].` The first half carries the search-anchored specific (number, proper noun, place, dollar amount, year); the second half carries the punch.

### Why anchor-first, twist-second

Three reasons:

1. **Mobile truncation safety.** The anchor is more likely to be search-relevant and information-dense; if the second half truncates, the user has still seen the searchable identifier.
2. **CTR mechanics.** The viewer's eye reads left-to-right, and the specific anchor primes the brain to expect a follow-up. The twist landing in position 2 punches harder than the twist landing in position 1 (where the brain doesn't yet have context for the twist to land against).
3. **Pattern coherence with the thumbnail patterns.** The Concrete Anchor + Twist pattern is the strongest thumbnail-headline pattern in the corpus. Reusing the structure at title scale creates a consistent house style across the dispatch's surfaces.

## Mechanism taxonomy

All three Gate-2 candidates use the two-part-stop *structure*. They differ in the *mechanism* the twist runs. Surface three different mechanisms per dispatch to give the user a meaningful pick.

### Authority-Asymmetry

First half describes what the viewer bought / owns / chose; second half names who actually controls the economics, pricing, or rules.

- Strong fit when the dispatch is about ownership-vs-control disjunction (governance capture, hidden franchisor authority, regulatory hand-off).
- Search anchors typically pair: the bought thing + the controlling entity.
- Example: `385,000 People Bought a Franchise. Nova Labs Owns the Pricing.` (Dispatch 004, picked)

### Specific Contradiction

First half states a concrete fact. Second half states an equally concrete contradicting fact. The two halves are in named, fact-checkable tension.

- Strong fit when the dispatch leans on a single sharp numerical or categorical contrast (200 pages vs one word, $125/day vs $56,000/day).
- Often the rhetorically loudest pattern; works on cold viewers who don't know the dispatch's subject.
- Example: `McDonald's Gives You 200 Pages. Helium Gave 385,000 People One Word.` (Dispatch 004 alt)

### Hidden Revenue / Hidden Move

First half describes the visible / marketed / pointed-at side. Second half names where the actual money or power lives.

- Strong fit when the dispatch unmasks a misdirection between what's marketed and what's profitable.
- Search anchor usually the marketed-side name; twist usually carries the dollar figure or percentage.
- Example: `Helium's IoT Side Earns $125 a Day. The Mobile Side Earns $56,000.` (Dispatch 004 alt)

### Completion-Pairing

First half opens a curiosity gap whose answer is *literally the thumbnail in-image headline*. Title and thumbnail compose into one rhetorical move.

- Strongest pairing of all mechanisms — the viewer's eye reads title, registers the gap, and the thumbnail headline fills it in before they click.
- Requires the thumbnail headline to be a short punchline-shaped phrase. Doesn't work when the thumbnail is purely visual identity (no in-image text).
- Use sparingly — overuse turns titles into perpetual setups, and a stand-alone title (without the thumbnail visible) feels incomplete.
- Example: `McDonald's Gives You 200 Pages. Helium Gave 385,000 People One Word.` paired with `Vibes ≠ Disclosure` thumbnail. Title sets up "what one word?"; thumbnail answers.

### Personal-Implication

First half describes the author's own action or stake. Second half delivers the consequence, reframe, or admission.

- Strong fit when the dispatch contains a real "I was wrong about X" or "I did Y, here's what I learned" moment.
- Sparingly only — most dispatches don't have an honest personal-stake angle, and forcing one reads as performative.
- Example direction (Dispatch 004 had this material but it wasn't picked): `I Ran 12 Datagram Nodes for 7 Months. The Same Standard Would Have Caught Helium.`

## Thumbnail-pairing modes

When `youtube-thumbnail.md` is present and the chosen in-image headline is known, the title's pairing with that thumbnail can take one of three shapes. The skill should name the shape in the candidate's rationale at Gate 2:

### Compound

Title and thumbnail attack the dispatch from two *related but distinct* angles. Both clickable on their own; together they reinforce a single thesis without restating each other.

- Example: thumbnail `Vibes ≠ Disclosure` (attacks disclosure absence) + title `385,000 People Bought a Franchise. Nova Labs Owns the Pricing.` (attacks authority asymmetry). Both indict the same Nova-Labs-vs-operators dynamic; neither restates the other.

### Completion

Title opens a curiosity gap that the thumbnail closes (or vice versa). Title and thumbnail compose into a single rhetorical move; viewing one without the other leaves a partial idea.

- Example: thumbnail `Vibes ≠ Disclosure` + title `McDonald's Gives You 200 Pages. Helium Gave 385,000 People One Word.` Title's "one word" is the gap; thumbnail's "Vibes" fills it.

### Orthogonal Compound

Title and thumbnail attack the dispatch from *fully separate angles*. Each carries an independent click-reason; together they widen the funnel by appealing to two different viewer concerns.

- Example: thumbnail `Vibes ≠ Disclosure` (disclosure absence) + title `Helium's IoT Side Earns $125 a Day. The Mobile Side Earns $56,000.` (revenue concentration). The two indictments are unrelated except by sharing the dispatch.

Use compound for the safest CTR; completion for the tightest paired-impression effect; orthogonal compound for the broadest viewer-net.

## Concrete-specific requirement

If the cold-open or transcript contains any of:

- A number (385,000 hotspots, 26% vote, $949)
- A place name (Austin, Reykjavík, the Bay Area)
- A dollar amount
- A year (2025, April 2026)
- A proper noun (Nova Labs, FAA, HIP-143, Datagram)

…then at least ONE of the three candidates MUST use it. The other two candidates can be more abstract for variety. The point is to anchor at least one candidate in a fact-check-able specific so the curiosity gap is earned, not invented.

## Title-specific bans (in addition to inherited list)

These are bans specific to the two-part-stop title format. The inherited bans from `thumbnail-headline-patterns.md` (banned hype adjectives, banned clickbait templates, anti-AI-tells) also apply.

### Equal-length halves

Both halves within 5 characters of equal length → reject.

Why: equal-length halves create a metered cadence that reads as AI-generated parallelism. Asymmetric halves — typically a shorter anchor and a longer twist, or a longer anchor and a punchier twist — read as written.

- BAD: `Helium Operators Bought a Lie. Nova Labs Sold Them a Bill.` (both halves 30 chars — too parallel, reads as cadenced)
- GOOD: `385,000 People Bought a Franchise. Nova Labs Owns the Pricing.` (34 vs 27)

### Second-half rephrase

Second half merely restates the first in different words → reject.

Why: spends two halves on a single idea, halving the title's information density.

- BAD: `Helium Operators Got No Disclosure. They Were Never Told the Pricing Rules.` (the second half is just "no disclosure" restated)
- GOOD: `Helium Operators Got No Disclosure. Nova Labs Sets the Pricing.` (the second half names the *consequence* of the first)

### Generic moralizing tail

Second half is a generic moral, conclusion, or vague-stakes phrase → reject.

Why: generic moralizing tails are pure clickbait shape. The viewer learns nothing from them; they exist to extract a click without earning one.

Examples to reject (case-insensitive):
- "Here's What That Means."
- "And It's Worse Than You Think."
- "You Won't Believe Why."
- "The Reason Will Shock You."
- "Here's What Happens Next."

If the dispatch genuinely *has* a consequence worth naming, name it concretely instead of moralizing about it.

## Anti-pattern gallery

Examples of title candidates that violate criteria, with the reason. Educational, not exhaustive.

- `SHOCKING: 385,000 People Got Scammed By Nova Labs!` — all-caps + banned hype adjective + exclamation point + generic "scammed" framing.
- `You Won't Believe What Helium Did to Their Hotspot Operators` — banned clickbait template + generic-YouTube shape + no concrete anchor in the truncation-visible first half.
- `Helium's Tokenomics: A Tapestry of Decentralized Promises` — anti-AI-tell ("tapestry") + abstract + no curiosity gap.
- `Nova Labs Did a Bad Thing. Here's What That Means.` — generic moralizing tail.
- `Helium Operators Got No Disclosure. They Were Never Given Pricing Documents.` — second-half rephrase (both halves say "no disclosure").
- `Helium Operators Bought a Lie. Nova Labs Sold Them a Bill.` — equal-length halves (both 30 chars; metered cadence reads as AI parallelism).
- `An In-Depth Look at the Helium Network's Governance Structure and What It Reveals About DePIN.` — over the 100-char hard ceiling, abstract, no curiosity gap, no twist.
- `Vibes Aren't Disclosure. Helium Operators Found Out the Hard Way.` — when thumbnail headline is `Vibes ≠ Disclosure`, this title's first half restates the thumbnail. Complementarity check fails.

## Worked example walkthroughs

### Dispatch 004 — "You Own the Hotspot. Nova Labs Owns What It Earns."

**Source:** recorded transcript (`Dispatch 004.en_US.srt`)
**Thumbnail in-image headline:** `Vibes ≠ Disclosure` (picked from the thumbnail skill at Gate 2)
**Cold-open (recorded):** "If you buy a McDonald's franchise, you get a two hundred page disclosure document. Federal law requires it. … Three hundred eighty five thousand people bought a Helium hotspot. For their franchise disclosure equivalent, they just got vibes."

**Concrete anchors mined from cold-open / transcript:**
- McDonald's franchise (universal cultural anchor)
- 200-page disclosure (concrete document specific)
- Federal law (regulatory frame)
- 385,000 (operator count)
- Helium hotspot, Nova Labs (dispatch-defining proper nouns)
- $949 hardware cost
- $4–8/month revenue, 10–20 year payoff (economic absurdity)
- HIP-143, April 2025 → April 2026 → April 2027 (governance timeline)
- 26% / 24% / 90% / 97% / 62% / 55% / 18% (vote concentration percentages)
- $125/day IoT vs $56,000/day Mobile (revenue concentration)
- 12 Datagram nodes, 7 months without pay (personal stake)

**3 drafted candidates with rationales:**

1. **"385,000 People Bought a Franchise. Nova Labs Owns the Pricing."** (62 chars · first half 34)
   — *Pattern: Concrete Anchor + Authority-Asymmetry Twist.* The operator count creates an expectation that buying = controlling economics; the second half reveals the authority sits elsewhere. Echoes the article's headline structure ("You Own the Hotspot. Nova Labs Owns What It Earns."). Search anchors: "Nova Labs" + "Franchise". Pairs with thumbnail `Vibes ≠ Disclosure` as **compound**.

2. **"McDonald's Gives You 200 Pages. Helium Gave 385,000 People One Word."** (69 chars · first half 31)
   — *Pattern: Specific Contradiction.* Universally recognizable cultural anchor (McDonald's, 200 pages) mirrored against named entity + dramatically smaller number. Sets up "what one word?" — the thumbnail's `Vibes ≠ Disclosure` completes it with "Vibes". Search anchors: "Helium" + "McDonald's". Pairs with thumbnail as **completion** (tightest pairing).

3. **"Helium's IoT Side Earns $125 a Day. The Mobile Side Earns $56,000."** (66 chars · first half 35)
   — *Pattern: Hidden Revenue Contradiction.* 450× ratio between the pointed-at side and the actual-revenue side. Sardonic by understatement — the math does the work, no adjectives. Search anchor: "Helium". Pairs with thumbnail as **orthogonal compound** (broadest viewer-net).

**Picked:** Candidate 1.

**Reason picked:** cleanest authority-asymmetry move, strongest article-headline coherence (the title and the article share the "X owns Y, Z owns W" structure), two distinct search anchors, broadest CTR appeal at the cost of slightly less tight thumbnail-pairing than Candidate 2's completion mechanic. The trade-off is acceptable because the thumbnail's `Vibes ≠ Disclosure` already lands as a stand-alone provocation — the title doesn't need to complete it to earn its impression.

(Add a second worked example after Dispatch 005 is produced.)

## How the skill uses this file

At drafting time (process step 5, SKILL.md §6), the skill:

1. Loads this file's contents into its drafting context.
2. Loads the inherited bans by reference from `../../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md`.
3. Extracts the cold-open candidate / first ~30 seconds of transcript, the dispatch concept, the thumbnail in-image headline (if present), and any concrete anchors.
4. Drafts 3 candidates following the two-part-stop pattern, each using a different mechanism from the taxonomy above.
5. Filters candidates against the inherited banned-word, banned-template, and anti-AI-tell lists, and against the title-specific bans in this file.
6. Runs the complementarity-with-thumbnail check if the thumbnail headline is known.
7. Re-drafts any failing slot up to 2 additional attempts.
8. Surfaces the passing candidates with one-line rationales per the Gate 2 display format (process step 6 in SKILL.md).
