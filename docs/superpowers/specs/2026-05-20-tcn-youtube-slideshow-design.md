# tcn-youtube-slideshow — Design Spec

**Status:** Approved (2026-05-20)
**Author:** Justin Hearn (drinkYourOJ / The Civic Node)
**Implementation track:** `tcn-youtube-slideshow` skill, to be built with `anthropic-skills:skill-creator`
**Position in ecosystem:** Step 2 of the TCN YouTube production workflow (upstream of recording)

---

## 1. Context — why this skill exists

The Civic Node publishes a flagship Substack article each week. Each article gets a companion 5-7 minute YouTube trailer-format video. The video pipeline so far:

1. `tcn-article-builder` produces the final article draft (existing).
2. `tcn-youtube-narration` produces a 5-7 minute trailer-format narration script with slide markers, pacing notes, and forward-compat hooks (built 2026-05-20).
3. **`tcn-youtube-slideshow` (this skill)** produces the visual companion deck.
4. Justin records the video reading the narration while presenting the deck.
5. Downstream packaging skills (`tcn-youtube-title`, `tcn-youtube-description`, `tcn-youtube-thumbnail`) handle YouTube upload.

Today, Justin's slideshow production workflow is ad-hoc: he opens `claude.ai/design`, references his existing TCN design system, references the prior week's deck, and asks Claude Design to make a new one. The result is competent but inconsistent. He also wants more visual energy — "more animation, more movement, like the pulsing logo but on steroids."

`tcn-youtube-slideshow` automates this: narration script in, a complete, structured Claude Design prompt out. The prompt references the existing TCN design system (CSS, kinetic JavaScript engine, slide-type templates, brand rules) and instructs Claude Design to build a bundled HTML slideshow with intensified-but-on-brand animation.

The skill does **not** generate slides from scratch. It is a **prompt-builder** that converts the narration's structure into a deterministic Claude Design brief. The design system already has everything the slideshow needs; the skill's job is precise context-handoff.

---

## 2. Position in the TCN ecosystem

```
Article workflow                 Video workflow                    YouTube packaging
(tcn-article-builder)            (upstream of recording)           (downstream of recording)
─────────────────────            ───────────────────────           ─────────────────────────
tcn-outline                                                         tcn-youtube-title
  ↓                                                                   ↑
tcn-outline-more                                                    tcn-youtube-description
  ↓                                                                   ↑
tcn-headline                                                        tcn-youtube-thumbnail
  ↓                                                                   ↑
tcn-opener                                                          (consumes timestamped transcript)
  ↓                                                                   ↑
tcn-draft                                                           ┌──── RECORDING ────┐
  ↓                                                                   ↑
tcn-readability                                                     tcn-youtube-slideshow  ← THIS SKILL
  ↓                                                                   ↑
tcn-text-humanizer                                                  (consumes youtube-narration.md)
  ↓                                                                   ↑
tcn-fact-check ↔ tcn-fact-reconcile                                 tcn-youtube-narration
  ↓                                                                   ↑
Final article draft  ──────────────────────────────────────────────  consumes the article
```

**This skill consumes:**
- `youtube-narration.md` — the narration script with slide markers + Script Notes footer (output of `tcn-youtube-narration`)
- The TCN design system bundle (CSS, deck-stage.js, slide templates, brand rules) — referenced, not duplicated

**This skill produces:**
- `youtube-slideshow.md` — a single, self-contained Claude Design prompt (markdown text) ready to paste into `claude.ai/design`

**Downstream consumers:**
- None directly. The deck is rendered by Claude Design and used by Justin during video recording.

---

## 3. Scope — in and out

**IN scope (this skill produces):**
- A single Claude Design prompt in markdown format
- Per-slide content directives (kicker text, headline, body, animation specs)
- A speaker-notes JSON block embedded in the prompt (the narration verbatim, slide-by-slide)
- Brand guardrails restated in the prompt (Terminal Authority aesthetic, restraint rules)

**OUT of scope (handled by other tools or skills):**
- Rendering the HTML deck (Claude Design renders)
- Authoring or extending the design system (it already exists; this skill references it)
- Extending `deck-stage.js` with new animation primitives (intentional limit — per Q8 decision)
- Generating narration (use `tcn-youtube-narration`)
- Producing thumbnails, social graphics, or YouTube metadata (separate planned skills)

---

## 4. Inputs and outputs (the skill's contract)

### Required input

- **Path to a finished narration:** typically `workspace/drafts/<slug>/youtube-narration.md`. The skill reads this file verbatim — slide markers, Script Notes footer, forward-compat hooks.

### Optional inputs

- **Path to TCN design system bundle.** Defaults to whatever path the user maintains (Justin's current path: `~/Documents/The Civic Node — Design System.zip`). If not provided, the skill leaves a placeholder in the prompt with an instruction to upload before pasting.
- **Steering** — free-text guidance like "use sl-compare instead of sl-frames on Slide 4" or "make Slide 3's chart larger" or "skip animation intensification on the Tease slide".
- **Override slide type** — for any individual slide, the user can force a specific template type (e.g., "Slide 3 must be sl-data with the SVG chart variant").

### Output artifact

- **File:** `workspace/drafts/<slug>/youtube-slideshow.md`
- **Contents:** a single, self-contained Claude Design prompt with all article-specific content filled in
- **Does NOT contain:** rendered HTML, CSS, or JavaScript — those are Claude Design's job

### Gate prompt presented to user

> Claude Design prompt complete (~[N] lines). Open `youtube-slideshow.md`, copy its contents, paste into a new Claude Design project at `claude.ai/design`, upload the design system files, and ask Claude Design to build the deck. Approve, redirect (e.g., 'swap slide 4 to sl-compare', 'lower animation intensity'), or cancel?

---

## 5. Slide-type mapping (narration → template)

The skill maps each narration slide to a slide-type from `slides/deck.html`. Mapping is deterministic by zone + slide sub-label, with one override hook for user steering:

| Narration slide | Default template type | Fallback / variant |
|---|---|---|
| Cold Open / Hook (Slide 1) | `sl-title` — full-bleed title, pulsing mark, slate-400 mark, mono kicker | — |
| Cold Open / Thesis (Slide 2) | `sl-lead` — prose-heavy lead with single h3 + 1-2 paragraph body | `sl-section` if thesis is one declarative phrase |
| Body / Receipt (data-heavy) | `sl-data` with `ms-numgrid` 3-column number layout | `sl-data` with `sl-chart` SVG if there's a real chart in the article |
| Body / Frame | `sl-frames` — [01]/[02]/[03] grid | `sl-compare` if it's two-way comparison |
| Body / Stakes | `sl-lead` | — |
| Body / Twist | `sl-frames` (numbered escalation) | `sl-compare` (before/after) |
| Body / Historical Echo | `sl-compare` (then/now) | `sl-lead` |
| Body / Verbatim | `sl-quote` — large pull quote, hairline above, source attribution below | — |
| Outro / Tease (Slide N-1) | `sl-lead` with bullet-style listing | `sl-section` with `[TEASE]` kicker if shorter |
| Outro / End (Slide N) | `sl-end` — canonical end-card, pulsing mark at 44px, disclosure block, URL CTA | — |

The skill picks the default per slide unless user steering or article structure flags a fallback. Picking is deterministic — the narration's slide sub-label (e.g., `THE RECEIPT, Unit Economics`) already indicates which type to use.

**Combined slide types (e.g., `THE FRAME + STAKES, Author's Debug` from dispatch-004):** the skill picks the first sub-label's type (`sl-frames` for Frame in this case) but adjusts the layout — fewer numbered columns, more prose — and notes the combination in the prompt. The skill does not invent new template types.

---

## 6. Kicker convention

The legacy decks used `PART ONE OF THREE` / `[01] CONTEXT` / `[02] FRAME` / `[03] CALL` kickers, mapping to the retired Cover/Part-One/Part-Two structure. The new convention uses the narration's actual zone + slide label:

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
- Middle dot `·` as separator (per README §3) — never `|`, never `/`
- Zero-padded dispatch number (`№004` not `№4`)
- Sub-labels in the kicker correspond to the narration's slide sub-label after the comma (e.g., `THE RECEIPT, Unit Economics` → `THE RECEIPT · UNIT ECONOMICS`)

---

## 7. Animation intensification directives (per Q8 decision: A, with later option for B)

The skill instructs Claude Design to use **existing primitives more aggressively**. No new CSS classes invented; no engine expansion. Specific directives:

| Primitive | Existing (in current decks) | Intensified (this skill prescribes) |
|---|---|---|
| `sl-reveal` cascade | Up to `sl-reveal-3` (3-stagger) | Up to `sl-reveal-5` (5-stagger), longer durations on body slides |
| `sl-mark-pulse` | Title slide only | Title + End slide + slow ambient pulse on Section dividers (mark at 24px) |
| `sl-caret` blinking | One kicker per page | Section heading kicker + end-card heading kicker (two per deck max) |
| `sl-chart-draw` | One data slide per deck | Every Data slide; if two data slides exist, second draws *after* first completes |
| `sl-glow` (radial slate) | Title slide only | Title + End slide + behind any single dominant number on Data slides |
| Hairline `sl-hairline` draws | Static lines | Animated draws on slide entry — left-to-right reveal in 360ms |

**Guardrails (preserved — non-negotiable):**
- No bounce, no spring, no rainbow gradients
- Easing remains `cubic-bezier(0.2, 0, 0, 1)`
- Durations remain in the 120/200/360ms family (no >500ms transitions)
- No emoji, no icon fonts, no shadows on dark
- One typeface (Courier Prime), Slate-400 / Slate-600 / Black / Twilight only

The prompt explicitly restates the guardrails so Claude Design does not drift toward exotic motion.

**Future option (Q8 = B, not built today):** if intensified primitives still feel static after Friday's deck, a future iteration can extend `deck-stage.js` with new primitives (e.g., scroll-triggered number counters, text-typewriter effects, programmatic chart morphing). The skill leaves room for this — the prompt structure can accept new animation directives without restructuring.

---

## 8. The prompt structure (what the skill outputs)

The output `youtube-slideshow.md` is a single markdown file with this structure:

```markdown
# Claude Design prompt — TCN Dispatch №[NNN] slideshow

## Context

You are building an HTML slideshow for The Civic Node, Dispatch №[NNN]:
"[Article Title]". The slideshow is the visual companion to a 5-7 minute
YouTube narration video; viewers will watch slides while listening to
the narration as audio.

## Inputs (attached / uploaded to this Claude Design project)

- `colors_and_type.css` — the brand CSS variable system. Load at runtime.
- `slides.css` — slide-specific styles (sl-title, sl-section, sl-lead, etc.)
- `deck-stage.js` — kinetic engine. Load via <script src="deck-stage.js">.
- `assets/mark.svg`, `assets/lockup-dark.svg` — brand marks.
- `slides/deck.html` — reference template; mimic its slide structure.

## Brand requirements (non-negotiable)

[Bulleted summary of design system §3-§4: voice, color, type, animation
guardrails, no emoji, no exclaim, mono typography only.]

## Slide-by-slide specification

### Slide 1 — sl-title
Kicker: `DISPATCH №[NNN] · HOOK`
Headline: [from narration Slide 1]
Tag (sub-line): [from narration cold-open candidate or steering]
Foot: `The Civic Node` / `[YYYY·MM·DD] · [N] MIN`
Animation: sl-mark-pulse on the mark; sl-reveal cascade 1→2→3 on
headline → tag → foot row. Hold for ~2s after pulse settles.

[... continues for all narration slides ...]

### Slide N — sl-end
[Canonical end-card with disclosure verbatim, pulsing mark at 44px,
URL CTA, sl-reveal cascade on disclosure block.]

## Speaker notes (embed as JSON at end of HTML)

[The complete narration script slide-by-slide, ready to paste into
the <script type="application/json" id="speaker-notes"> block. One
entry per slide. Narration text verbatim from youtube-narration.md.]

## Output requirements

- Single bundled HTML file named `dispatch-NNN.html`
- All resources loaded relatively (../colors_and_type.css, etc.)
- Speaker notes embedded as JSON
- Self-contained: opens in any browser, plays full deck via deck-stage.js
```

The skill's role is to compose this markdown prompt with all article-specific content filled in. The prompt is comprehensive enough that Claude Design can produce the bundle deterministically.

---

## 9. Skill process (internal steps)

1. **Locate the narration.** Read `youtube-narration.md` from the supplied path. Halt if missing.
2. **Parse slide structure.** Extract slide count, each slide's kicker sub-type (HOOK, THESIS, THE RECEIPT, etc.), the slide content, and the Script Notes footer.
3. **Parse forward-compat hooks** from the Script Notes footer. Use the "Cold-open candidate" to inform the Title slide's tag line. Use the "Refrain candidate" if present to inform animation timing (refrain lines get longer holds).
4. **Map each slide to a template slide type** per §5. Apply user steering or overrides if provided.
5. **Generate per-slide directives** — kicker text per §6, headline, body, animation specifications per §7.
6. **Compose the speaker-notes JSON block** — one entry per slide, narration text verbatim from `youtube-narration.md`.
7. **Verify design system bundle path.** If supplied, confirm the file exists. If not, leave a placeholder in the prompt with explicit instructions for the user to upload.
8. **Compute the dispatch date and runtime estimate** from the narration's Script Notes footer (runtime estimate is already calculated there; date is today's date or user-supplied recording date).
9. **Write the complete prompt** to `workspace/drafts/<slug>/youtube-slideshow.md`.
10. **Present to user with the standard gate prompt** (§4).

---

## 10. Failure modes & fallbacks

- **Narration file missing or unreadable** — halt, surface, ask for valid path.
- **Narration slides don't match expected structure** (no slide markers, no Script Notes footer, no zone labels) — surface to user; ask whether to proceed with best-effort parsing or halt. Default to halt if structure is severely malformed.
- **Design system bundle path not provided** — leave a placeholder in the prompt with a note ("upload your design system files to the Claude Design project before running this prompt") and continue.
- **More than 12 narration slides** — halt with warning. Trailer-format decks target 7-9 slides; >12 is a signal the upstream narration drifted from the format.
- **Combined slide type (e.g., FRAME + STAKES) encountered** — pick the first sub-label's template type, adjust the layout (fewer numbered columns, more prose), note the combination in the prompt's slide-by-slide block.
- **User redirects** — re-invoke the affected step. Common redirects:
  - "use sl-compare instead of sl-frames on Slide 4" → re-generate that slide's directive with the override
  - "lower animation intensity" → re-write all animation directives at one level lower (sl-reveal-3 max, no chained pulses, etc.)
  - "swap a slide" → re-map the affected slide and regenerate
  - "rebuild from scratch with steering X" → re-run the full process with steering applied

---

## 11. Relationship to companion skills

**Upstream (this skill consumes):**

| Source | Required? | Used for |
|--------|-----------|----------|
| `tcn-youtube-narration` output (`youtube-narration.md`) | Yes | Slide structure, content, Script Notes footer with forward-compat hooks |
| TCN design system bundle | Optional | Referenced in the prompt; not parsed by the skill itself |

**Downstream (sibling skills, planned, not built today):**
- `tcn-youtube-title` — packages titles for the YouTube upload
- `tcn-youtube-description` — packages descriptions
- `tcn-youtube-thumbnail` — produces thumbnail image prompts

**Shared design-system dependency:**
- The skill does NOT duplicate design-system content. It points at the bundle and trusts Claude Design to load and apply it. Same architecture pattern as the narration skill's reliance on `workspace/core/anti-ai-writing-style.md`.

---

## 12. Test criteria (definition of done)

The skill is working correctly when:

1. **Runs end-to-end on dispatch-004's narration** and produces a `youtube-slideshow.md` with: full Context block, brand requirements summary, slide-by-slide specifications for all 8 narration slides, speaker-notes JSON block, output requirements section.
2. **Each slide directive includes:** kicker text, slide type from the §5 mapping table, headline, body (or quote, or chart spec), animation directive per §7.
3. **Kicker convention is correct** — `DISPATCH №004 · [LABEL] · [SUB-LABEL]` pattern, middle-dot separator, zero-padded dispatch number, all caps.
4. **Speaker notes are verbatim from `youtube-narration.md`** — no paraphrasing, one entry per slide.
5. **Animation directives intensify existing primitives only** — no new CSS class names, no extensions to `deck-stage.js`.
6. **Brand guardrails are restated explicitly** in the Brand Requirements block.
7. **Dispatch number is detected** from the narration's title block (`Dispatch №NNN`), not regenerated.
8. **The output `youtube-slideshow.md` is self-contained** — opens in any markdown viewer, contains everything Claude Design needs in one paste.
9. **The skill halts gracefully** when narration is missing or malformed; surfaces the issue to the user before producing a partial prompt.
10. **End-to-end test:** Justin pastes the prompt into Claude Design, uploads the design system bundle, and Claude Design produces a working HTML deck without further clarification needed.

---

## 13. Implementation track

This spec hands off to:

1. **`superpowers:writing-plans`** — produces an implementation plan for the skill
2. **`anthropic-skills:skill-creator`** — produces the actual `SKILL.md` (and any `references/` files) following the conventions used by `tcn-youtube-narration` and the rest of the TCN skill family
3. **Test pass** — run the skill against `workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md` for Friday's dispatch-004 re-record; paste the resulting prompt into Claude Design; verify the rendered deck

**Source-of-truth location:** `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/SKILL.md`
**Runtime copy:** `~/.claude/skills/tcn-youtube-slideshow/SKILL.md` (symlink — per repo conventions)

---

## 14. Out of scope for this spec (deferred to separate brainstorms)

- **`tcn-youtube-title`** — title generation. Brainstorm largely complete; resume after Friday recording.
- **`tcn-youtube-description`** — description body + tags. Brainstorm largely complete; resume after Friday recording.
- **`tcn-youtube-thumbnail`** — image prompt + text overlay spec. Brainstorm largely complete; resume after Friday recording.
- **`tcn-youtube-shorts`** — Shorts variant. Future skill.
- **`tcn-youtube-pinned-comment`** — pinned comment generator. Future skill.
- **`tcn-youtube-end-screen`** — end-screen CTA script. Future skill.
- **deck-stage.js extension** — new animation primitives. Future iteration if Q8-A intensification proves insufficient.

---

## 15. Open architectural notes (not blocking)

- **Design system path portability.** Currently the canonical design-system bundle lives at `~/Documents/The Civic Node — Design System.zip`. As more skills consume it (slideshow today, future infographic / social-graphic / dashboard skills), this may want to move into a project-local path. Not in scope today; flag for later.
- **Kicker convention drift.** The new `DISPATCH №NNN · ZONE · SUB-LABEL` convention may want to migrate into the design system's `README.md` §3 as the canonical pattern, retiring the legacy `PART ONE OF THREE` convention from the spec itself. Not in scope today; flag for later when the slideshow skill has produced 2-3 decks and the convention is proven.
- **Speaker-notes parity with the narration script.** Today the narration script doubles as speaker notes by being embedded verbatim. If the recording workflow ever diverges from the narration (e.g., Justin ad-libs more), the speaker-notes block should reflect what was actually said, not the original narration. Not in scope today.
