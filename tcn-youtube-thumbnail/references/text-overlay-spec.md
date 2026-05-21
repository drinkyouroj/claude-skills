# Text Overlay Specification

The text overlay is composited onto the rendered thumbnail image in Figma/Canva/Photoshop *after* the image is generated. The skill produces this spec; the human (or future automation) executes it. The skill itself does NOT render text into the image.

## Canvas

- Source canvas: 1280 × 720 px (16:9). Match Figma/Canva frame size to this.
- Final YouTube display: variable, but the thumbnail is cropped aggressively for the mobile feed. Treat the center 80% (1024 × 576 px window, centered) as the safe zone. Anything outside that may get cropped.

## Mobile safe-zone rule

All text must stay inside the center 80%:
- Left edge of text: ≥ 128 px from canvas left.
- Right edge of text: ≤ 1152 px from canvas left.
- Top edge: ≥ 72 px from canvas top.
- Bottom edge: ≤ 648 px from canvas top.

The corner identity block exception: the dispatch number + mark may sit at ~96 px inset rather than 128 px to feel anchored to the corner. This is the only exception.

## Typeface

- Courier Prime only. Two weights used:
  - **Courier Prime Bold** — the headline.
  - **Courier Prime Regular** — the dispatch serial and any sub-line.
- Sourced from the TCN design system: `~/Documents/The Civic Node — Design System.zip` → fonts.

## Headline

- **Content:** the chosen candidate from Gate 2 (3–6 words).
- **Weight:** Courier Prime Bold.
- **Case:** sentence case. (Voice rule — no screaming.)
- **Size:** ~120 px at 1280 × 720. Scales to ~9.4% of canvas height.
- **Tracking:** -0.025em (tight, matches TCN display sizes).
- **Leading:** 1.05× size (~126 px) when the headline wraps to 2 lines.
- **Color:** slate-400 (`#557FA3`) or black (`#0D0D0F`). See "Color picking" below.
- **Optional stroke/halo:** 4–6 px stroke at 60% opacity in the opposite color (slate-400 stroke if black fill; black stroke if slate-400 fill). Use only when the underlying illustration is busy enough that flat text would lose legibility.
- **Position:** default center-left, baseline at ~55% of canvas height (~396 px from top). Left edge anchored to the safe-zone left edge (128 px in).
- **Max width:** 768 px (60% of canvas). Wrap to 2 lines if needed; never 3.

## Corner identity block

Two elements stacked:

- **Mark:** `mark.svg` from the design-system bundle.
  - Size: 40 × 40 px.
  - Color: slate-400 on dark scenes, slate-600 (`#3A6A8F`) on light scenes.
- **Dispatch serial:** `DISPATCH №NNN` (zero-padded).
  - Typeface: Courier Prime Regular.
  - Case: all-caps.
  - Tracking: 0.18em (wide, matches TCN kicker convention).
  - Size: 24 px.
  - Color: same as mark.

Stack: mark on top, dispatch serial below, 8 px gap between them.

Default position: top-right corner, both elements right-aligned. Right edge at 1184 px (96 px inset from canvas right). Top edge of mark at 72 px.

Alternative position: bottom-left, with mark above dispatch serial. Use this when the headline occupies the right half of the canvas.

## Color picking

The skill recommends a color pair (overlay-text color + optional stroke) in the artifact based on the chosen vibe's stated lighting:

- Vibe says "dark", "moody", "noir", "dramatic night", etc. → recommend slate-400 fill, no stroke.
- Vibe says "bright", "daytime", "editorial", "documentary daylight" → recommend black fill, no stroke.
- Vibe is ambiguous or mixed-lighting → recommend slate-400 fill with 4-px black stroke (works on most backgrounds).

The user can always override at composite time when looking at the actual rendered image.

## Palette restrictions

These four colors are the ONLY ones allowed on overlay text (headline, sub-line, dispatch serial, mark):

- slate-400 — `#557FA3`
- slate-600 — `#3A6A8F`
- black — `#0D0D0F`
- twilight — `#485070`

The illustrated scene (the image beneath the overlay) is NOT restricted to this palette. It can use any colors that serve CTR. The palette restriction is overlay-only — that's how the brand carries even when the scene goes loud.

## Sub-line / kicker (optional)

If the dispatch concept benefits from a context line beneath the headline (e.g., a zone or topic):

- Typeface: Courier Prime Regular.
- Case: all-caps.
- Tracking: 0.18em.
- Size: 18 px.
- Color: twilight (`#485070`).
- Position: directly below the headline, baseline at headline-baseline + 32 px.
- Length: 2–6 words max.

If the dispatch concept does NOT clearly benefit, omit. The skill should not force a sub-line.

## Spec block format (what the skill writes into youtube-thumbnail.md)

The skill writes this block into the artifact file's "Text overlay spec" section. Engineers reading this file should produce output in this shape:

```
## Text overlay spec

**Canvas:** 1280 × 720 (16:9). Center-80% safe zone.

**Headline:**
- Text: "<chosen headline>"
- Font: Courier Prime Bold, sentence case
- Size: 120 px
- Color: slate-400 #557FA3 (recommended for this vibe; black #0D0D0F also valid)
- Stroke: none recommended (4 px black if image is busier than expected)
- Position: center-left, baseline at 55% canvas height, left edge at 128 px

**Corner identity block (top-right):**
- Mark.svg: 40×40 px, slate-400
- Dispatch serial: "DISPATCH №NNN", Courier Prime Regular, 24 px, all-caps, tracking 0.18em, slate-400
- Both right-aligned at right edge 1184 px, mark top at 72 px

**Palette:** slate-400 #557FA3, slate-600 #3A6A8F, black #0D0D0F, twilight #485070. No other colors on overlay text.
```

## How the skill uses this file

At process step 9 (compose the text overlay spec), the skill:

1. Loads this file's contents.
2. Pulls the chosen headline and dispatch number.
3. Picks recommended color/stroke per the "Color picking" rules using the chosen vibe's lighting cues.
4. Writes the "Text overlay spec" block into `youtube-thumbnail.md` in the format above, substituting the chosen headline and dispatch number.
