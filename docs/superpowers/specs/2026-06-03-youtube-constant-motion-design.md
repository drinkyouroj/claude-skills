# YouTube Constant-Motion Format Design
**Date:** 2026-06-03
**Skills affected:** `tcn-youtube-narration`, `tcn-youtube-slideshow`
**Status:** Approved — ready for implementation

---

## Problem

The current YouTube production workflow targets 9-12 static slides with animation primitives (`sl-reveal`, `sl-chart-draw`, etc.) building up content within each slide. Two problems with this:

1. **Not enough motion.** A viewer sees the same thing on screen for 30-40 seconds per slide. The target is 1-3 seconds of static screen between visual changes — near-constant motion.
2. **Claude Design's multi-step animation UI doesn't work well.** Building up slide content through animation states is hard to preview, hard to edit, and produces inconsistent results. Discrete slides are easier to create and verify.

Dispatch-006 (`samsung's-400000-bonus-and-the-4000-one`) already proved out the target format manually: 10 scenes, 102 beats, ~3.8s average visual change rate. The design work here is formalizing that format into both skills.

---

## Architecture

### Execution split

| Skill | Runs in | Reads from | Produces |
|---|---|---|---|
| `tcn-youtube-narration` | Claude Code (local machine) | Local project files | `youtube-narration.md` |
| `tcn-youtube-slideshow` | Claude Design | Uploaded `youtube-narration.md` | HTML deck file |

The narration file is the handoff artifact. It contains all scenes, beats, element notes, and refrain markers. No other local file access is needed in Claude Design.

### New deck architecture

**Old format:** ~10 slides, animation primitives build content within each slide, `deck-stage.js` controls timing.

**New format:** ~100-110 discrete static slides (one per beat, plus one scene-header slide per scene), no within-slide animation states, manual keypress advances each slide, simple CSS cross-dissolve between slides. No dependency on `deck-stage.js` or the existing animation primitive system.

---

## `tcn-youtube-narration` changes

### What stays the same

- Three-zone structure (Cold Open / Body / Outro)
- Scene types: Hook, Thesis, Receipt, Frame, Stakes, Twist, Historical Echo, Verbatim, Tease, End
- Voice calibration (dial 6-7, Hank-Vox blend) and all spoken-word adaptations
- Voice canonical source (`workspace/core/anti-ai-writing-style.md`)
- Script Notes footer structure (most fields)
- Dispatch number detection
- Gate prompt

### What changes

**1. Output format — beats replace paragraphs**

The locked beat convention (as demonstrated in dispatch-006):

```
▸ **B5** · *element: "$400,000" lands over the left figure*
"This year, his bonus runs toward four hundred thousand dollars." **[stop — let the number sit]**
```

Each beat has exactly three parts:
- Beat number (`B1`, `B2`, etc.)
- `element:` note — one visual element only
- One spoken unit ending in `[stop]`, with optional timing annotation

**2. Targets**

Old: "9-12 slides total."
New: "8-12 scenes, 80-120 beats." Target approximately 8-12 beats per scene, ~3-4 seconds of screen time each.

**3. Per-beat rule replaces visible-text budget**

Old: ≤25 visible words per slide (designed to prevent panel-splits downstream).
New: one visual element per beat. The `element:` note describes it. If the note describes two things happening, it is two beats.

**4. Slide-splitting rule — removed**

Beats are the splits. No panel-split mechanism needed.

**5. Script Notes footer**

Add:
```
**Beat count:** [N] across [M] scenes
```

Remove: `**Visual density flags:**` — this was a workaround for the old split mechanism, no longer needed.

**6. Title block format tag**

Updated to match dispatch-006:
```
## [N] scenes · [N] beats · beat-segmented motion format · trailer · small-screen · 5-7 min target
```

**7. Failure modes**

- ">12 slides" → ">12 scenes"
- Add: ">120 beats total" surfaces a warning (narration is probably running long or scenes are too granular)

---

## `tcn-youtube-slideshow` changes

### Execution environment & skill format

The skill is rewritten as direct Claude Design execution instructions, not a prompt-builder. The user's workflow:

1. Open a new Claude Design project
2. Upload `youtube-narration.md`
3. Upload `SKILL.md` (or paste its contents as context)
4. Say "run this skill" — Claude Design follows the instructions directly

No intermediate `youtube-slideshow.md` prompt file. The HTML deck is the output.

### Beat type taxonomy

Every beat gets assigned one of five types before any slides are built:

| Type | Visual treatment | Needs image? |
|---|---|---|
| `scene-header` | Full TCN kicker + headline, dark BG | No |
| `stamp` | Short text/phrase, large, centered, Courier Prime | No |
| `hero-number` | Single large figure + optional unit/label | No |
| `refrain` | Full-screen recurring phrase, distinct visual treatment | No |
| `illustration` | AI-generated image base, optional text/number overlay in HTML | Yes |

**scene-header:** Generated from the scene label, not a narration beat. Appears at the start of each scene. Uses full TCN kicker format: `DISPATCH №NNN · HOOK`, `DISPATCH №NNN · THE RECEIPT · THE CHOKEPOINT`, etc. ~10 per deck. These are the only slides using the legacy TCN kicker + headline treatment.

**stamp:** All text-dominant beats where the visual is words on a dark background — "SAME SHIFT", "GRANTED", "NOT YET.", "STOP THE LINE", "A UNION", etc.

**hero-number:** Single-figure beats — "$400,000", "+755%", "$13.77 BILLION", "10.5%". One large number (`--type-hero` scale) plus optional label at `--type-body`.

**refrain:** Beats marked `[REFRAIN]` in the narration. Distinct visual treatment to signal recurrence — e.g. inverted colors (white background, black text), or a specific mark/border treatment. Must look the same every time the refrain appears so viewers recognize it.

**illustration:** Any beat whose `element:` note describes a visual that cannot be produced with typography alone — figures, maps, diagrams, abstract icons, animated metaphors. Text overlays on illustrations (e.g. "$400,000 lands over the left figure") are also illustration type: the fal.ai image provides the base visual, Claude Design adds the text layer as HTML/CSS on top.

**Typing rule:** if the `element:` note describes anything other than words, numbers, or phrases on a plain dark background, it is illustration type.

### Two-pass workflow

**Pass 1 — Image generation batch**

1. Read the uploaded narration file
2. Identify all illustration beats
3. Output a numbered batch of fal.ai image prompts in this format:

```
IMAGE BATCH — Dispatch №006 (38 images)

[001] Scene 01 · B1
Style: flat vector, dark palette (#0f172a background), muted slate tones,
clean lines, no gradients, no photography
Content: [description derived from element note]
Filename: 006-01-B1.png

[002] Scene 01 · B3
...
```

Each prompt includes: style anchor (flat vector, TCN dark palette `#0f172a`, muted slate tones, no gradients, no photography), content description derived from the element note, and a filename keyed to scene + beat number.

4. Full stop. Present instruction to user: "Generate these images using fal.ai. Upload the results to this Claude Design project. Then say 'continue' to build the deck."

**Pass 2 — Full deck build**

After images are uploaded:
1. Build scene-header slides from scene labels (~10 slides)
2. For each beat in sequence, apply its type's template
3. Illustration beats reference uploaded images by filename
4. Produce complete HTML deck

Total slides: ~100 beat slides + ~10 scene-header slides = ~110 slides per typical deck.

### HTML structure

- Each `.slide` div is a static frame — no animation states within a slide
- Simple CSS cross-dissolve between slides: 200ms, `cubic-bezier(0.2, 0, 0, 1)`
- Manual keypress or click advances each slide
- No dependency on `deck-stage.js`
- TCN brand constraints preserved: Courier Prime, slate palette (`#0f172a` dark BG, slate-400/slate-600 text), no emoji, no shadows on dark, no gradients
- Type scale: same `cqmin`-based scale as the existing design system (`--type-hero`, `--type-h1`, `--type-h2-mid`, `--type-body`, `--type-kicker`)
- Safe zone: same `min(85cqw, 85cqh)` square constraint — ensures multi-aspect compatibility

### Justoon — deferred

The current slideshow skill maps Justoon role A (pointing teacher) to Receipt/Stakes slides and role C (reaction-as-anchor) to Twist slides. Those slide types no longer exist as distinct slots in the beat format. Justoon could appear as an illustration-type beat ("Justoon appears pointing at the chokepoint diagram"), but defining that integration cleanly is out of scope for this change. The new skill marks Justoon as deferred with a placeholder for future reintroduction.

---

## Repo changes

### Files modified

- `tcn-youtube-narration/SKILL.md` — targeted edits per the narration changes section above
- `tcn-youtube-slideshow/SKILL.md` — near-complete rewrite per the slideshow changes section above

### Files updated

- `tcn-youtube-slideshow/references/template-mapping.md` — kicker convention section preserved (scene-header slides still use the `DISPATCH №NNN · SCENE NAME` format); sl-* type mapping and animation directive tables archived with a note pointing to this spec

### New files

- `tcn-youtube-slideshow/references/beat-types.md` — visual spec for each of the 5 beat types: layout rules, type scale, CSS skeleton, worked example from dispatch-006
- `tcn-youtube-slideshow/references/image-prompt-style.md` — fal.ai image style anchor for TCN aesthetic: color values, style descriptors, what to include, what to avoid

---

## What this is not changing

- Voice calibration, register, spoken-word adaptations — unchanged
- The three-zone scene structure (Cold Open / Body / Outro) — unchanged
- The scene type menu (Receipt, Frame, Stakes, Twist, etc.) — unchanged, just renamed from "slide types" to "scene types"
- The Script Notes footer fields (word count, runtime, refrain markers, cold-open candidate, cuts-from-article) — mostly unchanged
- The multi-aspect layout requirement (16:9 / 9:16 / 1:1 from one HTML source) — preserved via the safe-zone constraint
- Downstream skills (`tcn-youtube-title`, `tcn-youtube-description`, `tcn-youtube-thumbnail`) — unaffected; they consume the recorded transcript, not the narration file
