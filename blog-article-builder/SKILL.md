---
name: blog-article-builder
description: >
  End-to-end workflow orchestrator for blog articles. Sequences nine blog-*
  skills in order — blog-outline → blog-outline-more → blog-headline →
  blog-opener → blog-draft → blog-readability → blog-humanizer → blog-fact-check
  ↔ blog-fact-reconcile (loop) → final read-through. Pauses after every step for
  user approval. Detects existing workflow artifacts and offers to resume from
  the furthest completed step. Reads enabled steps from the active profile's
  preset + `profile.yaml.steps` overrides and skips disabled steps cleanly.
  Invoke when the user wants to build a full article from a source brief or
  notes file — including phrases like "build an article from this", "run the
  article workflow", "let's write a piece", "from outline through publish",
  "full article workflow", "blog-article-builder", "let's do a piece on X"
  with a source reference, or any variant of "turn this into an article". Also
  trigger when the user points at a source file and asks to write it up, or
  when the user says they want to resume a partially-built article. Does NOT
  apply to single-step invocations (those go directly to blog-outline,
  blog-headline, etc.) or to other content types handled by other skills.
---

# Blog Article Builder (Workflow Orchestrator)

## Profile resolution

Resolve the active blog profile per `~/.claude/blog-profiles/_resolution-contract.md` before doing anything else. The orchestrator resolves the profile **once** and passes the resolved profile reference and `quick.*` fields (brand, domain, platform) forward to each leaf-skill invocation as a hint. Each leaf skill still self-resolves per the contract — the hint is an optimization, not a bypass.

Loads: `profile.yaml` (for `paths.*`, `steps.*` overrides, and `preset`); `identity.md` (brand/platform context); the active preset (step defaults). Individual prose files (`voice.md`, `reader.md`, `templates.md`) are loaded by the leaf skills, not by this orchestrator.

---

## What this skill does

Runs the full blog article workflow from source brief to publish-ready draft. Calls each of the nine underlying `blog-*` skills via the Skill tool, presents output, waits for user approval, and threads state forward to the next step.

The point of this skill is to reduce the cognitive load of running nine sequential skills by hand — remembering which one runs next, what inputs to pass, where to save outputs, when to loop, and which version of the draft is the canonical "current" version. It does **not** replace the underlying skills' judgment; it sequences them.

Steps that are **disabled** in the active profile (via preset defaults or `profile.yaml.steps` overrides) are **skipped cleanly**: they are not invoked, the user is not asked to approve them, and the manifest records them as `skipped (profile)` rather than pending or failed.

---

## Sequence at a glance

| # | Step | Skill invoked | Output artifact (under working dir) | User gate |
|---|------|---------------|--------------------------------------|-----------|
| 0 | Pre-flight | (this skill) | `manifest.md` | Confirm source brief + ready to start |
| 1 | Outline | `blog-outline` | `01-outline.md` | Approve or redirect |
| 2 | Detailed outline | `blog-outline-more` | `02-outline-detailed.md` | Approve or redirect |
| 3 | Headlines | `blog-headline` | `03-headlines.md` | Pick one + supply slug |
| 4 | Opener variants | `blog-opener` | `04-opener.md` | Pick one variant |
| 5 | Draft (with locked opener) | `blog-draft` | `05-draft-v1.md` | Approve or redirect |
| 6 | Density/comprehension audit | `blog-readability` | `06-readability.md` + `05-draft-v2.md` after applying | Approve rewrites |
| 7 | Voice humanizer | `blog-humanizer` | `05-draft-v3.md` + `07-voice-audit.md` | Approve rewrites; audit verdict gates step 8 |
| 8 | Fact check | `blog-fact-check` | `08-fact-check-v{N}.md` | Approve recommendations |
| 9 | Fact reconcile | `blog-fact-reconcile` | `05-draft-v{N+1}.md` | Approve (loop back to 8 until clean or stuck) |
| 10 | Final read-through | (this skill) | `manifest.md` marked `ready-to-publish` | Confirm ship-ready |

Steps 8 and 9 loop. Termination: the loop stops when fact-check reports zero flagged claims, OR when two consecutive iterations surface the same set of unresolved items (no progress).

Steps disabled by the active profile (e.g. `fact-check` and `fact-reconcile` off under a fiction preset) are marked `skipped (profile)` in the manifest and do not block progress.

---

## Pre-flight: profile resolve + dependency check

**Before doing anything else**, verify two things:

1. **The active profile resolves successfully.** Run the resolution contract. If profile resolution fails (no profile found, required file missing), halt immediately and surface which file failed. Do not fall back to a hard-coded identity.

2. **The files required by enabled steps exist.** Read the enabled-steps list from the preset + `profile.yaml.steps` overrides, then check:
   - `voice.md` is present in the active profile (required by any voice-aware step: `blog-outline-more`, `blog-opener`, `blog-draft`, `blog-readability`, `blog-humanizer`). If any of these steps are enabled and `voice.md` is missing, halt.
   - `templates.md` is present in the active profile (required by `blog-outline`, `blog-outline-more`). If these steps are enabled and `templates.md` is missing, halt.
   - `reader.md` is present (required by `blog-outline-more` and `blog-draft`). Same logic.
   - If a step is disabled, its required files do not need to exist.

If any enabled-step dependency is missing, halt immediately:

> Pre-flight failed: [file] not found in the active profile. [Step name] requires this file. Restore it before running this workflow, or disable [step name] in `profile.yaml.steps`.

The cost of running an 8-step chain and discovering mid-chain that a required file was silently missing is higher than the cost of stopping at second 1.

---

## Resume detection

After the pre-flight check passes, scan the working directory (default `./drafts/`, or `profile.yaml.paths.workspace` if set) for existing workflow directories that look like in-progress articles. Each workflow directory contains a `manifest.md` with status, slug, and step-completion checklist.

If one or more workflows are in progress, present them to the user:

> Found in-progress articles in `./drafts/`:
>
> 1. `the-memory-market-gap/` — currently at step 7 (humanizer), last touched 2026-05-17
> 2. `power-deal-deep-dive/` — currently at step 3 (headlines), last touched 2026-05-15
>
> Resume one of these, or start a new article?

If the user picks an in-progress article, read its manifest to determine the current step, summarize what's done, and ask whether to resume from there or rewind to an earlier step.

If the user picks "start new" (or no workflows are in progress), proceed to seed input.

---

## Seed input

The workflow starts from a **source brief** — the research, notes, or synthesis the article is built from. This is more flexible than a single mandatory file format: accept any of:

- A **topic line** ("I want to write about X") — valid if the user wants to start from scratch or a mental concept only
- A **file path** to a source document (notes, research brief, interview transcript, synthesis file, or any other structured input)
- **Pasted content** directly into chat

Default lookup location: `profile.yaml.paths.source` (if set in the active profile). If `paths.source` is configured, check it first before asking.

Ask:

> What is this article built from? (Paste content, supply a file path, or describe the topic. Default source folder: `<profile.yaml.paths.source or ./notes/>`.)

Validate the input:
- If the user supplies a path, confirm the file exists. If not, ask again.
- If the user pastes content directly, save to a temp location and reference it.
- If the user is uncertain, list the 5 most-recently modified files in `profile.yaml.paths.source` (or `./notes/` as fallback) and offer to pick one.
- A bare topic line is acceptable — record it in the manifest as `seed: (topic line) "<topic>"` and pass it forward to each leaf skill as the starting brief.

Once the seed is locked, set up the workflow directory with a **temp slug** derived from the seed — e.g., `./drafts/wip-elasticity-policy-2026-05-18/` (or under `profile.yaml.paths.workspace` if set). The real slug arrives after step 3 (headline approval); pre-headline artifacts get renamed at that point.

Create `manifest.md` (see "Manifest format" below) and write the seed reference into it.

---

## The per-step loop

Every **enabled** step in the workflow follows the same pattern:

1. **Check if the step is enabled.** Before invoking any leaf skill, look up `steps.<step-name>` in the resolved preset (with `profile.yaml.steps` overrides applied). If the step is disabled (`false`), mark it `skipped (profile)` in the manifest, announce to the user ("Step [N] — [step name] is disabled for this profile; skipping."), and advance to the next step. Do not invoke the skill. Do not ask for approval.
2. **Announce.** Tell the user which step is starting and what the expected output is. One sentence.
3. **Invoke the underlying skill** via the Skill tool. Pass the resolved profile reference + `quick.*` fields plus the step-specific inputs. Do not freehand the work — every step is a delegation to a specialized skill.
4. **Save the output** to the appropriate artifact filename in the workflow directory.
5. **Update the manifest** — mark the step's checkbox, write the artifact filename, timestamp it.
6. **Present the output** to the user and ask for approval. Use the per-step gate prompt (see specifics).
7. **Branch on the user's response:**
   - **Approve** → continue to the next step.
   - **Redirect** ("try again with X different", "make it more Y") → re-invoke the underlying skill with the redirect baked into the prompt. Loop until approve.
   - **Cancel / pause** → save state, mark manifest as paused, tell user how to resume.

The user's approval gate is the workflow's primary correctness mechanism. Do not skip it for enabled steps. Do not infer approval from silence.

---

## Per-step specifics

### Step 1 — blog-outline

**Inputs:** the seed source (path or contents), plus any user-supplied steering ("focus on the technical angle", "use a comparison structure").

**Output artifact:** `01-outline.md`

**Gate prompt:** "Outline complete. Approve, redirect (e.g., 'rework the structure choice'), or cancel?"

**Redirect handling:** If the user wants a different structure or angle/hook, re-invoke `blog-outline` with the same seed plus the steering. Save successive outline drafts as `01-outline-v2.md`, etc., but keep only the approved one as the canonical `01-outline.md`.

### Step 2 — blog-outline-more

**Inputs:** the approved `01-outline.md`. Pass it as the input to `blog-outline-more`.

**Output artifact:** `02-outline-detailed.md`

**Gate prompt:** "Detailed outline complete. Reader-persona pre-assessment and accessibility pre-check are both included. Approve, redirect, or cancel?"

### Step 3 — blog-headline (then capture slug)

**Inputs:** the approved `01-outline.md` and `02-outline-detailed.md`. `blog-headline` only needs the outline, but pass both so it can draw on the sharper claims surfaced by outline-more.

**Output artifact:** `03-headlines.md` (the three headline + subheadline options)

**Gate prompt:** "Three headline options presented. Pick A, B, or C (or redirect)."

**After selection:** capture the picked headline into the manifest. Then ask for the slug:

> Headline locked: "[selected headline]". What slug should I use for the final filename? (e.g., `the-memory-market-gap` for `./drafts/the-memory-market-gap/draft-final.md`.)

Once the user supplies a slug:
1. Validate it (lowercase, kebab-case, no slashes; auto-clean if needed and show the cleaned version for confirmation).
2. **Rename the workflow directory** from `wip-<temp-slug>/` to `<real-slug>/`.
3. Update the manifest with the real slug.

### Step 4 — blog-opener

**Inputs:** the approved outline (`01-outline.md`), detailed outline (`02-outline-detailed.md`), and the locked headline + subheadline. Invoke `blog-opener` in **generate mode** to produce two variants.

**Output artifact:** `04-opener.md` (the two variants plus opener-close contract for each)

**Gate prompt:** "Two opener variants presented. Pick A or B (or redirect for new variants)."

**After selection:** capture the picked opener into the manifest. The opener is now locked — step 5 will use it verbatim, not regenerate.

### Step 5 — blog-draft (with locked opener)

**Inputs:** the approved outline, detailed outline, headline + subheadline, AND **the locked opener from step 4**. Invoke `blog-draft` with the locked opener supplied as an explicit input, with the instruction: "Use this opener verbatim as the article's opening paragraph(s). Do not regenerate. Build the rest of the draft around it according to the outline and detailed outline."

This is the "locked-opener handoff" — see the "Locked-opener contract with blog-draft" section below. `blog-draft`'s SKILL.md honors this input; when the locked opener is provided, it uses it verbatim as the article's opening paragraph(s) and builds the rest of the article around it. If `blog-draft` is ever invoked without a locked opener (single-step use), it falls back to its standard behavior of generating an opener from outline strategy.

**Output artifact:** `05-draft-v1.md`

**Gate prompt:** "Full draft complete (~[X] words). Approve to proceed to readability/voice/fact passes, or redirect a specific section?"

**Redirect handling:** if the user wants a section rewritten, re-invoke `blog-draft` with the steering ("rewrite the analysis section to be sharper on the core tension"). The redirect should be narrow — full draft rewrites are rare.

### Step 6 — blog-readability

**Inputs:** `05-draft-v1.md`. Invoke `blog-readability` on the full draft.

**Output artifact:** `06-readability.md` (the audit report) and, if the user approves rewrites, `05-draft-v2.md` (draft with rewrites applied).

**Gate prompt:** "Density/comprehension audit complete. [N] top-comprehension-breaking violations flagged with rewrites. Apply the rewrites, skip them, or redirect specific ones?"

**Apply mechanics:** `blog-readability` produces rewrites; the orchestrator (or a focused re-run of `blog-draft` on a specific section, as readability recommends) is what applies them to the draft. Save the rewritten draft as `05-draft-v2.md` and update the manifest to point to v2 as the canonical current draft.

### Step 7 — blog-humanizer

**Inputs:** the latest draft (`05-draft-v2.md` if step 6 produced rewrites, else `05-draft-v1.md`). Invoke `blog-humanizer`.

**Output artifact:** `05-draft-v3.md` (humanizer rewrites prose in place; the version increments). If step 7 must re-run because the first audit failed, save the re-humanized draft as `05-draft-v3-r1.md` and save the second audit as `07-voice-audit-r1.md` so the failing audit remains reviewable.

**Gate prompt:** "Voice humanizer pass complete. [N] passages rewritten. Voice audit verdict: [PASS/FAIL]. Approve, review specific rewrites, or redirect?"

**Voice audit record:** `blog-humanizer` ends with a self-audit of the final text against the profile's `voice.md` and emits a structured audit record with a terminal `Verdict: PASS | FAIL` line (see that skill's Step 4). The orchestrator saves that record as `07-voice-audit.md` alongside `05-draft-v3.md` (the `NN-` numbering is this orchestrator's convention — the leaf skill emits the record inline) and records both artifacts in the manifest, including the verdict.

**Voice audit gate (step 7 → 8):** the audit verdict gates entry to the fact-check loop.

- **PASS** → proceed to steps 8–9 as normal. STRONG/LIGHT findings and the recognizability-judge result are surfaced at the gate for the user's information; they do not block.
- **Missing or unparseable verdict** → treat exactly like a blocking failure: do **not** enter fact-check. Set manifest `status: blocked (voice audit)`, leave step 7 unchecked, and surface that no valid audit verdict was produced.
- **FAIL** (at least one residual HARD violation) → do **NOT** enter the step 8–9 fact-check loop. Re-invoke `blog-humanizer` **once**, passing the residual-violation list from the audit record as explicit steering ("fix exactly these residual HARD violations"). Keep the first failed audit as `07-voice-audit.md`, save the re-humanized draft as `05-draft-v3-r1.md`, and save the second audit as `07-voice-audit-r1.md`; never overwrite the FAIL record.
  - If the re-audit returns **PASS**, proceed to step 8 with `05-draft-v3-r1.md` as the canonical current draft and record both audit artifacts in the manifest.
  - If the re-audit still returns **FAIL**, halt the workflow and surface to the user: set manifest `status: blocked (voice audit)` and list the residual HARD violations from both audit records. Never proceed to fact-check on a FAIL verdict, and never infer a PASS that the record does not state.

A workflow blocked here resumes at step 7 (re-humanize), never at step 8 — resume detection must treat the blocked state as "step 7 incomplete." Humanizer re-run artifact names use the `-r1` suffix so they cannot collide with fact-reconcile versions such as `05-draft-v4.md`.

**Why this comes after readability:** structural cuts (step 6) can eliminate sentences the humanizer would have rewritten — running readability first avoids wasted lexical polish on prose that gets cut. This matches the order asserted by `blog-draft`'s "Workflow Position and Companion Skills" section and `blog-readability`'s "Related Skills" section.

### Step 8 ↔ Step 9 — blog-fact-check ↔ blog-fact-reconcile loop

**Step enable check:** before starting this loop, confirm both `steps.fact-check` and `steps.fact-reconcile` are enabled in the active profile. If either is disabled, mark the affected step(s) as `skipped (profile)` in the manifest and proceed directly to step 10. If `fact-check` is enabled but `fact-reconcile` is disabled, run `blog-fact-check` but skip the reconcile leg; surface the fact-check report for manual action.

**Why this comes last:** every voice/density rewrite that touched a fact-bearing sentence is now subject to source verification. Running fact-check after all voice work catches any subtle drift introduced by the humanizer or readability rewrites (a number rephrased, an attribution dropped, a causal claim sharpened beyond what the source supports).

### Step 10 final voice gate

Before marking the manifest `ready-to-publish`, compare the latest draft after the step 8-9 fact-check/reconcile loop against the draft named in the most recent passing voice audit. If the latest draft differs, run one final voice audit on the latest draft. Save a passing final audit as `09-final-voice-audit.md`; save a failing, missing, or unparseable final-audit attempt as `09-final-voice-audit-fail.md` (or `09-final-voice-audit-fail-r{N}.md` for repeated attempts) so blocking evidence is never overwritten by a later PASS.

`ready-to-publish` requires `Verdict: PASS` from the final audit. If the final audit is `FAIL`, missing, or unparseable, set manifest `status: blocked (voice audit)`, list the residual HARD violations, and do not mark the Issue ready to publish. The manifest must make the remediation step the current unchecked step: leave step 9 unchecked if fact reconciliation introduced the violation and the next action is to revise the reconciled draft, or leave step 7 unchecked if broader humanizer work is needed. Step 10 remains pending until a draft change is made and a final audit passes. The manifest must name the remediation target so the next run does not retry the same failing final audit without a draft change.


**Loop structure:**

1. **Run `blog-fact-check`** on the current canonical draft (`05-draft-v{latest}.md`). Save report as `08-fact-check-v1.md` on first iteration, `v2`, `v3`, ... on subsequent iterations.
2. **Gate:** "Fact check complete. [N] verified, [M] flagged. Review the flagged claims — approve recommendations, override specific ones, or stop the loop here?"
3. If zero flagged, exit loop and proceed to step 10.
4. If the user approves the recommendations (or supplies overrides), **run `blog-fact-reconcile`**. Pass it the current draft + the fact-check report (with any user overrides). Save the corrected draft as `05-draft-v{N+1}.md`.
5. **Gate:** "Reconcile complete. [count] corrections applied. Run fact-check again on the new draft?"
6. If user approves, loop back to step 1 with the new draft.

**Loop termination:**

- **Clean exit:** fact-check returns zero flagged claims. Proceed to step 10.
- **Stuck exit:** two consecutive fact-check iterations produce the same set of flagged claims (no progress). Halt the loop and surface to user: "Loop is stuck on the same [N] claims across the last 2 iterations. The likely causes are (a) primary source unavailable, (b) the claim can't be verified from any cite-able source, (c) the recommendation requires a manual call. Review the unresolved set and either accept them as editorial judgment or rework the prose to remove the dependency."
- **User override:** at any iteration, the user can say "stop the loop, ship as-is" or "stop, I want to rework this manually." Honor immediately.

Do **not** loop more than necessary. Each iteration costs source-fetches and tokens; the goal is convergence, not exhaustive coverage of every possible recommendation.

### Step 10 — Final read-through gate

The previous enabled steps caught structural, lexical, and factual issues each at their own level. None of them caught "does this feel like a complete piece when read end-to-end as the blog's reader persona would read it." That's the read-through gate's job.

Present the final draft to the user with this prompt:

> Final draft is `<working-dir>/<slug>/05-draft-v{latest}.md`. Read the whole thing as the blog's reader persona would — opener through close, no skimming. The audits caught structural, lexical, and factual issues, but they can't tell you whether the piece *feels* finished. Anything remaining to fix before this ships?

If the user says ship, update the manifest to `status: ready-to-publish` and announce the workflow is complete. If the user flags any specific issue, ask which step they want to revisit (rerun readability on the post-humanizer version? rerun the humanizer on a specific section? do a manual edit then loop fact-check again?). Route accordingly.

---

## Manifest format

Each workflow directory contains a `manifest.md` that tracks state. It's human-readable so the user can scan it directly, and machine-parseable enough that resume detection can find the current step.

Disabled steps are recorded as `skipped (profile)` — they are not left blank or marked failed.

```markdown
# <Working title or "Untitled until headline">

**Seed source:** <file path or "(topic line) '<topic>'" or "(pasted content)">
**Profile:** <active profile name>
**Slug:** <real slug if set, else "(temp: wip-...)">
**Status:** in-progress | paused | blocked (voice audit) | ready-to-publish
**Last touched:** 2026-05-18T15:45
**Current step:** 7 of 10 (humanizer)

## Step progress

- [x] 1. blog-outline → 01-outline.md (approved 2026-05-18T14:10)
- [x] 2. blog-outline-more → 02-outline-detailed.md (approved 2026-05-18T14:35)
- [x] 3. blog-headline → 03-headlines.md (selected: Option B — "The IOU That Broke the Memory Market"; slug locked: the-iou-that-broke-the-memory-market)
- [x] 4. blog-opener → 04-opener.md (selected: Variant A — Analogy That Narrows)
- [x] 5. blog-draft → 05-draft-v1.md (approved 2026-05-18T15:20; 2400 words)
- [x] 6. blog-readability → 06-readability.md, applied to 05-draft-v2.md (approved 2026-05-18T15:38)
- [x] 7. blog-humanizer → 05-draft-v3.md, 07-voice-audit.md (verdict: PASS) (approved 2026-05-18T15:45)
- [ ] 8. blog-fact-check → pending
- [ ] 9. blog-fact-reconcile → pending
- [ ] 10. final read-through → pending; if step 9 changed the draft, run `09-final-voice-audit.md` before ready-to-publish

## Fact-check loop history (filled in during steps 8–9)

| Iteration | Flagged before | Flagged after reconcile | Outcome |
|-----------|----------------|--------------------------|---------|
| 1         | -              | -                        | -       |

## Notes
<free-form notes captured during the workflow — user steering, decisions, source gaps surfaced>
```

Example with a disabled step (fiction preset):

```markdown
- [x] 7. blog-humanizer → 05-draft-v3.md (approved 2026-05-18T15:45)
- [-] 8. blog-fact-check → skipped (profile)
- [-] 9. blog-fact-reconcile → skipped (profile)
- [ ] 10. final read-through → pending
```

The manifest is updated at the end of every step. Resume detection works by reading the manifest and finding the first unchecked (or not-skipped) step. A manifest with `status: blocked (voice audit)` leaves step 7 unchecked (the humanizer pass is not complete until its audit passes), so resume lands at step 7 — re-humanize against the residual violations listed in `07-voice-audit.md`; never resume at step 8.

Example of a voice-audit-blocked manifest excerpt:

```markdown
**Status:** blocked (voice audit)

- [ ] 7. blog-humanizer → 05-draft-v3.md, 07-voice-audit.md (verdict: FAIL), 05-draft-v3-r1.md, 07-voice-audit-r1.md (verdict: FAIL after 1 re-run; residual HARD: [rule → span])
- [ ] 8. blog-fact-check → pending (gated: voice audit FAIL)
```

---

## Versioning conventions

- Outline / detailed-outline / headlines / opener artifacts (`01-` through `04-`) are single-version. If the user redirects, the new version overwrites — the workflow only keeps the approved version. Pre-approval scratch versions can be saved as `01-outline-v2.md`, `01-outline-v3.md`, etc., but the canonical `01-outline.md` is always the approved one.
- Draft artifacts (`05-draft-v{N}.md`) are multi-version. Every transformation produces a new version:
  - v1 = output of `blog-draft` (step 5)
  - v2 = after readability rewrites applied (step 6)
  - v3 = after voice-humanizer rewrites applied (step 7)
  - v4, v5, ... = after each fact-reconcile pass (steps 8–9 loop)
- The manifest's "current step" plus the latest `05-draft-v{N}.md` is always the canonical state. Older versions are kept so the user can diff or revert.

---

## Locked-opener contract with blog-draft

In the workflow, `blog-opener` (step 4) runs before `blog-draft` (step 5). Without an explicit contract, `blog-draft` would regenerate its own opener from the outline strategy and the work from step 4 would be wasted — or worse, would silently disagree with the drafted opener that's about to be replaced.

To fix this, `blog-draft`'s SKILL.md accepts an optional **locked opener** input. When that input is provided, `blog-draft` uses it verbatim as the article's opening paragraph(s) and builds the rest of the article around it.

This orchestrator MUST pass the locked opener to `blog-draft` in step 5. The invocation prompt should include:

> Locked opener (use verbatim — do not regenerate):
> ```
> <opener text from step 4>
> ```
> Build the rest of the draft from `02-outline-detailed.md`, treating the locked opener as the opening paragraph(s) and the close as the callback to it. Run the opener-close contract from step 4 — the close must return to the locked opener's image/fact/tension.

The locked-opener contract is also documented on the `blog-draft` side. If `blog-draft` is ever invoked without a locked opener (e.g., single-step use), it falls back to its standard behavior of generating an opener from outline strategy.

---

## Failure modes and fallbacks

**Seed source missing or unreadable.** The workflow can't start without it. Surface the failure and ask the user to fix the file, paste the content, or describe the topic.

**Profile resolution fails.** Halt before step 1 (see pre-flight check). Report which file failed. Do not proceed.

**An enabled-step dependency file is missing.** Halt before step 1 (see pre-flight check). Report which file is missing and which step requires it.

**An underlying skill returns an error or refuses to run.** Capture the error, surface it to the user, and ask whether to retry, skip the step (with a documented gap in the manifest), or cancel the workflow.

**User cancels mid-workflow.** Update the manifest to `status: paused` and tell the user the workflow can be resumed by re-invoking this skill (resume detection will find it).

**Fact-check loop stuck.** Already handled in the step-8/9 specifics — surface the unresolved set and ask for editorial judgment.

**Manifest corruption.** If the manifest file is missing fields or malformed, surface to the user and ask what state the workflow is actually in. Do not guess.

---

## What this skill is NOT

- **Not a replacement for the underlying skills.** Every actual writing/editing decision is made by `blog-outline`, `blog-outline-more`, etc. This skill sequences them and tracks state.
- **Not a way to skip user approval.** Every enabled step gate is mandatory. The point of a 9-step orchestration is that the user reviews each output, not just the final one.
- **Not for single-step work.** If the user wants just an outline, they should invoke `blog-outline` directly. This skill is the full chain.
- **Not for non-article content.** Other content types (social posts, newsletter notes, daily content plans) go through their own skills. None of those use this orchestrator.

---

## Companion skills (the chain)

In invocation order:

- **blog-outline** — research, angle/hook + structure selection, bullet-point outline
- **blog-outline-more** — paragraph-level expansion, accessibility pre-check, reader-persona pre-assessment
- **blog-headline** — three headline + subheadline options
- **blog-opener** — two opener variants with opener-close contracts
- **blog-draft** — full prose draft — accepts locked-opener input from step 4
- **blog-readability** — post-draft density/comprehension audit (paragraph length, grounding, statistics, rhythm, sentence drag)
- **blog-humanizer** — post-draft lexical AI-tell pass, calibrated to the blog's author voice
- **blog-fact-check** — source verification of every factual claim (no-op if disabled by active profile)
- **blog-fact-reconcile** — applies fact-check corrections, produces next draft version (no-op if disabled by active profile)

All voice-aware skills in this chain load the active profile's `voice.md` at runtime as their canonical source for vocabulary, banned words, AI-tell patterns, and voice calibration. The pre-flight check ensures those profile files are present before the chain starts.
