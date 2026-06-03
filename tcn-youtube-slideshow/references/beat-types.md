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

**Filename convention:** images are named `NNN-SS-BNN.png` where NNN = dispatch number (zero-padded 3 digits), SS = scene number (zero-padded 2 digits), BNN = B + beat number (zero-padded 2 digits). Example: `006-01-B01.png`.

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
