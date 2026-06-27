---
name: blog-fact-check
description: >
  Verify factual claims in a blog article draft against their cited sources. Invoke this skill
  when the user wants to verify sourcing before publishing — including phrases like "fact check this",
  "verify the sources", "check the links", "run fact check", "verify this draft", "check this before
  I publish", or when a blog-draft output is complete and the user asks for verification. Does NOT
  apply to writing, outlining, headline generation, or social media posts.
---

# Blog — Fact Checker (Post-Draft Verification)

## Profile resolution

Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else.

Loads: `identity.md` (for the blog's subject domain), active preset (to check step-disable flags).

---

## DISABLE-GUARD CONTRACT

**If the active profile disables this step (`profile.yaml` key `steps.fact-check: false`), this skill is a NO-OP.**

- When invoked via the **orchestrator**, the orchestrator must check the preset's `steps` block and skip this skill entirely if `steps.fact-check` is `false`. The skill is not called; nothing runs.
- When invoked **standalone** (direct `/blog-fact-check` call) under a profile that has `steps.fact-check: false` (e.g. a fiction or creative preset), the skill must detect this condition, print a single notice — "Fact-check is disabled for this profile (`steps.fact-check: false`). This skill is a no-op under the active preset. Remove or set `steps.fact-check: true` to enable." — and stop. It must not run any verification logic.

This guard exists because some content profiles (fiction, creative writing, satire) have no factual sourcing requirement. Running fact-check against them would generate false positives and wasted work.

---

## What This Skill Does

Reads a finished article draft, extracts every factual claim paired with its inline source link, resolves each source, and verifies that the claim actually exists in the cited source. Produces a verification report flagging discrepancies, unsourced claims, and inaccessible sources.

This is the final quality gate before publishing. It sits after blog-draft in the workflow.

The blog's subject domain (pulled from `identity.md` / `quick.domain`) informs which claim types are most common and what constitutes authoritative sourcing for that domain.

Load `references/verification-rules.md` for detailed guidance on what counts as verified, how to handle edge cases, and the difference between claim types.

---

## Why This Exists

One unsourced claim on something the blog's reader knows well collapses credibility across the entire piece. One wrong link — a source that doesn't actually contain the claimed fact — is worse than no link at all, because it signals the writer didn't check their own work.

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

For each **unique** URL extracted in Step 1 (de-dupe — one source cited in five claims gets resolved once), run three resolutions and reconcile them. The blog's source archive (if configured in `profile.yaml.paths.source`) is treated as **corroboration**, not a substitute for the live source. Every cited URL gets hit, every time.

**2a. URL sanity check (always runs first)**

Issue a lightweight request to the URL and capture:
- HTTP status (200 OK, 301/302 redirect, 403/404/410, 5xx, timeout)
- Final URL after redirects
- Page `<title>` (or first `<h1>`) for topic comparison

Flag any of the following as **link-health issues**, independent of content verification:
- Non-2xx status (404, 410, 403, 5xx, timeout)
- Redirect to a *different article* (path changed, or new URL points to a section/home page instead of the original article)
- Title/topic clearly unrelated to the recorded topic for that URL (cheap heuristic for "the article was replaced")

A link-health issue does not, by itself, make a claim unverified — the content cross-check in 2c-2d may still verify it via the live page or the source archive. But these issues are surfaced separately in the Link Health section of the report because dead/redirected links undermine reader trust regardless.

**2b. Source archive lookup (conditional — only if the active profile configures one)**

If the active profile configures a source archive (`profile.yaml.paths.source` is set), search it for a page whose `source_url` matches the URL. If found, load the summary, key points, and extracted quotes. This is the archive's *recorded* version of what the source said at ingestion time.

If a source archive page exists for a *different* URL on the same topic, surface this as a potential source upgrade — primary sources are always preferred over secondary ones.

If no source archive is configured (e.g., under a `general` profile or any profile without `paths.source`), skip this sub-step entirely. The verification path continues via live fetch in 2c; resolution state will be "Live-only mode" for all URLs.

**2c. Live content fetch (always runs, with escalation chain)**

The goal is to retrieve the current live content of the source. Try three methods in order, escalating on failure:

**2c.1 — WebFetch**

Default path. Fast, cheap, works for static pages and most news sites.

Escalate to 2c.2 if any of these occur:
- HTTP 403 (often clears with a real browser session)
- HTTP 404 from a domain known to JS-render content (the "page not found" is the SPA shell)
- Suspiciously short or stub-shaped HTML (e.g., `<div id="root"></div>` with no body content — likely a JS-rendered SPA that WebFetch can't execute)
- Timeout or connection refused

**2c.2 — Chrome MCP fallback**

Use the Claude Chrome extension (`mcp__Claude_in_Chrome__*` tools) to retrieve the page in a real browser session. This handles two failure modes WebFetch can't:
- **JavaScript-rendered pages** — React/Vue/Next/SPA apps render naturally in a real browser
- **403s on real-browser-only sites** — the Chrome session carries the user's cookies and a real `User-Agent`, which clears most bot-protection 403s

Workflow:
1. Confirm the Chrome extension is connected (`mcp__Claude_in_Chrome__list_connected_browsers`). If not, ask the user to install/enable it rather than silently dropping to manual.
2. `mcp__Claude_in_Chrome__navigate` to the URL.
3. `mcp__Claude_in_Chrome__get_page_text` (or `read_page`) to extract the rendered content.
4. Treat the extracted text as the live source for verification purposes.

Escalate to 2c.3 if Chrome can't reach the content either:
- Hard paywall (Stratechery, Bloomberg, WSJ subscriber-only) — page loads but only shows lede + paywall
- Login wall (the URL requires authentication the user hasn't set up in Chrome)
- Native PDF that doesn't render as text in the browser
- Region lock, captcha, or other access barrier

**2c.3 — Manual scrape protocol**

When automated retrieval fails through both prior steps, emit a structured request to the user:

> **Source not auto-retrievable:** `[URL]`
> **Why:** [paywall / login wall / PDF / region lock / captcha]
> **To verify the claim(s) sourced to this URL, please:**
> 1. Open the URL in your browser (logged in if needed)
> 2. Save the article as either: (a) "Save as PDF" or (b) copy the article text into a markdown file
> 3. Reply with the file path

When the user replies with a file path:
1. Read the file.
2. Use its contents as the live source for verification.
3. If the active profile configures a source archive (`profile.yaml.paths.source` is set): save the raw file to `{source-archive-root}/raw/_manual/[meaningful-slug].pdf` (or `.md`), then hand off the file + metadata to the source archive's Ingest flow so a source page is created (see "Ingestion delegation" below). If no source archive is configured, skip the archival step — just use the file for verification.

If the user declines or cannot scrape, proceed to 2d with `live = unavailable` and note the failure reason for the Link Health section.

**2d. Reconcile**

For each URL, you now have up to three signals: link health (2a), source archive extract (2b), live content (2c). Resolve into one of these states before claim-level verification in Step 3:

| Archive | Live | Resolution state |
|---|---|---|
| Found | Fetched | **Cross-check mode** — verify claim against both. Agreement → high-confidence Verified. Disagreement → Archive/Source Divergence (Step 3 rules decide verdict by claim type). |
| Found | Unavailable | **Archive-only mode** — verify against archive. Mark medium confidence and add the URL to the Link Health section noting it could not be fetched live. |
| Missing | Fetched | **Live-only mode** — verify against live (this matches the current fallback behavior). Recommend adding this URL to the archive for future runs. |
| Missing | Unavailable | **Source inaccessible** — cannot verify. Note failure reason. |

The point: a claim that previously passed silently because the archive agreed with it will now also be checked against the live page. The new failure mode this catches — **the archive and the live source disagree** — is what hardens the fact-check against stale ingestion and silent source edits.

---

### Step 2.5: Ingestion delegation (conditional — only if the active profile configures a source archive)

If the active profile does **not** configure a source archive (`profile.yaml.paths.source` is absent or unset), skip this entire step. The fact-check is self-contained: live fetch is the only verification path, and no archival delegation occurs.

If the active profile **does** configure a source archive, and Step 2c escalated to Chrome (2c.2) or manual scrape (2c.3) for a URL that **isn't yet in the source archive**, the fact-checker should hand off to the source archive's Ingest flow so the archive accumulates the work — every escalation makes future fact-checks faster and gives a permanent record of what the source said.

**When to delegate:**

| Resolution state | Action |
|---|---|
| WebFetch succeeded, archive missing | Optionally suggest ingest (the URL is re-fetchable; not urgent). |
| Chrome succeeded, archive missing | **Delegate ingest.** Chrome-only retrieval signals the source is JS-rendered or 403s without a real browser — re-fetch may not work later. |
| Manual scrape provided, archive missing | **Delegate ingest, always.** Paywalls and PDFs can't be re-retrieved automatically; the raw file is the only durable record. |
| Archive already has this URL | Don't re-ingest. If a divergence was detected, recommend the user re-run ingest manually to refresh the archive. |

**What to pass to the Ingest flow:**

The fact-checker invokes the Ingest flow with:
- **URL** (original, as cited in the article)
- **Canonical URL** if redirects happened (from Step 2a)
- **Retrieved content** (Chrome-extracted text, or path to the manually scraped file in `raw/_manual/`)
- **Provenance fields** to populate the source page frontmatter:
  - `ingest_method`: `chrome` or `manual` (WebFetch ingestions, if you choose to file them, get `webfetch`)
  - `raw_file`: relative path inside the archive's `raw/` directory (required for `chrome` and `manual`; absent or null for `webfetch`)
  - `status`: `ok` | `paywalled` | `partial` (e.g., Chrome got the lede only) | `404`
  - `notes`: brief one-liner on retrieval context (e.g., "WebFetch returned 403; Chrome succeeded with active login")

**Snapshot policy:**
- `webfetch` ingestions: no raw file persisted — URL is the source of truth, re-fetching is reliable
- `chrome` ingestions: raw file required (the extracted text saved to `raw/`)
- `manual` ingestions: raw file required (the original PDF/HTML the user saved)

This means that for any source archive page where `ingest_method ≠ webfetch`, the original artifact is preserved at `raw_file` and you can always re-open it to verify the archive's summary against the actual source text. For `webfetch` sources, the divergence check itself is the verification — if the URL ever drifts, the next fact-check that touches it will surface it.

See `references/verification-rules.md` → "When the archive and the live source disagree" for how divergences interact with re-ingest recommendations.

### Step 3: Verify Each Claim

For each claim + source pair, determine whether the source contains evidence supporting the specific claim.

**This is semantic verification, not string matching.** The article may phrase things differently than the source. "57.2 trillion won" should match "57.2 trillion won ($37.92 billion)" even if the surrounding words differ. "8.5x jump" should match "more than eightfold."

**Verification categories:**

| Category | Meaning | Action needed |
|---|---|---|
| **Verified** | Both archive and live source (or whichever was available) contain the claimed fact with matching or consistent figures | None |
| **Partially verified** | Source covers the topic but the specific figure or framing differs | Flag the discrepancy; recommend correction |
| **Not found in source** | Neither the live source nor the archive contains the claimed information | Recommend finding the correct source or removing the link |
| **Archive/source divergence** | Archive extract supports the claim but live source disagrees — *or vice versa* | See split-policy rules below; report both excerpts side-by-side |
| **Source inaccessible** | Could not fetch the URL live AND archive has no record (or live is the only available signal and failed) | Note failure reason; recommend manual verification |
| **Unsourced** | Factual claim with no inline link | Recommend adding a source or flagging as editorial judgment |

**Archive/source divergence — split-policy verdict:**

When the archive and the live source disagree on whether a claim is supported, the verdict depends on **what kind of claim it is**. Hard facts are decided by the live source because corrections and updates are usually authoritative. Prose-y claims (causal language, characterizations, framing) are surfaced without a verdict because prose drift is more ambiguous and often a judgment call the writer should make.

| Claim type | Verdict policy |
|---|---|
| Number, percentage, dollar figure, date, direct quote, named attribution | **Live wins.** Mark verified/unverified based on the live source. Flag the archive page as a candidate for re-ingestion in the report. |
| Causal language ("X triggered Y"), characterization ("a panic," "a collapse"), qualitative framing | **No verdict.** Report the archive excerpt and the live excerpt side-by-side. Recommend the writer decide whether the article phrasing, the archive, or the live page is the source of the divergence. |

In both cases, the divergence itself is surfaced prominently — even when "live wins" gives a clean verdict, the report records that the archive and live source disagreed, because that's a signal the archive may need a refresh.

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
**Verified:** [N] | **Partially verified:** [N] | **Not found in source:** [N] | **Archive/source divergence:** [N] | **Source inaccessible:** [N] | **Unsourced:** [N]
**Link health:** [N URLs OK] | [N redirected] | [N broken/inaccessible]

---

### Verified Claims

| # | Claim (from article) | Source | Cross-check | Status |
|---|---|---|---|---|
| 1 | [brief claim description] | [source name] | archive + live agree | ✓ Verified |
| 2 | ... | ... | live only (no archive) | ✓ Verified |

The "Cross-check" column records which signals agreed: `archive + live agree`, `archive only` (live unavailable), `live only` (no archive page), or `archive + live agree on hard fact` for divergence cases where live won cleanly.

---

### Flagged Claims

#### Claim #[N]: [brief description]
**Article says:** "[exact text from the draft]"
**Source says:** "[relevant passage from the source]"
**Discrepancy:** [what doesn't match and why it matters]
**Recommendation:** [specific fix — correct the figure / swap the source link / soften the claim]

[repeat for each flagged claim]

---

### Archive / Source Divergence

For each claim where the source archive extract and the live source disagreed. Hard-fact divergences include a verdict (live wins); prose divergences are surfaced without a verdict per the split policy in Step 3.

#### Claim #[N]: [brief description] — [hard fact | prose]
**Article says:** "[exact text from the draft]"
**Archive extract says:** "[relevant passage from archive/sources/...]" (ingested [date if available])
**Live source now says:** "[relevant passage from current live page]"
**Likely cause:** [source was edited or corrected | source was retracted | archive ingestion error | unclear]
**Verdict:** [✓ Verified against live / ✗ Not supported by live / ⚠ No verdict — writer judgment]
**Recommendation:** [correct the article to match live / re-ingest the archive page / flag for manual review]

[repeat for each divergence]

---

### Unsourced Claims

| # | Claim | Recommendation |
|---|---|---|
| 1 | [sentence with factual assertion but no link] | [add source / acceptable as editorial judgment] |

---

### Link Health

URL-level issues independent of content verification. Even when a claim verifies cleanly via the archive, a broken or redirected URL undermines reader trust and should be fixed.

| URL | Status | Issue | Recommendation |
|---|---|---|---|
| [URL] | 404 | Page no longer exists | Find replacement source or archive.org snapshot |
| [URL] | 301 → [new URL] | Redirects to unrelated page (was article, now section index) | Update link to the new article URL or use an archive snapshot |
| [URL] | 200 but title changed | Page title no longer matches the article's topic; may have been replaced | Spot-check manually; consider archive link |
| [URL] | timeout / paywall / JS-rendered | Live fetch failed; verification used source archive only | Manual verification recommended |

---

**Summary:** [one-paragraph assessment — overall sourcing quality, most critical issues to address, any archive pages flagged for re-ingestion, and whether the piece is ready to publish from a factual accuracy standpoint]
```

---

## Reference Files

- `references/verification-rules.md` — Detailed rules for claim classification, edge case handling, and the boundary between factual claims and editorial judgment
