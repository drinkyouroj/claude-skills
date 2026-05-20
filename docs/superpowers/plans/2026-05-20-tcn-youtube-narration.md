# tcn-youtube-narration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `tcn-youtube-narration` skill per the spec at [docs/superpowers/specs/2026-05-20-tcn-youtube-narration-design.md](../specs/2026-05-20-tcn-youtube-narration-design.md), deployable in time for the Friday 2026-05-22 re-recording of dispatch-004 ("You Own the Hotspot").

**Architecture:** Markdown-based Claude Code skill following established TCN-skill conventions: top-level source at `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/`, runtime copy at `~/.claude/skills/tcn-youtube-narration/` (symlinked, per repo conventions). Skill is built via `anthropic-skills:skill-creator` for frontmatter optimization and trigger accuracy, customized to the design spec, and validated against the dispatch-004 source article at `/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/10-final.md` before any production use.

**Tech Stack:** Markdown, YAML frontmatter, Bash for filesystem operations, `anthropic-skills:skill-creator` for skill scaffolding and trigger eval, git for atomic commits per task.

**Spec coverage map:**
- §1 (context) → captured in skill's "What this skill does" section (Task 3)
- §2 (ecosystem position) → companion-skills section (Task 3)
- §3 (scope) → "What this skill is NOT" section (Task 3)
- §4 (I/O contract) → "Inputs and outputs" section + frontmatter (Task 2-3)
- §5 (structure: Cold Open / Body / Outro) → "The structure" section + `references/structure-templates.md` (Task 3-5)
- §6 (voice calibration) → "Voice & vocabulary canonical source" section + `references/voice-calibration.md` (Task 3-4)
- §7 (output format) → "Output format" section + canonical examples in references (Task 3-5)
- §8 (skill process incl. dispatch detection) → "The process" section (Task 3)
- §9 (failure modes) → "Failure modes" section (Task 3)
- §10 (companion skills) → "Companion skills" section (Task 3)
- §11 (test criteria) → driven by Task 6 validation pass
- §12-13 (implementation track, deferred) → no implementation surface

---

## Task 1: Set up skill directory structure

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/`
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references/`
- Symlink: `~/.claude/skills/tcn-youtube-narration/` → top-level source

- [ ] **Step 1: Create source directory + references subdirectory**

```bash
mkdir -p /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references
```

Expected: silent success, two new directories on disk.

- [ ] **Step 2: Verify ~/.claude/skills/ is gitignored and exists**

```bash
ls ~/.claude/skills/ | head -5 && git -C /Users/justin/CascadeProjects/claude-skills check-ignore -v .claude/skills/tcn-youtube-narration 2>&1 | head -3
```

Expected: directory listing of existing runtime skills; check-ignore returns the gitignore rule (confirms the runtime symlink target is correctly gitignored). If `.claude/skills/` is not in `.gitignore`, halt and ask the user — repo convention requires the runtime cache to be gitignored.

- [ ] **Step 3: Create runtime symlink**

```bash
ln -sf /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration ~/.claude/skills/tcn-youtube-narration && ls -la ~/.claude/skills/tcn-youtube-narration
```

Expected: symlink resolves to the source-of-truth directory. If the runtime path already exists as a non-symlink directory, do not overwrite — ask the user.

- [ ] **Step 4: Commit empty skill directory marker**

Not applicable — skill directory has no files yet; commits come at the end of each subsequent task as content lands.

---

## Task 2: Scaffold SKILL.md via skill-creator

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/SKILL.md`

**Why skill-creator:** Justin explicitly requested skill-creator be invoked while creating this skill. skill-creator handles frontmatter description optimization (load-trigger accuracy), eval-driven trigger testing, and consistent structure across the skill family.

- [ ] **Step 1: Invoke `anthropic-skills:skill-creator` with the spec as input**

Pass the skill-creator the following:
- **Skill name:** `tcn-youtube-narration`
- **Spec path:** `/Users/justin/CascadeProjects/claude-skills/docs/superpowers/specs/2026-05-20-tcn-youtube-narration-design.md`
- **Source-of-truth location:** `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/`
- **Frontmatter description seed (from spec §4):**

> Step 1 of the Civic Node YouTube production workflow: converts an approved article draft into a 5-7 minute trailer-format narration script with slide markers, pacing notes, and refrain markers. Calibrated to a "Hank Green meets Vox" register and explicitly written to drive Substack click-through, not to summarize the article. Invoke when the user says "write the narration", "video script from this article", "narration script", "narrate this for YouTube", "do the script for Friday's video", or when the user points at a finished article draft and asks for a video script. Does NOT apply to social posts (tcn-post), full articles (tcn-draft), or YouTube packaging (title/description/thumbnail come from separate skills).

skill-creator may optimize this description for trigger accuracy. Accept its proposed optimizations but verify the trigger phrases in the spec are all still present.

- [ ] **Step 2: Verify SKILL.md was created at the expected path**

```bash
ls -la /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/SKILL.md
```

Expected: file exists, non-empty.

- [ ] **Step 3: Verify frontmatter has correct name + description**

```bash
head -20 /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/SKILL.md
```

Expected: YAML frontmatter with `name: tcn-youtube-narration` and a `description:` field that includes the trigger phrases from spec §4 (verify presence of: "write the narration", "narration script", "video script from this article").

- [ ] **Step 4: Commit the scaffold**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-youtube-narration/SKILL.md
git commit -m "scaffold tcn-youtube-narration skill via skill-creator

Initial frontmatter and skeleton. Body content will be filled in
from the design spec in subsequent commits."
```

---

## Task 3: Customize SKILL.md body to match spec

**Files:**
- Modify: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/SKILL.md`

The skill-creator scaffold provides frontmatter and skeleton. This task fills in the body sections by mapping spec sections to SKILL.md sections. Follow the structural pattern established by `tcn-headline/SKILL.md` and `tcn-draft/SKILL.md` — both already in the repo at the same top level.

**Sections to add (in this order, matching tcn-headline's structure):**

1. **Title heading** — `# The Civic Node — YouTube Narration (Step 1 of the YouTube Production Workflow)`
2. **What this skill does** — one paragraph from spec §1
3. **Voice & vocabulary canonical source** — copy verbatim from `tcn-headline/SKILL.md` lines 22-43 (the canonical-file dependency block) with two adjustments: replace "headline-form" → "video-narration-form", replace "headlines" → "narration scripts" where appropriate
4. **Position in the YouTube workflow** — from spec §2 (the ecosystem diagram, simplified to a single paragraph + bullet list)
5. **Inputs and outputs** — from spec §4
6. **The narration structure** — from spec §5 (Cold Open / Body / Outro). Inline the example slide markup. Reference `references/structure-templates.md` for the full templates.
7. **Voice calibration** — from spec §6. Inline the dial scale (1/4/7/10). Reference `references/voice-calibration.md` for full examples.
8. **Output format** — from spec §7. Include the canonical Script Notes footer template.
9. **The process** — from spec §8 (the 10 numbered steps including dispatch-number detection at step 9).
10. **Failure modes** — from spec §9.
11. **What this skill is NOT** — from spec §3 (the OUT-of-scope list, formatted as "this skill does not..." statements).
12. **Companion skills** — from spec §10 (the upstream and downstream skill relationships).
13. **Reference files** — pointer list to `references/voice-calibration.md` and `references/structure-templates.md`.

- [ ] **Step 1: Read tcn-headline/SKILL.md as the structural template**

```bash
cat /Users/justin/CascadeProjects/claude-skills/tcn-headline/SKILL.md | head -50
```

Expected: confirms the section-ordering pattern (frontmatter → title → what it does → voice canonical source → process → output format → reference files).

- [ ] **Step 2: Replace SKILL.md body content with the 13 sections listed above**

Use the spec as the authoritative source. For each section, copy the content from the spec section indicated and reformat to match `tcn-headline/SKILL.md`'s prose style (informal-but-precise, bullet-heavy, with clear gate prompts and process steps).

**Critical: the voice canonical source block must be near-verbatim from `tcn-headline/SKILL.md`.** Justin's feedback memory says this block lives in `workspace/core/anti-ai-writing-style.md` as the single source of truth — every voice-aware TCN skill loads from there. Do not duplicate the rules in the SKILL.md body.

**Critical: the structure section (§5 in spec) must use the renamed zone names:** Cold Open / Body / Outro. The legacy "Locked Open / Flexible Middle / Locked Close" names have been retired.

**Critical: the process section (§8 in spec) must include the dispatch-number detection step (step 9 in the spec's numbered list).** Default scan path: `workspace/dispatch-narration/` relative to active project root. Fallback: ask user explicitly.

- [ ] **Step 3: Verify SKILL.md has no em-dashes inside narration examples**

```bash
grep -nE "^[^#].*—" /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/SKILL.md | grep -iE "SLIDE [0-9]+|Vibes|Hook" | head -10 || echo "Clean — no em-dashes in slide examples"
```

Expected: "Clean" output. If em-dashes are found inside slide example blocks (between `**[SLIDE NN — ...]**` markers and the next `---` separator), they violate the skill's own no-em-dashes rule (spec §6.4) and must be replaced with period-restructure.

- [ ] **Step 4: Commit the body**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-youtube-narration/SKILL.md
git commit -m "fill in tcn-youtube-narration SKILL.md body from spec

Adds the 13 standard sections (what it does, voice canonical source,
structure, voice calibration, output format, process incl. dispatch-
number detection, failure modes, companion skills) per the design
spec at docs/superpowers/specs/2026-05-20-tcn-youtube-narration-design.md."
```

---

## Task 4: Write `references/voice-calibration.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references/voice-calibration.md`

This reference file holds the calibration anchors the skill needs to maintain register 6-7 across articles. Loaded by the skill at runtime when calibrating voice. Keep concise — references should be skim-able, not exhaustive.

**Required contents (sections in order):**

1. **The dial** (spec §6.1) — 1 / 4 / 7 / 10 reference points with one-line descriptions each
2. **Reference channels** (spec §6.2) — Hank Green + Vox Explained with one-sentence characterizations
3. **The two calibration tests** (spec §6.3) — Marcus-smirk + Hank-Vox, each with a pass/fail rule
4. **Worked example: dialing 002 → 7** — show one paragraph from dispatch-002, then the rewrite at register 7, then a short note on what changed
5. **Worked example: dialing 004 → 7** — show the McDonald's opener from dispatch-004 (the 004 version is register 4), then the register-7 rewrite from spec §5.1, then a short note on the moves used (rhetorical question + one-word landing)
6. **Spoken-word adaptations checklist** (spec §6.4) — the seven adaptations as a checklist with brief rationale for each

- [ ] **Step 1: Read dispatch-002 to extract a paragraph for the worked example**

```bash
sed -n '7,12p' '/Users/justin/Documents/substack-research/Substack Research/workspace/dispatch-narration/dispatch-002-strait-is-the-mandate.md'
```

Expected: the Slide 1 — Cover narration paragraph from dispatch-002. Capture verbatim as the "before" example.

- [ ] **Step 2: Write the rewritten register-7 version of the dispatch-002 paragraph**

Apply the spoken-word adaptations (no em-dashes, shorter sentences, one-word landings) to convert the 002 paragraph to register 7. Show the change in the reference file as a side-by-side or stacked before/after with a 1-2 sentence "what changed" note.

- [ ] **Step 3: Write the full reference file**

Compose all six sections per the requirements above. Save to:

```
/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references/voice-calibration.md
```

- [ ] **Step 4: Verify the file is well-formed markdown and under 300 lines**

```bash
wc -l /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references/voice-calibration.md
```

Expected: line count under 300. References are meant to be skim-able; over 300 lines suggests the file is doing too much and should be split.

- [ ] **Step 5: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-youtube-narration/references/voice-calibration.md
git commit -m "add voice-calibration reference for tcn-youtube-narration

Contains the dial scale (1/4/7/10), reference channels (Hank Green +
Vox Explained), the two calibration tests, two worked examples
(dialing 002 → 7 and 004 → 7), and the spoken-word adaptations
checklist."
```

---

## Task 5: Write `references/structure-templates.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references/structure-templates.md`

This reference file holds the canonical templates for each zone and slide type. Loaded at runtime when the skill needs to instantiate a slide.

**Required contents (sections in order):**

1. **Slide markup format** — the `**[SLIDE NN — TITLE]**` convention with rationale (spec §7.2)
2. **Cold Open templates** (spec §5.1):
   - Slide 1 — Hook template (with the McDonald's example at register 7)
   - Slide 2 — Thesis template (with the "they thought they were buying a business" example)
3. **Body slide menu** (spec §5.2) — for each of the six middle-slide types (Receipt / Frame / Stakes / Twist / Historical Echo / Verbatim), a one-paragraph definition + a brief example phrasing
4. **Outro templates** (spec §5.3):
   - Slide N-1 — Tease template (with explicit-cut-naming example from spec)
   - Slide N — End template (the canonical channel-branding close, verbatim)
5. **Script Notes footer template** (spec §7.3) — the full template with all required fields including forward-compat hooks (Cold-open candidate / Refrain candidate / Cuts from the article)
6. **Title block template** (spec §7.1) — `# [Title]` / `## The Civic Node · Dispatch №[NNN]` / `## [N] slides · trailer-format · 5-7 min target`

- [ ] **Step 1: Write the full reference file**

Compose all six sections per requirements above. Save to:

```
/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references/structure-templates.md
```

- [ ] **Step 2: Verify the file is well-formed markdown and under 300 lines**

```bash
wc -l /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references/structure-templates.md
```

Expected: under 300 lines.

- [ ] **Step 3: Verify the canonical Outro close is verbatim**

```bash
grep -A2 "The Civic Node" /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/references/structure-templates.md | head -6
```

Expected: the close reads exactly `The Civic Node. Subscribe free at drinkyouroj.substack.com. Weekly. No hype.` — same close every video for channel branding.

- [ ] **Step 4: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-youtube-narration/references/structure-templates.md
git commit -m "add structure-templates reference for tcn-youtube-narration

Canonical templates for Cold Open / Body / Outro zones, the six
body slide types, the Script Notes footer, and the title block.
Slide markup convention documented per spec §7.2."
```

---

## Task 6: Validate skill against dispatch-004 source article

**Files:**
- Test input: `/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/10-final.md`
- Optional test input: `/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/08-fact-check.md`
- Expected output: `/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md`

**Why this article:** Friday's re-record is dispatch-004 ("You Own the Hotspot"). The existing dispatch-004 narration (in `workspace/dispatch-narration/`) is at register 4 with the legacy Cover/Part-One structure — the new skill should produce a register-7 version with the new Cold Open / Body / Outro structure. This is the natural validation case.

- [ ] **Step 1: Confirm voice file dependency is met**

```bash
ls '/Users/justin/Documents/substack-research/Substack Research/workspace/core/anti-ai-writing-style.md'
```

Expected: file exists. If missing, halt — the skill is designed to halt rather than fall back to generic voice rules.

- [ ] **Step 2: Confirm the source article exists**

```bash
ls '/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/10-final.md'
```

Expected: file exists. This is the post-fact-check canonical draft.

- [ ] **Step 3: Invoke the skill against the article**

In a fresh Claude Code conversation in the substack-research project, run:

> "Use the tcn-youtube-narration skill on the article at workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/10-final.md. The fact-check report is at workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/08-fact-check.md. This is for re-recording dispatch-004."

Expected: skill produces a complete narration script at `workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md`.

- [ ] **Step 4: Verify the output against spec §11 test criteria**

For each of the 10 test criteria from spec §11, confirm:

1. ☐ Runs end-to-end and produces `youtube-narration.md` with Cold Open + Body + Outro structure, word count 700-1,050, complete Script Notes footer
2. ☐ Cold-open passes the Hank-Vox test (read aloud; Hank could deliver, Vox could chyron a key phrase)
3. ☐ Cold-open passes the Marcus-smirk test (Marcus would smirk, not wince)
4. ☐ Refrain markers correctly placed if a refrain candidate was detected
5. ☐ Script Notes footer is complete (word count, runtime, pacing cues, cold-open candidate, refrain candidate, cuts-from-article populated)
6. ☐ Tease slide explicitly names article content the video did not cover
7. ☐ End slide uses the canonical close verbatim (`The Civic Node. Subscribe free at drinkyouroj.substack.com. Weekly. No hype.`)
8. ☐ No em-dashes in narration prose; sentences average under 16 words; no subordinate-clause stacks
9. ☐ Skill halts gracefully on missing voice file / missing article / unresolved fact-check items (verify with a separate run that deliberately removes one input)
10. ☐ Dispatch number detected as `004` from existing `dispatch-narration/` files, OR correctly prompted from user (since 004 already exists; this is a re-record — verify the skill surfaces the ambiguity)

- [ ] **Step 5: Document validation results**

Create a short validation note. Save to:

```
/Users/justin/CascadeProjects/claude-skills/docs/superpowers/plans/2026-05-20-tcn-youtube-narration-validation.md
```

Contents: each of the 10 test criteria with pass/fail and a one-sentence note. If any failed, list the gap.

- [ ] **Step 6: Commit validation note**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add docs/superpowers/plans/2026-05-20-tcn-youtube-narration-validation.md
git commit -m "validate tcn-youtube-narration against dispatch-004 source

Runs the skill against the You Own the Hotspot article and checks
output against all 10 test criteria from spec §11."
```

---

## Task 7: Iterate on failing criteria (if any)

**Files:** Whichever files (SKILL.md or references) the validation pass identifies as needing change.

This task only runs if Task 6 surfaces failed criteria. If all 10 criteria passed, skip to Task 8.

- [ ] **Step 1: List the failing criteria from the validation note**

Read the validation file. For each failed criterion, identify the root cause: ambiguous instruction in SKILL.md, missing example in references, or unclear gate prompt.

- [ ] **Step 2: Fix the highest-impact failure first**

Make the minimum change to address the failure. Re-test against the same article.

- [ ] **Step 3: Commit the fix**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-youtube-narration/
git commit -m "fix tcn-youtube-narration: [one-line description of the fix]"
```

- [ ] **Step 4: Re-run validation (Task 6 Step 3-5) and update the validation note**

If new failures appear, loop back to this Task 7 Step 1. Iteration termination: all 10 criteria pass OR two consecutive iterations produce the same failures (which signals the issue is in the spec, not the skill — escalate to user).

---

## Task 8: Hand off to Justin for Friday's re-recording

**Files:** None — handoff is conversational.

- [ ] **Step 1: Confirm validation pass is complete**

Re-read the validation note. All 10 criteria should be checked off.

- [ ] **Step 2: Surface the working narration to Justin**

> The skill is built and validated. The dispatch-004 narration is at `workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md` — read it through as Marcus, then as Hank-watching-on-his-phone. If both pass, you're ready to record. If either flinches, redirect the skill ("dial catchier", "swap the Stakes slide for a Twist") and re-run.

- [ ] **Step 3: Note open items for the next session**

Capture for the next brainstorm session: `tcn-youtube-slideshow` design (the next skill in the upstream pipeline). Friday's slide-deck production is still on the user, who will produce slides manually in Claude Design for this one recording.

---

## Self-Review (run after writing the plan, before handoff)

**1. Spec coverage:** Every spec section (§1-11) maps to a task (per the coverage map at top of plan). ✓

**2. Placeholder scan:** All steps contain concrete commands or concrete instructions. No "TBD" or "implement later." Worked examples in Task 4 require reading dispatch-002 to extract a paragraph — that's a concrete instruction, not a placeholder.

**3. Type/name consistency:**
- Skill name `tcn-youtube-narration` used consistently throughout ✓
- Zone names Cold Open / Body / Outro used consistently (no legacy Locked/Flexible mentions) ✓
- Voice file path `workspace/core/anti-ai-writing-style.md` consistent ✓
- Dispatch-number format `Dispatch №[NNN]` (zero-padded to three digits) consistent ✓

**4. Granularity:** Each step is 2-5 minutes of focused work. The biggest step (Task 3 Step 2) is multi-section content authoring — that's intentionally larger because it's content, not code, and splitting by section would create artificial commit churn.

**5. Friday feasibility:** Tasks 1-5 can run sequentially in ~60-90 minutes of focused work. Task 6 validation takes another 30-45 minutes including reading the output. Task 7 iteration adds 0-60 minutes depending on what fails. Total: 2-4 hours from start to Friday-ready output. Plan is feasible for the deadline.
