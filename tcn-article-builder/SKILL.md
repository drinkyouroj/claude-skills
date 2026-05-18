---
name: tcn-article-builder
description: >
  End-to-end workflow orchestrator for The Civic Node Substack articles. Chains
  nine TCN skills in order — tcn-outline → tcn-outline-more → tcn-headline →
  tcn-opener → tcn-draft → tcn-readability → tcn-text-humanizer → tcn-fact-check
  ↔ tcn-fact-reconcile (loop) → final read-through. Pauses after every step for
  user approval. Detects existing workflow artifacts and offers to resume from
  the furthest completed step. ALWAYS invoke this skill when Justin wants to
  build a full TCN article from a wiki synthesis page — including phrases like
  "build an article from this synthesis", "run the article workflow", "let's
  write the next piece", "from outline through publish", "full article
  workflow", "tcn-article-builder", "let's do a piece on X" with a synthesis
  reference, or any variant of "turn this synthesis into an article". Also
  trigger when Justin points at a file under wiki/syntheses/ and asks to write
  it up, or when Justin says he wants to resume a partially-built article.
  Does NOT apply to single-step invocations (those go directly to tcn-outline,
  tcn-headline, etc.), social posts (tcn-post), Substack Notes
  (tcn-substack-notes), or daily content planning (tcn-content-plan).
---

# The Civic Node — Article Builder (Workflow Orchestrator)

## What this skill does

Runs the full Civic Node article workflow from wiki synthesis to publish-ready draft. Calls each of the nine underlying TCN skills via the Skill tool, presents output, waits for user approval, and threads state forward to the next step.

The point of this skill is to reduce the cognitive load of running nine sequential skills by hand — remembering which one runs next, what inputs to pass, where to save outputs, when to loop, and which version of the draft is the canonical "current" version. It does **not** replace the underlying skills' judgment; it sequences them.

## Sequence at a glance

| # | Step | Skill invoked | Output artifact (under `workspace/drafts/<slug>/`) | User gate |
|---|------|---------------|-----------------------------------------------------|-----------|
| 0 | Pre-flight | (this skill) | `manifest.md` | Confirm synthesis page + ready to start |
| 1 | Outline | `tcn-outline` | `01-outline.md` | Approve or redirect |
| 2 | Detailed outline | `tcn-outline-more` | `02-outline-detailed.md` | Approve or redirect |
| 3 | Headlines | `tcn-headline` | `03-headlines.md` | Pick one + supply slug |
| 4 | Opener variants | `tcn-opener` | `04-opener.md` | Pick one variant |
| 5 | Draft (with locked opener) | `tcn-draft` | `05-draft-v1.md` | Approve or redirect |
| 6 | Readability audit | `tcn-readability` | `06-readability.md` + `05-draft-v2.md` after applying | Approve rewrites |
| 7 | Voice humanizer | `tcn-text-humanizer` | `05-draft-v3.md` | Approve rewrites |
| 8 | Fact check | `tcn-fact-check` | `08-fact-check-v{N}.md` | Approve recommendations |
| 9 | Fact reconcile | `tcn-fact-reconcile` | `05-draft-v{N+1}.md` | Approve (loop back to 8 until clean or stuck) |
| 10 | Final read-through | (this skill) | `manifest.md` marked `ready-to-publish` | Confirm ship-ready |

Steps 8 and 9 loop. Termination: the loop stops when fact-check reports zero flagged claims, OR when two consecutive iterations surface the same set of unresolved items (no progress).

---

## Pre-flight: voice file dependency check

**Before doing anything else**, verify `workspace/core/anti-ai-writing-style.md` exists in the active project. Every voice-aware step in the chain (tcn-outline-more, tcn-opener, tcn-draft, tcn-readability, tcn-text-humanizer) depends on this file. With it missing, the underlying skills fall back to "structural-only" mode, which produces a draft without voice calibration — exactly the failure mode this workflow exists to prevent.

If the file is missing, halt immediately:

> Voice canonical file not found at `workspace/core/anti-ai-writing-style.md`. The article-builder workflow depends on this file being present so each voice-aware step can resolve banned vocabulary, vocabulary cliff rules, closing-line abstraction, and AI-tell patterns at runtime. Restore the file before running this workflow.

Do not proceed to outline or any later step. The cost of running an 8-step chain and discovering at the end that voice was silently skipped is higher than the cost of stopping at second 1.

---

## Resume detection

After the voice-file check passes, scan `workspace/drafts/` for existing workflow directories that look like in-progress articles. Each workflow directory contains a `manifest.md` with status, slug, and step-completion checklist.

If one or more workflows are in progress, present them to the user:

> Found in-progress articles in `workspace/drafts/`:
>
> 1. `the-71-billion-bluff/` — currently at step 7 (humanizer), last touched 2026-05-17
> 2. `samsung-fab-power-deal/` — currently at step 3 (headlines), last touched 2026-05-15
>
> Resume one of these, or start a new article?

If the user picks an in-progress article, read its manifest to determine the current step, summarize what's done, and ask whether to resume from there or rewind to an earlier step.

If the user picks "start new" (or no workflows are in progress), proceed to seed input.

---

## Seed input

The workflow always starts from a wiki synthesis page. Ask:

> Which synthesis page is this article built from? (Path under `wiki/syntheses/`, or paste the contents.)

Validate the input:
- If the user supplies a path, confirm the file exists. If not, ask again.
- If the user pastes contents directly, that's fine — save to a temp location and reference it.
- If the user is uncertain, list the most-recent 5 files in `wiki/syntheses/` and offer to pick one.

Once the synthesis is locked, set up the workflow directory with a **temp slug** derived from the synthesis filename — e.g., `workspace/drafts/wip-elasticity-policy-2026-05-18/`. The real slug arrives after step 3 (headline approval); pre-headline artifacts get renamed at that point.

Create `manifest.md` (see "Manifest format" below) and write the synthesis reference into it.

---

## The per-step loop

Every step in the workflow follows the same pattern. Internalize this once and apply it across all 9 steps + the final gate:

1. **Announce.** Tell the user which step is starting and what the expected output is. One sentence.
2. **Invoke the underlying skill** via the Skill tool. Pass the inputs that step needs (see per-step specifics below). Do not freehand the work — every step is a delegation to a specialized skill.
3. **Save the output** to the appropriate artifact filename in the workflow directory.
4. **Update the manifest** — mark the step's checkbox, write the artifact filename, timestamp it.
5. **Present the output** to the user and ask for approval. Use the per-step gate prompt (see specifics).
6. **Branch on the user's response:**
   - **Approve** → continue to the next step.
   - **Redirect** ("try again with X different", "make it more Y") → re-invoke the underlying skill with the redirect baked into the prompt. Loop until approve.
   - **Cancel / pause** → save state, mark manifest as paused, tell user how to resume.

The user's approval gate is the workflow's primary correctness mechanism. Do not skip it. Do not infer approval from silence.

---

## Per-step specifics

### Step 1 — tcn-outline

**Inputs:** the synthesis page (path or contents), plus any user-supplied steering ("focus on the labor angle", "this is a Pattern Report").

**Output artifact:** `01-outline.md`

**Gate prompt:** "Outline complete. Approve, redirect (e.g., 'rework the template choice'), or cancel?"

**Redirect handling:** If the user wants a different template or viral trigger, re-invoke tcn-outline with the same synthesis plus the steering. Save successive outline drafts as `01-outline-v2.md`, etc., but keep only the approved one as the canonical `01-outline.md`.

### Step 2 — tcn-outline-more

**Inputs:** the approved `01-outline.md`. Pass it as the input to tcn-outline-more.

**Output artifact:** `02-outline-detailed.md`

**Gate prompt:** "Detailed outline complete. Marcus pre-assessment and accessibility pre-check are both included. Approve, redirect, or cancel?"

### Step 3 — tcn-headline (then capture slug)

**Inputs:** the approved `01-outline.md` and `02-outline-detailed.md`. tcn-headline only needs the outline, but pass both so it can draw on the sharper claims surfaced by outline-more.

**Output artifact:** `03-headlines.md` (the three headline + subheadline options)

**Gate prompt:** "Three headline options presented. Pick A, B, or C (or redirect)."

**After selection:** capture the picked headline into the manifest. Then ask for the slug:

> Headline locked: "[selected headline]". What slug should I use for the final filename? (e.g., `the-71-billion-bluff` for `workspace/drafts/the-71-billion-bluff/draft-final.md`.)

Once the user supplies a slug:
1. Validate it (lowercase, kebab-case, no slashes; auto-clean if needed and show the cleaned version for confirmation).
2. **Rename the workflow directory** from `wip-<temp-slug>/` to `<real-slug>/`.
3. Update the manifest with the real slug.

### Step 4 — tcn-opener

**Inputs:** the approved outline (`01-outline.md`), detailed outline (`02-outline-detailed.md`), and the locked headline + subheadline. Invoke tcn-opener in **generate mode** to produce two variants.

**Output artifact:** `04-opener.md` (the two variants plus opener-close contract for each)

**Gate prompt:** "Two opener variants presented. Pick A or B (or redirect for new variants)."

**After selection:** capture the picked opener into the manifest. The opener is now locked — step 5 will use it verbatim, not regenerate.

### Step 5 — tcn-draft (with locked opener)

**Inputs:** the approved outline, detailed outline, headline + subheadline, AND **the locked opener from step 4**. Invoke tcn-draft with the locked opener supplied as an explicit input, with the instruction: "Use this opener verbatim as the article's opening paragraph(s). Do not regenerate. Build the rest of the draft around it according to the outline and detailed outline."

This is the "locked-opener handoff" — see the "Locked-opener contract with tcn-draft" section near the bottom for the contract details. tcn-draft's SKILL.md has been updated to honor this input.

**Output artifact:** `05-draft-v1.md`

**Gate prompt:** "Full draft complete (~[X] words). Approve to proceed to readability/voice/fact passes, or redirect a specific section?"

**Redirect handling:** if the user wants a section rewritten, re-invoke tcn-draft with the steering ("rewrite the Source Code section to be sharper on the buyer/seller asymmetry"). The redirect should be narrow — full draft rewrites are rare.

### Step 6 — tcn-readability

**Inputs:** `05-draft-v1.md`. Invoke tcn-readability on the full draft.

**Output artifact:** `06-readability.md` (the audit report) and, if the user approves rewrites, `05-draft-v2.md` (draft with rewrites applied).

**Gate prompt:** "Readability audit complete. [N] top-comprehension-breaking violations flagged with rewrites. Apply the rewrites, skip them, or redirect specific ones?"

**Apply mechanics:** tcn-readability produces rewrites; the orchestrator (or a focused re-run of tcn-draft on a specific section, as readability recommends) is what applies them to the draft. Save the rewritten draft as `05-draft-v2.md` and update the manifest to point to v2 as the canonical current draft.

### Step 7 — tcn-text-humanizer

**Inputs:** the latest draft (`05-draft-v2.md` if step 6 produced rewrites, else `05-draft-v1.md`). Invoke tcn-text-humanizer.

**Output artifact:** `05-draft-v3.md` (humanizer rewrites prose in place; the version increments)

**Gate prompt:** "Humanizer pass complete. [N] passages rewritten. Approve, review specific rewrites, or redirect?"

**Why this comes after readability:** structural cuts (step 6) can eliminate sentences humanizer would have rewritten — running readability first avoids wasted lexical polish on prose that gets cut. This matches the order asserted by tcn-draft's "Workflow Position and Companion Skills" section and tcn-readability's "Related Skills" section.

### Step 8 ↔ Step 9 — tcn-fact-check ↔ tcn-fact-reconcile loop

**Why this comes last:** every voice/density rewrite that touched a fact-bearing sentence is now subject to source verification. Running fact-check after all voice work catches any subtle drift introduced by humanizer or readability rewrites (a number rephrased, an attribution dropped, a causal claim sharpened beyond what the source supports).

**Loop structure:**

1. **Run tcn-fact-check** on the current canonical draft (`05-draft-v{latest}.md`). Save report as `08-fact-check-v1.md` on first iteration, `v2`, `v3`, ... on subsequent iterations.
2. **Gate:** "Fact check complete. [N] verified, [M] flagged. Review the flagged claims — approve recommendations, override specific ones, or stop the loop here?"
3. If zero flagged, exit loop and proceed to step 10.
4. If the user approves the recommendations (or supplies overrides), **run tcn-fact-reconcile**. Pass it the current draft + the fact-check report (with any user overrides). Save the corrected draft as `05-draft-v{N+1}.md`.
5. **Gate:** "Reconcile complete. [count] corrections applied. Run fact-check again on the new draft?"
6. If user approves, loop back to step 1 with the new draft.

**Loop termination:**

- **Clean exit:** fact-check returns zero flagged claims. Proceed to step 10.
- **Stuck exit:** two consecutive fact-check iterations produce the same set of flagged claims (no progress). Halt the loop and surface to user: "Loop is stuck on the same [N] claims across the last 2 iterations. The likely causes are (a) primary source unavailable, (b) the claim can't be verified from any cite-able source, (c) the recommendation requires a manual call. Review the unresolved set and either accept them as editorial judgment or rework the prose to remove the dependency."
- **User override:** at any iteration, the user can say "stop the loop, ship as-is" or "stop, I want to rework this manually." Honor immediately.

Do **not** loop more than necessary. Each iteration costs source-fetches and tokens; the goal is convergence, not exhaustive coverage of every possible recommendation.

### Step 10 — Final read-through gate

The previous nine steps caught structural, lexical, and factual issues each at their own level. None of them caught "does this feel like a complete piece when read end-to-end as Marcus would read it." That's the read-through gate's job.

Present the final draft to the user with this prompt:

> Final draft is `workspace/drafts/<slug>/05-draft-v{latest}.md`. Read the whole thing as Marcus would — opener through close, no skimming. The audits caught structural, lexical, and factual issues, but they can't tell you whether the piece *feels* finished. Anything remaining to fix before this ships?

If the user says ship, update the manifest to `status: ready-to-publish` and announce the workflow is complete. If the user flags any specific issue, ask which step they want to revisit (rerun readability on the post-humanizer version? rerun humanizer on a specific section? do a manual edit then loop fact-check again?). Route accordingly.

---

## Manifest format

Each workflow directory contains a `manifest.md` that tracks state. It's human-readable so the user can scan it directly, and machine-parseable enough that resume detection can find the current step.

```markdown
# <Working title or "Untitled until headline">

**Synthesis source:** wiki/syntheses/<file>.md
**Slug:** <real slug if set, else "(temp: wip-...)">
**Status:** in-progress | paused | ready-to-publish
**Last touched:** 2026-05-18T15:45 ET
**Current step:** 7 of 10 (humanizer)

## Step progress

- [x] 1. tcn-outline → 01-outline.md (approved 2026-05-18T14:10)
- [x] 2. tcn-outline-more → 02-outline-detailed.md (approved 2026-05-18T14:35)
- [x] 3. tcn-headline → 03-headlines.md (selected: Option B — "The IOU That Broke the Memory Market"; slug locked: the-iou-that-broke-the-memory-market)
- [x] 4. tcn-opener → 04-opener.md (selected: Variant A — Analogy That Narrows)
- [x] 5. tcn-draft → 05-draft-v1.md (approved 2026-05-18T15:20; 2400 words)
- [x] 6. tcn-readability → 06-readability.md, applied to 05-draft-v2.md (approved 2026-05-18T15:38)
- [x] 7. tcn-text-humanizer → 05-draft-v3.md (approved 2026-05-18T15:45)
- [ ] 8. tcn-fact-check → pending
- [ ] 9. tcn-fact-reconcile → pending
- [ ] 10. final read-through → pending

## Fact-check loop history (filled in during steps 8–9)

| Iteration | Flagged before | Flagged after reconcile | Outcome |
|-----------|----------------|--------------------------|---------|
| 1         | -              | -                        | -       |

## Notes
<free-form notes captured during the workflow — user steering, decisions, source gaps surfaced>
```

The manifest is updated at the end of every step. Resume detection works by reading the manifest and finding the first unchecked step.

---

## Versioning conventions

- Outline / detailed-outline / headlines / opener artifacts (`01-` through `04-`) are single-version. If the user redirects, the new version overwrites — the workflow only keeps the approved version. Pre-approval scratch versions can be saved as `01-outline-v2.md`, `01-outline-v3.md`, etc., but the canonical `01-outline.md` is always the approved one.
- Draft artifacts (`05-draft-v{N}.md`) are multi-version. Every transformation produces a new version:
  - v1 = output of tcn-draft (step 5)
  - v2 = after readability rewrites applied (step 6)
  - v3 = after humanizer rewrites applied (step 7)
  - v4, v5, ... = after each fact-reconcile pass (steps 8–9 loop)
- The manifest's "current step" plus the latest `05-draft-v{N}.md` is always the canonical state. Older versions are kept so the user can diff or revert.

---

## Locked-opener contract with tcn-draft

In the workflow, tcn-opener (step 4) runs before tcn-draft (step 5). Without an explicit contract, tcn-draft would regenerate its own opener from the outline strategy and the work from step 4 would be wasted — or worse, would silently disagree with the drafted opener that's about to be replaced.

To fix this, tcn-draft's SKILL.md has been updated to accept an optional **locked opener** input. When that input is provided, tcn-draft uses it verbatim as the article's opening paragraph(s) and builds the rest of the article around it.

This orchestrator MUST pass the locked opener to tcn-draft in step 5. The invocation prompt should include:

> Locked opener (use verbatim — do not regenerate):
> ```
> <opener text from step 4>
> ```
> Build the rest of the draft from `02-outline-detailed.md`, treating the locked opener as the opening paragraph(s) and the close as the callback to it. Run the opener-close contract from step 4 — the close must return to the locked opener's image/fact/tension.

The locked-opener contract is also documented on the tcn-draft side. If tcn-draft is ever invoked without a locked opener (e.g., single-step use), it falls back to its standard behavior of generating an opener from outline strategy.

---

## Failure modes and fallbacks

**Synthesis page missing or unreadable.** The workflow can't start without it. Surface the failure and ask the user to fix the file or pick a different synthesis.

**Voice canonical file missing.** Halt before step 1 (see pre-flight check). Do not proceed.

**An underlying skill returns an error or refuses to run.** Capture the error, surface it to the user, and ask whether to retry, skip the step (with a documented gap in the manifest), or cancel the workflow.

**User cancels mid-workflow.** Update the manifest to `status: paused` and tell the user the workflow can be resumed by re-invoking this skill (resume detection will find it).

**Fact-check loop stuck.** Already handled in the step-8/9 specifics — surface the unresolved set and ask for editorial judgment.

**Manifest corruption.** If the manifest file is missing fields or malformed, surface to the user and ask what state the workflow is actually in. Do not guess.

---

## What this skill is NOT

- **Not a replacement for the underlying skills.** Every actual writing/editing decision is made by tcn-outline, tcn-outline-more, etc. This skill sequences them and tracks state.
- **Not a way to skip user approval.** Every step gate is mandatory. The point of a 9-step orchestration is that the user reviews 9 outputs, not 1.
- **Not for single-step work.** If the user wants just an outline, they should invoke tcn-outline directly. This skill is the full chain.
- **Not for non-article content.** Social posts go through tcn-post, Substack Notes through tcn-substack-notes, daily content plans through tcn-content-plan. None of those use this orchestrator.

---

## Companion skills (the chain)

In invocation order:

- **tcn-outline** — research, template selection, viral trigger, bullet-point outline (Step 1 of 3 in the underlying skill numbering)
- **tcn-outline-more** — paragraph-level expansion, accessibility pre-check, Marcus pre-assessment (Step 1b)
- **tcn-headline** — three headline + subheadline options (Step 2 of 3)
- **tcn-opener** — two opener variants with opener-close contracts
- **tcn-draft** — full prose draft (Step 3 of 3) — accepts locked-opener input from step 4
- **tcn-readability** — post-draft density audit (paragraph length, grounding, statistics, rhythm, sentence drag)
- **tcn-text-humanizer** — post-draft lexical AI-tell pass, calibrated to Justin's voice
- **tcn-fact-check** — source verification of every factual claim
- **tcn-fact-reconcile** — applies fact-check corrections, produces next draft version

All voice-aware skills in this chain load `workspace/core/anti-ai-writing-style.md` at runtime as their canonical source for vocabulary, banned words, negative parallelisms, vocabulary cliff, closing-line abstraction, and AI-tell patterns. The pre-flight check exists to ensure that file is present before the chain starts.
