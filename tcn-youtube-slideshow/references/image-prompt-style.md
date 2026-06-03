# TCN Style Brief — for `ai-image-prompts` remix

*Pass this as the style constraint when invoking `ai-image-prompts` in Content Illustration Mode during Pass 1. After `ai-image-prompts` selects a template prompt from its library, include this brief in the remix step (Step 5) so the customized output matches TCN's visual aesthetic.*

---

## Style brief (include in the ai-image-prompts remix step)

```
TCN visual style: dark editorial aesthetic, dark background (#0f172a near-black),
muted slate color palette for supporting elements (#334155 mid-slate, #475569 slate,
#64748b light-slate, #e2e8f0 near-white for highlights and focal elements), flat
design sensibility, clean geometric composition, editorial illustration register.

No photography, no realistic textures, no lens flare, no bright saturated colors
outside the slate palette. No readable text in the image — text is added as HTML
overlays in the deck. No faces or recognizable real people — silhouettes and geometric
figure abstraction only. No brand logos or company marks.

**Aspect ratio: 16:9 (1920×1080) by default.** This is the standard for full-bleed
slides — backdrop and standalone image moments. Generate at 16:9 unless the image is
not fullscreen (e.g. a small inline illustration within a slide, or a portrait-format
figure). Leave compositional breathing room — backdrop images will have typography
overlaid on top of them.
```

---

## What to provide as content input to ai-image-prompts

For each image moment, pass:
1. **The narration text** for the relevant beats — this is the "content" for Content Illustration Mode
2. **A one-sentence narrative summary** of what the image needs to communicate
3. **Usage note** — whether this is a backdrop (text will overlay) or standalone (image fills the full slide)

Example input for dispatch-006 Image 1:
```
Content: "Two workers walk out of the same Samsung plant in Korea. Same shift. They
worked it a hundred yards apart. One of them builds memory chips. His bonus runs toward
four hundred thousand dollars. The other builds phones and televisions. His bonus comes
to about four thousand. Same company. Same shift. A hundred to one."

Narrative: Two figures representing the same-company pay gap — the core visual hook of the video.

Usage: Backdrop — stamps and numbers will overlay this image across several beats.
```

---

## Image placement filename convention

Article-specific images are named `NNN-NN.png`:
- NNN = dispatch number, zero-padded 3 digits (e.g. `006`)
- NN = image sequence number within the dispatch, zero-padded 2 digits (e.g. `01`, `02`)

Example: `006-01.png` = dispatch 006, first image. `006-05.png` = dispatch 006, fifth image.

The placement map in Pass 1 lists which image number covers which beats/scenes.

---

## Targeting the right ai-image-prompts category

The `infographic-edu-visual` category is the closest match for TCN's editorial visual style. Try it first. If no strong match, try `others` (for more unusual editorial compositions) or `comic-storyboard` (for figurative/narrative scenes with people or figures).

Avoid `product-marketing`, `social-media-post`, and `profile-avatar` — these skew commercial and bright, away from TCN's tone.
