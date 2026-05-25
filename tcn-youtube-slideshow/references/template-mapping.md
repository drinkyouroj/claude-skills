# Template Mapping — tcn-youtube-slideshow

*Loaded at runtime when mapping a specific narration slide to a slide directive. Holds the slide-type table, kicker convention, and animation intensification rules — pulled out of `SKILL.md` so the main file stays skim-able.*

---

## 1. Slide-type mapping

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

The skill picks the **default** unless user steering or article structure flags a fallback. The narration's slide sub-label (e.g., `THE RECEIPT, Unit Economics`) already indicates which type to use — picking is deterministic, not creative.

**Combined slide types** (e.g., `THE FRAME + STAKES, Author's Debug`) → pick the FIRST sub-label's template type, adjust the layout (fewer numbered columns, more prose), note the combination in the prompt. Do NOT invent new template types.

---

## 2. Kicker convention

The canonical pattern:

```
DISPATCH №[NNN] · [ZONE LABEL] · [optional SUB-LABEL]
```

All 8 kickers from the dispatch-004 narration on disk:

```
DISPATCH №004 · HOOK
DISPATCH №004 · THESIS
DISPATCH №004 · THE RECEIPT · UNIT ECONOMICS
DISPATCH №004 · THE RECEIPT · HIP-143
DISPATCH №004 · THE TWIST · VOTE CONCENTRATION
DISPATCH №004 · THE FRAME + STAKES · AUTHOR'S DEBUG
DISPATCH №004 · TEASE
DISPATCH №004 · END
```

Kicker rules:

- Mono typeface (Courier Prime), wide-tracked at `0.18em`, all-caps, slate-400 (`#557FA3`) on dark background
- Middle dot `·` as separator (per design system README §3) — never `|`, never `/`
- Zero-padded dispatch number (`№004`, not `№4`)
- Sub-labels in the kicker come from the narration's slide sub-label after the comma (e.g., `THE RECEIPT, Unit Economics` from the narration → `THE RECEIPT · UNIT ECONOMICS` in the kicker)
- The legacy kicker convention (`PART ONE OF THREE`, `[01] CONTEXT`, `[02] FRAME`, `[03] CALL`) is retired

---

## 3. Animation intensification

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
- One typeface (Courier Prime), Slate-400 / Slate-600 / Black / Twilight palette only

The skill's prompt explicitly restates these guardrails so Claude Design doesn't drift toward exotic motion. Intensification means more uses of existing primitives, longer staggers, broader application — not new motion vocabulary.

---

## 4. Visible-text budgets per template type

Each slide displays ≤25 visible words across all on-screen elements (kicker + headline + body + foot row + attribution), OR one hero number + ≤15 supporting words. Speaker notes are separate; this budget applies only to what *renders on screen.*

| Template | Visible-text budget | Thumbnail anchor |
|---|---|---|
| `sl-title` | ~12 words total; headline ≤8 words | Headline (`--type-h1`) |
| `sl-lead` | ~22 words total; heading ≤6 words, body ≤16 words | Heading (`--type-h2`) |
| `sl-section` | ~10 words total; section label ≤5 words | Section label (`--type-h2`) |
| `sl-data` (numgrid) | one hero number + ≤15 words of labels/units | The dominant figure (`--type-hero`) |
| `sl-data` (chart) | chart + axis labels + ≤10 words of caption | The highest bar / dominant data point |
| `sl-frames` | ~20 words across [01]/[02]/[03] (~6-7 per frame) | The current frame's label (rendered at `--type-h1`) |
| `sl-compare` | ~18 words total (~8-9 per side) | The compared term currently on screen |
| `sl-quote` | ≤25 words quote + ≤10 words attribution | First clause of the quote (`--type-h1`) |
| `sl-end` | ≤25 words total | "The Civic Node" or the Substack URL |

Going over budget on any single element is the trigger for splitting (§ 5). Going under is fine — a hero number with a 4-word caption is exactly the slide we want.

### Per-element size assignment

Every visible text element is assigned exactly one of these roles (defined in the prompt's `:root` block as CSS custom properties — see SKILL.md "Small-screen / multi-aspect requirements"):

- `--type-hero` — the single dominant element, ≥20% safe-zone height
- `--type-h1` / `--type-h2` — the slide's headline / heading
- `--type-body` — supporting paragraphs, bullets, sub-lines
- `--type-kicker` — kicker, foot row, attribution, disclosure copy

No ad-hoc `font-size` declarations elsewhere in the deck.

---

## 5. Slide-splitting rules

When a narration slide's mapped content exceeds the visible-text budget for its template, split the *visual* into two panels with a shared kicker. The narration stays one slide for pacing and speaker-notes purposes.

### When to split

Split if any of:

- Total visible word count > budget for the template type
- Number of distinct data points > what the template comfortably holds (e.g., 4 numbers in `sl-data` numgrid which targets 3, 4 frames in `sl-frames` which targets 3, 3 columns in `sl-compare` which targets 2)
- Hero anchor cannot be identified because no single element dominates

Do NOT split for narrative reasons. Split only when visible-text density would break thumbnail readability. Narrative re-pacing is the narration skill's job.

### How to split

- The narration block stays one entry in the `speaker-notes` JSON, verbatim.
- The visual deck renders two slides labeled `[N]-a` and `[N]-b`.
- Both panels carry the **same kicker** (e.g., `DISPATCH №004 · THE RECEIPT · HIP-143`).
- Panel-a includes a `data-advance-at="MM:SS"` attribute pointing to the timestamp inside the narration when panel-b should appear. The `deck-stage.js` engine handles the auto-advance.
- The split point in the narration is chosen to align with a sentence boundary, ideally a one-word landing or a refrain marker.

### Per-template splitting patterns

| Template | Typical split |
|---|---|
| `sl-data` (numgrid) with 4-6 numbers | Panel-a: numbers 1-3 with their captions. Panel-b: numbers 4-6 + sl-glow behind the dominant figure. Shared kicker. |
| `sl-frames` with 4-5 escalating frames | Panel-a: frames [01]–[03]. Panel-b: frames [04]–[05] with a hairline draw on entry to signal continuation. |
| `sl-lead` with 3+ paragraphs of body | Panel-a: heading + first paragraph. Panel-b: heading repeated + remaining paragraph(s), shifted vertical position. |
| `sl-compare` with 3 compared columns | Panel-a: first two columns. Panel-b: third column alone or paired with the most-contrasting prior column. |
| `sl-quote` longer than ~25 words | Panel-a: first half of quote + hairline. Panel-b: second half + attribution. Both at `--type-h1`. |

### Splitting cap

If more than ~2 slides in a single deck need splitting, halt and surface to the user before producing the prompt. That signal means the upstream narration drifted long for small-screen format — the fix is to re-pace the narration (target 9-12 slides at smaller per-slide density), not to mass-split visually. Silent half-deck splits would hide the upstream problem.

---

## 6. Future-option seam

Per the spec's Q8=B path, a future iteration may extend `deck-stage.js` with NEW animation primitives — scroll-triggered number counters (numbers ticking up), text-typewriter effects on quote slides, programmatic chart morphing between data slides, dynamic radial-glow pulses that breathe with the slide. Not built today — the existing primitives, used aggressively, should be enough for the first few decks. When/if needed, the prompt structure can accept new animation directives without restructuring the skill itself — only the §3 animation table and the SKILL.md's Animation Intensification section need updating.
