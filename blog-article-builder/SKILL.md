---
name: blog-article-builder
description: >
  End-to-end workflow orchestrator for blog articles. Sequences nine blog-*
  skills in order — blog-outline → blog-outline-more → blog-headline →
  blog-opener → blog-draft → blog-readability → blog-humanizer → blog-fact-check
  ↔ blog-fact-reconcile (legacy loop) or blog-fact-swarm for newsroom profiles
  → final read-through. Pauses after every step for
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
| 8 | Fact check | `blog-fact-check` (non-newsroom) or `blog-fact-swarm` (newsroom) | `08-fact-check-v{N}.md` or `08-fact-swarm-summary.md` with board section plus `receipt.md` for newsroom | Approve recommendations or review swarm summary/board/Receipt |
| 9 | Fact reconcile | `blog-fact-reconcile` (non-newsroom) or swarm decision gate | `05-draft-v{N+1}.md` or manifest state | Approve (loop back to 8 until clean or stuck) or decide unresolved Claims |
| 10 | Final read-through | (this skill) | `manifest.md` marked `ready-to-publish` only after all active gates pass | Confirm ship-ready; newsroom also requires attorney sign-off |

For non-newsroom profiles, steps 8 and 9 keep the legacy loop. Termination: the loop stops when fact-check reports zero flagged claims, OR when two consecutive iterations surface the same set of unresolved items (no progress).

For `preset: newsroom`, step 8 invokes `blog-fact-swarm` for Claim extraction plus bounded swarm verification. Step 9 is not an automatic `blog-fact-reconcile` pass against the swarm summary; it is a user decision gate over unresolved Claims unless the swarm is clean.

For `preset: newsroom`, final readiness also requires a fresh retained Receipt, attorney sign-off in `<workflow-dir>/approval.json` for the exact delivered draft and Receipt `source_hash`, and a no-unresolved-Claims publish gate over the validated Claim store. Sign-off is a recorded document exchange; it is not publication and it is not a Claim override.

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

### Step 8 ↔ Step 9 — fact verification boundary

**Step enable check:** before starting this boundary, confirm `steps.fact-check` is enabled in the active profile. If `steps.fact-check: false`, mark step 8 as `skipped (profile)`. If `steps.fact-reconcile: false`, mark step 9 as `skipped (profile)` and do not invoke reconcile behavior. Disabled steps do not bypass the step 7 voice-audit gate; they only skip fact work after the gate has passed.

**Preset routing:** if the resolved profile uses `preset: newsroom`, run the newsroom swarm path below. All other presets keep the legacy serial path.

**Why this comes last:** every voice/density rewrite that touched a fact-bearing sentence is now subject to source verification. Running fact-check after all voice work catches any subtle drift introduced by the humanizer or readability rewrites (a number rephrased, an attribution dropped, a causal claim sharpened beyond what the source supports).

**Legacy non-newsroom loop:**

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

**Newsroom swarm path:**

1. Confirm the step 7 voice audit has a terminal `Verdict: PASS` and the current draft is the same draft covered by that passing audit. If missing, unparseable, or failed, use the existing voice-audit block behavior and do not extract Claims.
2. Invoke `blog-fact-swarm` on the current canonical draft. If `claims/` is absent or stale for the current draft, run extraction first and stop for the swarm skill's Claim extraction approval gate before writing the store.
3. Run bounded swarm verification through `blog-fact-swarm`. The default limit is the swarm skill default unless the operator gives a per-run limit.
4. Save the swarm summary as `08-fact-swarm-summary.md` with a `## Fact Swarm Board` section, or save a sibling `08-fact-swarm-board.md` if the board is kept separate.
5. Update `manifest.md` with the `claims/` directory, `08-fact-swarm-summary.md`, any separate board artifact or board-section pointer, total Claim count, terminal-stage counts, recall flag count, open recall flag count, effective concurrency limit, and unresolved terminal states.
6. If `receipt.md` already exists, run `blog-fact-swarm` Receipt Mode freshness check. If it is stale, record `receipt_status: stale` in `manifest.md` and route to Receipt Mode before any later sign-off wording.
7. Gate: "Swarm verification complete. Review `08-fact-swarm-summary.md` and its board evidence: [summary counts]. Approve this fact state, generate or refresh the retained Receipt, adjudicate paused Claims, request manual rewrite/source work for unresolved Claims, or pause?"
8. Do not run legacy `blog-fact-reconcile` automatically against the Claim-store summary. If `adjudication-paused` Claims remain, surface their Claim ids and tell the Operator to run `blog-fact-swarm` Adjudication Mode before continuing. After adjudication, regenerate `08-fact-swarm-summary.md` and `08-fact-swarm-board.md` (or the board section), update the manifest pointers/counts, mark any existing Receipt stale, and return to this gate. If other unresolved Claims remain (`attention`, `failed`, `no-verdict`, or open recall flags), halt at this gate and ask for operator decision, Receipt generation for retained evidence, or manual rewrite/source work. When the Operator requests Receipt generation or refresh, run `blog-fact-swarm` Receipt Mode, write `<workflow-dir>/receipt.md`, and update `manifest.md` with `receipt`, `receipt_source_hash`, `receipt_status`, unresolved counts, open recall count, and divergence counts. If every Claim is `verified` or explicitly `operator-overridden`, no recall flags remain open, recall dispositions are cleared/overridden where needed, and the Receipt is fresh, mark step 9 as `skipped (swarm clean or explicitly dispositioned)` and proceed to step 10. If unresolved Claims or open recall flags remain, keep them at the fact-state boundary until the Operator chooses adjudication, manual rewrite/source work, retained Receipt review, or the explicit Story 3.3 override helpers; do not auto-run legacy `blog-fact-reconcile` against a Claim-store summary.

### Step 10 final voice gate

Before marking the manifest `ready-to-publish`, compare the latest draft after fact verification against the draft named in the most recent passing voice audit. If the latest draft differs, run one final voice audit on the latest draft. Save a passing final audit as `09-final-voice-audit.md`; save a failing, missing, or unparseable final-audit attempt as `09-final-voice-audit-fail.md` (or `09-final-voice-audit-fail-r{N}.md` for repeated attempts) so blocking evidence is never overwritten by a later PASS.

`ready-to-publish` requires `Verdict: PASS` from the final audit. If the final audit is `FAIL`, missing, or unparseable, set manifest `status: blocked (voice audit)`, list the residual HARD violations, and do not mark the Issue ready to publish. The manifest must make the remediation step the current unchecked step: leave step 9 unchecked if fact reconciliation or manual swarm follow-up introduced the violation and the next action is to revise the verified draft, or leave step 7 unchecked if broader humanizer work is needed. Step 10 remains pending until a draft change is made and a final audit passes. The manifest must name the remediation target so the next run does not retry the same failing final audit without a draft change.

### Step 10 — Final read-through gate

The previous enabled steps caught structural, lexical, and factual issues each at their own level. None of them caught "does this feel like a complete piece when read end-to-end as the blog's reader persona would read it." That's the read-through gate's job.

Present the final draft to the user with this prompt:

> Final draft is `<working-dir>/<slug>/05-draft-v{latest}.md`. Read the whole thing as the blog's reader persona would — opener through close, no skimming. The audits caught structural, lexical, and factual issues, but they can't tell you whether the piece *feels* finished. Anything remaining to fix before this ships?

For non-newsroom profiles, if the user says ship, update the manifest to `status: ready-to-publish` and announce the workflow is complete.

For `preset: newsroom`, **before** treating ship as available, present the delivered-draft base capture, attorney sign-off gate, returned-edit capture option, and then the Claim-store publish gate (do not infer approval from silence):

1. Identify the current canonical draft as `05-draft-v{latest}.md`, the Receipt path (`receipt.md`), and the Receipt `source_hash` from Receipt metadata / manifest.
2. Before sending the draft to the Client, present the base-record command and tell the Operator this must capture the exact delivered draft:

```text
python3 ~/.claude/skills/blog-voice-patch/scripts/capture_edit_diff.py --record-base --workflow-dir <workflow-dir> --draft-path 05-draft-v{latest}.md --delivery-method "<method>" --delivery-evidence "<operator note>"
```

Stop and Present the recorded base path, SHA-256, byte count, and `edit_diff_status: base-recorded`. Do not proceed as though the Client reviewed the draft until the Operator confirms this is the exact version being sent.

3. If the Operator already has a returned Markdown/plain-text document from the Client, present capture mode:

```text
python3 ~/.claude/skills/blog-voice-patch/scripts/capture_edit_diff.py --capture-return --workflow-dir <workflow-dir> --returned-path <returned-file.md> --return-method "<method>" --return-evidence "<operator note>"
```

Stop and Present the `edit-diff.json` path, pair count, and whether the diff is empty. Returned edits are voice-signal capture only; they do not imply attorney approval and do not clear Receipt, sign-off, final voice/read-through, or Claim-store publish blockers.

4. Run the sign-off checker against that exact draft path (required `--expected-draft`):

```text
python3 ~/.claude/blog-profiles/scripts/record_attorney_signoff.py --workflow-dir <workflow-dir> --check --expected-draft 05-draft-v{latest}.md
```

5. Present draft path, Receipt path, Receipt `source_hash`, Edit Diff status/path if present, and the checker outcome. Ask the Operator to **record attorney approval or pause**. Do not proceed to `ready-to-publish` until the checker returns `approved:` exit 0 for that canonical draft and a fresh Receipt.

The Edit Diff capture and sign-off gate are independent gates. Edit Diff capture does not bypass sign-off, final voice/read-through, Claim-store, or Receipt gates; sign-off does not replace any Claim-store or Receipt gate. The sign-off checker updates `approval_status` (and related mirrors) in the newsroom Claim-store Notes list of `manifest.md`.

If the checker returns non-zero, keep the manifest non-ready with `status: awaiting-attorney-signoff` or `status: blocked (sign-off)`, set `publication_action: not-triggered`, keep the checker-written `approval_status`, and keep resume detection pointed at this gate. Ask the Operator to record attorney approval with:

```text
python3 ~/.claude/blog-profiles/scripts/record_attorney_signoff.py --workflow-dir <workflow-dir> --approver "<name>" --approver-role "<role>" --approval-method "<source>" --approval-evidence "<operator note>" --draft-path 05-draft-v{latest}.md --receipt-path receipt.md
```

If `approval.json` was written but the manifest mirrors failed (exit 15), repair with:

```text
python3 ~/.claude/blog-profiles/scripts/record_attorney_signoff.py --workflow-dir <workflow-dir> --sync-manifest
```

Do not infer approval from silence or from the presence of returned edits. Do not publish, distribute, upload, post, trigger a webhook, mutate `voice.md`, propose/apply Rule Patches, or hand-edit `edit-diff.json`. Do not hand-edit Claim JSON or invent silent approvals. Explicit Claim-store publish exceptions are allowed only via Story 3.3 helpers `write_claim_override.py` and `write_recall_flag.py`. After approval is valid, run the publish gate checker against the same canonical draft:

```text
python3 ~/.claude/skills/blog-fact-swarm/scripts/check_publish_gate.py --workflow-dir <workflow-dir> --expected-draft 05-draft-v{latest}.md
```

If it blocks, keep the manifest non-ready with `status: blocked (publish gate)`, set `publish_gate_status: blocked`, keep `publication_action: not-triggered`, surface exact blocker Claim ids and recall ids, and keep resume detection pointed at the fact/publish gate. If it passes and the final voice/read-through gate has passed, mark the Issue ready for publication as manifest state only: `status: ready-to-publish`, `publish_gate_status: passed`, blocker counts zero, and `publication_action: not-triggered`.

If the user flags any specific issue, ask which step they want to revisit (rerun readability on the post-humanizer version? rerun the humanizer on a specific section? do a manual edit then loop fact-check again?). Route accordingly.

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
- [ ] 8. blog-fact-check/blog-fact-swarm → pending
- [ ] 9. blog-fact-reconcile/swarm decision → pending
- [ ] 10. final read-through → pending; if step 9 changed the draft, run `09-final-voice-audit.md` before ready-to-publish

## Fact-check / swarm history (filled in during steps 8–9)

| Iteration | Flagged before | Flagged after reconcile | Outcome |
|-----------|----------------|--------------------------|---------|
| 1         | -              | -                        | -       |

For newsroom swarm runs, record the Claim store state in the Notes section:

- `claims_dir`: `<workflow-dir>/claims`
- `summary`: `08-fact-swarm-summary.md`
- `board`: `08-fact-swarm-summary.md#fact-swarm-board` or `08-fact-swarm-board.md` if separate
- `claim_count`: `<N>`
- `terminal_stage_counts`: `<verified/attention/failed/no-verdict/adjudication-paused/operator-overridden>`
- `divergence_counts`: `<paused/adjudicated>`
- `adjudicated_divergence_claims`: `<none or list>`
- `recall_flag_count`: `<N>`
- `open_recall_flag_count`: `<N>`
- `effective_concurrency_limit`: `<N>`
- `unresolved_terminal_states`: `<none or list>`
- `receipt`: `<workflow-dir>/receipt.md` or `<none yet>`
- `receipt_source_hash`: `<sha256>` or `<none yet>`
- `receipt_status`: `fresh | stale | missing`
- `approval`: `<workflow-dir>/approval.json` or `<none yet>`
- `approval_status`: `approved | missing | stale-draft | stale-receipt | missing-receipt | invalid`
- `approval_approver`: approver name or `<none yet>`
- `approval_approved_at`: ISO-8601 UTC `Z` timestamp or `<none yet>`
- `approval_draft_sha256`: `<sha256>` or `<none yet>`
- `approval_receipt_source_hash`: `<write_receipt.py source_hash>` or `<none yet>`
- `publish_gate_status`: `passed | blocked | not-checked`
- `publish_gate_blocked_claims`: `<none or list>`
- `publish_gate_blocked_recall`: `<none or list>`
- `publication_action`: `not-triggered`

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
  - v4, v5, ... = after each fact-reconcile pass (legacy steps 8–9 loop) or manual newsroom rewrite after swarm review
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

**Legacy fact-check loop stuck.** Already handled in the step-8/9 specifics — surface the unresolved set and ask for editorial judgment.

**Newsroom swarm has unresolved Claims.** Do not auto-reconcile the summary. If `adjudication-paused` Claims exist, surface their Claim ids and route them to `blog-fact-swarm` Adjudication Mode first. After adjudication, regenerate the summary/board artifacts, mark any existing Receipt stale, and update the manifest pointers/counts before returning to the fact boundary. For other unresolved Claims, surface `08-fact-swarm-summary.md`, keep the manifest at the fact boundary, and ask whether to generate/refresh the retained Receipt, rewrite, supply manual source material, or pause. Publish overrides remain later Epic 3 scope.

**Newsroom Receipt stale or missing.** If `receipt.md` is absent or its `source_hash` does not match the current validated Claim store, record `receipt_status: missing` or `stale` in `manifest.md` and route to `blog-fact-swarm` Receipt Mode before any later attorney sign-off wording. A fresh Receipt is retained evidence only; it does not mark the Issue ready to publish.

**Newsroom attorney sign-off missing, invalid, or stale.** At final read-through, present draft path / Receipt path / `source_hash` and run `python3 ~/.claude/blog-profiles/scripts/record_attorney_signoff.py --workflow-dir <workflow-dir> --check --expected-draft 05-draft-v{latest}.md`. The helper maps outcomes into Claim-store Notes `approval_status`: `approved` -> `approved`; `missing-approval` -> `missing`; `stale-draft` -> `stale-draft` (also when `--expected-draft` does not match stored `draft_path`); `stale-receipt-source` -> `stale-receipt`; `invalid-approval` -> `invalid`; `missing-receipt` -> `missing-receipt`; `missing-draft` -> `stale-draft`. Any non-zero checker exit blocks `ready-to-publish`, keeps `publication_action: not-triggered`, and resumes at the sign-off gate. Re-sign-off means intentionally archive the prior `approval.json` to `approval.json.revoked.<YYYYMMDDTHHMMSSZ>` (add a suffix such as `-2` if the archive name already exists), then record fresh approval for the current delivered draft and Receipt.

**Newsroom publish gate blocked.** After final voice/read-through and sign-off pass, run `python3 ~/.claude/skills/blog-fact-swarm/scripts/check_publish_gate.py --workflow-dir <workflow-dir> --expected-draft 05-draft-v{latest}.md`. If it reports blocked Claims, open recall flags, stale/missing Receipt, missing/invalid sign-off, or invalid store state, do not mark `ready-to-publish`. Keep `publication_action: not-triggered`, record `publish_gate_status: blocked`, surface exact blocker ids, and resume at the fact/publish gate. The Operator may adjudicate, rewrite/source manually, regenerate the retained Receipt, record fresh sign-off, or use Story 3.3's `write_claim_override.py` / `write_recall_flag.py` helpers for explicit Claim-store exceptions.

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
- **blog-fact-swarm** — newsroom Claim extraction plus bounded swarm verification (no-op if disabled by active profile)
- **blog-fact-reconcile** — applies fact-check corrections, produces next draft version (no-op if disabled by active profile)

All voice-aware skills in this chain load the active profile's `voice.md` at runtime as their canonical source for vocabulary, banned words, AI-tell patterns, and voice calibration. The pre-flight check ensures those profile files are present before the chain starts.
