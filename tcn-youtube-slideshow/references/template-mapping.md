# Template Mapping — tcn-youtube-slideshow

*Kicker convention reference for scene-header slides. Loaded at runtime by `tcn-youtube-slideshow`.*

*Note: §1 (slide-type mapping) and §3+ (animation intensification) were superseded by the beat-segmented format introduced 2026-06-03. See `references/beat-types.md` for the current beat type taxonomy and `docs/superpowers/specs/2026-06-03-youtube-constant-motion-design.md` for the design rationale. The archived content is preserved below the `---ARCHIVED---` marker.*

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

---ARCHIVED (superseded 2026-06-03)---

## 1. Slide-type mapping [ARCHIVED]

| Narration slide | Default template type | Fallback / variant |
|---|---|---|
| Cold Open / Hook (Slide 1) | `sl-title` — full-bleed title, pulsing mark, slate-400 mark, mono kicker | — |
| Cold Open / Thesis (Slide 2) | `sl-lead` — prose-heavy lead with single h3 + 1-2 paragraph body | `sl-section` if thesis is one declarative phrase |
| Body / Receipt (data-heavy) | `sl-data` with `ms-numgrid` 3-column number layout | `sl-data` with `sl-chart` SVG if there's a real chart in the article |
| Body / Frame | `sl-frames` — [01]/[02]/[03] grid | `sl-compare` if it's two-way comparison |
| Body / Anaphora (paired-statement refrain) | `sl-compare` — two-pair side-by-side, paired statements are the rhetorical move | `sl-frames` if more than two pairs |
| Body / Stakes | `sl-lead` | — |
| Body / Twist | `sl-frames` (numbered escalation) | `sl-compare` (before/after) |
| Body / Historical Echo | `sl-compare` (then/now) | `sl-lead` |
| Body / Verbatim | `sl-quote` — large pull quote, hairline above, source attribution below | — |
| Outro / Tease (Slide N-1) | `sl-lead` with bullet-style listing | `sl-section` with `[TEASE]` kicker if shorter |
| Outro / End (Slide N) | `sl-end` — canonical end-card, pulsing mark at 44px, disclosure block, URL CTA | — |

The skill picks the **default** unless user steering or article structure flags a fallback. The narration's slide sub-label (e.g., `THE RECEIPT, Unit Economics`) already indicates which type to use — picking is deterministic, not creative.

**Combined slide types** (e.g., `THE FRAME + STAKES, Author's Debug`) → pick the FIRST sub-label's template type, adjust the layout (fewer numbered columns, more prose), note the combination in the prompt. Do NOT invent new template types.

---

## 3. Animation intensification [ARCHIVED]

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

## 4. Visible-text budgets per template type [ARCHIVED]

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

## 5. Slide-splitting rules [ARCHIVED]

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

## 6. Future-option seam [ARCHIVED]

Per the spec's Q8=B path, a future iteration may extend `deck-stage.js` with NEW animation primitives — scroll-triggered number counters (numbers ticking up), text-typewriter effects on quote slides, programmatic chart morphing between data slides, dynamic radial-glow pulses that breathe with the slide. Not built today — the existing primitives, used aggressively, should be enough for the first few decks. When/if needed, the prompt structure can accept new animation directives without restructuring the skill itself — only the §3 animation table and the SKILL.md's Animation Intensification section need updating.

---

## 7. Justoon variant-pick guidance [ARCHIVED]

Activated when `--justoon-refs` is provided to the skill. Read this section at process step 5b ("Pick Justoon variants").

The Justoon role per slide type is locked in the SKILL.md mapping table (Receipt/Stakes → A; Twist → C; others → none). This section is the **interpretive layer** that picks the specific filename inside each role based on the slide's content.

### Role A — Pointing teacher (full-body)

Picked for Receipt and Stakes slides. Available variants:

| File | When to pick |
|---|---|
| `justoon-point-right.png` | **Default.** Slide layout has the hero stat / headline on the right; Justoon left points across to it. Receipt slides almost always land here. |
| `justoon-point-up.png` | Slide layout has the hero stat / headline above Justoon. Less common — use when the narration phrasing implies "look up at this" or when a vertical 9:16 derivative wants Justoon at the bottom pointing up to text above. |
| `justoon-point-down.png` | Slide layout has the hero stat below Justoon (rare — only when the visual composition really wants Justoon at the top half pointing down). |
| `justoon-point-open-palm.png` | **Bidirectional fallback.** Soft "here's the thing" presenting gesture. Use when the slide content is more presentational than data-pointed (e.g., a Stakes slide that summarizes rather than naming a specific number). Also use when neither the right-pointing nor up-pointing variants feel right. |

Picking rule:
- If the slide has a single dominant hero number / hero word in the right half of the safe-zone → `justoon-point-right.png`
- If the dominant element is above Justoon → `justoon-point-up.png`
- If the slide is presentational (multiple supporting points, no single hero stat) → `justoon-point-open-palm.png`
- Default fallback within role A → `justoon-point-right.png`

### Role C — Reaction-as-anchor (bust)

Picked for Twist slides. Available variants:

| File | When to pick |
|---|---|
| `justoon-react-deadpan.png` | The dry, flat-stare register. For Twist slides whose narration close is deadpan / "by whom, the company says, can't be known" / "the cause was impossible to determine" / any slide where the rhetorical move is *the absence of expression*. The canonical role C variant. |
| `justoon-react-raised-eyebrow.png` | The "really?" register. For Twist slides where the absurdity is the move but the figure shouldn't editorialize fully. |
| `justoon-react-concerned.png` | Furrowed brow, alarm. For Twist slides where the stakes are real and the figure should signal that. |
| `justoon-react-smirk.png` | The sardonic-amused register. For Twist slides whose narration carries dry wit or "you can't make this up" energy. The TCN signature dial. |
| `justoon-react-shocked.png` | Open mouth, "they did WHAT". For Twist slides at the highest-arousal register. **Use sparingly** — shock loses force when overused; reserve for genuinely visceral reveals (~1 in 5 Twist slides). |

Picking rule (interpretive — read the slide's narration body, not just the kicker):
- Default fallback within role C → `justoon-react-deadpan.png` (the canonical TCN-Marcus close)
- Narration ends with a "you can't make this up" smirk → `justoon-react-smirk.png`
- Narration carries an "I want to react but I'm restraining myself" beat → `justoon-react-raised-eyebrow.png`
- Narration signals real-stakes alarm → `justoon-react-concerned.png`
- Narration is high-arousal incredulity → `justoon-react-shocked.png`

### Anchor / fallback

`justoon-neutral.png` is the required anchor. Used when:
- A mapped variant is missing from the refs dir (silent substitution; note in artifact header)
- A future skill consumer needs a stable Justoon image without role context (e.g., a `tcn-youtube-thumbnail` cross-reference)

### Coherence across slides

Don't aggressively vary Justoon variants across a single deck — the figure should feel consistent. A deck with three Twist slides shouldn't pick three different reactions just for variety; pick the variant that fits the dominant register and reuse it unless a specific slide demands a different read.

### Worked example (dispatch-005, bill-of-rights-contractors-door)

The 11-slide deck has 4 slides with Justoon roles active:

- Slide 3 (Receipt · Bend): role A → `justoon-point-right.png` (hero stat "279" is in the right half)
- Slide 4 (Receipt · Scale): role A → `justoon-point-right.png` (consistency with Slide 3; hero stats "364,000" / "1.6 million" / "4,500" all live in the right half)
- Slide 8 (Twist): role C → `justoon-react-deadpan.png` (the narration close "By whom, the company says, can't be known." is the canonical deadpan beat)
- Slide 9 (Stakes): role A → `justoon-point-open-palm.png` (presentational summary of Atlanta's resolution stack, no single hero stat)

The other 7 slides (Hook, Thesis, Frame, Anaphora ×2, Tease, End) stay typography-only.
