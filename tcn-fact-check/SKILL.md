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

### Step 2: Resolve Sources

For each URL extracted in Step 1:

1. **Check the wiki first.** Search `wiki/sources/` for a page whose `source_url` matches the URL. If found, read the wiki source page — it contains a summary, key points, and quotes already extracted from the original. This is faster and more reliable than re-fetching.

2. **If not in the wiki, use WebFetch** to retrieve the page content from the URL.

3. **If WebFetch fails** (paywall, JavaScript-rendered, blocked domain, 403/404), flag the source as **"source inaccessible"** rather than marking the claim unverified. Note the failure reason.

4. **If the wiki source page exists but the URL is different** (e.g., the draft links to a Tom's Hardware article, but the wiki has the same data sourced from a TrendForce report), note this as a potential source improvement — the claim may be verifiable from a better source.

### Step 3: Verify Each Claim

For each claim + source pair, determine whether the source contains evidence supporting the specific claim.

**This is semantic verification, not string matching.** The article may phrase things differently than the source. "57.2 trillion won" should match "57.2 trillion won ($37.92 billion)" even if the surrounding words differ. "8.5x jump" should match "more than eightfold."

**Verification categories:**

| Category | Meaning | Action needed |
|---|---|---|
| **Verified** | Source contains the claimed fact with matching or consistent figures | None |
| **Partially verified** | Source covers the topic but the specific figure or framing differs | Flag the discrepancy; recommend correction |
| **Not found in source** | Source does not contain the claimed information | Recommend finding the correct source or removing the link |
| **Source inaccessible** | Could not fetch the URL (paywall, error, etc.) | Note failure reason; recommend manual verification |
| **Unsourced** | Factual claim with no inline link | Recommend adding a source or flagging as editorial judgment |

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
**Verified:** [N] | **Partially verified:** [N] | **Not found in source:** [N] | **Source inaccessible:** [N] | **Unsourced:** [N]

---

### Verified Claims

| # | Claim (from article) | Source | Status |
|---|---|---|---|
| 1 | [brief claim description] | [source name] | ✓ Verified |
| 2 | ... | ... | ✓ Verified |

---

### Flagged Claims

#### Claim #[N]: [brief description]
**Article says:** "[exact text from the draft]"
**Source says:** "[relevant passage from the source]"
**Discrepancy:** [what doesn't match and why it matters]
**Recommendation:** [specific fix — correct the figure / swap the source link / soften the claim]

[repeat for each flagged claim]

---

### Unsourced Claims

| # | Claim | Recommendation |
|---|---|---|
| 1 | [sentence with factual assertion but no link] | [add source / acceptable as editorial judgment] |

---

### Source Accessibility Issues

| URL | Issue | Recommendation |
|---|---|---|
| [URL] | [403 / paywall / JS-rendered] | [manual verification needed / use archive link] |

---

**Summary:** [one-paragraph assessment — overall sourcing quality, most critical issues to address, whether the piece is ready to publish from a factual accuracy standpoint]
```

---

## Reference Files

- `references/verification-rules.md` — Detailed rules for claim classification, edge case handling, and the boundary between factual claims and editorial judgment
