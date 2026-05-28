---
name: tcn-fact-check
description: >
  Verify factual claims in a Civic Node article draft against their cited sources. Invoke this skill
  when the user wants to verify sourcing before publishing — including phrases like "fact check this",
  "verify the sources", "check the links", "run fact check", "verify this draft", "check this before
  I publish", or when a tcn-draft output is complete and the user asks for verification. Does NOT
  apply to writing, outlining, headline generation, wiki operations, or social media posts.
---

# The Civic Node — Fact Checker (Post-Draft Verification)

## What This Skill Does

Reads a finished article draft, extracts every factual claim paired with its inline source link, resolves each source, and verifies that the claim actually exists in the cited source. Produces a verification report flagging discrepancies, unsourced claims, and inaccessible sources.

This is the final quality gate before publishing. It sits after tcn-draft in the workflow.

Load `references/verification-rules.md` for detailed guidance on what counts as verified, how to handle edge cases, and the difference between claim types.

---

## Why This Exists

One unsourced claim on something Marcus knows well collapses credibility across the entire piece. One wrong link — a source that doesn't actually contain the claimed fact — is worse than no link at all, because it signals the writer didn't check their own work.

During drafting, common sourcing errors include:
- A source URL cited for a claim it doesn't actually contain
- A secondary source (blog post, YouTube transcript) cited instead of the original reporting
- Generic domain links (e.g., `https://www.trendforce.com`) instead of specific article URLs
- Figures rounded or restated in ways the original source doesn't support
- Quotes attributed via paraphrase without flagging the paraphrase

This skill catches all of these before publication.

---

## The Process

### Step 1: Extract Claims and Links

Parse the draft markdown. For every inline link `[linked text](URL)`:

1. Extract the **linked text** (the clickable words)
2. Extract the **full URL**
3. Extract the **surrounding sentence** (the claim context — the full assertion being sourced)

Then scan the entire draft for sentences containing factual assertions — numbers, dates, dollar figures, percentages, proper nouns paired with specific actions or attributes — that have **no inline link**. These are unsourced claims.

**What counts as a factual claim** (see `references/verification-rules.md` for full rules):
- Any specific number, date, percentage, or dollar figure
- Any attribution ("X said Y", "X reported Y")
- Any causal claim ("X caused Y", "X triggered Y")
- Any specific event with a date ("On October 1, 2025, Sam Altman signed...")

**What does NOT need sourcing:**
- The writer's own analysis or opinion ("The mechanism is more important than the actor")
- Logical inferences stated as such ("That threshold is remarkably low")
- The personal reflection section (first-person experience)
- Widely known background context that isn't contested

Present the extraction as a numbered list before proceeding to verification.

### Step 2: Resolve and Cross-Check Sources

For each **unique** URL extracted in Step 1 (de-dupe — one source cited in five claims gets resolved once), run three resolutions and reconcile them. The wiki is treated as **corroboration**, not a substitute for the live source. Every cited URL gets hit, every time.

**2a. URL sanity check (always runs first)**

Issue a lightweight request to the URL and capture:
- HTTP status (200 OK, 301/302 redirect, 403/404/410, 5xx, timeout)
- Final URL after redirects
- Page `<title>` (or first `<h1>`) for topic comparison

Flag any of the following as **link-health issues**, independent of content verification:
- Non-2xx status (404, 410, 403, 5xx, timeout)
- Redirect to a *different article* (path changed, or new URL points to a section/home page instead of the original article)
- Title/topic clearly unrelated to the wiki's recorded topic for that URL (cheap heuristic for "the article was replaced")

A link-health issue does not, by itself, make a claim unverified — the content cross-check in 2c-2d may still verify it via the live page or the wiki. But these issues are surfaced separately in the Link Health section of the report because dead/redirected links undermine reader trust regardless.

**2b. Wiki lookup**

Search `wiki/sources/` for a page whose `source_url` matches the URL. If found, load the summary, key points, and extracted quotes. This is the wiki's *recorded* version of what the source said at ingestion time.

If a wiki page exists for a *different* URL on the same topic (e.g., the draft cites Tom's Hardware, but the wiki has the same data from the original TrendForce report), surface this as a potential source upgrade — Marcus benefits from primary sources.

**2c. Live content fetch (always runs)**

WebFetch the URL and capture the live page content. This is the source's *current* version of the facts.

If WebFetch fails (hard paywall, JavaScript-rendered without fallback, blocked domain, 403/404), capture the failure reason and proceed to 2d with `live = unavailable`.

**2d. Reconcile**

For each URL, you now have up to three signals: link health (2a), wiki extract (2b), live content (2c). Resolve into one of these states before claim-level verification in Step 3:

| Wiki | Live | Resolution state |
|---|---|---|
| Found | Fetched | **Cross-check mode** — verify claim against both. Agreement → high-confidence Verified. Disagreement → Wiki/Source Divergence (Step 3 rules decide verdict by claim type). |
| Found | Unavailable | **Wiki-only mode** — verify against wiki. Mark medium confidence and add the URL to the Link Health section noting it could not be fetched live. |
| Missing | Fetched | **Live-only mode** — verify against live (this matches the current fallback behavior). Recommend adding this URL to the wiki for future runs. |
| Missing | Unavailable | **Source inaccessible** — cannot verify. Note failure reason. |

The point: a claim that previously passed silently because the wiki agreed with it will now also be checked against the live page. The new failure mode this catches — **the wiki and the live source disagree** — is what hardens the fact-check against stale ingestion and silent source edits.

### Step 3: Verify Each Claim

For each claim + source pair, determine whether the source contains evidence supporting the specific claim.

**This is semantic verification, not string matching.** The article may phrase things differently than the source. "57.2 trillion won" should match "57.2 trillion won ($37.92 billion)" even if the surrounding words differ. "8.5x jump" should match "more than eightfold."

**Verification categories:**

| Category | Meaning | Action needed |
|---|---|---|
| **Verified** | Both wiki and live source (or whichever was available) contain the claimed fact with matching or consistent figures | None |
| **Partially verified** | Source covers the topic but the specific figure or framing differs | Flag the discrepancy; recommend correction |
| **Not found in source** | Neither the live source nor the wiki contains the claimed information | Recommend finding the correct source or removing the link |
| **Wiki/source divergence** | Wiki extract supports the claim but live source disagrees — *or vice versa* | See split-policy rules below; report both excerpts side-by-side |
| **Source inaccessible** | Could not fetch the URL live AND wiki has no record (or live is the only available signal and failed) | Note failure reason; recommend manual verification |
| **Unsourced** | Factual claim with no inline link | Recommend adding a source or flagging as editorial judgment |

**Wiki/source divergence — split-policy verdict:**

When the wiki and the live source disagree on whether a claim is supported, the verdict depends on **what kind of claim it is**. Hard facts are decided by the live source because corrections and updates are usually authoritative. Prose-y claims (causal language, characterizations, framing) are surfaced without a verdict because prose drift is more ambiguous and often a judgment call the writer should make.

| Claim type | Verdict policy |
|---|---|
| Number, percentage, dollar figure, date, direct quote, named attribution | **Live wins.** Mark verified/unverified based on the live source. Flag the wiki page as a candidate for re-ingestion in the report. |
| Causal language ("X triggered Y"), characterization ("a panic," "a collapse"), qualitative framing | **No verdict.** Report the wiki excerpt and the live excerpt side-by-side. Recommend the writer decide whether the article phrasing, the wiki, or the live page is the source of the divergence. |

In both cases, the divergence itself is surfaced prominently — even when "live wins" gives a clean verdict, the report records that the wiki and live source disagreed, because that's a signal the wiki may need a refresh.

**Pay special attention to:**
- Exact numbers — is it 171% or 170%? $710 or $700? These matter.
- Dates — is the event dated correctly?
- Attribution — is the quote from the person named, or paraphrased from someone else?
- Causal claims — does the source support the causal relationship, or just the correlation?
- Derived calculations — if the article says "294% increase" from $180→$710, verify the math: ($710-$180)/$180 = 294%. But also verify the $180 and $710 figures themselves.

### Step 4: Report

Present the verification report in the format below. Group by status. For every flagged claim, include the relevant passage from the source so the writer can compare without re-fetching.

---

## Output Format

```markdown
## Fact Check Report: [Article Title]

**Claims extracted:** [N linked] + [N unsourced]
**Verified:** [N] | **Partially verified:** [N] | **Not found in source:** [N] | **Wiki/source divergence:** [N] | **Source inaccessible:** [N] | **Unsourced:** [N]
**Link health:** [N URLs OK] | [N redirected] | [N broken/inaccessible]

---

### Verified Claims

| # | Claim (from article) | Source | Cross-check | Status |
|---|---|---|---|---|
| 1 | [brief claim description] | [source name] | wiki + live agree | ✓ Verified |
| 2 | ... | ... | live only (no wiki) | ✓ Verified |

The "Cross-check" column records which signals agreed: `wiki + live agree`, `wiki only` (live unavailable), `live only` (no wiki page), or `wiki + live agree on hard fact` for divergence cases where live won cleanly.

---

### Flagged Claims

#### Claim #[N]: [brief description]
**Article says:** "[exact text from the draft]"
**Source says:** "[relevant passage from the source]"
**Discrepancy:** [what doesn't match and why it matters]
**Recommendation:** [specific fix — correct the figure / swap the source link / soften the claim]

[repeat for each flagged claim]

---

### Wiki / Source Divergence

For each claim where the wiki extract and the live source disagreed. Hard-fact divergences include a verdict (live wins); prose divergences are surfaced without a verdict per the split policy in Step 3.

#### Claim #[N]: [brief description] — [hard fact | prose]
**Article says:** "[exact text from the draft]"
**Wiki extract says:** "[relevant passage from wiki/sources/...]" (ingested [date if available])
**Live source now says:** "[relevant passage from current live page]"
**Likely cause:** [source was edited or corrected | source was retracted | wiki ingestion error | unclear]
**Verdict:** [✓ Verified against live / ✗ Not supported by live / ⚠ No verdict — writer judgment]
**Recommendation:** [correct the article to match live / re-ingest the wiki page / flag for manual review]

[repeat for each divergence]

---

### Unsourced Claims

| # | Claim | Recommendation |
|---|---|---|
| 1 | [sentence with factual assertion but no link] | [add source / acceptable as editorial judgment] |

---

### Link Health

URL-level issues independent of content verification. Even when a claim verifies cleanly via the wiki, a broken or redirected URL undermines reader trust and should be fixed.

| URL | Status | Issue | Recommendation |
|---|---|---|---|
| [URL] | 404 | Page no longer exists | Find replacement source or archive.org snapshot |
| [URL] | 301 → [new URL] | Redirects to unrelated page (was article, now section index) | Update link to the new article URL or use an archive snapshot |
| [URL] | 200 but title changed | Page title no longer matches the article's topic; may have been replaced | Spot-check manually; consider archive link |
| [URL] | timeout / paywall / JS-rendered | Live fetch failed; verification used wiki only | Manual verification recommended |

---

**Summary:** [one-paragraph assessment — overall sourcing quality, most critical issues to address, any wiki pages flagged for re-ingestion, and whether the piece is ready to publish from a factual accuracy standpoint]
```

---

## Reference Files

- `references/verification-rules.md` — Detailed rules for claim classification, edge case handling, and the boundary between factual claims and editorial judgment
