# YouTube Constant-Motion Format Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `tcn-youtube-narration` and `tcn-youtube-slideshow` to produce a ~100-slide constant-motion deck format (one static slide per beat, ~2-3 seconds on screen each) replacing the old 10-slide animated format.

**Architecture:** The narration skill (runs in Claude Code) formalizes the beat-segmented format already proven in dispatch-006 — 8-12 scenes with 80-120 individual beat markers. The slideshow skill is rewritten to run directly in Claude Design, accepting an uploaded narration file and producing the HTML deck in a two-pass workflow: first a fal.ai image-generation batch for illustration beats, then the full ~110-slide deck build after images are uploaded.

**Tech Stack:** Markdown skill files, HTML/CSS for the deck output, fal.ai for AI image generation.

**Design spec:** `docs/superpowers/specs/2026-06-03-youtube-constant-motion-design.md`

---

## File Map

| Action | File | Responsibility |
|---|---|---|
| Modify | `tcn-youtube-narration/SKILL.md` | Targeted edits — beat format as standard, remove old slide budget/splitting |
| Modify | `tcn-youtube-slideshow/SKILL.md` | Near-complete rewrite — Claude Design execution, beat taxonomy, two-pass workflow |
| Modify | `tcn-youtube-slideshow/references/template-mapping.md` | Archive sl-* sections, preserve kicker convention |
| Create | `tcn-youtube-slideshow/references/beat-types.md` | Visual spec for all 5 beat types |
| Create | `tcn-youtube-slideshow/references/image-prompt-style.md` | fal.ai style anchor for TCN aesthetic |

---

## Task 1: Narration skill — pacing target, frontmatter, beat markup convention

**Files:**
- Modify: `tcn-youtube-narration/SKILL.md:3` (frontmatter description)
- Modify: `tcn-youtube-narration/SKILL.md:10-12` (what-it-does + pacing target)
- Modify: `tcn-youtube-narration/SKILL.md:83` (output artifact contents)
- Modify: `tcn-youtube-narration/SKILL.md:96` (narration structure opening)
- Modify: `tcn-youtube-narration/SKILL.md:205-227` (output format: title block + slide markup)

- [ ] **Step 1: Update frontmatter description**

In `tcn-youtube-narration/SKILL.md` line 3, change:

```
description: Step 1 of the Civic Node YouTube production workflow — converts an approved article draft into a 5-7 minute trailer-format narration script with slide markers, pacing notes, and refrain markers.
```

to:

```
description: Step 1 of the Civic Node YouTube production workflow — converts an approved article draft into a 5-7 minute trailer-format narration script with beat markers, pacing notes, and refrain markers. Produces a beat-segmented script (8-12 scenes, 80-120 beats) where each beat is one spoken unit paired with one visual element. Calibrated to a "Hank Green meets Vox" register and written to drive Substack click-through, not to summarize the article. Invoke this skill when the user says "write the narration", "narration script", "video script from this article", "narrate this for YouTube", "do the script for Friday's video", or when the user points at a finished article draft and asks for a video script. Does NOT apply to social posts (that's tcn-post), full articles (tcn-draft), or YouTube packaging — title, description, and thumbnail come from separate skills.
```

- [ ] **Step 2: Update what-it-does opening paragraph (line 10)**

Change:

```
Converts a finished Civic Node article draft into a 5-7 minute trailer-format YouTube narration script (700-1,050 words at ~140 wpm) with standardized slide markers and a Script Notes footer.
```

to:

```
Converts a finished Civic Node article draft into a 5-7 minute trailer-format YouTube narration script (700-1,050 words at ~140 wpm) with beat markers and a Script Notes footer.
```

- [ ] **Step 3: Update pacing target paragraph (line 12)**

Change:

```
**Slide pacing target: 9-12 slides total**, calibrated for small-screen / phone-thumbnail consumption of the downstream slideshow (see `tcn-youtube-slideshow`). Same 5-7 min runtime as before; the slide budget is finer-grained so each slide carries less on-screen content and the visual cadence matches mobile viewing. Going under 9 slides usually means the piece is too compressed for video; going over 12 means the upstream article needs a tighter cold-open angle.
```

to:

```
**Beat pacing target: 8-12 scenes, 80-120 beats total**, calibrated for the downstream constant-motion slideshow (see `tcn-youtube-slideshow`). Same 5-7 min runtime; each beat carries one visual element, producing a visual change every ~3-4 seconds on average (~3.8s in the dispatch-006 reference). Going under 8 scenes usually means the piece is too compressed for video; going over 12 scenes usually means the cold-open angle isn't narrow enough — too many distinct sub-arguments competing for screen time. Going over 120 beats usually means individual scenes are over-granular; scenes typically run 8-12 beats.
```

- [ ] **Step 4: Update output artifact contents (line 83)**

Change:

```
- **Contents:** Title block (article title + dispatch number + slide count + format tag), 9-12 slide blocks in standardized markup (each within the ≤25-visible-words/slide budget), Script Notes footer.
```

to:

```
- **Contents:** Title block (article title + dispatch number + scene/beat count + format tag), 8-12 scene blocks in beat-segmented markup, Script Notes footer.
```

- [ ] **Step 5: Update narration structure opening (line 96)**

Change:

```
Three zones, **9-12 slides total**, 700-1,050 words at ~140 wpm. Each slide carries **≤25 visible-text words** that would render on screen (see "Visible-text budget" below) — the spoken narration is longer than what appears on the slide, but the on-screen text per slide stays inside the small-screen budget so the downstream `tcn-youtube-slideshow` doesn't have to split slides visually.
```

to:

```
Three zones, **8-12 scenes, 80-120 beats total**, 700-1,050 words at ~140 wpm. Each beat carries **one visual element** — the spoken narration can be longer, but the on-screen element is always exactly one thing. The downstream `tcn-youtube-slideshow` maps each beat to one static slide.
```

- [ ] **Step 6: Update title block example (lines 205-213)**

Change the Title block subsection under Output Format:

```markdown
### Title block

```markdown
# [Article Title in Spoken-Word Friendly Form]
## The Civic Node · Dispatch №[NNN]
## [N] slides · trailer-format · small-screen · 5-7 min target
```

The dispatch number is detected from existing dispatches in the workspace (see step 9 of the process), or captured from the user. The format tag (`trailer-format · small-screen`) distinguishes the current format (9-12 slides, ≤25-visible-words/slide budget, multi-aspect deck downstream) from the legacy `Part One / Part Two` format and from the older 7-9-slide pre-small-screen-pacing scripts.
```

to:

```markdown
### Title block

```markdown
# [Article Title in Spoken-Word Friendly Form]
## The Civic Node · Dispatch №[NNN]
## [N] scenes · [N] beats · beat-segmented motion format · trailer · small-screen · 5-7 min target
```

The dispatch number is detected from existing dispatches in the workspace (see step 9 of the process), or captured from the user. The format tag (`beat-segmented motion format · trailer · small-screen`) distinguishes the current format from the legacy `Part One / Part Two` format and the older 7-9-slide pre-beat-format scripts.
```

- [ ] **Step 7: Replace slide markup convention (lines 215-227)**

Change the "Slide markup convention" subsection:

```markdown
### Slide markup convention

```markdown
**[SLIDE NN — SLIDE TITLE]**

[narration text — short sentences, no em-dashes, one-word landings welcome]

[blank line between paragraphs to mark a breath point]

---
```

The `---` between slides is intentional. It gives the reader visual separation when reading aloud.
```

to:

```markdown
### Beat markup convention

Each scene opens with a scene label followed by its beat count. Each beat has three parts: beat number, one `element:` note, and one spoken unit ending in `[stop]`.

```markdown
**[SLIDE NN — SCENE TITLE]** · [N] beats

▸ **B1** · *element: [one visual element — a stamp, a number, a phrase, or an illustration description]*
"[spoken narration — one unit, short sentences]" **[stop]**

▸ **B2** · *element: [one visual element]*
"[spoken narration]" **[stop]**

---
```

The `---` between scenes is intentional. Timing annotations (`[stop — let it sit]`, `[hold ~1.5s]`, `[REFRAIN]`) attach to the `[stop]` marker of the beat they modify.

**One element per beat.** If the `element:` note describes two independent things appearing simultaneously, split into two beats. An overlay (text landing on top of an existing illustration context) counts as one element.
```

- [ ] **Step 8: Verify changes**

Read `tcn-youtube-narration/SKILL.md` lines 1-230 and confirm:
- Frontmatter description mentions "beat markers" not "slide markers"
- Pacing target says "8-12 scenes, 80-120 beats total"
- Output artifact Contents says "8-12 scene blocks in beat-segmented markup"
- Narration structure opening says "one visual element" per beat
- Title block format tag shows scenes · beats · beat-segmented motion format
- Beat markup convention shows the `▸ **B1** · *element:*` pattern

- [ ] **Step 9: Commit**

```bash
git add tcn-youtube-narration/SKILL.md
git commit -m "feat(tcn-youtube-narration): beat-segmented format as standard

Replace 9-12-slide static model with 8-12-scene 80-120-beat target.
Update title block, markup convention, pacing language throughout."
```

---

## Task 2: Narration skill — visible-text budget, splitting rule, Script Notes, failure modes

**Files:**
- Modify: `tcn-youtube-narration/SKILL.md:135-147` (visible-text budget section)
- Modify: `tcn-youtube-narration/SKILL.md:229-265` (Script Notes footer template)
- Modify: `tcn-youtube-narration/SKILL.md:293-300` (Process step 7)
- Modify: `tcn-youtube-narration/SKILL.md:319-326` (failure modes)

- [ ] **Step 1: Replace visible-text budget section (lines 135-147)**

Change the "Visible-text budget (per slide)" subsection and its closing sentence entirely:

```markdown
### Visible-text budget (per slide)

Each slide is a small-screen object first. The downstream `tcn-youtube-slideshow` skill must produce a deck that's readable at thumbnail playback (~240px wide on a phone) and that works across 16:9, 9:16, and 1:1 aspect ratios from one HTML source. To make that possible, the *narration itself* paces around what will be visible on screen.

**The rule:** for each slide, identify what would actually render on the slide visual — the kicker, the headline/hook line, supporting bullets or one big number, source attribution if any. That visible content must stay **≤25 words total**, OR **one hero number plus ≤15 supporting words**. The spoken narration around it can be longer (a slide's spoken portion is typically 60-90 words ≈ 25-40 sec); the budget applies only to what would be lifted onto the slide as visible text.

**Practical effect:**

- A Receipt slide with five numbers becomes two slides (e.g., `THE RECEIPT · UNIT ECONOMICS` and `THE RECEIPT · HIP-143`), each carrying ≤3 numbers visually.
- A Frame slide with a four-part argument becomes a Frame slide (the framing line) followed by a Stakes or Twist slide (the consequences) — instead of one dense slide that tries to do both.
- A Verbatim quote longer than ~25 words gets trimmed to its sharpest clause for the visual; the full quote stays in the spoken narration.

If the visible budget can't be met by re-pacing — e.g., a chart that genuinely needs eight labels — flag it in the Script Notes footer under a `**Visual density flags:**` bullet so the slideshow skill knows to plan a panel-split for that slide specifically. Panel-splits at the visual layer are a last resort; re-pacing at narration time is the cleaner fix.
```

to:

```markdown
### Per-beat rule

Each beat carries **one visual element**. The `element:` note in the beat markup describes exactly what lands on screen when that beat fires.

**The rule:** one `element:` note = one thing on screen. If a note describes two independent things appearing simultaneously, it is two beats. An overlay (e.g. "$400,000 lands over the left figure") counts as one element — the illustration context is already established by an earlier beat.

**Practical effect:**

- A Receipt scene with five numbers becomes five beats — one number per beat, each on screen for ~3 seconds.
- A Frame scene with a four-part argument becomes four beats — one part per beat.
- A Verbatim quote is one beat: the quote (or its sharpest clause) is the element.

There is no word-count budget at the beat level — the `element:` note is inherently one thing.
```

- [ ] **Step 2: Update Script Notes footer template (lines 229-264)**

Change the Script Notes footer block. Replace:

```markdown
**Word count:** [N]
**Estimated runtime:** [M]:[SS] at ~140 wpm (TCN-natural pace)
**Voice register:** [N]/10 (Hank-Vox blend) — verified against workspace/core/anti-ai-writing-style.md

**Refrain markers (read slow each time):**
- "[refrain line]" (Slides [list], callback in Slide [N])

**Breath / pacing cues:**
- Slide [NN]: [cue, e.g., "hold the silence after 'Vibes.' for ~1 second"]
- Slide [NN]: [cue]

**Supersedence (if the article has fact-corrections post-narration):**
- (none on this pass — Script Notes block surfaces corrections when present)

**Cold-open candidate** (for thumbnail / title-skill downstream use):
- [the analogy or hook the cold open uses, in one phrase]

**Refrain candidate** (for slideshow skill downstream use):
- [the refrain line, if any]

**Cuts from the article** (what we deliberately did not cover, for Tease slide reference):
- [bulleted list of major article sections not in the video]

**Visual density flags** (for slideshow skill — slides that will need a panel-split):
- Slide [NN]: [reason, e.g., "chart needs 8 axis labels", "Verbatim quote 47 words"]
- (none on this pass — narration paced within ≤25 visible-words/slide budget)
```

with:

```markdown
**Word count:** [N]
**Beat count:** [N] across [M] scenes
**Estimated runtime:** [M]:[SS] at ~140 wpm (TCN-natural pace) + ~0.4s × [beat count] beat-stops
**Voice register:** [N]/10 (Hank-Vox blend) — verified against workspace/core/anti-ai-writing-style.md

**Refrain markers (read slow each time):**
- "[refrain line]" (Scene [NN] / B[N], callback at Scene [NN] / B[N])

**Breath / pacing cues:**
- Scene [NN] / B[N]: [cue, e.g., "hold the silence after 'Vibes.' for ~1 second"]
- Scene [NN] / B[N]: [cue]

**Supersedence (if the article has fact-corrections post-narration):**
- (none on this pass — Script Notes block surfaces corrections when present)

**Cold-open candidate** (for thumbnail / title-skill downstream use):
- [the analogy or hook the cold open uses, in one phrase]

**Refrain candidate** (for slideshow skill downstream use):
- [the refrain line, if any]

**Cuts from the article** (what we deliberately did not cover, for Tease scene reference):
- [bulleted list of major article sections not in the video]
```

- [ ] **Step 3: Update the forward-compat hooks note (line 264)**

Change:

```
The "Cold-open candidate," "Refrain candidate," "Cuts from the article," and "Visual density flags" fields are **forward-compat hooks** the slideshow + title + thumbnail skills will read later. They cost nothing to produce now and save work downstream. The Visual density flags field is the explicit handoff to `tcn-youtube-slideshow` for slides that should panel-split at the visual layer.
```

to:

```
The "Cold-open candidate," "Refrain candidate," and "Cuts from the article" fields are **forward-compat hooks** the slideshow + title + thumbnail skills will read later. They cost nothing to produce now and save work downstream.
```

- [ ] **Step 4: Update Process step 7 (around line 298)**

Change:

```
For each slide, mentally identify the *visible* subset — the kicker, headline/hook line, supporting bullets or hero number, attribution. Hold that subset to ≤25 words (or one hero number + ≤15 supporting words). If a slide can't meet the budget by re-pacing — e.g., a chart with eight required axis labels, a Verbatim quote that's irreducible — record the slide number under `**Visual density flags**` in the Script Notes footer so the slideshow skill can plan a panel-split. Re-pace at the narration layer first; flag for visual split only as a last resort.
```

to:

```
For each scene, break the spoken content into beats. Each beat is one spoken unit paired with one `element:` note describing a single on-screen visual. Write beats in order, applying timing annotations (`[stop — let it sit]`, `[hold ~1.5s]`, `[REFRAIN]`) where the delivery calls for them. Aim for 8-12 beats per scene; scenes shorter than 5 beats usually need more granularity, scenes longer than 15 beats should be split into two scenes with distinct sub-labels.
```

- [ ] **Step 5: Update failure modes (around lines 319-326)**

Change:

```
- **Cannot pace to 9-12 slides within the visible-text budget** — if even after re-pacing the script lands at <9 slides (too compressed) or >12 slides (too sprawling), surface to user. <9 usually means the article is too thin for video. >12 usually means the cold-open angle isn't narrow enough — too many distinct sub-arguments competing for screen time. Don't silently exceed; ask the user whether to re-pick the hook or to accept the over/under count.
- **More than ~3 visual density flags** — narration is the wrong place to be visually dense. If 3+ slides need a panel-split flag, the body menu picked too few categories or the chosen sub-labels are too broad. Re-pick before finalizing.
```

to:

```
- **Cannot pace to 8-12 scenes** — if the script lands at <8 scenes (too compressed) or >12 scenes (too sprawling), surface to user. <8 usually means the article is too thin for video. >12 usually means the cold-open angle isn't narrow enough. Don't silently exceed; ask the user whether to re-pick the hook or accept the count.
- **Beat count outside 80-120** — if total beats land under 80 (scenes too coarse) or over 120 (scenes too granular), surface to user with the actual count. Under 80: ask whether to add more granularity to the body scenes. Over 120: ask whether to merge closely related beats.
```

- [ ] **Step 6: Verify changes**

Read `tcn-youtube-narration/SKILL.md` lines 130-330 and confirm:
- "Visible-text budget (per slide)" heading is gone, replaced by "Per-beat rule"
- Script Notes footer no longer has `**Visual density flags:**` field
- Script Notes footer has `**Beat count:**` field
- Process step 7 describes beat-by-beat drafting, not slide-level visible budget
- Failure modes say "8-12 scenes" and "80-120 beats"

- [ ] **Step 7: Commit**

```bash
git add tcn-youtube-narration/SKILL.md
git commit -m "feat(tcn-youtube-narration): per-beat rule, Script Notes beat count, updated failure modes

Remove visible-text-budget and slide-splitting sections. Replace with
per-beat rule (one element per beat). Update Script Notes footer to add
beat count and remove visual density flags. Update failure modes."
```

---

## Task 3: Create `beat-types.md` reference file

**Files:**
- Create: `tcn-youtube-slideshow/references/beat-types.md`

- [ ] **Step 1: Create the file**

Create `tcn-youtube-slideshow/references/beat-types.md` with this content:

```markdown
# Beat Types — tcn-youtube-slideshow

*Loaded at runtime when typing beats and building slides. Defines the 5 beat types, their visual treatment, and the CSS skeleton Claude Design applies to each.*

---

## How beat typing works

Every beat from the narration gets a type before any slides are built. The type determines the slide's visual treatment. The typing rule:

> If the `element:` note describes anything other than words, numbers, or short phrases on a plain dark background — it is `illustration` type.

Everything else is one of the four typography types.

---

## The 5 types

### 1. `scene-header`

**Source:** Generated from the scene label — not a narration beat. One per scene.
**Visual:** Full TCN kicker treatment. Dark background. Kicker line only (no body text).
**When:** Appears as the first slide of each scene, before beat B1.

**Kicker format:** `DISPATCH №NNN · SCENE NAME` (e.g. `DISPATCH №006 · THE RECEIPT · THE CHOKEPOINT`)
Full kicker convention: `references/template-mapping.md` §2.

**CSS skeleton:**
```css
.slide.scene-header {
  background: #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
}
.slide.scene-header .kicker {
  font-family: 'Courier Prime', monospace;
  font-size: clamp(10px, 2.5cqmin, 36px);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #557FA3; /* slate-400 */
}
```

---

### 2. `stamp`

**Source:** Narration beats where `element:` is a short word or phrase on a plain dark background.
**Visual:** Text centered or positioned, large, Courier Prime. No kicker. One typographic element.
**Examples:** "SAME SHIFT", "GRANTED", "NOT YET.", "STOP THE LINE", "A UNION", "SAME COMPANY"

**Size rule:** Short stamps (1-3 words) → `--type-h1` (`clamp(28px, 9cqmin, 144px)`). Longer phrases (4-8 words) → `--type-h2-mid` (`clamp(22px, 6.5cqmin, 96px)`).

**CSS skeleton:**
```css
.slide.stamp {
  background: #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: min(7.5cqw, 7.5cqh);
}
.slide.stamp .text {
  font-family: 'Courier Prime', monospace;
  font-size: clamp(28px, 9cqmin, 144px); /* adjust to h2-mid for longer phrases */
  color: #e2e8f0; /* slate-200 */
  text-align: center;
  text-wrap: balance;
}
```

---

### 3. `hero-number`

**Source:** Narration beats where `element:` is a single figure (dollar amount, percentage, ratio, count).
**Visual:** One large number at `--type-hero` scale, optional short label below at `--type-body`. No kicker.
**Examples:** "$400,000", "+755%", "$13.77 BILLION", "10.5%", "100 : 1"

**CSS skeleton:**
```css
.slide.hero-number {
  background: #0f172a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1cqmin;
}
.slide.hero-number .number {
  font-family: 'Courier Prime', monospace;
  font-size: clamp(80px, 24cqmin, 360px);
  color: #e2e8f0;
  text-align: center;
  line-height: 1;
}
.slide.hero-number .label {
  font-family: 'Courier Prime', monospace;
  font-size: clamp(14px, 5cqmin, 72px);
  color: #557FA3; /* slate-400 */
  text-align: center;
  text-wrap: balance;
}
```

---

### 4. `refrain`

**Source:** Narration beats marked `[REFRAIN]`.
**Visual:** Full-screen recurring phrase with inverted treatment — white (`#f8fafc`) background, black (`#0f172a`) text. Every refrain beat looks identical so viewers recognize recurrence.
**Examples:** "WHO GETS TO SAY NO?" in dispatch-006 (appears at Scene 02/B9 and Scene 04/B11 with callback at Scene 09/B8-B10).

**Important:** The inverted colors are load-bearing. The refrain IS a rhetorical device; the visual inversion signals its repetition. Do not vary the treatment across instances.

**CSS skeleton:**
```css
.slide.refrain {
  background: #f8fafc; /* inverted — white */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: min(7.5cqw, 7.5cqh);
}
.slide.refrain .text {
  font-family: 'Courier Prime', monospace;
  font-size: clamp(28px, 9cqmin, 144px);
  color: #0f172a; /* inverted — black */
  text-align: center;
  text-wrap: balance;
}
```

---

### 5. `illustration`

**Source:** Narration beats where `element:` describes a visual that cannot be produced with typography alone — figures, maps, diagrams, abstract icons, metaphorical compositions.
**Visual:** Full-bleed AI-generated image (from fal.ai Pass 1 batch) as the slide background. Optional text or number overlay in HTML/CSS on top. Image fills the slide; text is layered.
**Examples:** "two figure silhouettes, Samsung plant outline behind them", "a US map with a single dot", "a lone ratepayer figure, no union behind it", "$400,000 lands over the left figure"

**Text overlay rule:** if the beat's `element:` note includes text appearing over an illustration ("$400,000 lands over…", "GRANTED + checkmark"), add the text as an absolutely positioned HTML overlay. The overlay uses `hero-number` or `stamp` sizing as appropriate.

**Filename convention:** images are named `NNN-SS-BNN.png` where NNN = dispatch number (zero-padded 3 digits), SS = scene number (zero-padded 2 digits), BNN = beat number (zero-padded 2 digits). Example: `006-01-B01.png`.

**CSS skeleton:**
```css
.slide.illustration {
  position: relative;
  background: #0f172a;
}
.slide.illustration .bg-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
/* overlay text — used when beat has text landing over illustration */
.slide.illustration .overlay-text {
  position: absolute;
  bottom: 15cqh;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Courier Prime', monospace;
  font-size: clamp(80px, 24cqmin, 360px); /* hero-number for figures */
  color: #e2e8f0;
  text-align: center;
  text-shadow: 0 0 40px rgba(0,0,0,0.8); /* only exception to no-shadows rule — needed for legibility over image */
  white-space: nowrap;
}
```

---

## Typing decision tree

```
Does the element: note describe only words/numbers/phrases on a plain dark background?
  YES → stamp or hero-number (is it primarily a figure? hero-number; otherwise stamp)
  NO  → Does it match [REFRAIN] marker?
          YES → refrain
          NO  → illustration
Is it a generated scene label (not a beat)?
  → scene-header
```
```

- [ ] **Step 2: Verify**

Read `tcn-youtube-slideshow/references/beat-types.md` and confirm:
- All 5 types are present with CSS skeletons
- Illustration type has the filename convention `NNN-SS-BNN.png`
- Refrain type documents the inverted-colors rationale
- Typing decision tree is present at the end

- [ ] **Step 3: Commit**

```bash
git add tcn-youtube-slideshow/references/beat-types.md
git commit -m "feat(tcn-youtube-slideshow): add beat-types reference with CSS skeletons"
```

---

## Task 4: Create `image-prompt-style.md` reference file

**Files:**
- Create: `tcn-youtube-slideshow/references/image-prompt-style.md`

- [ ] **Step 1: Create the file**

Create `tcn-youtube-slideshow/references/image-prompt-style.md` with this content:

```markdown
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
- BNN = beat number within scene, zero-padded 2 digits (e.g. `B01`)

Example: `006-01-B01.png` = dispatch 006, scene 01, beat 1.

---

## What to avoid

- No photography, no realistic rendering, no 3D effects
- No text inside the image (text overlays are HTML/CSS)
- No gradients, no lens flare, no shadows
- No bright saturated colors outside the slate palette
- No faces or recognizable people — silhouettes and geometric figures only
- No brand logos or real company marks
```

- [ ] **Step 2: Verify**

Read `tcn-youtube-slideshow/references/image-prompt-style.md` and confirm:
- Style anchor is present and copy-pasteable
- Three worked examples from dispatch-006 are present
- Filename convention `NNN-SS-BNN.png` matches what beat-types.md says
- "What to avoid" section is present

- [ ] **Step 3: Commit**

```bash
git add tcn-youtube-slideshow/references/image-prompt-style.md
git commit -m "feat(tcn-youtube-slideshow): add image-prompt-style reference for fal.ai Pass 1"
```

---

## Task 5: Archive old sections in `template-mapping.md`

**Files:**
- Modify: `tcn-youtube-slideshow/references/template-mapping.md`

- [ ] **Step 1: Archive sections 1, 3, and beyond; preserve section 2**

Read `tcn-youtube-slideshow/references/template-mapping.md` in full. The file has:
- §1 Slide-type mapping (sl-title, sl-lead, etc.) — **archive**
- §2 Kicker convention — **preserve**
- §3 Animation intensification — **archive**
- Any remaining sections — **archive**

Replace the file header and §1 with an archive notice, keep §2 intact, then append an archive block for the removed content:

```markdown
# Template Mapping — tcn-youtube-slideshow

*Kicker convention reference for scene-header slides. Loaded at runtime by `tcn-youtube-slideshow`.*

*Note: §1 (slide-type mapping) and §3+ (animation intensification) were superseded by the beat-segmented format introduced in 2026-06-03. See `references/beat-types.md` for the current beat type taxonomy and `docs/superpowers/specs/2026-06-03-youtube-constant-motion-design.md` for the design rationale. The archived content is preserved below the `---ARCHIVED---` marker.*

---

## Kicker convention

[KEEP EXISTING §2 CONTENT VERBATIM — do not change a word from line 29 through the end of §2]

---

---ARCHIVED (superseded 2026-06-03)---

[PASTE THE ORIGINAL §1 AND §3+ CONTENT HERE VERBATIM]
```

- [ ] **Step 2: Verify**

Read `tcn-youtube-slideshow/references/template-mapping.md` and confirm:
- Archive notice at the top explains the supersedence and points to beat-types.md
- §2 kicker convention is intact and unchanged
- `---ARCHIVED---` marker is present before the old content
- Old §1 (sl-title, sl-lead, etc.) is in the archived section, not deleted

- [ ] **Step 3: Commit**

```bash
git add tcn-youtube-slideshow/references/template-mapping.md
git commit -m "refactor(tcn-youtube-slideshow): archive sl-* mapping and animation tables in template-mapping

Kicker convention preserved. Beat-type taxonomy moved to beat-types.md."
```

---

## Task 6: Rewrite `tcn-youtube-slideshow/SKILL.md` — Part 1

Covers: frontmatter, What This Skill Does, Why Beats Not Animation, Position in Workflow, Inputs and Outputs.

**Files:**
- Modify: `tcn-youtube-slideshow/SKILL.md`

- [ ] **Step 1: Replace frontmatter description**

Change the `description:` field in the frontmatter to:

```yaml
description: "Step 2 of the Civic Node YouTube production workflow: runs directly in Claude Design to convert an uploaded beat-segmented narration script into a complete ~110-slide constant-motion HTML deck. Two-pass workflow: Pass 1 identifies illustration beats and outputs a fal.ai image-generation batch; Pass 2 (after images are uploaded) builds the full deck with one slide per beat plus scene-header slides. Invoke when the user uploads a youtube-narration.md in Claude Design and says 'build the slideshow', 'make the slides', or 'run this skill'. Does NOT apply to article slides, social media graphics, or thumbnail generation."
```

- [ ] **Step 2: Replace "What This Skill Does" section**

Replace the existing "What This Skill Does" section with:

```markdown
## What This Skill Does

Converts a finished YouTube narration script into a complete ~110-slide constant-motion HTML deck. Each narration beat becomes one static slide; scene labels become scene-header slides. The deck plays as near-continuous motion — ~2-3 seconds of static screen between slide advances.

**This skill runs directly in Claude Design.** It does not produce a prompt file for a human to paste. The user uploads `youtube-narration.md` to a Claude Design project, loads this skill as context, and Claude Design executes the workflow directly.

**Two-pass workflow:**
- **Pass 1:** Read the narration, identify illustration beats, output a numbered fal.ai image-generation batch. Pause for the user to generate and upload images.
- **Pass 2:** After images are uploaded, build the full HTML deck — scene-header slides + one beat slide per narration beat — referencing uploaded images for illustration beats.

**Output:** A single bundled HTML file (`dispatch-NNN.html`) with ~110 slides, simple CSS cross-dissolve transitions, and manual keypress advancement. No dependency on `deck-stage.js` or the existing animation primitive system.
```

- [ ] **Step 3: Replace "Why a Prompt-Builder..." section with "Why Beats, Not Animation States"**

Replace the existing "Why a Prompt-Builder, Not a Slideshow Generator" section with:

```markdown
## Why Beats, Not Animation States

The previous format used ~10 slides with animation primitives (`sl-reveal` cascades, `sl-chart-draw`, etc.) that built up content within each slide. Two problems:

1. **Claude Design's animation UI is hard to verify.** You can't see beat 7 of 13 without playing through the animation. If beat 7 is wrong, you have to describe an animation state change and hope Claude Design re-generates it correctly.

2. **On-screen motion came from animation, not from visual change.** A viewer watched one slide for 30-40 seconds while elements appeared. That's not constant motion.

With discrete static slides — one per beat — both problems disappear. Each slide is a visible, editable object. Motion comes from advancing slides, not from animation triggers. The recording workflow (Justin pressing a key at each beat-stop) produces genuine visual change every 2-3 seconds.

**What this means for Claude Design:** build simple, static slides. The only transition is a 200ms cross-dissolve between slides. No `sl-reveal`, no `sl-chart-draw`, no cascade primitives. The content is what changes; the animation is incidental.
```

- [ ] **Step 4: Update "Position in the YouTube Workflow" section**

Find and update the upstream/downstream description to reflect that this skill now runs in Claude Design and produces an HTML deck (not a prompt file):

```markdown
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
```

- [ ] **Step 5: Replace "Inputs and Outputs" section**

```markdown
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

> Deck complete — [N] slides ([M] scenes + [K] beat slides + [J] scene-headers). Open `dispatch-NNN.html` in a browser, resize to 1:1 (1080×1080), and advance through the deck to verify. Approve, redirect, or cancel?

**Stop after each pass gate.** Do not proceed to Pass 2 without user confirmation that images have been uploaded.
```

- [ ] **Step 6: Verify Part 1**

Read the updated `tcn-youtube-slideshow/SKILL.md` from the top and confirm:
- Frontmatter description mentions "runs directly in Claude Design" and "two-pass workflow"
- What This Skill Does mentions Pass 1 / Pass 2 and the ~110-slide output
- "Why Beats" section explains the two problems with the old format
- Position section no longer says "planned" for slideshow skill
- Inputs and Outputs has two gate prompts (Pass 1 and Pass 2)

- [ ] **Step 7: Commit**

```bash
git add tcn-youtube-slideshow/SKILL.md
git commit -m "feat(tcn-youtube-slideshow): rewrite Part 1 — execution environment, two-pass overview, inputs/outputs"
```

---

## Task 7: Rewrite `tcn-youtube-slideshow/SKILL.md` — Part 2

Covers: Beat Type Taxonomy, Two-Pass Workflow.

**Files:**
- Modify: `tcn-youtube-slideshow/SKILL.md`

- [ ] **Step 1: Replace "Slide-Type Mapping" section with "Beat Type Taxonomy"**

Remove the existing §5 slide-type mapping table (sl-title, sl-lead, etc.) and replace with:

```markdown
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
```

- [ ] **Step 2: Remove the old Kicker Convention section**

The kicker convention is now in `references/template-mapping.md` §2. Remove the inline kicker convention section from SKILL.md (it was §6 in the original). Replace with a one-line pointer:

```markdown
## Kicker Convention

Full kicker convention, rules, and examples: `references/template-mapping.md` §2.
```

- [ ] **Step 3: Replace the Animation Intensification section with Two-Pass Workflow**

Remove the old "Animation Intensification" section entirely. Add the new "Two-Pass Workflow" section:

```markdown
## Two-Pass Workflow

### Pass 1 — Image generation batch

1. **Read the uploaded narration.** Parse scenes, beats, element notes, refrain markers.

2. **Type every beat.** Apply the typing rule from Beat Type Taxonomy above. List the typed beat inventory (count of each type).

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
    /* TCN brand: Courier Prime, #0f172a background, slate palette */
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
      /* 1:1 primary canvas; 16:9 and 9:16 work by resizing the browser window */
    }

    .slide {
      position: absolute;
      inset: 0;
      container-type: size;
      opacity: 0;
      transition: opacity 200ms cubic-bezier(0.2, 0, 0, 1);
      pointer-events: none;

      /* CSS custom properties for type scale */
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

    /* [beat type CSS from references/beat-types.md — scene-header, stamp, hero-number, refrain, illustration] */
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
```

- [ ] **Step 4: Verify Part 2**

Read the updated `tcn-youtube-slideshow/SKILL.md` beat taxonomy and workflow sections and confirm:
- Beat taxonomy table has all 5 types with the "Needs image?" column
- Typing rule is explicit: "anything other than words/numbers/short phrases → illustration"
- Two-Pass section has the exact image batch format (numbered, with filename convention)
- Pass 2 includes the complete HTML boilerplate with the JS slide-advance logic

- [ ] **Step 5: Commit**

```bash
git add tcn-youtube-slideshow/SKILL.md
git commit -m "feat(tcn-youtube-slideshow): rewrite Part 2 — beat taxonomy, two-pass workflow with HTML boilerplate"
```

---

## Task 8: Rewrite `tcn-youtube-slideshow/SKILL.md` — Part 3

Covers: HTML Structure, The Process, Failure Modes, Justoon deferral, What This Skill Is NOT, Companion Skills, Reference Files.

**Files:**
- Modify: `tcn-youtube-slideshow/SKILL.md`

- [ ] **Step 1: Replace "Small-Screen Readability and Multi-Aspect Layout" section with "HTML Structure"**

Remove the old section (type scale table, safe-zone logic, thumbnail anchor rule, visible-text budget, slide-splitting rule, panel-split mechanism). Replace with:

```markdown
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
```

- [ ] **Step 2: Replace "The Process" section**

Replace the 10-step process with a shorter Claude Design-oriented version:

```markdown
## The Process

### 1. Parse the narration

Read the uploaded `youtube-narration.md`. Extract:
- Dispatch number (from title block `## The Civic Node · Dispatch №NNN`)
- Scene labels and beat count per scene
- Each beat's element note and spoken text
- Refrain markers (`[REFRAIN]`)
- Script Notes footer (cold-open candidate, etc.)

Halt if the file is missing or the beat markup convention (`▸ **B1** · *element:*`) is not present.

### 2. Type every beat

Apply the typing rule from Beat Type Taxonomy. Produce a brief inventory:

```
Beat inventory — Dispatch №006 (102 beats across 10 scenes):
  scene-header: 10 (generated)
  stamp: 38
  hero-number: 14
  refrain: 2
  illustration: 38
  Total slides: 112
```

If illustration count is 0, skip Pass 1 entirely and proceed to Pass 2.

### 3. Pass 1 — image batch

For every illustration beat, write one numbered image prompt (see Two-Pass Workflow §Pass 1 for format). Present the batch and the Pass 1 gate prompt. Stop.

### 4. Pass 2 — deck build

After user confirms image uploads: build all slides in scene order. Scene-header first, then beats B1 through BN for each scene. Write `dispatch-NNN.html`. Present Pass 2 gate prompt. Stop.
```

- [ ] **Step 3: Replace Failure Modes**

```markdown
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
```

- [ ] **Step 4: Add Justoon — Deferred section**

```markdown
## Justoon — Deferred

The previous slideshow skill mapped Justoon (a TCN character illustration) to specific slide types — role A (pointing teacher) on Receipt/Stakes slides, role C (reaction-as-anchor) on Twist slides. In the beat format, those slide types no longer exist as distinct slots.

Justoon could appear in the new format as an illustration-type beat: the `element:` note would reference a Justoon image ("Justoon appears pointing at the chokepoint diagram") and the fal.ai image would be replaced by a Justoon PNG from `~/Pictures/tcn-justin-slideshow/`. This integration is **not implemented in this version**.

To reintroduce Justoon: define a `justoon` beat type or subtype, add it to the typing decision tree in `references/beat-types.md`, and define the Pass 1 behavior (no image prompt needed — use the local PNG directly in Pass 2).
```

- [ ] **Step 5: Update What This Skill Is NOT**

```markdown
## What This Skill Is NOT

- This skill does **not** produce a prompt file for a human to paste into Claude Design. It runs directly in Claude Design and builds the deck.
- This skill does **not** generate narration. That's `tcn-youtube-narration` (Step 1).
- This skill does **not** generate the fal.ai images. It produces the prompts in Pass 1; the user generates images externally and uploads them.
- This skill does **not** extend the TCN design system CSS. The deck's CSS is self-contained in the HTML file.
- This skill does **not** produce thumbnails, social graphics, YouTube titles, descriptions, or chapter timestamps. Those are separate skills that run after recording.
- This skill does **not** fact-check the article. That happened upstream.
```

- [ ] **Step 6: Update Companion Skills and Reference Files**

```markdown
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
```

- [ ] **Step 7: Final verify — full SKILL.md read**

Read `tcn-youtube-slideshow/SKILL.md` in full. Confirm:
- No references to `deck-stage.js` except in "What This Skill Is NOT" context
- No references to `sl-reveal`, `sl-chart-draw`, or other old animation primitives outside the "no animation primitives" section
- No references to producing a `youtube-slideshow.md` prompt file
- All 5 beat types appear in both the taxonomy table and the two-pass workflow
- HTML boilerplate is present in Pass 2 with the JS advance logic
- Justoon deferral section is present
- Reference Files section points to the three new/updated reference files

- [ ] **Step 8: Commit**

```bash
git add tcn-youtube-slideshow/SKILL.md
git commit -m "feat(tcn-youtube-slideshow): rewrite Part 3 — HTML structure, process, failure modes, Justoon deferral"
```

---

## Task 9: Smoke-test the full change set

- [ ] **Step 1: Verify narration skill against dispatch-006**

Read `tcn-youtube-narration/SKILL.md` and the dispatch-006 narration at `workspace/drafts/samsungs-400000-bonus-and-the-4000-one/youtube-narration.md` (or its equivalent path). Confirm that dispatch-006's format (10 scenes, 102 beats, `▸ **B1** · *element:*` pattern) matches what the updated skill prescribes exactly. List any gaps.

- [ ] **Step 2: Verify slideshow skill reference consistency**

Read `tcn-youtube-slideshow/references/beat-types.md` and `tcn-youtube-slideshow/references/image-prompt-style.md`. Confirm:
- Filename convention is `NNN-SS-BNN.png` in both files (not `NNN-01-B01.png` with different zero-padding)
- CSS skeletons in beat-types.md use the same custom property names (`--type-hero`, `--type-h1`, etc.) as the HTML boilerplate in SKILL.md
- Color values are consistent: `#0f172a` dark BG, `#557FA3` slate-400, `#e2e8f0` near-white

- [ ] **Step 3: Confirm no orphaned references**

Search for references to removed concepts:
```bash
grep -r "youtube-slideshow.md\|deck-stage.js\|sl-reveal\|sl-chart-draw\|panel.split\|Visual density flags\|9-12 slides\|≤25 visible" \
  tcn-youtube-narration/ tcn-youtube-slideshow/
```
Expected: zero matches (all occurrences should have been removed or moved to the archived section of template-mapping.md).

- [ ] **Step 4: Final commit**

```bash
git add tcn-youtube-narration/ tcn-youtube-slideshow/
git commit -m "chore: smoke-test verified — constant-motion format implementation complete"
```
