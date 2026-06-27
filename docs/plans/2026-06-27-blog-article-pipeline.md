# blog-* Generic Article Pipeline — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a parallel `blog-*` skill family that reproduces the `tcn-article-builder` pipeline but reads every blog-specific decision from a swappable profile, so one pipeline serves any blog type.

**Architecture:** Ten `blog-*` skills (1 orchestrator + 9 leaf), each a de-branded port of its `tcn-*` ancestor. Every leaf skill self-resolves the active profile (Approach A) via a shared resolution contract, then loads only the profile files it needs. A profile is a folder (`profile.yaml` + `identity.md` + `voice.md` + `reader.md` + `templates.md`); profiles resolve local-override → named-central → ask. Presets set per-blog-type step defaults.

**Tech Stack:** Markdown `SKILL.md` files with YAML frontmatter; YAML profile config; bash (`grep`, `python3 -c` for YAML validity), symlinks, git. No runtime test framework — verification is grep/structural checks + two manual dry-run gates.

**Reference docs:**
- Spec: `docs/specs/2026-06-27-blog-article-pipeline-design.md` (decisions D1–D8, success criteria §11)
- Pattern source: `/Users/justin/CascadeProjects/claude-skills/tcn-article-builder/SKILL.md` and the nine `tcn-*` companion skills.

## Global Constraints

*(Every task's requirements implicitly include this section. Exact values from the spec.)*

- **TCN untouched:** the `tcn-*` skills must be byte-for-byte unchanged at the end (`git status` shows no `tcn-*` modifications). [Success criterion 5]
- **Skill location:** new skills live in `/Users/justin/CascadeProjects/claude-skills/blog-*`, symlinked into `~/.claude/skills/` (matching the `tcn-*` convention).
- **Profile library:** canonical library in-repo at `claude-skills/blog-profiles/`, symlinked to `~/.claude/blog-profiles/`.
- **Resolution order (every run):** local `blog-profile/` in the working project → named central profile under `~/.claude/blog-profiles/<name>/` → list available + ask.
- **Approach A:** every leaf skill resolves the profile itself and must be independently runnable (not dependent on the orchestrator for correctness).
- **Default preset:** `general` = de-branded TCN 9-step sequence, all steps enabled.
- **No identity leak:** the completeness grep (below) must return zero hits in every `blog-*/SKILL.md` (or each hit must be a reviewed generic example listing non-TCN alternatives too).
- **1:1 naming:** skills map to ancestors per spec §3 (`blog-outline`↔`tcn-outline`, … `blog-humanizer`↔`tcn-text-humanizer`).
- **Branch discipline:** all work on a feature branch off `main`; never commit to `main`.

### Completeness grep (the leak oracle)

Run against any finished skill file. **Zero hits required** (or reviewed generic examples only):

```bash
grep -rinE "Marcus|Justin|drinkYourOJ|Civic Node|Substack|wiki/syntheses|anti-ai-writing-style|workspace/core|workspace/drafts|Pattern Report|viral trigger" <path>/SKILL.md
```

### Shared substitution mapping (the de-TCN-ing recipe)

Applied to every ported skill. Read the ancestor, then replace each TCN concept with the generic concept sourced from the profile:

| TCN token / concept | Generic replacement | Profile source |
|---|---|---|
| "The Civic Node" / "Civic Node" / "drinkYourOJ" | the blog's brand/name | `identity.md` / `profile.yaml.quick.brand` |
| "Justin" / author-voice references | the blog's author voice | `voice.md` |
| "Marcus" / reader persona | the blog's reader persona | `reader.md` |
| "Substack" / platform assumptions | the blog's platform | `identity.md` / `profile.yaml.quick.platform` |
| civics / policy / news domain assumptions | the blog's subject domain | `identity.md` / `profile.yaml.quick.domain` |
| `workspace/core/anti-ai-writing-style.md` | the active profile's `voice.md` | resolution contract |
| `wiki/syntheses/` (mandatory seed) | the profile's seed source / flexible seed | `profile.yaml.paths.source` |
| `workspace/drafts/<slug>/` | the profile's workspace, default `./drafts/<slug>/` | `profile.yaml.paths.workspace` |
| "viral trigger" / "template selection" | "angle/hook + structure selection" | `templates.md` |
| "Pattern Report" + named templates | the profile's content-structure library | `templates.md` |
| "Marcus pre-assessment" | "reader-persona pre-assessment" | `reader.md` |

### Shared porting procedure (referenced by every leaf-skill task)

1. Read the `tcn-*` ancestor `SKILL.md` in full.
2. Copy it to the new `blog-*/SKILL.md`.
3. Rewrite the frontmatter `name` and `description` to the `blog-*` name and a de-branded description (no "Civic Node", "Justin", "Marcus", "Substack").
4. **Reference** the shared resolution contract (`~/.claude/blog-profiles/_resolution-contract.md`, produced in Task 1) in one line near the top — do **not** embed it — then add a one-line note naming which profile files this step uses.
5. Apply the shared substitution mapping above, plus the task's skill-specific notes.
6. Run the completeness grep until it returns zero (or reviewed generic examples only).
7. Confirm frontmatter validity and commit.

---

## File Structure

**Created (in `/Users/justin/CascadeProjects/claude-skills/`):**

- `blog-article-builder/SKILL.md` — orchestrator (port of `tcn-article-builder`)
- `blog-outline/SKILL.md` … `blog-fact-reconcile/SKILL.md` — 9 leaf skills
- `blog-profiles/_resolution-contract.md` — canonical profile-resolution contract (referenced one-line by every skill)
- `blog-profiles/_template/{profile.yaml,identity.md,voice.md,reader.md,templates.md}` — clone-able, runnable generic profile
- `blog-profiles/_presets/general.md` — built preset; `journalism.md`, `legal.md`, `technical.md`, `fiction.md` — documented stubs
- `docs/plans/2026-06-27-blog-article-pipeline.md` — this file

**Created (in `~/.claude/`):** 10 skill symlinks `skills/blog-*` + 1 library symlink `blog-profiles`.

**Untouched:** all `tcn-*` directories.

---

## Task 0: Branch + commit the spec

**Files:**
- Modify: git branch state only

- [ ] **Step 1: Create the feature branch off main**

Run:
```bash
cd /Users/justin/CascadeProjects/claude-skills && git checkout -b blog-pipeline
```
Expected: `Switched to a new branch 'blog-pipeline'`

- [ ] **Step 2: Commit the already-written spec**

Run:
```bash
git add docs/specs/2026-06-27-blog-article-pipeline-design.md docs/plans/2026-06-27-blog-article-pipeline.md
git commit -m "docs: spec + plan for blog-* generic article pipeline"
```
Expected: one commit created on `blog-pipeline`.

- [ ] **Step 3: Verify TCN baseline is clean**

Run: `git status --short tcn-*`
Expected: no output (no `tcn-*` changes).

---

## Task 1: Profile system foundation (`_template/` + resolution contract)

**Files:**
- Create: `blog-profiles/_template/profile.yaml`
- Create: `blog-profiles/_template/identity.md`
- Create: `blog-profiles/_template/voice.md`
- Create: `blog-profiles/_template/reader.md`
- Create: `blog-profiles/_template/templates.md`
- Create: `blog-profiles/_resolution-contract.md`

**Interfaces:**
- Produces: the `profile.yaml` schema (keys `id, name, preset, paths.{identity,voice,reader,templates,source,workspace}, steps.{outline,outline-more,headline,opener,draft,readability,humanizer,fact-check,fact-reconcile}, quick.{brand,domain,platform}`) and the canonical resolution preamble text — both consumed by every later task.

- [ ] **Step 1: Write `_template/profile.yaml`** (runnable generic defaults, with guidance comments)

```yaml
id: template
name: "Generic Blog (template — clone and edit me)"
preset: general

paths:
  identity: identity.md
  voice: voice.md
  reader: reader.md
  templates: templates.md
  source: ""          # dir or file holding seed material; empty → orchestrator asks
  workspace: ./drafts # per-article working dirs created here

steps:                # omit a key to inherit the preset default
  outline: true
  outline-more: true
  headline: true
  opener: true
  draft: true
  readability: true
  humanizer: true
  fact-check: true
  fact-reconcile: true

quick:
  brand: "Your Blog Name"
  domain: "your subject domain"
  platform: "your platform"
```

- [ ] **Step 2: Write the four prose files** with generic, fill-in-the-blank guidance (no TCN identity)

`identity.md`: sections "Brand", "Subject domain", "Platform & format conventions", "Audience in one line".
`voice.md`: a "Universal AI-tell rules (keep)" section (banned generic vocab, negative parallelisms, vocabulary cliff, closing-line abstraction) + a "This blog's calibration (edit)" section (banned words, register, sentence rhythm, closing-line rule, 2–3 in-voice sample sentences).
`reader.md`: sections "Who they are", "What they already know", "What they need from a piece", "What loses them".
`templates.md`: sections "Structures" (2–3 generic article skeletons), "Angles / hooks", "When to use which".

- [ ] **Step 3: Write the canonical resolution contract** to `blog-profiles/_resolution-contract.md` (skills reference this file in one line rather than embedding it)

```markdown
## Profile resolution (run before anything else)

This skill is profile-driven. Resolve the active blog profile before doing the skill's work:

1. **Local override:** if the current working directory (the blog project) contains a `blog-profile/` folder, use it as the active profile.
2. **Named profile:** else, if a profile name or path was provided (by the orchestrator or the user), resolve it under `~/.claude/blog-profiles/<name>/`.
3. **Ask:** else, list the profiles in `~/.claude/blog-profiles/` (excluding `_template` and `_presets`) and ask the user to pick one.

Once resolved, read `profile.yaml` for structured knobs, then load only the prose files this step needs:
- `identity.md` — brand, subject domain, platform, audience one-liner
- `voice.md` — author voice + banned vocab + AI-tell calibration
- `reader.md` — reader persona
- `templates.md` — content-structure / framework / angle library

Apply the active preset (`profile.yaml.preset`, resolved under `~/.claude/blog-profiles/_presets/<preset>.md`) for step defaults and framing vocabulary, with any `profile.yaml.steps` overrides.

If a required file for this step is missing, halt and report which file failed to resolve — do not fall back to a hard-coded identity.
```

- [ ] **Step 4: Verify YAML validity**

Run: `python3 -c "import yaml,sys; yaml.safe_load(open('blog-profiles/_template/profile.yaml')); print('ok')"`
Expected: `ok`

- [ ] **Step 5: Verify no TCN leak in the template**

Run the completeness grep against `blog-profiles/_template/*` and `blog-profiles/_resolution-contract.md`.
Expected: zero hits.

- [ ] **Step 6: Commit**

```bash
git add blog-profiles/_template blog-profiles/_resolution-contract.md
git commit -m "feat: profile schema, runnable _template, and canonical resolution contract"
```

---

## Task 2: `general` preset + preset stubs

**Files:**
- Create: `blog-profiles/_presets/general.md`
- Create: `blog-profiles/_presets/{journalism,legal,technical,fiction}.md`

**Interfaces:**
- Consumes: the `steps.*` keys and substitution mapping from Task 1 / Global Constraints.
- Produces: `general` preset definition (all 9 steps on, de-branded framing vocabulary) consumed by the orchestrator and leaf skills.

- [ ] **Step 1: Write `general.md`**

Contents: a "Step defaults" table listing all 9 steps = on; a "Framing vocabulary" section mapping the de-TCN'd terms ("angle/hook + structure selection", "reader-persona pre-assessment", "density/comprehension audit"); a one-line statement that `general` is the neutral default suitable for most non-fiction blogs.

- [ ] **Step 2: Write the four stubs**

Each stub states: intended blog type, which steps differ from `general` (e.g. `fiction`: `fact-check: false`, `fact-reconcile: false`, readability→pacing; `legal`: "viral trigger"→"stakes framing", IRAC structures), and a `> STATUS: documented stub — not built in first release` line.

- [ ] **Step 3: Verify no TCN leak**

Run the completeness grep against `blog-profiles/_presets/*.md`.
Expected: zero hits.

- [ ] **Step 4: Commit**

```bash
git add blog-profiles/_presets
git commit -m "feat: general preset + documented preset stubs"
```

---

## Tasks 3–11: Leaf skills (one task each)

Each leaf task follows the **Shared porting procedure** and **substitution mapping** (above), then runs the **completeness grep** and commits. Below, each task names its ancestor, the profile files it loads, and its skill-specific TCN constructs to neutralize.

> Each task's steps are: **(1)** read ancestor → **(2)** create `blog-<name>/SKILL.md` via the porting procedure with the skill-specific notes → **(3)** run completeness grep, expect zero → **(4)** verify frontmatter has de-branded `name`+`description` → **(5)** commit `git add blog-<name> && git commit -m "feat: blog-<name> (de-branded port of tcn-<ancestor>)"`.

### Task 3: `blog-outline`
- Ancestor: `tcn-outline`. Loads: `identity.md`, `reader.md`, `templates.md`, preset.
- Skill-specific: replace "viral trigger" + "template selection" + named templates ("Pattern Report") with **angle/hook + structure selection driven by `templates.md`**. Replace civic/news topic assumptions with `quick.domain`.

### Task 4: `blog-outline-more`
- Ancestor: `tcn-outline-more`. Loads: `reader.md`, `templates.md`, `voice.md`, preset.
- Skill-specific: "Marcus pre-assessment" → **reader-persona pre-assessment** from `reader.md`; keep the accessibility pre-check (generic).

### Task 5: `blog-headline`
- Ancestor: `tcn-headline`. Loads: `identity.md`, `reader.md`, preset.
- Skill-specific: headline conventions de-branded; platform-specific length/style assumptions → `quick.platform` / `identity.md`.

### Task 6: `blog-opener`
- Ancestor: `tcn-opener`. Loads: `reader.md`, `voice.md`, preset.
- Skill-specific: keep the opener-close contract (generic); persona references → `reader.md`.

### Task 7: `blog-draft`
- Ancestor: `tcn-draft`. Loads: `voice.md`, `reader.md`, `templates.md`, preset.
- Skill-specific: replace `workspace/core/anti-ai-writing-style.md` with the active `voice.md`; **preserve the locked-opener input contract verbatim** (it's already generic); draft paths → `paths.workspace`.

### Task 8: `blog-readability`
- Ancestor: `tcn-readability`. Loads: `reader.md`, `voice.md`, preset.
- Skill-specific: audit is near-generic; add the preset hook so a `pacing` mode (fiction) can be selected via preset, defaulting to density/comprehension.

### Task 9: `blog-humanizer`
- Ancestor: `tcn-text-humanizer` (note the name compresses `text-`). Loads: `voice.md`, preset.
- Skill-specific: every "Justin's voice" / `anti-ai-writing-style.md` reference → the active `voice.md`.

### Task 10: `blog-fact-check`
- Ancestor: `tcn-fact-check`. Loads: `identity.md` (domain), preset.
- Skill-specific: nearly clean already (2–3 hits). Add a guard: **if the preset/`steps` disables fact-check, this skill is a no-op the orchestrator skips** — document that contract here.

### Task 11: `blog-fact-reconcile`
- Ancestor: `tcn-fact-reconcile`. Loads: preset.
- Skill-specific: nearly clean already; same disable-guard contract as Task 10.

---

## Task 12: `blog-article-builder` (orchestrator)

**Files:**
- Create: `blog-article-builder/SKILL.md`

**Interfaces:**
- Consumes: all 9 leaf skill names; the resolution contract (Task 1); the `general` preset (Task 2); `profile.yaml.steps` + `paths`.
- Produces: the end-user entry point.

- [ ] **Step 1: Read `tcn-article-builder/SKILL.md` in full.**

- [ ] **Step 2: Create `blog-article-builder/SKILL.md`** via the porting procedure, with these orchestrator-specific changes:
  - Frontmatter `name: blog-article-builder`, de-branded `description` (sequence of nine `blog-*` skills; resume; per-step gates).
  - Reference the shared resolution contract (`~/.claude/blog-profiles/_resolution-contract.md`) in one line; the orchestrator resolves the profile once and passes the profile reference + `quick.*` fields forward to each leaf invocation (optimization only; leaves still self-resolve).
  - **Pre-flight** generalized from "voice file exists" to **"active profile resolves and the files required by enabled steps exist."**
  - **Seed input** generalized to the flexible source brief (topic line / path / pasted content), default location `profile.yaml.paths.source`; keep TCN's validate-and-offer-recent-files behavior.
  - **Step sequence** reads enabled steps from preset + `steps` overrides; **skip disabled steps cleanly** (e.g. fact-check/reconcile off for fiction) with the manifest recording them as `skipped (profile)`.
  - Working dir = `paths.workspace` (default `./drafts/<slug>/`); manifest format, resume detection, locked-opener handoff, and fact-check-loop termination carried over unchanged.
  - Invoke each leaf skill by its `blog-*` name.

- [ ] **Step 3: Run the completeness grep on `blog-article-builder/SKILL.md`.** Expected: zero hits.

- [ ] **Step 4: Verify the step-toggle contract** — grep the file for `skipped (profile)` and `steps` handling; confirm disabled steps are described as skipped, not failed.

Run: `grep -in "skip" blog-article-builder/SKILL.md`
Expected: at least one line describing skipping disabled steps.

- [ ] **Step 5: Commit**

```bash
git add blog-article-builder
git commit -m "feat: blog-article-builder orchestrator (de-branded, profile-driven)"
```

---

## Task 13: Symlinks into `~/.claude/`

**Files:**
- Create: 10 symlinks in `~/.claude/skills/`, 1 symlink `~/.claude/blog-profiles`

- [ ] **Step 1: Symlink the skills**

Run:
```bash
cd ~/.claude/skills
for d in /Users/justin/CascadeProjects/claude-skills/blog-*/; do ln -snf "$d" "$(basename "$d")"; done
```

- [ ] **Step 2: Symlink the profile library**

Run: `ln -snf /Users/justin/CascadeProjects/claude-skills/blog-profiles ~/.claude/blog-profiles`

- [ ] **Step 3: Verify all symlinks resolve**

Run:
```bash
ls -l ~/.claude/skills/blog-* | grep -c '\->'; readlink -f ~/.claude/blog-profiles
```
Expected: count `10`, and the profile path resolves to the repo `blog-profiles`.

- [ ] **Step 4: Commit** (symlinks live outside the repo; record completion)

```bash
git commit --allow-empty -m "chore: wire blog-* skills + profile library symlinks into ~/.claude"
```

---

## Task 14: End-to-end verification against success criteria (final gate)

**Files:** none (verification only)

- [ ] **Step 1: Criterion 5 — TCN byte-for-byte unchanged**

Run: `cd /Users/justin/CascadeProjects/claude-skills && git status --short tcn-* && git diff --stat tcn-*`
Expected: no output (zero `tcn-*` changes).

- [ ] **Step 2: No identity leak across the whole family**

Run the completeness grep across all `blog-*/SKILL.md` and `blog-profiles/`.
Expected: zero hits (or reviewed generic examples only — inspect any hit).

- [ ] **Step 3: Criterion 3 — fact-check disable is clean**

Inspect `blog-article-builder/SKILL.md` + `blog-fact-check`/`blog-fact-reconcile`: confirm a profile with `fact-check: false` is described as skipping steps 8–9 with manifest `skipped (profile)` and no orphaned loop state.

- [ ] **Step 4: Criterion 4 — standalone leaf run (manual gate)**

Pick one leaf skill (e.g. `blog-draft`), confirm its resolution preamble lets it resolve a profile and run without the orchestrator. Document the check in the commit message.

- [ ] **Step 5: Criterion 1 & 2 — dry-run (manual gate)**

Using the `_template` profile (cloned to a scratch `blog-profile/` with a 1-line topic seed), walk `blog-article-builder` through outline → at least draft. Confirm: (a) no TCN identity in output/prompts; (b) editing the profile's `identity.md`/`voice.md` changes output identity with no skill edits. This gate requires user judgment — present results and get sign-off.

- [ ] **Step 6: Finalize**

```bash
git add -A && git commit -m "test: verify blog-* pipeline against spec success criteria"
```
Then offer: open a PR / merge `blog-pipeline`, or continue with the deferred archetype profiles (legal/technical/fiction).

---

## Self-Review (completed by plan author)

- **Spec coverage:** D1 (parallel family)→Tasks 3–12; D2 (profile folder)→Task 1; D3 (presets+flags)→Task 2 + Task 12 step 2; D4 (flexible seed)→Task 12 step 2; D5 (mechanism + 1 template)→Task 1 (`_template`) + deferred stubs Task 2; D6 (`blog-*`)→all; D7 (hybrid resolution)→Task 1 step 3 + Task 13; D8 (Approach A)→resolution preamble embedded per leaf (Tasks 3–11) + Global Constraints. Success criteria 1–5 → Task 14. No gaps found.
- **Placeholder scan:** profile/preset stubs are intentional deliverables (explicitly marked), not plan placeholders; every build step shows concrete content or a concrete command. The two manual gates are labeled as such with explicit pass conditions.
- **Type consistency:** `profile.yaml` keys, the `_presets/<preset>.md` path, `paths.workspace`, and `steps.*` names are used identically in Tasks 1, 2, 12, and 14.
