# description-anatomy.md

Living reference for `tcn-youtube-description`. Block-by-block decision rules, the Audit-Standard mechanism definition, channel-evergreen hashtag canon, and one full worked example. The SKILL.md references this file at drafting time.

---

## The Audit-Standard mechanism (description-only)

A sixth mechanism specific to the description hook surface, added to the five inherited from `../tcn-youtube-title/references/title-patterns.md`.

**Definition.** The hook proposes a known industry, regulatory, or institutional standard that the subject failed to meet. The first half names the standard; the second half names the gap.

**Why description-only?** Audit-Standard hooks need ~20-40 words to land — too long for a title (10-14 words) and too text-heavy for a thumbnail (3-6 words). The description's above-fold budget (200 chars / ~30-40 words) is the right surface for it.

**Distinct from:**
- **Specific Contradiction** — Audit-Standard anchors to an *external* standard the reader can verify (federal law, industry convention, regulatory floor). Specific Contradiction just states two contradicting facts without naming a standard.
- **Authority-Asymmetry** — Audit-Standard proposes what the standard *should have been*; Authority-Asymmetry just names who controls what.

**Worked examples:**

1. **Helium / Dispatch 004 (the canonical example).**
   - Hook: "Federal law requires McDonald's franchisees get a 200-page disclosure. Helium hotspot buyers got vibes."
   - Standard named: federal franchise disclosure (FTC Franchise Rule).
   - Gap named: zero disclosure for a $949 hardware buy-in with 10-20 year payback.

2. **Generic Fed-policy example.**
   - Hook: "Every Fed Chair since Volcker has briefed Congress quarterly. This one updated a blog."
   - Standard named: post-Volcker Fed communications convention.
   - Gap named: institutional-communications floor missed.

3. **Generic DePIN example.**
   - Hook: "Public companies file annual reports under penalty of perjury. This token project files vibes on Discord."
   - Standard named: SEC public-company disclosure regime.
   - Gap named: voluntary-but-marketed-as-rigorous reporting.

**When to use:** Justin's editorial frame is repeatedly "what disclosure / what audit / what standard would have caught this?" Audit-Standard surfaces that frame directly above the fold. Use when the dispatch's thesis is fundamentally about a missing institutional floor.

**When NOT to use:** if the dispatch is a debugging post-mortem (Personal-Implication fits better), a revenue-concentration receipt (Hidden Revenue fits better), or a "who controls X" piece (Authority-Asymmetry fits better).

---

## Channel-evergreen hashtag canon

The two constant tags appended to every dispatch's hashtag block:

- `#TheCivicNode`
- `#drinkYourOJ`

**Stability commitment.** These tags should NOT change without a deliberate channel-identity decision. The reason they exist as evergreens is to build channel-level discoverability over time — tags that appear on every dispatch accumulate weight in YouTube's hashtag-clustering signal.

**If a third evergreen is added** (e.g., as Justin's coverage stabilizes around a domain), append to this list with the date of the decision and the dispatch number where it first appeared. Do not retroactively edit prior artifacts.

**Format rules** (apply to dispatch-specific tags too):
- Sentence case for single-word: `#Helium`, `#Bluesky`.
- PascalCase / camelCase for multi-word: `#TheCivicNode`, `#NovaLabs`, `#HIP143`, `#drinkYourOJ`.
- No spaces, no punctuation. YouTube hashtags honor `[A-Za-z0-9_]` only.
- Lowercase numbers and letters are fine; ALL-CAPS is banned.

---

## Channel link block canon

Default Substack URL: `https://drinkyouroj.substack.com`
Default Bluesky URL: `https://bsky.app/profile/thecivicnode.bsky.social`

Both are overrideable per-invocation. Update this canon if Justin moves handles.

Default boilerplate text:

```
-- THE CIVIC NODE --
Weekly. No hype.

Substack:  https://drinkyouroj.substack.com
Bluesky:   https://bsky.app/profile/thecivicnode.bsky.social
```

The two-space alignment between `Substack:`/`Bluesky:` and the URLs is decorative. YouTube collapses to single-space at render time.

---

## Transcript fuzzy-match threshold (chapter timestamps)

When mining `.srt` for chapter timestamps post-record, fuzzy-match the first 4-6 words of each narration slide's opener against the transcript text. Recommended thresholds:

- **High confidence (use timestamp):** Levenshtein ratio ≥ 0.85 OR exact word-sequence match.
- **Medium confidence (use timestamp + warning):** Levenshtein ratio 0.7-0.85. Surface a one-line metadata note: `slide N matched at medium confidence; verify timestamp`.
- **Low confidence (fall back to narration estimate):** Levenshtein ratio < 0.7. Use narration WPM math for that slide; surface metadata note: `slide N not located in transcript; using estimated timestamp`.

This threshold tolerates light improv during recording while catching genuinely abandoned passages (which deserve user attention before publishing).

---

## Worked example — Dispatch 004 ("You Own the Hotspot")

Input narration: `workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md` (8 slides, 5:11 runtime, 727 words at 140 wpm).

Paired title (hypothetical): "Buy a Helium hotspot. Nova Labs sets the price." (Authority-Asymmetry mechanism)
Paired thumbnail headline (hypothetical): "Vibes ≠ Disclosure" (Specific-Contradiction mechanism)

**Orthogonal mechanism choice for description hook:** title runs Authority-Asymmetry, thumbnail runs Specific-Contradiction. Description hook must run something else. **Audit-Standard fits the dispatch concept best** — the article's whole frame is "the four disclosures Helium operators should have received."

**Block 1 (hook punch):**

```
Federal law requires McDonald's franchisees get a 200-page disclosure.
385,000 Helium hotspot buyers got vibes.
```

(150 chars total. Audit-Standard mechanism. Bare numeral "385,000" not spelled out, matching description-vs-narration rule.)

**Block 3 (summary):**

```
After the August 2025 halving, a Helium hotspot earns $4-$8/month. The hardware costs $949. The pricing that determines the payback is set by Nova Labs, the same company that voted itself 26% of the HIP-143 ballot that handed it pricing authority. The piece on Substack walks the four disclosures Helium operators should have received, the HIP-148 vote that traded subscriber rewards for gift cards, and the Datagram debug that broke the author's own counter-example.
```

(498 chars. Front-loads anchors: $4-$8, $949, 26%, HIP-143, HIP-148, Datagram. References cuts from the article. Ends on a click-motivator.)

**Block 5 (article CTA):**

```
→ Read the full piece on Substack:
https://drinkyouroj.substack.com/p/you-own-the-hotspot-nova-labs-owns-what-it-earns
```

**Block 7 (chapters, pre-record estimate at 140 wpm):**

```
-- CHAPTERS --
0:00  The McDonald's standard
0:38  What Helium operators bought
1:09  The unit math after the halving
2:01  How the pricing vote extended itself
2:54  Who actually controlled the vote
3:47  The audit standard that catches this
4:34  What the article covers that this video doesn't
5:02  Subscribe at drinkyouroj.substack.com
```

(Eight chapters, one per narration slide. End slide included. Viewer-rewritten labels at 8/10 register.)

**Block 9 (channel link block):** canon boilerplate, no changes.

**Block 11 (hashtags):**

```
#Helium #DePIN #NovaLabs #HIP143 #HIP148 #TheCivicNode #drinkYourOJ
```

(7 tags: 5 dispatch-specific proper nouns + 2 channel-evergreens. Sentence-case PascalCase. Dispatch-specific tags first.)

**Total assembled description: ~1,650 chars** including dividers and blank lines. Well within the 1,500-2,500 target.

**Metadata block written to artifact:**

```
**Generated:** 2026-05-21
**Source:** narration (timestamps estimated)
**Article URL:** https://drinkyouroj.substack.com/p/you-own-the-hotspot-nova-labs-owns-what-it-earns
**Paired title:** "Buy a Helium hotspot. Nova Labs sets the price."
**Paired title mechanism:** Authority-Asymmetry
**Paired thumbnail headline:** "Vibes ≠ Disclosure"
**Paired thumbnail mechanism:** Specific-Contradiction
**Description hook mechanism:** Audit-Standard
```
