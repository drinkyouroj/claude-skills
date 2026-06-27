# Design Spec — `blog-*` Generic Article Writing Pipeline

**Date:** 2026-06-27
**Author:** Justin Hearn (with Claude)
**Status:** Approved design — ready for implementation planning
**Source of pattern:** `tcn-article-builder` and its 9 companion skills (`/Users/justin/CascadeProjects/claude-skills/tcn-*`)

---

## 1. Purpose & Problem

`tcn-article-builder` is an end-to-end Substack article workflow hard-wired to **The Civic Node** (TCN): one brand, one author voice ("Justin"), one reader persona ("Marcus"), one platform (Substack), one input convention (`wiki/syntheses/`), and a TCN-specific content-framework vocabulary ("viral triggers", "Pattern Report"). The orchestration spine, however, is brand-agnostic.

**Goal:** Produce a parallel **`blog-*`** skill family that preserves the proven pipeline mechanics but reads every blog-specific decision from an importable **profile**, so the same pipeline can produce a legal blog, a technical blog, a fiction blog, etc., by swapping the profile — never by editing the skills.

**Non-goal:** Modifying, replacing, or reusing the existing `tcn-*` skills. They stay 100% untouched and keep running. TCN is conceptually "just another profile" but is **not** ported in this build.

---

## 2. Decisions (locked)

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| D1 | Relationship to TCN skills | **New parallel `blog-*` family** | Zero risk to working TCN production; clean separation. |
| D2 | Customization file shape | **Profile folder** of focused files | Mirrors TCN's existing split (voice file vs. persona); each step loads only what it needs. |
| D3 | Step selection per blog type | **Presets + per-step flags** | Archetype defaults with manual override; fiction ≠ journalism ≠ legal. |
| D4 | Seed / input source | **Flexible source brief** | Topic line, brief, notes, transcript, or synthesis — generalizes `wiki/syntheses/`. |
| D5 | First-build delivery scope | **Mechanism + 1 worked template profile** | Fastest path to a usable system; real profiles authored later. |
| D6 | Skill family name | **`blog-*` prefix** | Self-documenting and discoverable. |
| D7 | Profile location model | **Hybrid: central library + local override** | Reusable central profiles, per-project override when needed. |
| D8 | How leaf skills get the profile | **Approach A — each skill resolves the profile itself** | Keeps every `blog-*` skill independently usable (standalone runs); faithful to how TCN skills already load `anti-ai-writing-style.md`. |

---

## 3. Skill Family (parallel to TCN, 1:1 traceable)

Lives in `/Users/justin/CascadeProjects/claude-skills/blog-*`, symlinked into `~/.claude/skills/` exactly like the `tcn-*` skills.

| Order | New skill | TCN ancestor | Role |
|-------|-----------|--------------|------|
| — | `blog-article-builder` | `tcn-article-builder` | Orchestrator: sequences the chain, manifest/resume, approval gates. |
| 1 | `blog-outline` | `tcn-outline` | Research framing, structure selection, angle/hook, bullet outline. |
| 2 | `blog-outline-more` | `tcn-outline-more` | Paragraph-level expansion, reader-persona pre-assessment, accessibility pre-check. |
| 3 | `blog-headline` | `tcn-headline` | Headline + subheadline options. |
| 4 | `blog-opener` | `tcn-opener` | Opener variants + opener-close contract. |
| 5 | `blog-draft` | `tcn-draft` | Full prose draft; accepts locked-opener input. |
| 6 | `blog-readability` | `tcn-readability` | Density / comprehension audit (reframed as pacing where the preset says so). |
| 7 | `blog-humanizer` | `tcn-text-humanizer` | Lexical AI-tell pass calibrated to the profile's voice. |
| 8 | `blog-fact-check` | `tcn-fact-check` | Source verification (toggleable capability). |
| 9 | `blog-fact-reconcile` | `tcn-fact-reconcile` | Applies fact-check corrections (toggleable, paired with 8). |

> Names are adjustable; `blog-humanizer` drops the `text-` infix for brevity but maps to `tcn-text-humanizer`.

---

## 4. The Profile (the "tuning" unit)

### 4.1 Folder layout

```
<profile-id>/
  profile.yaml     # structured knobs — the machine-readable index
  identity.md      # brand name, subject domain, output platform, one-line audience
  voice.md         # author voice + banned vocab + AI-tell calibration (generalized anti-ai-writing-style.md)
  reader.md        # reader persona — the generic "Marcus": who they are, what they know, what they need
  templates.md     # content-structure / framework / angle library for this blog type
```

`profile.yaml` is the index and structured-knobs file; the four `.md` files hold the prose each step loads at runtime.

### 4.2 `profile.yaml` schema (draft — finalize in implementation)

```yaml
id: <kebab-id>                 # e.g. "general-blog", "my-legal-blog"
name: <human label>
preset: <preset-name>          # journalism | legal | technical | fiction | general  (default: general)

paths:
  identity: identity.md
  voice: voice.md
  reader: reader.md
  templates: templates.md
  source: <dir or file>        # where seed material lives (flexible; may be empty → ask at runtime)
  workspace: <dir>             # per-article drafts root (default: ./drafts)

steps:                         # per-step override of the preset's defaults; omit to inherit preset
  outline: true
  outline-more: true
  headline: true
  opener: true
  draft: true
  readability: true
  humanizer: true
  fact-check: <true|false>     # e.g. false for fiction
  fact-reconcile: <true|false>

quick:                         # small fields injected directly into prompts (cheap to pass around)
  brand: <string>
  domain: <string>             # subject matter, e.g. "U.S. civic policy", "appellate litigation"
  platform: <string>           # e.g. "Substack", "company blog (WordPress)", "Medium"
```

### 4.3 The four prose files (generalization mapping)

- **`identity.md`** — replaces every hard-coded "The Civic Node" / "drinkYourOJ" / "Substack" reference. Brand, subject domain, platform conventions, audience one-liner.
- **`voice.md`** — generalizes `workspace/core/anti-ai-writing-style.md`. **Keeps** the universal AI-tell rules (banned generic vocab, negative parallelisms, vocabulary cliff, closing-line abstraction). **Parameterizes** the personal calibration: this blog's banned words, register, sentence rhythm, closing-line rules, and 2–3 sample sentences in-voice.
- **`reader.md`** — generalizes the "Marcus" persona, the pipeline's center of gravity. Who the reader is, what they already know, what they need from a piece, what bores/loses them. Consumed by `blog-outline-more` (pre-assessment), `blog-headline`, `blog-opener`, `blog-draft`.
- **`templates.md`** — generalizes TCN's "viral trigger" + "template selection" + "Pattern Report" vocabulary into a per-blog **content-structure / framework / angle library**. A legal profile's library differs from a fiction profile's.

---

## 5. Profile Resolution (Hybrid — D7) + Loading Contract (Approach A — D8)

### 5.1 Central library + local override

- **Central library:** `~/.claude/blog-profiles/` holds reusable profiles plus the `_template/` skeleton.
- **Local override:** a `blog-profile/` folder inside the current blog project directory wins if present.
- **Resolution order (every run):**
  1. Local `blog-profile/` in the working project → use it.
  2. Else a profile named/pathed by the invocation argument → resolve from central library.
  3. Else list available central profiles + ask the user to pick.

### 5.2 Loading contract (shared preamble in every `blog-*` skill)

Every leaf skill begins with a **"Profile resolution"** preamble that:
1. Resolves the active profile via §5.1.
2. Loads only the file(s) that step needs (e.g. `blog-humanizer` loads `voice.md`; `blog-outline-more` loads `reader.md` + `templates.md`).
3. Binds the values, then performs its work.

This mirrors how TCN skills already load `anti-ai-writing-style.md` at runtime and keeps each `blog-*` skill **independently runnable** (a user can invoke `blog-draft` alone with a resolvable profile). The orchestrator additionally passes the resolved profile reference + the `quick:` fields forward so leaf skills don't each re-derive them, but leaf skills never *depend* on the orchestrator for correctness.

---

## 6. Presets + Per-Step Flags (D3)

`profile.yaml.preset` selects a named preset that sets step defaults and supplies domain-appropriate framing language; `profile.yaml.steps` overrides individual steps.

- **Shipped now:** the **`general`** preset = the proven TCN 9-step sequence, de-branded, all steps on. This is the default and the basis of the template profile.
- **Documented stubs (not built now):** `journalism` (≈ TCN: fact-check on, hook/angle selection), `legal` (fact-check on; "viral trigger" → sober "stakes framing"; IRAC-style structures in `templates.md`), `technical` (fact-check optional; problem→approach→tradeoffs structures; optional code-accuracy emphasis), `fiction` (fact-check + fact-reconcile **off**; `readability` reframed as **pacing**; narrative-beat structures). These are filled in a later pass per D5.

**De-TCN-ing of step-internal vocabulary** (applies across presets):
- "Viral trigger" / "template selection" (outline) → **angle/hook + structure selection** driven by `templates.md`.
- "Marcus pre-assessment" (outline-more) → **reader-persona pre-assessment** from `reader.md`.
- `wiki/syntheses/`, `workspace/...` paths → **profile-named seed source** + per-article working dir.

---

## 7. Seed / Input (D4)

The orchestrator accepts any of: a topic line, a path to notes/brief/transcript/synthesis, or pasted content. `profile.yaml.paths.source` names the default location; if empty or missing, the orchestrator asks. Validation mirrors TCN's seed-input handling (confirm path exists; offer to list recent files in the source dir; accept pasted content to a temp location).

---

## 8. Carried Over Unchanged from TCN (already brand-agnostic)

- Per-step loop: **announce → invoke leaf skill → save artifact → update manifest → approval gate → branch (approve / redirect / cancel)**.
- `manifest.md` format + **resume detection** (scan working dir, find first unchecked step).
- **Locked-opener handoff** between `blog-opener` (step 4) and `blog-draft` (step 5).
- **Fact-check ↔ reconcile loop** + termination logic (clean exit at zero flagged; stuck exit when two consecutive iterations surface the same unresolved set; user override any time). Only runs when the profile enables steps 8–9.
- Versioning conventions (`01-`–`04-` single-version; `05-draft-v{N}.md` multi-version).
- Pre-flight dependency check — generalized from "voice canonical file exists" to **"active profile resolves and required files for enabled steps exist."**

---

## 9. First-Build Scope (per D5)

**In scope now:**
1. The 10 `blog-*` skills (orchestrator + 9 leaf), de-TCN'd, with the §5.2 profile-resolution preamble.
2. The profile schema (`profile.yaml` + four `.md` files) and the `_template/` skeleton in `~/.claude/blog-profiles/`.
3. The `general` preset (de-branded TCN sequence) + the **one worked template profile** that uses it.
4. Hybrid resolution logic (§5.1) wired into the orchestrator and the shared preamble.
5. `voice.md` generalized from `anti-ai-writing-style.md` (universal rules kept, personal calibration parameterized).
6. Symlinks into `~/.claude/skills/` matching the TCN convention.

**Explicitly deferred (documented stubs only):** the `journalism` / `legal` / `technical` / `fiction` presets and any per-archetype example profiles.

---

## 10. Open Items to Resolve During Planning

- Exact `profile.yaml` field finalization (§4.2 is a draft).
- Whether `_template/` ships inside `blog-article-builder/` (always-available clone source) **and** is copied to the central library on first setup, or central-only.
- Final wording of the shared profile-resolution preamble so it's identical across all 10 skills (single source to copy).
- Whether `blog-readability`'s "pacing" reframe is a preset-driven mode inside one skill or a documented behavior switch.

---

## 11. Success Criteria

1. Running `blog-article-builder` against the template profile produces a full draft with **no** TCN identity leaking into output or prompts.
2. Swapping the profile folder (different brand/voice/reader/templates) changes the output's identity with **no skill edits**.
3. Setting `fact-check: false` in a profile cleanly skips steps 8–9 with no orphaned manifest state.
4. Any single leaf skill (e.g. `blog-draft`) runs standalone given a resolvable profile.
5. The `tcn-*` skills are byte-for-byte unchanged.
