# Image Prompt Style — tcn-youtube-slideshow

*The TCN aesthetic anchor for fal.ai image generation. Use this when writing Pass 1 image prompts in the two-pass workflow. Include the style anchor verbatim in every prompt.*

---

## Style anchor (include verbatim in every prompt)

```
Style: flat vector illustration, dark background (#0f172a), muted slate color palette
(#334155 mid-slate, #475569 slate, #64748b light-slate, #e2e8f0 near-white for
highlights), clean geometric lines, no gradients, no photography, no realistic
textures, no shadows, no lens flare, minimal detail, geometric simplification,
editorial illustration aesthetic
```

---

## What to specify in the Content field

The content description translates the narration's `element:` note into a visual brief. Rules:

1. **Describe the composition, not the meaning.** "Two human figure silhouettes facing right, side by side" — not "two workers representing labor inequality."
2. **Name colors from the palette.** "Left figure in near-white (#e2e8f0), right figure in mid-slate (#334155)" rather than "one bright, one dark."
3. **Specify negative space.** If part of the frame should be empty (for a text overlay that Claude Design will add), say so: "lower third empty for text overlay."
4. **Avoid text in images.** Any text (stamps, numbers, labels) will be added as HTML/CSS overlays — do not include readable text in the fal.ai image.
5. **Use geometric abstractions for concepts.** A "chokepoint" → a funnel shape. A "union" → overlapping circles or a cluster. A "power grid" → grid lines radiating from a central node. Flat vector, not literal.

---

## Reference dispatch-006 examples

**006-01-B01** (two figure silhouettes):
```
Style: [style anchor above]
Content: Two simplified human figure silhouettes, flat geometric, side by side facing
right. Left figure near-white (#e2e8f0), right figure mid-slate (#334155). Faint
rectangular outline behind them suggesting an industrial building. Figures centered,
lower two-thirds of frame. Upper third empty. No text. No detail beyond basic body shape.
```

**006-03-B08** (globe with ripple):
```
Style: [style anchor above]
Content: Simplified flat globe outline, dark slate (#334155) lines on dark background
(#0f172a). Concentric ripple rings emanating from a point in the northern hemisphere,
near-white (#e2e8f0) rings fading outward. Centered in frame. Clean, minimal, no
continents labeled, no text.
```

**006-05-B07** (US map with single dot):
```
Style: [style anchor above]
Content: Flat outline of the contiguous United States, mid-slate (#475569) fill,
slightly lighter slate border (#64748b). Single small bright dot (#e2e8f0) in
western Pennsylvania. No state borders, no labels, no text. Map centered in frame,
generous margin on all sides.
```

---

## Filename convention

`NNN-SS-BNN.png`
- NNN = dispatch number, zero-padded 3 digits (e.g. `006`)
- SS = scene number, zero-padded 2 digits (e.g. `01`)
- BNN = B + beat number within scene, zero-padded 2 digits (e.g. `B01`)

Example: `006-01-B01.png` = dispatch 006, scene 01, beat 1.

---

## What to avoid

- No photography, no realistic rendering, no 3D effects
- No text inside the image (text overlays are HTML/CSS)
- No gradients, no lens flare, no shadows
- No bright saturated colors outside the slate palette
- No faces or recognizable people — silhouettes and geometric figures only
- No brand logos or real company marks
