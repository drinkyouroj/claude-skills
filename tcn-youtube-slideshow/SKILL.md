---
name: tcn-youtube-slideshow
description: "Step 2 of the Civic Node YouTube production workflow: converts an approved narration script into a single Claude Design prompt that produces a complete slide deck bundled HTML file matching the TCN design system. The skill maps each narration slide to a template slide type, applies intensified-but-on-brand animation directives, and embeds the narration as speaker notes. Invoke when the user says \"build the slideshow\", \"make the slides\", \"Claude Design prompt for this deck\", \"turn this narration into slides\", or has approved a youtube-narration.md and wants the deck. Does NOT apply to article slides, social media graphics, or thumbnail generation (those come from separate skills)."
---

# The Civic Node — YouTube Slideshow (Step 2 of the YouTube Production Workflow)

## What This Skill Does

Converts a finished YouTube narration script into a single, self-contained Claude Design prompt that yields a complete slide deck as one bundled HTML file. The prompt maps each narration slide to a TCN design system slide template, restates the brand guardrails, prescribes intensified-but-on-brand animation directives, and embeds the narration verbatim as speaker notes. The output is a markdown file (`youtube-slideshow.md`) ready to paste into a new Claude Design project at `claude.ai/design`.

This skill is a **prompt-builder, not a slideshow generator.** It does not render HTML, ship CSS, or extend the kinetic engine. It assembles a precise context handoff to Claude Design, which does the rendering against the TCN design system.

---

## Why a Prompt-Builder, Not a Slideshow Generator

The TCN design system already exists. The CSS variables, slide-type stylesheets, `deck-stage.js` kinetic engine, brand marks, and the `slides/deck.html` reference template are all in the canonical design-system bundle. The slide vocabulary (`sl-title`, `sl-lead`, `sl-section`, `sl-data`, `sl-frames`, `sl-compare`, `sl-quote`, `sl-end`) is fixed. The animation primitives (`sl-reveal`, `sl-mark-pulse`, `sl-caret`, `sl-chart-draw`, `sl-glow`, `sl-hairline`) are fixed.

The bottleneck is not "we need a new slideshow design." The bottleneck is "every week, Justin manually composes a Claude Design brief from the narration and the design system, and the result drifts in consistency." This skill removes that bottleneck.

What this skill produces is a deterministic, article-specific brief — kicker text, slide type, headline, body, animation directives, speaker notes — that Claude Design can execute against the existing design system without further clarification. The design rules live in the design system. This skill just wires the narration to them.

---

## Position in the YouTube Workflow

This skill is **Step 2 of the YouTube production workflow** — it runs after the narration is approved and before video recording.

**Upstream (what this skill reads):**
- `tcn-youtube-narration` output (`youtube-narration.md`) — slide structure, content, Script Notes footer with forward-compat hooks
- The TCN design system bundle (CSS, deck-stage.js, slide templates) — referenced in the produced prompt, not parsed by the skill

**Downstream (sibling skills, planned, not built today):**
- `tcn-youtube-title` — packages titles for YouTube upload (consumes the recorded transcript)
- `tcn-youtube-description` — packages descriptions and chapter timestamps (consumes the recorded transcript)
- `tcn-youtube-thumbnail` — produces thumbnail image prompts (consumes the recorded transcript and the cold-open candidate)

The packaging skills run after recording because they consume the timestamped transcript, not the upstream narration. This skill is the last upstream-of-recording step.

The full ecosystem diagram lives in the design spec at `docs/superpowers/specs/2026-05-20-tcn-youtube-slideshow-design.md`.

---

## Inputs and Outputs

### Required input

- **Path to a finished narration.** Typically `workspace/drafts/<slug>/youtube-narration.md`. The skill reads this file verbatim — slide markers, Script Notes footer, forward-compat hooks. If the user pastes the narration contents directly instead of supplying a path, save the paste to a temp file and proceed.

### Optional inputs

- **Path to the TCN design system bundle.** Defaults to the user's maintained path (Justin's current path: `~/Documents/The Civic Node — Design System.zip`). If not provided, the skill leaves a placeholder in the prompt with an instruction to upload before pasting.
- **Steering** — free-text guidance like "use sl-compare instead of sl-frames on Slide 4", "make Slide 3's chart larger", or "skip animation intensification on the Tease slide".
- **Override slide type** — for any individual slide, the user can force a specific template (e.g., "Slide 3 must be sl-data with the SVG chart variant").

### Output artifact

- **File:** `workspace/drafts/<slug>/youtube-slideshow.md`
- **Contents:** a single, self-contained Claude Design prompt with all article-specific content filled in
- **Does NOT contain:** rendered HTML, CSS, or JavaScript — those are Claude Design's job

### Gate prompt presented to user

> Claude Design prompt complete (~[N] lines). Open `youtube-slideshow.md`, copy its contents, paste into a new Claude Design project at `claude.ai/design`, upload the design system files, and ask Claude Design to build the deck. Approve, redirect (e.g., 'swap slide 4 to sl-compare', 'lower animation intensity'), or cancel?

**Stop after presenting the prompt.** Wait for user approval or redirect before doing anything else.

---

## Slide-Type Mapping

Each narration slide maps deterministically to a slide template type from `slides/deck.html`. The mapping is driven by the narration's zone (Cold Open / Body / Outro) and slide sub-label.

| Narration slide | Default template | Fallback / variant |
|---|---|---|
| Cold Open / Hook (Slide 1) | `sl-title` | — |
| Cold Open / Thesis (Slide 2) | `sl-lead` | `sl-section` if thesis is one declarative phrase |
| Body / Receipt (data-heavy) | `sl-data` with `ms-numgrid` | `sl-data` with `sl-chart` SVG if the article has a chart |
| Body / Frame | `sl-frames` | `sl-compare` for two-way comparison |
| Body / Stakes | `sl-lead` | — |
| Body / Twist | `sl-frames` (numbered escalation) | `sl-compare` (before/after) |
| Body / Historical Echo | `sl-compare` (then/now) | `sl-lead` |
| Body / Verbatim | `sl-quote` | — |
| Outro / Tease (Slide N-1) | `sl-lead` with bullet listing | `sl-section` with `[TEASE]` kicker if shorter |
| Outro / End (Slide N) | `sl-end` | — |

**Combined slide types** (e.g., `THE FRAME + STAKES, Author's Debug` from dispatch-004): pick the first sub-label's template type, adjust the layout (fewer numbered columns, more prose), and note the combination in the prompt. Do not invent new template types.

The full mapping table with fallback rules, combined-type handling, and worked examples lives in `references/template-mapping.md`.

---

## Kicker Convention

The legacy decks used `PART ONE OF THREE` / `[01] CONTEXT` / `[02] FRAME` / `[03] CALL` kickers tied to the retired Cover/Part-One/Part-Two structure. Those are retired. The new convention uses the narration's actual zone and slide label:

```
DISPATCH №004 · HOOK                              ← Cold Open / Slide 1
DISPATCH №004 · THESIS                            ← Cold Open / Slide 2
DISPATCH №004 · THE RECEIPT · UNIT ECONOMICS      ← Body slide with sub-label
DISPATCH №004 · THE RECEIPT · HIP-143             ← Body slide
DISPATCH №004 · THE TWIST · VOTE CONCENTRATION    ← Body slide
DISPATCH №004 · THE FRAME + STAKES · AUTHOR'S DEBUG  ← Body slide (combined type)
DISPATCH №004 · TEASE                             ← Outro / Slide N-1
DISPATCH №004 · END                               ← Outro / Slide N
```

**Kicker rules:**
- Mono typeface, wide-tracked (`0.18em`), all-caps, slate-400 on dark
- Middle dot `·` as separator — never `|`, never `/`
- Zero-padded dispatch number (`№004`, not `№4`)
- Sub-labels in the kicker correspond to the narration's slide sub-label after the comma (e.g., `THE RECEIPT, Unit Economics` → `THE RECEIPT · UNIT ECONOMICS`)

Full kicker conventions, edge cases, and the substitution rule for combined slide types live in `references/template-mapping.md`.

---

## Animation Intensification

The skill instructs Claude Design to use **existing primitives more aggressively.** No new CSS classes are invented; no extensions to `deck-stage.js`. Six primitives, intensified:

- **`sl-reveal` cascade** — up to `sl-reveal-5` (5-stagger), longer durations on body slides
- **`sl-mark-pulse`** — title slide + end slide + slow ambient pulse on Section dividers (mark at 24px)
- **`sl-caret` blinking** — section heading kicker + end-card heading kicker (two per deck max)
- **`sl-chart-draw`** — every Data slide; if two data slides exist, second draws after first completes
- **`sl-glow`** (radial slate) — title + end slide + behind any single dominant number on Data slides
- **Hairline `sl-hairline` draws** — animated left-to-right reveal in 360ms on slide entry

**Guardrails (preserved — non-negotiable):**
- No bounce, no spring, no rainbow gradients
- Easing remains `cubic-bezier(0.2, 0, 0, 1)`
- Durations remain in the 120/200/360ms family (no >500ms transitions)
- No emoji, no icon fonts, no shadows on dark
- One typeface (Courier Prime); slate-400 / slate-600 / black / twilight palette only

The prompt restates the guardrails verbatim so Claude Design does not drift toward exotic motion. Full directive tables and worked examples live in `references/template-mapping.md`.

---

## Output Format

The output `youtube-slideshow.md` is a single markdown file with this structure. The skill fills in every bracketed placeholder from the narration.

```markdown
# Claude Design prompt — TCN Dispatch №[NNN] slideshow

## Context

You are building an HTML slideshow for The Civic Node, Dispatch №[NNN]:
"[Article Title]". The slideshow is the visual companion to a 5-7 minute
YouTube narration video; viewers will watch the slides while listening to
the narration as audio.

## Inputs (attached / uploaded to this Claude Design project)

- `colors_and_type.css` — the brand CSS variable system. Load at runtime.
- `slides.css` — slide-specific styles (sl-title, sl-section, sl-lead,
  sl-data, sl-frames, sl-compare, sl-quote, sl-end).
- `deck-stage.js` — kinetic engine. Load via <script src="deck-stage.js">.
- `assets/mark.svg`, `assets/lockup-dark.svg` — brand marks.
- `slides/deck.html` — reference template; mimic its slide structure.

## Brand requirements (non-negotiable)

- One typeface: Courier Prime.
- Palette: slate-400 / slate-600 / black / twilight only. No other colors.
- No emoji, no icon fonts, no exclamation points, no shadows on dark.
- Middle dot `·` as the kicker separator. Never `|`, never `/`.
- Easing on every animation: `cubic-bezier(0.2, 0, 0, 1)`.
- Durations: 120ms, 200ms, or 360ms. Nothing longer than 500ms.
- No bounce, no spring, no rainbow gradients.
- Kickers: mono, wide-tracked (0.18em), all-caps, slate-400.

## Slide-by-slide specification

### Slide 1 — sl-title
Kicker: `DISPATCH №[NNN] · HOOK`
Headline: [from narration Slide 1]
Tag (sub-line): [from narration cold-open candidate or steering]
Foot row: `The Civic Node` / `[YYYY·MM·DD] · [N] MIN`
Animation: sl-mark-pulse on the mark; sl-reveal cascade 1→2→3 on
  headline → tag → foot row. Hold for ~2s after the pulse settles.

### Slide 2 — sl-lead
Kicker: `DISPATCH №[NNN] · THESIS`
Heading: [from narration Slide 2, declarative]
Body: [1-2 paragraphs from narration Slide 2]
Animation: sl-reveal cascade 1→2 on heading → body. sl-hairline draws
  left-to-right on entry, 360ms.

[... continues for each narration slide, following the §5 mapping table ...]

### Slide N — sl-end
Kicker: `DISPATCH №[NNN] · END`
Heading: `The Civic Node`
Body: Substack URL CTA + disclosure block (verbatim from narration
  Outro / End slide)
Animation: sl-mark-pulse on the mark at 44px; sl-glow radial slate
  behind the mark; sl-reveal cascade on the disclosure block.

## Speaker notes (embed as JSON at end of HTML)

Embed as a `<script type="application/json" id="speaker-notes">` block.
One entry per slide. Each entry is the narration text verbatim from
`youtube-narration.md` — no paraphrasing.

```json
[
  { "slide": 1, "text": "[Slide 1 narration verbatim]" },
  { "slide": 2, "text": "[Slide 2 narration verbatim]" },
  ...
  { "slide": [N], "text": "[Slide N narration verbatim]" }
]
```

## Output requirements

- Single bundled HTML file named `dispatch-[NNN].html`.
- All external resources loaded relatively (`../colors_and_type.css`, etc.).
- Speaker notes embedded as JSON in the document.
- Self-contained: opens in any browser, plays the full deck via
  `deck-stage.js`.
- No external CDN calls. No remote fonts. No analytics.
```

The skill fills every bracketed placeholder with article-specific content. The prompt is comprehensive enough that Claude Design produces the bundle deterministically without further clarification.

---

## The Process

### 1. Locate the narration

Read `youtube-narration.md` from the supplied path. Halt if missing or unreadable.

### 2. Parse slide structure

Extract slide count, each slide's zone (Cold Open / Body / Outro), kicker sub-type (HOOK, THESIS, THE RECEIPT, THE FRAME, etc.), slide content, and the Script Notes footer.

### 3. Detect the dispatch number

Read the dispatch number from line 2 of the narration file (the title block — `## The Civic Node · Dispatch №NNN`). The narration step already locked this number; do not re-scan the workspace, do not re-derive. If the title block is malformed or the number is missing, halt and ask the user to confirm.

### 4. Parse forward-compat hooks

From the Script Notes footer, read the "Cold-open candidate" to inform the Title slide's tag line, and the "Refrain candidate" (if present) to inform animation timing — refrain lines get longer holds.

### 5. Map each slide to a template type

Apply the §5 mapping table. Apply user steering or overrides if provided. For combined slide types (e.g., `FRAME + STAKES`), pick the first sub-label's template type and note the combination in the prompt.

### 6. Generate per-slide directives

For each slide, compose: kicker text (per §6), headline, body, animation specifications (per §7).

### 7. Compose the speaker-notes JSON block

One entry per slide. Narration text is verbatim from `youtube-narration.md` — no paraphrasing, no compression, no register adjustment.

### 8. Verify the design system bundle path

If a path was supplied, confirm the file exists. If not supplied, leave a placeholder in the prompt with an explicit instruction for the user to upload the design system files to the Claude Design project before running the prompt.

### 9. Compute date and runtime

Pull the runtime estimate from the narration's Script Notes footer (it is already calculated there). The date is today's date or the user-supplied recording date.

### 10. Write the prompt and present to user

Write the complete prompt to `workspace/drafts/<slug>/youtube-slideshow.md`. Present to user with the standard gate prompt (§4). Wait for approval or redirect.

---

## Failure Modes

- **Narration file missing or unreadable** — halt, surface, ask for valid path.
- **Narration slides don't match expected structure** (no slide markers, no Script Notes footer, no zone labels) — surface to user; ask whether to proceed with best-effort parsing or halt. Default to halt if structure is severely malformed.
- **Dispatch number missing from title block** — halt and ask the user to confirm. Do not guess.
- **Design system bundle path not provided** — leave a placeholder in the prompt with a note ("upload your design system files to the Claude Design project before running this prompt") and continue.
- **More than 12 narration slides** — halt with a warning. Trailer-format decks target 7-9 slides; >12 is a signal the upstream narration drifted from the format.
- **Combined slide type encountered** (e.g., `FRAME + STAKES`) — pick the first sub-label's template type, adjust the layout (fewer numbered columns, more prose), note the combination in the prompt's slide-by-slide block.
- **User redirects** — re-invoke the affected step. Common redirects:
  - "use sl-compare instead of sl-frames on Slide 4" → re-generate that slide's directive with the override
  - "lower animation intensity" → re-write all animation directives at one level lower (sl-reveal-3 max, no chained pulses)
  - "swap a slide" → re-map the affected slide and regenerate
  - "rebuild from scratch with steering X" → re-run the full process with steering applied

---

## What This Skill Is NOT

- This skill does **not** render slideshows. It produces a prompt; Claude Design renders the HTML.
- This skill does **not** author or extend the TCN design system. The design system already exists; this skill references it.
- This skill does **not** extend `deck-stage.js` with new animation primitives. Animation intensification reuses existing primitives only — new primitives are deferred to a future iteration.
- This skill does **not** generate narration. That's `tcn-youtube-narration` (Step 1).
- This skill does **not** produce thumbnails, social graphics, YouTube titles, descriptions, or chapter timestamps. Those are separate planned skills that run after recording.
- This skill does **not** fact-check the article or rewrite voice. Those happen upstream in the article workflow.

---

## Companion Skills

**Upstream (this skill reads from):**
- `tcn-youtube-narration` — the finished narration script is the required input. Slide markers, zone labels, and the Script Notes footer (with cold-open candidate and refrain candidate) all feed this skill.

**Downstream (sibling skills, planned, not built today):**
- `tcn-youtube-title` — title generation, consumes the recorded transcript.
- `tcn-youtube-description` — description body, tags, chapter timestamps — consumes the recorded transcript.
- `tcn-youtube-thumbnail` — thumbnail image prompt + text overlay — consumes the recorded transcript and the cold-open candidate.

**Shared design-system dependency:**
- The skill does NOT duplicate design-system content. It references the canonical bundle (`~/Documents/The Civic Node — Design System.zip` by default) and trusts Claude Design to load and apply it. This is the same architecture pattern the voice-aware TCN skills use with `workspace/core/anti-ai-writing-style.md` — one canonical source of truth, referenced at runtime, never duplicated.

---

## Reference Files

- `references/template-mapping.md` — full narration-zone → slide-template mapping table with fallback rules, combined-type handling, kicker convention details, and animation directive tables.
