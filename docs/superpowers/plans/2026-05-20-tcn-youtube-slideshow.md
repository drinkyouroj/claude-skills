# tcn-youtube-slideshow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `tcn-youtube-slideshow` skill per the spec at [docs/superpowers/specs/2026-05-20-tcn-youtube-slideshow-design.md](../specs/2026-05-20-tcn-youtube-slideshow-design.md), deployable in time for Friday 2026-05-22's re-recording of dispatch-004.

**Architecture:** Markdown-based Claude Code skill mirroring the structural conventions of `tcn-youtube-narration` (built earlier today). Source-of-truth at `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/`, runtime symlink at `~/.claude/skills/tcn-youtube-slideshow/`. Skill is built via `anthropic-skills:skill-creator`, customized per the design spec, and validated against the dispatch-004 narration that's already on disk at `/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md`.

**Tech Stack:** Markdown, YAML frontmatter, Bash for filesystem ops, `anthropic-skills:skill-creator` for scaffolding, git for atomic commits per task.

**Spec coverage map:**
- §1-§3 (context, ecosystem, scope) → SKILL.md "What this skill does" + "Position in workflow" + "What this skill is NOT" sections (Task 3)
- §4 (I/O contract) → SKILL.md "Inputs and Outputs" section + frontmatter triggers (Tasks 2-3)
- §5 (slide-type mapping) → references/template-mapping.md + summarized in SKILL.md (Task 3-4)
- §6 (kicker convention) → references/template-mapping.md (Task 4)
- §7 (animation directives) → references/template-mapping.md (Task 4)
- §8 (prompt structure) → SKILL.md "Output format" section with full template inline (Task 3)
- §9 (skill process) → SKILL.md "The process" section, 10 steps (Task 3)
- §10 (failure modes) → SKILL.md "Failure modes" section (Task 3)
- §11 (companion skills) → SKILL.md "Companion skills" section (Task 3)
- §12 (test criteria) → driven by Task 5 validation pass
- §13-§15 (implementation track, OOS, open notes) → no implementation surface

---

## Task 1: Set up skill directory + symlink

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/`
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/references/`
- Symlink: `~/.claude/skills/tcn-youtube-slideshow/` → top-level source

- [ ] **Step 1: Create source directory + references subdirectory**

```bash
mkdir -p /Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/references
```

Expected: two new directories on disk.

- [ ] **Step 2: Verify runtime symlink target does not already exist**

```bash
ls ~/.claude/skills/tcn-youtube-slideshow 2>/dev/null || echo "OK_NOT_EXISTS"
```

Expected: "OK_NOT_EXISTS". If a non-symlink directory exists at that path, halt and ask the user.

- [ ] **Step 3: Create runtime symlink**

```bash
ln -sf /Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow ~/.claude/skills/tcn-youtube-slideshow && readlink ~/.claude/skills/tcn-youtube-slideshow
```

Expected: symlink resolves to the source-of-truth directory.

- [ ] **Step 4: No commit yet** — directory has no files; first commit lands in Task 2.

---

## Task 2: Scaffold SKILL.md via skill-creator

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/SKILL.md`

- [ ] **Step 1: Invoke `anthropic-skills:skill-creator` with the spec as input**

Pass skill-creator:
- **Skill name:** `tcn-youtube-slideshow`
- **Source-of-truth location:** `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/`
- **Spec path:** `/Users/justin/CascadeProjects/claude-skills/docs/superpowers/specs/2026-05-20-tcn-youtube-slideshow-design.md`
- **Frontmatter description seed (from spec §4):**

> Step 2 of the Civic Node YouTube production workflow: converts an approved narration script into a single Claude Design prompt that produces a complete slide deck bundled HTML file matching the TCN design system. The skill maps each narration slide to a template slide type, applies intensified-but-on-brand animation directives, and embeds the narration as speaker notes. Invoke when the user says "build the slideshow", "make the slides", "Claude Design prompt for this deck", "turn this narration into slides", or has approved a youtube-narration.md and wants the deck. Does NOT apply to article slides, social media graphics, or thumbnail generation (those come from separate skills).

skill-creator may optimize. Verify the three required trigger phrases survive: "build the slideshow", "make the slides", "Claude Design prompt for this deck".

This task ONLY scaffolds the frontmatter + skeleton. Task 3 fills in the body.

- [ ] **Step 2: Verify SKILL.md created and frontmatter is correct**

```bash
head -10 /Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/SKILL.md
```

Expected: YAML frontmatter with `name: tcn-youtube-slideshow` and a `description:` containing the three trigger phrases above (verified as continuous substrings, not split across line breaks — use plain scalar form, not YAML folded style, same lesson as Task 2 of the narration skill).

- [ ] **Step 3: Commit the scaffold**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-slideshow/SKILL.md && git commit -m "scaffold tcn-youtube-slideshow skill via skill-creator

Initial frontmatter and skeleton. Body content will be filled in
from the design spec in subsequent commits.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 3: Fill in SKILL.md body from spec

**Files:**
- Modify: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/SKILL.md`

Mirror the structural conventions of `tcn-youtube-narration/SKILL.md` (built earlier today). Read that file as the structural template before writing.

**Sections to write, in this order:**

1. **Title heading** — `# The Civic Node — YouTube Slideshow (Step 2 of the YouTube Production Workflow)`
2. **What This Skill Does** — one paragraph from spec §1. Emphasize: prompt-builder, not slideshow renderer.
3. **Why a Prompt-Builder, Not a Slideshow Generator** — short section explaining the framing from spec §1 (the TCN design system already exists; this skill assembles precise context-handoff to Claude Design rather than reinventing the design language).
4. **Position in the YouTube Workflow** — from spec §2. Brief bullet list of upstream (`tcn-youtube-narration`) and siblings (planned packaging skills).
5. **Inputs and Outputs** — from spec §4. Required input + optional inputs + output artifact + gate prompt.
6. **Slide-Type Mapping** — summary table from spec §5 (narration zone → template slide type). Reference `references/template-mapping.md` for the full table with fallbacks and combined-type rules.
7. **Kicker Convention** — summary of spec §6, with the dispatch-004 example block. Reference `references/template-mapping.md` for the full rules.
8. **Animation Intensification** — summary of spec §7 (the six intensified primitives). Reference `references/template-mapping.md` for the full directive table. Include the guardrails (no bounce/spring/rainbow, easing cubic-bezier, 120/200/360ms).
9. **Output Format** — from spec §8. Include the full Claude Design prompt template **inline** (not in references) — it's the skill's main artifact and belongs in SKILL.md so the skill can produce it directly.
10. **The Process** — from spec §9, the 10 numbered steps.
11. **Failure Modes** — from spec §10.
12. **What This Skill Is NOT** — from spec §3 OUT-of-scope as "this skill does not..." bullets.
13. **Companion Skills** — from spec §11.
14. **Reference Files** — pointer to `references/template-mapping.md`.

**Critical constraints:**

- The skill is a prompt-builder. It does NOT render HTML, edit `deck-stage.js`, or invent design rules. Reinforce this in §3 and §12.
- The output prompt template in §9 must include all subsections: Context, Inputs, Brand requirements, Slide-by-slide specification, Speaker notes, Output requirements. Each subsection labeled exactly as in spec §8.
- Process step 9 in spec §9 says the skill writes `youtube-slideshow.md` to the **same workflow folder** as the narration (`workspace/drafts/<slug>/`). The SKILL.md must make this path explicit so the skill doesn't default to a different location.

- [ ] **Step 1: Read the structural template**

```bash
head -100 /Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/SKILL.md
```

Expected: confirms the section ordering used by the narration skill.

- [ ] **Step 2: Write the body sections**

Replace the SKILL.md body (preserving frontmatter at lines 1-4) with the 14 sections listed above. Use the spec as the authoritative content source; use `tcn-youtube-narration/SKILL.md` as the structural template.

- [ ] **Step 3: Verify**

```bash
grep -c "^## " /Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/SKILL.md
grep -i "locked open\|flexible middle\|locked close\|part one of three" /Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/SKILL.md || echo "Clean — no legacy zone names"
wc -l /Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/SKILL.md
```

Expected: ~14 `## ` headings; "Clean" output for legacy-zone check; line count 250-400.

- [ ] **Step 4: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-slideshow/SKILL.md && git commit -m "fill in tcn-youtube-slideshow SKILL.md body from spec

Adds the 14 standard sections per the design spec at
docs/superpowers/specs/2026-05-20-tcn-youtube-slideshow-design.md.
Models the structural pattern after tcn-youtube-narration/SKILL.md.
The Claude Design prompt template is inlined in the Output Format
section (it's the skill's main artifact, not a reference).

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 4: Write `references/template-mapping.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/references/template-mapping.md`

This file holds the full slide-type mapping, kicker convention, and animation directive tables — pulled out of SKILL.md to keep the main file skim-able. Loaded by the skill at runtime when mapping a specific narration slide to a slide directive.

**Required sections, in this order:**

1. **Slide-type mapping table (full)** — from spec §5. All 10 narration slide types in the left column, default template type, fallback/variant. Plus the "combined slide types" rule (e.g., `FRAME + STAKES` → first sub-label's type, layout adjusted).

2. **Kicker convention (full)** — from spec §6. The kicker format pattern, the dispatch-004 example block, the kicker rules list (mono, wide-tracked, all-caps, slate-400, middle-dot separator, zero-padded dispatch number).

3. **Animation intensification table (full)** — from spec §7. All six primitives with the existing-vs-intensified column. Plus the preserved guardrails list (no bounce/spring/rainbow, easing, durations, no emoji, single typeface, palette constraints).

4. **Future-option seam** — short paragraph noting that the Q8=B path (extending `deck-stage.js` with new primitives) is not built today but the prompt structure can accept new directives without restructuring.

- [ ] **Step 1: Write the file**

Compose all 4 sections from the spec. Keep under 250 lines. The tables are mostly mechanical copies from the spec.

- [ ] **Step 2: Verify the file is well-formed markdown and under 250 lines**

```bash
wc -l /Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/references/template-mapping.md
```

Expected: under 250 lines.

- [ ] **Step 3: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-slideshow/references/template-mapping.md && git commit -m "add template-mapping reference for tcn-youtube-slideshow

Full slide-type mapping table, kicker convention, animation
intensification directives. Pulled out of SKILL.md so the main
file stays skim-able. Loaded by the skill at runtime when mapping
each narration slide to a slide directive.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 5: Validate skill against dispatch-004 narration

**Files:**
- Test input: `/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md` (already exists — produced by `tcn-youtube-narration` and approved by Justin)
- Optional test input: design system bundle at `~/Documents/The Civic Node — Design System.zip`
- Expected output: `/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-slideshow.md`

- [ ] **Step 1: Confirm narration exists at the expected path**

```bash
ls '/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md'
```

Expected: file exists.

- [ ] **Step 2: Confirm design system bundle exists (optional input)**

```bash
ls '/Users/justin/Documents/The Civic Node — Design System.zip'
```

Expected: file exists. If not, the skill should still run and produce a prompt with a placeholder for the user to upload manually.

- [ ] **Step 3: Invoke the skill against the narration**

In a fresh Claude Code conversation in the substack-research project:

> "Use the tcn-youtube-slideshow skill on the narration at workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md. Design system bundle is at ~/Documents/The Civic Node — Design System.zip."

Expected: skill produces `youtube-slideshow.md` in the same workflow folder.

- [ ] **Step 4: Verify output against spec §12 test criteria**

For each of the 10 test criteria from spec §12, check:

1. ☐ Produces `youtube-slideshow.md` with all required blocks: Context, Inputs, Brand requirements, Slide-by-slide spec, Speaker notes, Output requirements
2. ☐ Each slide directive includes: kicker text, slide type from §5 mapping, headline, body (or quote, or chart spec), animation directive per §7
3. ☐ Kicker convention correct: `DISPATCH №004 · [LABEL] · [SUB-LABEL]` pattern, middle-dot separator, zero-padded `№004`, all caps
4. ☐ Speaker notes verbatim from `youtube-narration.md` — no paraphrasing, one entry per slide
5. ☐ Animation directives intensify existing primitives only — no new CSS class names, no extensions to `deck-stage.js`
6. ☐ Brand guardrails restated explicitly in Brand Requirements block
7. ☐ Dispatch number `№004` detected from narration's title block (line 2: `## The Civic Node · Dispatch №004`)
8. ☐ The output `youtube-slideshow.md` is self-contained — one paste into Claude Design produces a working deck
9. ☐ Skill halts gracefully on missing/malformed narration
10. ☐ **End-to-end test:** Justin pastes the prompt into Claude Design, uploads the design system bundle, and Claude Design produces a working HTML deck without further clarification

- [ ] **Step 5: Document validation results**

Create a short validation note at:

```
/Users/justin/CascadeProjects/claude-skills/docs/superpowers/plans/2026-05-20-tcn-youtube-slideshow-validation.md
```

Each criterion with pass/fail and a one-sentence note. If any failed, list the gap.

- [ ] **Step 6: Commit validation note**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add docs/superpowers/plans/2026-05-20-tcn-youtube-slideshow-validation.md && git commit -m "validate tcn-youtube-slideshow against dispatch-004 narration

Runs the skill against the dispatch-004 youtube-narration.md and
checks output against all 10 test criteria from spec §12.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 6: Iterate on failing criteria (if any)

This task only runs if Task 5 surfaces failures. If all 10 criteria passed, skip to Task 7.

- [ ] **Step 1: List failing criteria from validation note; identify root causes**
- [ ] **Step 2: Fix the highest-impact failure first; make the minimum change**
- [ ] **Step 3: Commit the fix with a one-line description of what changed**
- [ ] **Step 4: Re-run validation (Task 5 Step 3-5)**
- [ ] **Loop termination:** all 10 criteria pass OR two consecutive iterations produce the same failures (signal that the issue is in the spec, not the skill — escalate to user)

---

## Task 7: Hand off to Friday's recording

**Files:** None — handoff is conversational.

- [ ] **Step 1: Confirm validation pass complete; all 10 criteria checked**

- [ ] **Step 2: Surface working deck to Justin**

> The slideshow skill is built and validated. Paste `workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-slideshow.md` into a fresh `claude.ai/design` project, upload the design system bundle, and let Claude Design build the deck. If the rendered deck still feels too static, the Q8=B path (new animation primitives via `deck-stage.js` extension) is available as a future iteration.

- [ ] **Step 3: Note open items for next session**

Capture for future:
- If Friday's deck still feels too static, consider extending `deck-stage.js` with new primitives (scroll-triggered counters, typewriter effects, programmatic chart morphing)
- Resume `tcn-youtube-title` / `tcn-youtube-description` / `tcn-youtube-thumbnail` design after Friday recording (they consume the recorded transcript, so they can't be built until the video exists)

---

## Self-Review

**1. Spec coverage:** Every spec section (§1-§12) maps to a task per the coverage map at top of plan. ✓

**2. Placeholder scan:** All steps contain concrete commands or concrete instructions. The validation note in Task 5 Step 5 has a defined structure (10 criteria with pass/fail) — not a placeholder.

**3. Type/name consistency:**
- Skill name `tcn-youtube-slideshow` used consistently throughout ✓
- Path `workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/` consistent across Tasks 5-7 ✓
- Reference file path `references/template-mapping.md` consistent across Tasks 3-4 ✓
- Dispatch number format `№NNN` (with zero-padding) consistent ✓

**4. Granularity:** Steps are 2-5 minutes. Task 3 Step 2 is multi-section content authoring (larger) — intentional, as content authoring is the unit, not individual sections.

**5. Friday feasibility:** Tasks 1-4 sequential in ~45-60 min focused work. Task 5 validation 20-30 min including reading the produced prompt. Task 6 iteration adds 0-30 min depending on what fails. **Total: 1.5-2.5 hours from start to Friday-ready output.** This plan is shorter than the narration plan because the skill is structurally simpler (prompt-builder vs. content generator).
