---
name: tcn-youtube-slideshow
description: "Step 2 of the Civic Node YouTube production workflow: runs directly in Claude Design to convert an uploaded beat-segmented narration script into a complete ~110-slide constant-motion HTML deck. Two-pass workflow: Pass 1 identifies illustration beats and outputs a fal.ai image-generation batch; Pass 2 (after images are uploaded) builds the full deck with one slide per beat plus scene-header slides. Invoke when the user uploads a youtube-narration.md in Claude Design and says 'build the slideshow', 'make the slides', or 'run this skill'. Does NOT apply to article slides, social media graphics, or thumbnail generation."
---

# The Civic Node — YouTube Slideshow (Step 2 of the YouTube Production Workflow)

## What This Skill Does

Converts a finished YouTube narration script into a complete ~110-slide constant-motion HTML deck. Each narration beat becomes one static slide; scene labels become scene-header slides. The deck plays as near-continuous motion — ~2-3 seconds of static screen between slide advances.

**This skill runs directly in Claude Design.** It does not produce a prompt file for a human to paste. The user uploads `youtube-narration.md` to a Claude Design project, loads this skill as context, and Claude Design executes the workflow directly.

**Two-pass workflow:**
- **Pass 1:** Read the narration, identify illustration beats, output a numbered fal.ai image-generation batch. Pause for the user to generate and upload images.
- **Pass 2:** After images are uploaded, build the full HTML deck — scene-header slides + one beat slide per narration beat — referencing uploaded images for illustration beats.

**Output:** A single bundled HTML file (`dispatch-NNN.html`) with ~110 slides, simple CSS cross-dissolve transitions, and manual keypress advancement. No dependency on `deck-stage.js` or the existing animation primitive system.

---

## Why Beats, Not Animation States

The previous format used ~10 slides with animation primitives (`sl-reveal` cascades, `sl-chart-draw`, etc.) that built up content within each slide. Two problems:

1. **Claude Design's animation UI is hard to verify.** You can't see beat 7 of 13 without playing through the animation. If beat 7 is wrong, you have to describe an animation state change and hope Claude Design re-generates it correctly.

2. **On-screen motion came from animation, not from visual change.** A viewer watched one slide for 30-40 seconds while elements appeared. That's not constant motion.

With discrete static slides — one per beat — both problems disappear. Each slide is a visible, editable object. Motion comes from advancing slides, not from animation triggers. The recording workflow (Justin pressing a key at each beat-stop) produces genuine visual change every 2-3 seconds.

**What this means for Claude Design:** build simple, static slides. The only transition is a 200ms cross-dissolve between slides. No `sl-reveal`, no `sl-chart-draw`, no cascade primitives. The content is what changes; the animation is incidental.

---

## Position in the YouTube Workflow

This skill is **Step 2 of the YouTube production workflow** — it runs after the narration is approved and before video recording.

**Upstream (what this skill reads):**
- `tcn-youtube-narration` output (`youtube-narration.md`) — uploaded to Claude Design. Contains scenes, beats, element notes, refrain markers, Script Notes footer.

**Downstream (sibling skills, planned):**
- `tcn-youtube-title` — title generation, consumes the recorded transcript.
- `tcn-youtube-description` — description body, tags, chapter timestamps, consumes the recorded transcript.
- `tcn-youtube-thumbnail` — thumbnail image prompt + text overlay, consumes the recorded transcript and cold-open candidate.

The packaging skills run after recording because they consume the timestamped transcript, not the upstream narration. This skill is the last upstream-of-recording step.

The full design rationale lives in `docs/superpowers/specs/2026-06-03-youtube-constant-motion-design.md`.

---

## Inputs and Outputs

### Required input (upload to Claude Design project)

- **`youtube-narration.md`** — the finished beat-segmented narration from `tcn-youtube-narration`. Contains scene labels, beat markers (`▸ **B1** · *element:* ...`), `[REFRAIN]` markers, and Script Notes footer.

### Optional inputs

- **Uploaded fal.ai images** — present only in Pass 2. Named per the `NNN-SS-BNN.png` convention (see `references/image-prompt-style.md`). Absence in Pass 1 is expected; absence in Pass 2 means the illustration slides will render with placeholder boxes.
- **Steering** — free-text guidance like "make the refrain treatment use a border instead of inverted colors", "scene 4 needs a different illustration approach", "no scene-header slides".

### Output artifact

- **File:** `dispatch-NNN.html`
- **Contents:** ~110 static slides (one per beat + one scene-header per scene), CSS cross-dissolve transitions, manual keypress advancement
- **Does NOT contain:** speaker notes, animation primitives, deck-stage.js dependency

### Gate prompt presented to user (Pass 1)

> Image batch complete — [N] illustration beats across [M] scenes. Generate these images using fal.ai with the style anchor from `references/image-prompt-style.md`. Upload the results to this Claude Design project, then say "continue" to build the deck.

### Gate prompt presented to user (Pass 2)

> Deck complete — [N] slides ([M] scenes × 1 scene-header + [K] beat slides). Open `dispatch-NNN.html` in a browser, resize to 1:1 (1080×1080), and advance through the deck to verify. Approve, redirect, or cancel?

**Stop after each pass gate.** Do not proceed to Pass 2 without user confirmation that images have been uploaded.

---

## Beat Type Taxonomy

Every beat from the narration is assigned one of five types before any slides are built. Full CSS skeletons and worked examples for each type live in `references/beat-types.md`.

| Type | Source | Visual treatment | Needs image? |
|---|---|---|---|
| `scene-header` | Generated from scene label (not a beat) | TCN kicker, dark BG, kicker text only | No |
| `stamp` | Beat with short text/phrase as element | Text centered, Courier Prime, dark BG | No |
| `hero-number` | Beat with a single figure as element | Large number + optional label, dark BG | No |
| `refrain` | Beat marked `[REFRAIN]` | Full-screen phrase, **inverted colors** (white BG, black text) | No |
| `illustration` | Beat whose element can't be produced with typography | Full-bleed fal.ai image, optional text overlay | **Yes** |

**Typing rule:** if the `element:` note describes anything other than words, numbers, or short phrases on a plain dark background — type it as `illustration`. Everything else falls to stamp, hero-number, or refrain.

**scene-header slides** are generated (not typed from beats). One scene-header per scene. Kicker format: `DISPATCH №NNN · SCENE NAME`. Full kicker convention in `references/template-mapping.md` §2.

**refrain treatment is non-negotiable.** The inverted colors (white background, black text) signal recurrence to the viewer. Every `[REFRAIN]` beat gets identical visual treatment — no variation between instances.

**illustration overlays:** when a beat's element note includes text landing over an illustration (e.g. "$400,000 lands over the left figure"), the fal.ai image is the base visual and the text is an HTML/CSS overlay. The image is still generated in Pass 1; the overlay is added in Pass 2 using the `illustration` CSS skeleton's `.overlay-text` class.

---

## Kicker Convention

Full kicker convention, rules, and examples: `references/template-mapping.md` §2.

---

## Two-Pass Workflow

### Pass 1 — Image generation batch

1. **Read the uploaded narration.** Parse scenes, beats, element notes, refrain markers.

2. **Type every beat.** Apply the typing rule from Beat Type Taxonomy above. Produce a brief inventory:

```
Beat inventory — Dispatch №006 (102 beats across 10 scenes):
  scene-header: 10 (generated)
  stamp: 38
  hero-number: 14
  refrain: 2
  illustration: 38
  Total slides: 112
```

3. **Output the image batch.** For every `illustration` beat, produce one numbered image prompt in this format:

```
IMAGE BATCH — Dispatch №NNN ([N] images)

[001] Scene SS · BNN
Style: flat vector illustration, dark background (#0f172a), muted slate color palette
(#334155 mid-slate, #475569 slate, #64748b light-slate, #e2e8f0 near-white for
highlights), clean geometric lines, no gradients, no photography, no realistic
textures, no shadows, no lens flare, minimal detail, geometric simplification,
editorial illustration aesthetic
Content: [description derived from element note — composition, colors from palette,
negative space for text overlays, no text in image]
Filename: NNN-SS-BNN.png

[002] Scene SS · BNN
...
```

Full style anchor and worked examples: `references/image-prompt-style.md`.

4. **Present Pass 1 gate prompt and stop.** Do not proceed until the user confirms images have been uploaded.

### Pass 2 — Full deck build

1. **Confirm image uploads.** Check that the uploaded filenames match the batch. Note any missing images (those illustration slides will render with a dark placeholder box and a note).

2. **Build scene-header slides.** One per scene, in order. Kicker text from the scene label. Format: `DISPATCH №NNN · [SCENE NAME IN CAPS]`.

3. **Build beat slides in order.** For each beat:
   - Apply the beat's type template (CSS skeletons in `references/beat-types.md`)
   - For illustration beats: reference the uploaded image by filename; add text overlay if the element note includes text landing over the image
   - For refrain beats: apply the inverted-color treatment
   - For stamp/hero-number beats: apply the typography template

4. **Write the complete HTML deck.** One file: `dispatch-NNN.html`. Structure:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>The Civic Node — Dispatch №NNN</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #000;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      overflow: hidden;
    }

    .deck {
      position: relative;
      width: min(100vw, 100vh);
      height: min(100vw, 100vh);
    }

    .slide {
      position: absolute;
      inset: 0;
      container-type: size;
      opacity: 0;
      transition: opacity 200ms cubic-bezier(0.2, 0, 0, 1);
      pointer-events: none;

      --type-hero:   clamp(80px, 24cqmin, 360px);
      --type-h1:     clamp(28px,  9cqmin, 144px);
      --type-h2-mid: clamp(22px,  6.5cqmin, 96px);
      --type-body:   clamp(14px,  5cqmin,  72px);
      --type-kicker: clamp(10px,  2.5cqmin, 36px);
      --safe-zone:   min(85cqw, 85cqh);
    }

    .slide.active {
      opacity: 1;
      pointer-events: auto;
    }

    /* Beat type CSS — see references/beat-types.md for full skeletons */
    .slide.scene-header { background: #0f172a; display: flex; align-items: center; justify-content: center; }
    .slide.scene-header .kicker { font-family: 'Courier Prime', monospace; font-size: var(--type-kicker); letter-spacing: 0.18em; text-transform: uppercase; color: #557FA3; }

    .slide.stamp { background: #0f172a; display: flex; align-items: center; justify-content: center; padding: min(7.5cqw, 7.5cqh); }
    .slide.stamp .text { font-family: 'Courier Prime', monospace; font-size: var(--type-h1); color: #e2e8f0; text-align: center; text-wrap: balance; }

    .slide.hero-number { background: #0f172a; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1cqmin; }
    .slide.hero-number .number { font-family: 'Courier Prime', monospace; font-size: var(--type-hero); color: #e2e8f0; text-align: center; line-height: 1; }
    .slide.hero-number .label { font-family: 'Courier Prime', monospace; font-size: var(--type-body); color: #557FA3; text-align: center; text-wrap: balance; }

    .slide.refrain { background: #f8fafc; display: flex; align-items: center; justify-content: center; padding: min(7.5cqw, 7.5cqh); }
    .slide.refrain .text { font-family: 'Courier Prime', monospace; font-size: var(--type-h1); color: #0f172a; text-align: center; text-wrap: balance; }

    .slide.illustration { position: relative; background: #0f172a; }
    .slide.illustration .bg-image { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center; }
    .slide.illustration .overlay-text { position: absolute; bottom: 15cqh; left: 50%; transform: translateX(-50%); font-family: 'Courier Prime', monospace; font-size: var(--type-hero); color: #e2e8f0; text-align: center; text-shadow: 0 0 40px rgba(0,0,0,0.8); white-space: nowrap; }
  </style>
</head>
<body>
  <div class="deck" id="deck">

    <!-- Scene 01: HOOK -->
    <div class="slide scene-header active" id="s01-header">
      <div class="kicker">DISPATCH №NNN · HOOK</div>
    </div>

    <!-- Scene 01 · B1 — illustration -->
    <div class="slide illustration" id="s01-b01">
      <img class="bg-image" src="NNN-01-B01.png" alt="">
    </div>

    <!-- Scene 01 · B2 — stamp -->
    <div class="slide stamp" id="s01-b02">
      <div class="text">SAME SHIFT</div>
    </div>

    <!-- [continues for all beats...] -->

  </div>
  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    let current = 0;

    function advance() {
      slides[current].classList.remove('active');
      current = Math.min(current + 1, slides.length - 1);
      slides[current].classList.add('active');
    }

    function retreat() {
      slides[current].classList.remove('active');
      current = Math.max(current - 1, 0);
      slides[current].classList.add('active');
    }

    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'ArrowDown') advance();
      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') retreat();
    });

    document.addEventListener('click', advance);
  </script>
</body>
</html>
```

5. **Present Pass 2 gate prompt.** See Inputs and Outputs section.

---

## Small-Screen Readability and Multi-Aspect Layout

The deck must be **readable at thumbnail size** (a phone watching a YouTube card, ~240px wide playback) and must play correctly at **16:9, 9:16, and 1:1 from a single HTML source**. This is non-negotiable. The prompt encodes the rules explicitly so Claude Design enforces them at render time.

### 1:1 is the primary canvas; other aspects are derivative

**Recording happens at 1:1 (1080×1080).** The 16:9 and 9:16 outputs are derived from the same HTML by changing the recording window's aspect — the slide content does not reflow. This was confirmed by the 2026-05-25 hand-test (see `docs/superpowers/reference-renders/2026-05-25-justoon-slideshow-layout.html` in the Substack Research project for the proven layout).

The mechanism that makes one HTML work at three aspects: the **safe zone is always a square** (`min(85cqw, 85cqh)`), so designing slide content inside the safe zone means it renders identically at any aspect — only the empty viewport margin differs. Critical insight: think of the slide-design problem as "what fits inside a square," not "what fits inside a 16:9 rectangle."

- Each `.slide` element uses `container-type: size` so cq-units scale to the slide, not the viewport. This decouples slide layout from page layout — necessary if multiple slides ever share a page.
- Define `--safe-zone: min(85cqw, 85cqh)` per slide. Every slide's critical-content container is exactly this size, centered.
- Critical content (kicker, headline, body, hero numbers, source attributions, CTA, disclosure, any Justoon image) lives ONLY inside the safe zone.
- Decorative elements (brand mark, `sl-hairline` rules, `sl-glow` radial, slide background fill) may extend to slide edges.
- No fixed-pixel widths on layout containers. No media queries based on aspect ratio. Layout is identical at every aspect; only the empty margin differs.

### Type scale (cqmin-based; tuned for 1:1 primary canvas)

Using `cqmin` (1% of the slide container's smaller dimension) means a 1080-tall slide and a 1080-wide slide produce identical type — exactly what multi-aspect requires. The clamps below are tuned for 1:1 as the primary recording aspect, with floors gentle enough that derivative aspects (16:9 / 9:16) stay legible without overweighting them.

| Role | Size | Why this floor |
|---|---|---|
| **Hero number / hero word** (the slide's thumbnail anchor) | `clamp(80px, 24cqmin, 360px)` | Readable at 240px playback. Occupies ~25% of safe-zone height. Floor lowered from 180px (vmin era) because cqmin scales per slide, not viewport. |
| **Headline (h1, used for primary heading slides)** | `clamp(28px, 9cqmin, 144px)` | Comfortably readable at full size; legible at thumbnail. |
| **Headline mid (h2-mid, used for body slides where the headline isn't the anchor)** | `clamp(22px, 6.5cqmin, 96px)` | New role added during the 2026-05-25 hand-test for slides where Justoon is the anchor and the headline is supporting (role C twist slides especially). |
| **Body / supporting text (h3, p, bullet)** | `clamp(14px, 5cqmin, 72px)` | Floor lowered from 30px (vmin era) so body text stays clean at thumbnail without forcing the headline floor up. |
| **Kicker, foot row, disclosure copy** | `clamp(10px, 2.5cqmin, 36px)` | Decorative / contextual. Floor lowered from 18px so thumbnail kicker reads as texture, not legible content. |

No exceptions. No `font-size: 14px` (or other ad-hoc values) anywhere in the deck.

**Text-wrap directive:** every headline and caption uses `text-wrap: balance` to distribute lines visually rather than greedy-fill ragged-right. This was added during the hand-test after the 9:16 portrait view produced 2-character-wide ragged lines without it.

### Thumbnail-anchor rule (one per slide)

**Every slide must have exactly one element ≥20% of the safe-zone height.** That element is the slide's *thumbnail anchor* — what a phone viewer sees when the video appears as a 240px card.

| Template | Thumbnail anchor |
|---|---|
| `sl-title` | The dispatch title (h1) |
| `sl-lead` | The lead heading (h2) |
| `sl-section` | The section label (h2) |
| `sl-data` | The single dominant number (`ms-numgrid`'s lead figure, OR the highest bar in the chart) |
| `sl-frames` | The current frame's label (rendered large; supporting numbers stay small) |
| `sl-compare` | The compared term currently on screen (rotates if both shown) |
| `sl-quote` | The quote's first short clause (rendered large; rest of quote in body size) |
| `sl-end` | "The Civic Node" wordmark or the Substack URL |

If a slide cannot identify a single anchor, the slide is too dense — split it (see below).

### Visible-text budget (per slide)

Each slide displays **≤25 visible words** across all elements (kicker + headline + body + foot row + attribution), OR **one hero number + ≤15 supporting words**. Speaker notes are separate; this budget is for what *renders on screen.*

| Template | Typical budget |
|---|---|
| `sl-title` | ~12 words (kicker + headline + tag + foot row) |
| `sl-lead` | ~22 words (kicker + heading + 1-2 short body sentences) |
| `sl-section` | ~10 words (kicker + section label) |
| `sl-data` | one hero number + ≤15 words of labels/units/supporting text |
| `sl-frames` | ~20 words across [01]/[02]/[03] combined (~6-7 per frame) |
| `sl-compare` | ~18 words across both columns (~8-9 per side) |
| `sl-quote` | ≤25 words of quote + ≤10 words of attribution |
| `sl-end` | ≤25 words (URL + tagline + disclosure) |

### Slide-splitting rule

If a narration slide's mapped content exceeds the visible-text budget for its template, **split the visual into two panels with a shared kicker**:

- The narration stays one slide (one entry in `speaker-notes` JSON, with the full narration verbatim).
- The visual becomes Slide N-a and Slide N-b in the rendered deck.
- Both panels share the same kicker (e.g., `DISPATCH №004 · THE RECEIPT · HIP-143`).
- The narration plays continuously across both panels; the second panel auto-advances mid-narration via a `data-advance-at` timestamp on the slide element (`deck-stage.js` already supports timed advance — no engine extension needed).

Splitting is a last resort. The narration skill (`tcn-youtube-narration`) targets 9-12 slides specifically so most content arrives pre-paced for small-screen consumption and splitting is rare. If splitting fires on more than ~2 slides in a deck, surface that to the user as a signal the narration drifted long; do not silently split half the deck.

### What this means for Claude Design

The prompt produced by this skill includes (a) a `--safe-zone` CSS variable with the `min(85vw, 85vh)` formula, (b) the full type-scale table as concrete CSS rules, (c) explicit per-slide visible-text budgets in each slide's directive, (d) the thumbnail-anchor rule called out per slide, and (e) explicit panel-split markup wherever the skill split a slide. Claude Design renders these as written; it does not re-decide layout.

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

## Small-screen / multi-aspect requirements (non-negotiable)

This deck must render correctly at 16:9, 9:16, and 1:1 from this single
HTML file, and must be readable at thumbnail playback (~240px wide on a
phone). **The primary recording aspect is 1:1 (1080×1080).** The 16:9
and 9:16 outputs are derived from the same HTML by changing the
recording window's aspect — slide content does not reflow.

The mechanism: the safe zone is always a square (`min(85cqw, 85cqh)`).
Design slide content inside the safe zone and it renders identically at
any aspect — only the empty viewport margin differs.

- Each `.slide` element uses `container-type: size` so cq-units scale
  to the slide, not the viewport. This decouples slide layout from
  page layout.
- Define `--safe-zone: min(85cqw, 85cqh)` per slide. Every slide's
  critical-content container is exactly this size, centered.
- Critical content (kicker, headline, body, hero numbers, source
  attributions, CTA, disclosure, Justoon image when present) lives
  ONLY inside the safe zone.
- Decorative elements (brand mark, `sl-hairline` rules, `sl-glow`
  radial, slide background fill) may extend to slide edges.
- No fixed-pixel widths on layout containers. No media queries based on
  aspect ratio. Layout is identical at every aspect; only the empty
  margin differs.

**Type scale (apply per slide via container-query units):**

```css
.slide {
  container-type: size;
  --type-hero:    clamp(80px, 24cqmin, 360px);
  --type-h1:      clamp(28px,  9cqmin, 144px);
  --type-h2-mid:  clamp(22px,  6.5cqmin, 96px);
  --type-body:    clamp(14px,  5cqmin,  72px);
  --type-kicker:  clamp(10px,  2.5cqmin, 36px);
  --safe-zone:    min(85cqw, 85cqh);
}
```

No element renders below `--type-kicker`. The hero/h1/h2-mid/body/kicker
roles are the only sizes used on the deck. Use `--type-h2-mid` (not
`--type-h1`) on body slides where Justoon is the anchor and the headline
is supporting (role C twist slides specifically).

**Text-wrap directive:** every `.headline` and `.caption` element uses
`text-wrap: balance` to distribute lines visually.

**Slide zone modifier class.** Each `.slide` element gets a zone modifier class derived from the narration's zone label: `slide-hook`, `slide-thesis`, `slide-receipt`, `slide-frame`, `slide-stakes`, `slide-twist`, `slide-historical-echo`, `slide-verbatim`, `slide-tease`, `slide-end`. The class enables the Justoon CSS rules below and supports any future zone-specific styling without changing the markup pattern. Example: `<div class="slide slide-twist">…</div>`.

**Justoon CSS rules** (apply when any slide includes a `.justoon` image):

```css
/* Role A — full-body pointing teacher (Receipt + Stakes slides) */
.slide-receipt .justoon, .slide-stakes .justoon {
  position: absolute;
  left: 0;
  bottom: calc(var(--type-kicker) + 1.5cqh);
  height: 88cqh;
  width: auto;
  max-width: 32%;
  object-fit: contain;
  object-position: left bottom;
}

/* Role C — bust reaction-as-anchor (Twist slides) */
.slide-twist .justoon {
  position: absolute;
  right: 0;
  bottom: calc(var(--type-kicker) + 1.5cqh);
  height: 75cqh;
  width: auto;
  max-width: 55%;
  object-fit: contain;
  object-position: right bottom;
}
```

DO NOT use CSS grid with `align-items: center` for Justoon placement;
grid's row auto-sizing with image children makes `height: 100%` resolve
to the image's natural pixel height (a 2048×2048 PNG renders at 2048px,
breaking the layout). Always use absolute positioning with explicit
`cqh` max-heights. (See the reference layout at
`docs/superpowers/reference-renders/2026-05-25-justoon-slideshow-layout.html`
for the proven implementation.)

**Thumbnail-anchor rule:** every slide has exactly one element at
`--type-hero` (or `--type-h1` for slides without a numeric anchor; or
the Justoon image itself for role C reaction-as-anchor slides). That
element must occupy ≥20% of the safe-zone height.

**Visible-text budget:** ≤25 visible words per slide across all on-
screen elements, OR one hero number + ≤15 supporting words. Speaker
notes and Justoon images are not counted against this budget. Where a
slide is marked as panel-a / panel-b below, render both panels and use
the `data-advance-at` attribute on panel-a to auto-advance to panel-b
at the specified mid-narration timestamp.

## Slide-by-slide specification

**Per-slide directive shape.** Each slide directive lists: kicker, anchor element, supporting content, visible-text budget, animation directive, AND — when Justoon is in play on this slide — a Justoon block of the form:

```
Justoon role: A | C
Justoon variant: <filename from ~/Pictures/tcn-justin-slideshow/>
Justoon placement: per the role's CSS rule (above)
```

Slides without Justoon omit the Justoon block entirely. When `--justoon-refs` is not provided, NO slide gets a Justoon block.

### Slide 1 — sl-title
Kicker: `DISPATCH №[NNN] · HOOK`
Headline (anchor, `--type-h1`): [from narration Slide 1]
Tag (sub-line, `--type-body`): [from narration cold-open candidate or steering]
Foot row (`--type-kicker`): `The Civic Node` / `[YYYY·MM·DD] · [N] MIN`
Visible-text budget: ~12 words. Headline ≤8 words.
Animation: sl-mark-pulse on the mark; sl-reveal cascade 1→2→3 on
  headline → tag → foot row. Hold for ~2s after the pulse settles.
Justoon: none.

### Slide 2 — sl-lead
Kicker: `DISPATCH №[NNN] · THESIS`
Heading (anchor, `--type-h2`): [from narration Slide 2, declarative]
Body (`--type-body`): [1-2 short sentences from narration Slide 2]
Visible-text budget: ~22 words total. If narration Slide 2 exceeds
  this, split into Slide 2-a / Slide 2-b with shared kicker.
Animation: sl-reveal cascade 1→2 on heading → body. sl-hairline draws
  left-to-right on entry, 360ms.

[... continues for each narration slide, following the §5 mapping
table. Every slide includes: kicker, anchor element at --type-h1 or
--type-hero, supporting content, visible-text budget, animation
directive. Slides marked panel-a / panel-b include data-advance-at
timestamps on panel-a. ...]

### Slide N — sl-end
Kicker: `DISPATCH №[NNN] · END`
Heading (anchor, `--type-h1`): `The Civic Node`
Body (`--type-body`): Substack URL CTA + disclosure block (verbatim
  from narration Outro / End slide)
Visible-text budget: ≤25 words.
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
- Renders correctly at 16:9 (1920×1080), 9:16 (1080×1920), and 1:1
  (1080×1080) from this same file. Test by resizing the browser window
  to each target aspect before recording — type sizes and safe-zone
  content stay identical; only the empty viewport margin changes.
- Every slide passes the thumbnail test: scale the browser window to
  240px wide and confirm the slide's anchor element is legible.
- Every slide passes the visible-text budget (≤25 visible words OR one
  hero number + ≤15 supporting words). Speaker notes excluded.
- Panel-split slides render both panels and auto-advance via
  `data-advance-at` on panel-a; speaker-notes JSON has ONE entry per
  narration slide, not per visual panel.
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

### 5b. Pick Justoon variants (only when `--justoon-refs` is provided)

Resolve `--justoon-refs` (invocation argument, or default `~/Pictures/tcn-justin-slideshow/`). If the path doesn't exist, log "no Justoon" mode and skip this step entirely.

For each slide whose template-type row in the mapping table specifies a Justoon role (A or C):

1. Apply the role's variant-pick rule from `references/template-mapping.md` §7 (interpretive — based on the slide's specific content, not a rigid table).
2. Verify the picked file exists in `--justoon-refs`. If missing, fall back to `justoon-neutral.png` and note the substitution in the artifact header.
3. Honor any per-slide override from user steering ("Slide 8: use raised-eyebrow instead of deadpan" / "Slide 4: no Justoon").

Slides whose role is `none` get no Justoon. Slides that would have been Justoon-active but where the user steered "no Justoon on this dispatch" get no Justoon.

If `justoon-neutral.png` itself is missing from the refs dir, halt and surface to the user: the anchor / fallback is required.

### 6. Generate per-slide directives

For each slide, compose: kicker text (per §6), headline, body, animation specifications (per §7), AND — when Justoon is in play on this slide — the Justoon block (role + variant filename) per the Output Format spec.

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
- **More than 18 narration slides** — halt with a warning. Trailer-format decks target 9-12 narration slides (small-screen pacing); >18 is a signal the upstream narration drifted from the format. Visual panel-splits do NOT count against this threshold — only narration-slide count does.
- **Panel-splitting fires on more than ~2 slides** — surface to user before writing the prompt. If half the deck needs splitting, the narration drifted long and the right fix is upstream re-pacing, not silent visual splitting.
- **Combined slide type encountered** (e.g., `FRAME + STAKES`) — pick the first sub-label's template type, adjust the layout (fewer numbered columns, more prose), note the combination in the prompt's slide-by-slide block. Justoon role also uses the first sub-label's role.
- **`--justoon-refs` path provided but directory missing** — halt with a setup note (where to place files, link to `~/Pictures/tcn-justin-slideshow/CLAUDE.md` convention).
- **`justoon-neutral.png` missing from the refs dir** — halt with the same setup note. The anchor / fallback is required; without it, missing-variant substitution can't fall back safely.
- **Mapped Justoon variant missing from the refs dir** — fall back silently to `justoon-neutral.png` and note the substitution in the artifact's header (e.g., `**Justoon substitution:** intended justoon-react-deadpan.png on Slide 8, used justoon-neutral.png (file not found).`).
- **No `--justoon-refs` flag and no config file** — produce today's typography-only output unchanged. Not a failure; the absence is the explicit opt-out.
- **User redirects** — re-invoke the affected step. Common redirects:
  - "use sl-compare instead of sl-frames on Slide 4" → re-generate that slide's directive with the override
  - "lower animation intensity" → re-write all animation directives at one level lower (sl-reveal-3 max, no chained pulses)
  - "swap a slide" → re-map the affected slide and regenerate
  - "merge the panel-split on slide N" → re-render slide N as a single panel; the visible-text budget is overridden for this slide only (user accepts thumbnail-readability tradeoff)
  - "split slide N for readability" → force a panel-split even if the slide is under budget (user wants slower visual pacing here)
  - "rebuild from scratch with steering X" → re-run the full process with steering applied
  - "swap Slide N Justoon to <variant>" → re-pick that slide's Justoon variant and regenerate the Justoon block in the prompt only
  - "drop Justoon from Slide N" → set Slide N's Justoon to none; regenerate that slide's directive without the Justoon block
  - "no Justoon on this dispatch" → re-run with Justoon mode forced off; produce typography-only output even though refs are present

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

- `references/template-mapping.md` — full narration-zone → slide-template mapping table with fallback rules, combined-type handling, kicker convention details, animation directive tables, AND (as of 2026-05-25) the §7 Justoon variant-pick guidance for role A and role C slides.
- **Justoon layout reference (in the Substack Research project repo, not in this skill dir):** `docs/superpowers/reference-renders/2026-05-25-justoon-slideshow-layout.html` — the proven CSS layout from the 2026-05-25 hand-test. Open this in a browser to see the target output the Claude Design prompt should produce. Both role A (pointing teacher) and role C (reaction-as-anchor) are demonstrated at 1:1, 16:9, 9:16, and 1:1 thumbnail (240×240) aspects.
- **Justoon library convention:** `~/Pictures/tcn-justin-slideshow/CLAUDE.md` — naming, format spec, inventory, regeneration workflow. The skill reads its `--justoon-refs` from here by default.
