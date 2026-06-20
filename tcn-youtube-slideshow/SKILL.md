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

Every beat from the narration is assigned one of four types before any slides are built. CSS skeletons and examples live in `references/beat-types.md`.

| Type | Source | Visual treatment |
|---|---|---|
| `scene-header` | Generated from scene label (not a beat) | TCN kicker, dark BG, kicker text only |
| `stamp` | Beat with short text/phrase as element | Text centered, Courier Prime, dark BG |
| `hero-number` | Beat with a single figure as element | Large number + optional label, dark BG |
| `refrain` | Beat marked `[REFRAIN]` | Full-screen phrase, **inverted colors** (white BG, black text) |

**Typing rule:** every beat is one of the four types above. All are pure HTML/CSS — no external images are needed for beat slides themselves.

**Abstract visual elements** (diagrams, charts, bars, arrows, maps, flows, icons) are rendered as HTML/CSS/SVG inline by Claude Design. If a beat's `element:` note describes a non-typographic visual that can be communicated through geometric shapes and CSS — a scale bar, a funnel, a simple map outline, a grid of ticks — Claude Design composes it directly. These are not sent for image generation.

**scene-header slides** are generated (not typed from beats). One scene-header per scene. Kicker format: `DISPATCH №NNN · SCENE NAME`. Full kicker convention in `references/template-mapping.md` §2.

**refrain treatment is non-negotiable.** The inverted colors (white background, black text) signal recurrence to the viewer. Every `[REFRAIN]` beat gets identical visual treatment — no variation between instances.

**Article-specific images** are separate from beat slides and handled in Pass 1. An image may display as a full-bleed backdrop behind a stretch of beats, or stand alone as a dedicated image slide. Images are scarce — 4-10 per dispatch — and placed by narrative logic, not beat-to-beat.

---

## Kicker Convention

Full kicker convention, rules, and examples: `references/template-mapping.md` §2.

---

## Two-Pass Workflow

### Pass 1 — Narrative image placement and prompt generation

Images are scarce and thematic — not beat-matched. The goal is 4-10 images per dispatch, each covering a meaningful stretch of narrative (typically 10-30 seconds, multiple beats). Images appear at visual context transitions: when the story enters a new physical setting, introduces a key subject or figure, or needs a pictorial anchor that an abstract HTML/CSS diagram cannot provide.

1. **Read the uploaded narration.** Parse scenes, beats, element notes, refrain markers. Read the full narration as a story — follow the narrative arc, not the beat list.

2. **Identify image moments.** Mark where a real pictorial image would ground the viewer. Triggers:
   - The story introduces a specific physical setting or subject (a factory, a figure, a place)
   - A character or subject recurs across scenes (the chip worker, the ratepayer)
   - A moment of visual contrast or juxtaposition that words and diagrams alone don't carry
   - The tease/outro where the viewer needs to feel the stakes

   For each image moment, determine:
   - Which scenes and beats it covers (the image may persist across many beat advances)
   - Whether it's a **backdrop** (image held behind typography beats; text overlays on top) or a **standalone slide** (image is the full visual for one beat or a pause)

   If no genuine image moments exist (rare), skip Pass 1 entirely and proceed to Pass 2.

3. **Output the image placement map:**

```
IMAGE PLACEMENT — Dispatch №NNN (N images)

[IMAGE 1] Scenes 01-02 · Backdrop · 1:1
Narrative: two workers at the Samsung plant, same shift, hundred yards apart
Covers: S01 B1-B4 (image persists; stamps and numbers overlay it)
Usage: backdrop — typography beats layer over this image

[IMAGE 2] Scene 03 · Standalone + Backdrop · 1:1
Narrative: the chokepoint — the memory chip at the center of the boom
Covers: S03 B1 (standalone), B2-B8 (backdrop behind receipt beats)
Usage: mixed

...
```

**Aspect ratio in the placement map:** mark each full-bleed image as `1:1` (1080×1080) — the deck records on a square canvas (`min(100vw, 100vh)`) and places full-bleed images with `object-fit: cover`, so a 16:9 source would be center-cropped to the square and lose ~43% of its width. The finished video reaches 16:9 by compositing this 1:1 deck beside the host's talking-head cam — that widening happens outside the deck, not in the source image. Use a non-square ratio only for an image that is not full-bleed (a small inline illustration, or a portrait-format figure). Pass this ratio to `ai-image-prompts` as part of the remix step — full guidance in `references/image-prompt-style.md`.

4. **Generate an image prompt for each moment using the `ai-image-prompts` skill.** For each image in the placement map, invoke `ai-image-prompts` in Content Illustration Mode:
   - Provide the narration text for the relevant beats as the content input
   - In the remix step, pass the TCN style brief from `references/image-prompt-style.md` as the style constraint — this keeps the output consistent with TCN's dark, editorial aesthetic
   - Work through all images before presenting any to the user

5. **Present the placement map and all generated prompts, then stop.**

> Image prompts complete — [N] images for Dispatch №NNN. Generate each image using your preferred image generation tool, naming files `NNN-01.png`, `NNN-02.png`, etc. (dispatch number + image sequence). Upload the results to this Claude Design project, then say "continue" to build the deck.

### Pass 2 — Full deck build

1. **Confirm image uploads.** Check that the uploaded filenames match the placement map (`NNN-01.png`, `NNN-02.png`, etc.). Note any missing images — those positions will render with a dark placeholder. Do not halt.

2. **Build scene-header slides.** One per scene, in order. Kicker text from the scene label. Format: `DISPATCH №NNN · [SCENE NAME IN CAPS]`.

3. **Build beat slides in order.** For each beat:
   - Apply the beat's type template (CSS skeletons in `references/beat-types.md`)
   - For refrain beats: apply the inverted-color treatment
   - For stamp/hero-number beats: apply the typography template
   - For beats with abstract visual elements (diagrams, charts, bars, icons): render as HTML/CSS/SVG inline — no image file needed
   - For **backdrop beats** (beats covered by an image from the placement map): display the image as a full-bleed background `<img>`, add the beat's typographic element as an absolutely-positioned HTML overlay

4. **Insert standalone image slides** at the positions in the placement map marked as standalone. Each is a full-bleed `<div class="slide image-moment">` with the uploaded file referenced by filename.

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

## HTML Structure

### Canvas and aspect ratio

**Primary recording canvas: 1:1 (1080×1080).** The deck element is sized to `min(100vw, 100vh)` — a square that fills the smaller viewport dimension. Recording at 1:1 by setting the browser window to 1080×1080 produces the primary output. 16:9 and 9:16 derivatives work by resizing the browser window — slide content does not reflow.

### Type scale

All font sizes use `cqmin` (container-query minimum unit) so a 1080-tall slide and a 1080-wide slide produce identical rendering:

```css
--type-hero:   clamp(80px, 24cqmin, 360px);  /* single dominant number */
--type-h1:     clamp(28px,  9cqmin, 144px);  /* scene-header headline */
--type-h2-mid: clamp(22px,  6.5cqmin, 96px); /* longer stamp phrases */
--type-body:   clamp(14px,  5cqmin,  72px);  /* labels, overlays */
--type-kicker: clamp(10px,  2.5cqmin, 36px); /* scene-header kicker */
```

### Transitions

Simple CSS opacity cross-dissolve between slides:

```css
.slide {
  transition: opacity 200ms cubic-bezier(0.2, 0, 0, 1);
}
```

No bounce, no spring, no slide-in. The content change IS the motion — the transition is incidental.

### Advancement

Manual keypress or click. Right arrow / Space / Down arrow = advance. Left arrow / Up arrow = retreat. Click = advance. No auto-advance, no timed transitions.

### No animation primitives

This deck does not use `sl-reveal`, `sl-mark-pulse`, `sl-caret`, `sl-chart-draw`, `sl-glow`, or `sl-hairline`. These primitives were part of the old format's within-slide build-up mechanism. In the beat format, the visual change happens between slides, not within them.

---

## Output Format

The output is `dispatch-NNN.html` — a single self-contained HTML file produced directly in Claude Design. The full HTML structure, including CSS for all beat types and the JS advance logic, is shown in the Two-Pass Workflow section (Pass 2, step 4).

---

## The Process

### 1. Parse the narration

Read the uploaded `youtube-narration.md`. Extract:
- Dispatch number (from title block `## The Civic Node · Dispatch №NNN`)
- Scene markers and beat count per scene. **Scene markers appear as `[SCENE NN — TITLE]`.** Older decks (dispatches 002-006) labeled them `[SLIDE NN — TITLE]` — treat that as a scene marker too; it never meant a rendered slide. Either way, this skill renders **one slide per beat** plus one scene-header per scene, and assigns its own slide IDs (`sNN-header`, `sNN-bMM`); it does not reuse the narration's scene numbers as slide numbers.
- Each beat's element note and spoken text
- Refrain markers (`[REFRAIN]`)
- Script Notes footer (cold-open candidate, refrain candidate / motifs, etc.)

Halt if the file is missing or the beat markup convention (`▸ **B1** · *element:*`) is not present.

### 2. Type every beat

Apply the typing rule from Beat Type Taxonomy. Produce a brief inventory:

```
Beat inventory — Dispatch №006 (102 beats across 10 scenes):
  scene-header: 10 (generated)
  stamp: 40
  hero-number: 14
  refrain: 2
  [abstract visual / HTML+CSS]: 36
  Total beat slides: 112
```

### 3. Pass 1 — narrative image placement and prompts

Read the full narration as a story. Identify 4-10 image moments (see Two-Pass Workflow §Pass 1 for the full placement logic). Invoke `ai-image-prompts` in Content Illustration Mode for each moment. Present the placement map and all generated prompts. Stop and wait for image uploads.

### 4. Pass 2 — deck build

After user confirms image uploads: build all slides in scene order. Scene-header first, then beats B1 through BN for each scene. Write `dispatch-NNN.html`. Present Pass 2 gate prompt. Stop.

---

## Failure Modes

- **Narration file missing or not uploaded** — halt, tell the user to upload `youtube-narration.md` to this Claude Design project.
- **Beat markup not found** (no `▸ **B1** · *element:*` pattern) — halt. The file may be a legacy static-slide format narration. Tell the user to run `tcn-youtube-narration` to produce a beat-segmented script first.
- **Dispatch number missing from title block** — halt and ask the user to confirm.
- **Illustration images missing in Pass 2** — render those slides with a dark placeholder box containing the filename and element note as debug text. Note missing images in the deck header comment. Do not halt.
- **More than 150 beats** — surface a warning before Pass 1: "This deck has [N] beats — more than typical (80-120). Confirm to continue, or return to the narration and reduce scope."
- **User redirects** — re-invoke the relevant step:
  - "swap slide X to a different treatment" → re-type that beat and rebuild that slide only
  - "refrain treatment should use a border not inverted colors" → re-render all refrain slides with the new treatment
  - "replace image for scene X beat Y" → user re-uploads the image; rebuild that slide only
  - "no scene-header slides" → rebuild without scene-header slides (reduces deck by ~10 slides)

---

## Justoon — Deferred

The previous slideshow skill mapped Justoon (a TCN character illustration) to specific slide types — role A (pointing teacher) on Receipt/Stakes slides, role C (reaction-as-anchor) on Twist slides. In the beat format, those slide types no longer exist as distinct slots.

Justoon could appear in the new format as an illustration-type beat: the `element:` note would reference a Justoon image ("Justoon appears pointing at the chokepoint diagram") and the fal.ai image would be replaced by a Justoon PNG from `~/Pictures/tcn-justin-slideshow/`. This integration is **not implemented in this version**.

To reintroduce Justoon: define a `justoon` beat type or subtype, add it to the typing decision tree in `references/beat-types.md`, and define the Pass 1 behavior (no image prompt needed — use the local PNG directly in Pass 2).

---

## What This Skill Is NOT

- This skill does **not** produce a prompt file for a human to paste into Claude Design. It runs directly in Claude Design and builds the deck.
- This skill does **not** generate narration. That's `tcn-youtube-narration` (Step 1).
- This skill does **not** generate the fal.ai images. It produces the prompts in Pass 1; the user generates images externally and uploads them.
- This skill does **not** extend the TCN design system CSS. The deck's CSS is self-contained in the HTML file.
- This skill does **not** produce thumbnails, social graphics, YouTube titles, descriptions, or chapter timestamps. Those are separate skills that run after recording.
- This skill does **not** fact-check the article. That happened upstream.

---

## Companion Skills

**Upstream (this skill reads from):**
- `tcn-youtube-narration` — the finished beat-segmented narration is the required input.

**Downstream (these skills read the recorded transcript, not this skill's output):**
- `tcn-youtube-title` — title generation.
- `tcn-youtube-description` — description body, tags, chapter timestamps.
- `tcn-youtube-thumbnail` — thumbnail image prompt + text overlay.

---

## Reference Files

- `references/beat-types.md` — visual spec and CSS skeletons for all 5 beat types
- `references/image-prompt-style.md` — fal.ai style anchor for TCN aesthetic, worked examples, filename convention
- `references/template-mapping.md` — kicker convention for scene-header slides (§2); old sl-* mapping archived in same file
