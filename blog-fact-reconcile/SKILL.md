---
name: blog-fact-reconcile
description: >
  Apply fact-check corrections to a blog article draft, producing the next clean version. Invoke this
  skill after a blog-fact-check report has been generated — including phrases like "reconcile the
  fact check", "apply the corrections", "fix the sourcing", "write the next version", "reconcile
  this", or when the user reviews a fact-check report and says to proceed with fixes. Requires
  two inputs: the current draft and the fact-check report. Does NOT apply to writing new content,
  outlining, headline generation, or other pipeline steps.
---

# Blog — Fact Reconciliation (Post-Check Correction)

## Profile resolution

Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else.

Loads: active preset (to check step-disable flags).

---

## DISABLE-GUARD CONTRACT

**If the active profile disables this step (`profile.yaml` key `steps.fact-reconcile: false`), this skill is a NO-OP.**

- When invoked via the **orchestrator**, the orchestrator must check the preset's `steps` block and skip this skill entirely if `steps.fact-reconcile` is `false`. The skill is not called; nothing runs.
- When invoked **standalone** (direct `/blog-fact-reconcile` call) under a profile that has `steps.fact-reconcile: false` (e.g. a fiction or creative preset), the skill must detect this condition, print a single notice — "Fact-reconcile is disabled for this profile (`steps.fact-reconcile: false`). This skill is a no-op under the active preset. Remove or set `steps.fact-reconcile: true` to enable." — and stop. It must not run any reconciliation logic.

This guard exists because some content profiles (fiction, creative writing, satire) have no factual sourcing requirement. Running fact-reconcile against them would generate false positives and wasted work.

---

## What This Skill Does

Takes a fact-check report and the draft it was run against, applies every correction from the report, and writes the next version of the draft as a clean file. No triage, no intermediate step — the fact-check report is the correction plan. The output is the next draft version.

---

## Why This Is a Separate Skill

The fact-checker identifies problems. The reconciler fixes them. Keeping these separate means:
1. The user reviews the fact-check report and can override or adjust recommendations before invoking this skill
2. The reconciler can be re-run if the user makes manual edits and wants a clean pass
3. The correction logic is focused — it doesn't re-draft or re-voice, it fixes sourcing

---

## Inputs

The skill requires two inputs present in the conversation or referenced by file path:

1. **The current draft** — the markdown file that was fact-checked (e.g., `drafts/article-slug-v7.md`)
2. **The fact-check report** — the output of blog-fact-check, containing verified claims, flagged claims with recommendations, unsourced claims, and source accessibility issues

If either input is missing, ask the user to provide it before proceeding.

---

## The Process

### Step 1: Read Both Inputs

Read the current draft and the fact-check report. For each item in the report, classify the required action:

| Action type | What it means | Example |
|---|---|---|
| **Swap link** | Claim is correct but linked to the wrong source | Percentage stat linked to a secondary aggregator; should link to the primary research report |
| **Fix link** | URL is broken, generic, or doesn't resolve | Generic domain URL → specific article URL |
| **Correct figure** | Number in article doesn't match source | "8-9%" → "6-8%" per the primary source |
| **Add context** | Claim needs a qualifier the source provides | "6-8% in the pessimistic scenario" |
| **Add link** | Unsourced factual claim needs an inline source | Dollar figure needs link to the originating report |
| **Rewrite claim** | Claim as stated isn't supported; needs rephrasing | Attribute statement to match what the primary source actually records |
| **No action** | Verified, or acceptable editorial judgment | Analysis, personal reflection, derived math |

### Step 2: Apply Corrections

Work through the draft top to bottom:

1. For each flagged item, apply the fact-check report's recommendation:
   - **Swap link / Fix link**: Replace the URL in the inline link; keep the linked text unless it also needs updating
   - **Correct figure**: Update the number and its inline link if the source changes
   - **Add context**: Insert the qualifier naturally into the sentence — don't make it read like a footnote was crammed in
   - **Add link**: Choose 2-4 words in the existing sentence and wrap them in a link — follow the inline sourcing convention established in the active profile's `templates.md`
   - **Rewrite claim**: Rephrase the sentence to match what the source actually says; preserve the article's voice and flow (see active profile's `voice.md`)
2. Do NOT change anything the fact-check report didn't flag — this is a correction pass, not a rewrite
3. If the fact-check report says "recommend finding the correct source" and the correct source URL is not available, leave a visible placeholder (`[NEEDS SOURCE]`) in the draft rather than guessing or using a generic link

### Step 3: Source Archive Audit

Before writing the new draft, verify that **every URL linked in the article** exists in the source archive — either as an ingested source page (check `source_url` in frontmatter) or as a raw file awaiting ingestion.

The source archive location comes from `profile.yaml.paths.source` (the active profile's configured seed/source path).

For each linked URL:
1. Search the source archive for a page whose `source_url` matches the URL
2. If not found in ingested sources, check the `raw/` directory for a file whose frontmatter `source:` field matches the URL
3. If the URL exists in neither location:
   - Create a minimal raw file in `raw/` with frontmatter containing the `source:` URL, author, and publication date
   - Add it to the **archive audit** section of the reconciliation summary so the user knows it needs full ingestion later

This ensures the source archive is a complete record of every source ever cited in a published piece. No article goes out with a source link that isn't tracked in the archive.

**Output for this step:** A list of all linked URLs with their archive status (ingested / raw only / newly created raw file).

### Step 4: Write the New Draft

Save the corrected and archive-audited draft as a new version file using the workspace path from `profile.yaml.paths.workspace` (default: `./drafts/`): `[workspace]/[slug]-v[N+1].md`

Update the frontmatter:
- `version:` incremented
- `created:` today's date
- `status: review`

Update the draft notes at the bottom with a reconciliation summary:

```
**Reconciliation (vN → vN+1):**
- Corrections applied: [N]
- Links swapped: [list]
- Links fixed: [list]
- Figures corrected: [list]
- Context added: [list]
- Links added: [list]
- Claims rewritten: [list]
- Skipped / unresolved: [list, with reasons]
- Archive audit: [N] sources linked, [N] already ingested, [N] in raw/ only, [N] new raw files created
  - New raw files: [list of filenames created — these need full ingestion]
```

This summary should make it possible to understand every change without diffing the two files.

---

## Source Authority Rules

Every inline link in a published article must point to a **primary or authoritative source**. The source archive is a research tool, not a publication-grade source library — many archive entries are secondary sources (blog posts, video transcripts, aggregator posts) that summarize primary reporting. The article must link to the primary reporting, not to the summary.

### Source hierarchy (use the highest tier available)

| Tier | Source type | Examples | Use in articles? |
|---|---|---|---|
| **1 — Primary** | Official statements, press releases, earnings calls, government data, academic papers, company filings | The organization's own press release, an investor relations page, government statistical agency data, an academic journal article | Always preferred |
| **2 — Authoritative reporting** | Major news outlets with original reporting and editorial standards | Established wire services, major financial press, leading trade publications in the blog's domain | Yes — when primary source is paywalled or unavailable |
| **3 — Credible secondary** | Established outlets reporting from primary sources | Well-regarded domain-specific outlets, reputable tech or industry media | Acceptable if Tier 1-2 unavailable; verify the claim against their cited source |
| **4 — Non-authoritative** | Blogs, YouTube channels, Medium posts, aggregator sites, forums | Personal blogs, fan channels, random Medium articles, Reddit | **Never link in published articles.** Use only as research leads to find Tier 1-2 sources |

The blog's subject domain (from `identity.md` / `quick.domain`) determines which specific outlets fall into each tier for that domain. The tier descriptions above are domain-neutral; apply them with domain knowledge from the profile.

### How to apply this during reconciliation

When the fact-check report recommends a source and that source is Tier 4:
1. Check the source archive page — what primary sources does it cite?
2. Search for the specific claim in Tier 1-2 outlets
3. If a Tier 1-2 source exists, use it. If only Tier 3 exists, use it with awareness.
4. If the claim can ONLY be sourced to a Tier 4 source (i.e., it's original reporting by a blogger/YouTuber, not aggregation), mark it `[NEEDS PRIMARY SOURCE]` in the draft

**Exception — quotable sources:** A Tier 4 source can be linked when it IS the content being referenced (e.g., linking to a post you're quoting, linking to a video you're citing as a primary artifact). The rule applies to factual claims, not to references to the source itself.

---

## General Rules

- **Preserve voice.** Every correction must read naturally in the author's voice (see active profile's `voice.md`). Don't insert academic sourcing language ("according to," "as reported by") — use the inline link convention and let the link do the attribution work.
- **Minimize diff.** Change only what the fact-check report flags. If a sentence is verified, don't touch it. If a paragraph has one bad link and four good ones, fix the one.
- **Don't resolve ambiguity yourself.** If a correct source URL isn't available, use `[NEEDS SOURCE]` or `[NEEDS PRIMARY SOURCE]` rather than guessing. The user will fill it in during their editorial pass.
- **Track every change.** The reconciliation summary in draft notes must account for every flagged item — applied, skipped, or unresolved.
- **One output.** The output is the new draft file. No triage tables, no intermediate approvals — the fact-check report already served that purpose.
