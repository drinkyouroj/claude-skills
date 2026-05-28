# Verification Rules — Full Reference

*Detailed guidance on what counts as a factual claim, how to handle edge cases, and the boundary between verifiable assertions and editorial judgment.*

---

## What Counts as a Factual Claim

A factual claim is any assertion in the article that could be independently verified or falsified by checking a source. If someone could say "that's wrong" and prove it with evidence, it's a factual claim.

### Always requires sourcing:

- **Specific numbers:** "$400," "57.2 trillion won," "900,000 wafer starts per month"
- **Percentages:** "171% year-over-year," "a 294% increase," "57% reduction"
- **Dates of events:** "On October 1, 2025," "In March," "by Q3 2025"
- **Attributions:** "HP says," "Gartner projects," "Samsung posted"
- **Causal claims:** "triggered a global panic," "caused Apple to lock in deals"
- **Quantified comparisons:** "up from 15%," "an 8.5x jump year-over-year"
- **Specific events:** "the Stargate data center expansion was killed," "Sora was shuttered"
- **Direct quotes:** Any text presented as someone's words
- **Named organizations taking specific actions:** "Micron exited its consumer Crucial brand"

### Does NOT require sourcing:

- **Writer's own analysis:** "The mechanism is more important than the actor"
- **Logical inferences:** "In a three-producer market, that threshold is remarkably low"
- **Rhetorical framing:** "That's not a technology company posting strong earnings"
- **Personal reflection section:** First-person experience and opinion
- **Widely accepted background:** "Samsung and SK Hynix are South Korean companies" (uncontested common knowledge)
- **The article's thesis statement:** This is the writer's argument, not a factual claim
- **Metaphors and analogies:** "The same way a state actor exploits a geographic one" (analytical framing, not a factual assertion about Iran)

### Gray zone — use judgment:

- **Round numbers used for readability:** If the source says "$379.99" and the article says "~$400," that's acceptable approximation — note it but don't flag as a discrepancy
- **Temporal claims without dates:** "In the interim" or "since then" — verify the implied timeline is correct
- **Composite claims:** A sentence that combines facts from multiple sources. Each individual fact needs its own verification; the combination is the writer's synthesis

---

## Handling Specific Edge Cases

### Approximate vs. exact figures

If the article rounds a figure for readability, verify:
1. The underlying figure is correct
2. The rounding doesn't change the meaning
3. The rounding direction doesn't mislead

**Acceptable:** Source says "$379.99," article says "$400" (round number for readability, doesn't mislead)
**Not acceptable:** Source says "6-8% in pessimistic scenario," article says "8-9%" (overstates the range and changes the scenario framing)

### Derived calculations

When the article states a calculated figure (e.g., "294% increase"):
1. Verify the base numbers the calculation derives from ($180 and $710)
2. Verify the math: ($710 - $180) / $180 = 294.4% ≈ 294% ✓
3. Both the inputs AND the output need to be correct

### Paraphrased quotes

If the article attributes a paraphrase rather than a direct quote:
- Verify the original quote exists and the paraphrase accurately represents it
- Flag if the paraphrase changes the meaning or emphasis
- Note if the quote is from a paywalled source (e.g., Stratechery) and attributed via secondary reporting

### Claims sourced to paywalled, JS-rendered, or blocked content

The skill's architecture is **always-live + wiki-corroboration**, with a three-step escalation chain in Step 2c: WebFetch → Chrome MCP → manual scrape. Most "inaccessible" sources resolve at one of these tiers; the wiki is only the verifier of last resort when all three escalation steps fail.

**Walk the escalation chain in order:**

1. **WebFetch** — try it first. Paywalls sometimes return enough lede/dek for verification; JS-rendered pages may return enough static fallback. If WebFetch succeeds with usable content, you're done.
2. **Chrome MCP** — escalate if WebFetch returns 403, an SPA stub, or times out. This is the right tier for:
   - JavaScript-rendered news sites and SPAs (rendered in a real browser)
   - 403s from sites with bot detection (the Chrome session presents real cookies + UA)
   - Soft paywalls (sometimes a Chrome session with the user's login clears them)
3. **Manual scrape** — escalate if Chrome can't reach the content either. This is the right tier for:
   - Hard paywalls (Stratechery, Bloomberg, WSJ subscriber-only)
   - Login walls without an active browser session
   - Native PDFs that don't render as extractable text in the browser
   - Region locks, captchas, other access barriers
4. **Wiki-only verification** — only if all three tiers fail AND the wiki has an existing page for the URL. Mark medium confidence and add the URL to the Link Health section.
5. **Secondary source check** — if even the wiki has nothing, check whether a secondary source (news outlet) reported the same data with attribution. Note in the report.
6. **Flag as inaccessible** — if none of those work, mark "source inaccessible" and recommend the writer find an accessible secondary source or remove the claim.

When the wiki is the only signal available, mark the verification at **medium confidence** and add the URL to the Link Health section noting the live fetch failed — readers clicking the link will hit the same paywall, which is its own credibility issue worth surfacing.

**Manual scrape isn't a punt — it's an investment.** When the user provides a scraped file, the fact-checker hands it to llm-wiki's Ingest flow (see Step 2.5 in SKILL.md). The result: future fact-checks against the same URL skip the manual step entirely because the wiki now has the source. Over time, the wiki absorbs the publication's worth of paywalled/PDF sources and becomes increasingly self-sufficient.

### When the wiki and the live source disagree

This is the new failure mode the cross-check architecture is designed to catch. Three things can cause it, and they have different fixes:

1. **The source was edited or corrected after wiki ingestion.** News outlets quietly update articles all the time — figures get corrected, paragraphs get added, retractions get appended. The live page is the current truth.
2. **The source was replaced or retracted.** The URL still resolves but now points to a different article, an editor's note, or a section index. The link is effectively dead even though it returns 200.
3. **The wiki ingestion was wrong.** The wiki extract captured the wrong figure, misattributed a quote, or summarized the source incorrectly at ingestion time. The live page is what the source actually says.

Distinguishing these matters for the recommendation:

- **Edited/corrected source:** correct the article to match live; wiki should be re-ingested
- **Replaced/retracted source:** find a new source for the claim, or remove the claim; flag the wiki page for retirement or re-ingestion against the new URL
- **Wiki ingestion error:** correct the article only if it was relying on the wrong wiki summary; flag the wiki page for re-ingestion regardless

The split-policy verdict (from Step 3 of SKILL.md) decides whether the report renders a verified/unverified verdict or just surfaces the divergence:

- **Hard facts** (numbers, percentages, dollar figures, dates, direct quotes, named attributions): **Live wins.** The verdict comes from the live page. Corrections to hard facts are almost always authoritative — if Reuters changed "$700M" to "$710M" three months after the original report, $710M is the truth and the article should match.
- **Prose claims** (causal language like "triggered a panic," characterizations like "a collapse," qualitative framing): **No verdict.** Surface both excerpts and let the writer judge. Prose drift is more ambiguous: the live page softening "triggered" to "preceded" might be a legitimate correction or might be later-edition hedging the writer chose to ignore. Not a verdict the fact-checker should auto-make.

Every divergence — regardless of verdict — should also note that the wiki page may need re-ingestion. Over time this turns the fact-checker into a feedback loop that hardens the wiki itself.

### Secondary vs. primary sources

The fact-checker should note when a claim is sourced to secondary reporting rather than the primary source:
- **Primary:** Reuters reporting Samsung's earnings directly
- **Secondary:** A blog post summarizing the Reuters report

Both can be valid, but primary is always preferred. If the wiki has the primary source, recommend linking to it instead.

### Causal claims

Causal claims ("X caused Y," "X triggered Y") are the hardest to verify because sources often report correlation without asserting causation. The fact-checker should:
1. Verify that the source reports both X and Y
2. Check whether the source asserts the causal link or merely reports temporal proximity
3. If the source only reports correlation, flag the causal claim as "partially verified — source reports correlation, article asserts causation"

---

## Verification Confidence Levels

Not all verifications are equal. When reporting, indicate confidence:

- **High confidence:** The source contains the exact figure, date, or quote. No ambiguity.
- **Medium confidence:** The source contains consistent information but uses different phrasing, rounding, or framing. The claim is supported but not verbatim.
- **Low confidence:** The source touches on the topic but doesn't directly support the specific claim. The writer may be synthesizing across sources.

---

## Red Flags to Always Escalate

These should always be called out in the report, regardless of verification status:

1. **A source that doesn't contain the claimed fact at all** — this is the most damaging error for credibility
2. **A non-authoritative source (blog, YouTube, Medium) cited for a factual claim when primary reporting exists** — Marcus clicks through to a blog and credibility collapses. The wiki often contains Tier 4 sources (blogs, YouTube transcripts) as research inputs; these are never acceptable as article sources for factual claims. Flag and recommend the primary source. See the source tier hierarchy in the tcn-fact-reconcile skill.
3. **A secondary source cited when the primary source is available and accessible** — even credible outlets (Tom's Hardware, WCCFTech) are secondary when they're reporting someone else's data. Prefer the original: the Reuters earnings report over Tom's Hardware summarizing it, the Korea Economic Daily over WCCFTech citing it
4. **A quote attributed to Person A that the source attributes to Person B**
5. **A figure that appears in the article but in no available source** — may have been hallucinated during drafting
6. **A URL that returns 404 or redirects to a different article** — dead links undermine trust
7. **Generic domain links** (e.g., `https://www.reuters.com`) instead of specific article URLs — this signals the link was never verified
