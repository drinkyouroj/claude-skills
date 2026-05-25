# DNA Checklist — Per-Concept Vetting

Run this checklist on each candidate concept before surfacing it at step 5. A concept that fails any check is not surfaced — either re-compose silently or drop to two concepts.

The full DNA principles, with reasoning and exemplars, live in `workspace/core/_template-flagship-cover.md`. This file is the **operational checklist** — short prompts the skill runs against each concept, with red-flag examples that should fail.

---

## Check 1: Metaphor compression, not evidence illustration

**Question:** Does this image carry the thesis through ONE relationship — face-IS-bureaucracy, camera-vs-neighborhood, signature-vs-collapse, steam-engine-↔-DDR5? Could a reader find the metaphor in under a second?

**Pass:** A single visual relationship that compresses the argument. The reader's eye lands on the metaphor before the title is read.

**Fail (red flags):**
- Documentary-evidence collage — multiple objects representing different parts of the story.
- Labeled blueprint or cross-section — castle/building/system diagram with callouts.
- Document stack or cork-board with sticky notes — illustrating what the piece is *built from* instead of what it *argues*.
- Encyclopedic infographic — multi-panel "here's everything you need to know."
- "Reader has to read the cover before they can understand it" — that's a verbal job the title already does.

**The Process-Is-the-Punishment failure was this check:** a labeled castle blueprint with three competing zones (castle + courthouse + calendar) illustrating *evidence* instead of compressing *argument*.

---

## Check 2: ≤2 primary visual elements

**Question:** Does the image have either one central subject (a face, an object, a unified scene) OR two icons in a clean comparison? At thumbnail size, does it resolve as ONE image — not as several elements competing for attention?

**Pass:** One subject. Or two icons in deliberate comparison. Or a scene whose multiple objects form one compositional unity (the ukiyo-e scholars on the cliff are technically two figures, but they read as a single tableau — pass).

**Fail (red flags):**
- Three competing zones (e.g., castle + courthouse + calendar all fighting for visual weight).
- Multi-panel layout (split-frame "before/after," 2×2 grid, etc.).
- Labeled diagram with multiple callouts.
- A "busy" scene where the viewer's eye has nowhere to land first.

**Test:** Shrink the concept description to a Substack feed thumbnail in your mind. Can a viewer at that size resolve it as one image, or does it scatter?

---

## Check 3: No embedded text in the image

**Question:** Does the image avoid embedded labels, sticky-note callouts, document captions, "stamped" words, chart titles, annotation badges?

**Pass:** Image is purely visual. Post title and subtitle do all verbal work.

**Fail (red flags):**
- Labels naming parts of the scene ("moats / curtain / supply lines / provisions").
- Sticky notes with words on them.
- Chart titles, axis labels, data callouts.
- Stamped editorial words ("BREAKING," "REPORT," etc.).
- A magazine cover layout with "headline overlay" rendered IN the image.

**Exception (rare):** when the metaphor *requires* a piece of text that exists as a real-world physical element — like the hand-painted "Welcoming City ATL GA" sign reflected in the Atlanta Flock camera housing, where the sign IS the metaphor. In that case the text must be photographed signage (a thing the world contains), not an editorial annotation added on top. The Atlanta cover's text passes because the camera is the editorial element and the sign is the world.

**Critical:** image generators default toward including text when prompted with concepts that involve text. The prompt MUST include explicit negative-prompt instructions — see [`prompt-source-paths.md`](prompt-source-paths.md) for the exact block.

---

## Check 4: Cinematic OR technical illustration register

**Question:** Does this concept sit in one of the permitted registers, and avoid the excluded ones?

**Permitted registers:**
- **Editorial poster** — B&W subject + saturated color backdrop, single hard key light, film grain. *($71B Bluff)*
- **Surreal symbolic** — one symbolic object composed of unexpected materials. *(System Is Functioning Correctly)*
- **Photographic with reflection device** — one photographed object whose surface embeds the secondary subject. *(Atlanta)*
- **Clean technical illustration** — isometric, white background, industrial palette. *(Cheaper AI)*
- **Narrative scene** — single illustrated tableau in a stylistically distinct register. *(I Had the Wrong Protagonist, ukiyo-e)*

**Excluded registers:**
- Documentary scrapbook (newspaper-clippings-and-sticky-notes pinned to a wall).
- Encyclopedic infographic (data-viz-poster aesthetic).
- Labeled blueprint (architectural cross-section with callouts).
- Split-frame "before/after" with cluttered scenes on both sides.
- Screenshot composite (UI mockups, "screen within a screen").
- YouMind #4847 archival-infographic template — explicitly excluded.

**Pass:** the concept's register is on the permitted list.

**Fail:** any of the excluded registers, or a register the skill cannot place on either list (which usually means it isn't editorial enough).

---

## Check 5: High contrast as the carrying device

**Question:** Is there a specific contrast that carries the argument — and would the cover lose its editorial weight without it?

**Examples of carrying contrast:**
- B&W subject vs. saturated backdrop ($71B Bluff: B&W Altman + green DRAM).
- Cold color vs. warm color (Atlanta: steel-blue camera + amber reflected scene).
- Present vs. absent (an empty chair beside an occupied one).
- Sparse vs. ornate (one clean icon against a chaotic background).
- Photographed-real vs. illustrated-symbolic (a photographed object whose reflection is illustrated).

**Pass:** there's a specific, named contrast carrying the argument. You can articulate what the contrast IS and what argument it carries.

**Fail (red flags):**
- Uniformly toned image — everything the same value, same temperature, same saturation.
- Default-AI saturated photography (every element equally bright, no compositional hierarchy).
- "Rainbow" palette — many colors at similar saturation, none carrying a contrast role.
- Contrast that exists but doesn't argue (e.g., bright/dark for purely decorative reasons).

---

## After running the five checks

For each concept, write the result inline in the concept brief:

```
DNA checks: 5/5
  ✓ Compression: [one-line confirmation of the relationship]
  ✓ ≤2 elements: [confirmation]
  ✓ No embedded text: [confirmation, or noted exception with reasoning]
  ✓ Permitted register: [which register]
  ✓ Contrast: [what the contrast is and what it argues]
```

If a check fails: re-compose the concept silently and re-run the checklist. If you cannot fix the failure within the same compression strategy, drop the concept entirely. Better to surface two strong concepts than three where one is weak.

---

## What the checklist is NOT

This is not a creative-direction tool. It's a **filter** — it catches concepts that fail the DNA before the user sees them. The creative work happens upstream in step 3 (identify the core compression) and step 5 (propose 2–3 compressions). The checklist is the last gate before user review.

If every concept you compose keeps failing the checklist, the problem is upstream — you're either misreading the piece's argument or reaching for compositions the DNA doesn't permit. Go back to step 3 and re-read the article's thesis.
