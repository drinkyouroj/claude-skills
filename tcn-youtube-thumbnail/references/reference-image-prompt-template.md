# Reference-Image Prompt Template (default mode)

Active when no Flux LoRA URL is found. Prompts produced in this mode are model-agnostic — designed to work in Freepik, Nano Banana 2 / Gemini, Midjourney (with `--cref`), Flux Kontext (image-to-image), or any other tool that accepts a character reference image.

The skill reads this file at process step 8 (compose the two prompt variants). It holds two responsibilities the skill defers to runtime judgment:

1. **Selection** — which file from the reference library to pin to each variant, given the dispatch's tone and concept. **Interpretive, not prescriptive** — pick the ref whose register lands hardest against the specific cold-open, not by mechanical rule.
2. **Phrasing** — how to express the character-reference instruction in a way the chosen image-generation tool understands.

---

## Reference-Image Library

The skill expects a directory of tone-mapped illustrated-Justin reference images, sourced one-time via a trained character + fixed seed in Magnific/Freepik/Nano Banana 2. The directory location comes from SKILL.md "Optional inputs" lookup chain (default `~/Pictures/tcn-justin-references/`).

All files share the same illustrated-portrait style, fixed seed, trained character, and wardrobe (plaid bucket cap with red brand patch, olive-grey t-shirt, dark jeans, grey sneakers, blue square-frame glasses, salt-and-pepper brown beard).

**Naming convention:** `[framing]-[expression-or-gesture].png`. The skill reads filenames semantically — anything matching `headshot-*` or `bust-*` is a Variant B (close-up) candidate; anything matching `fullbody-*` is a Variant A (wide editorial) candidate. New files can be added to the library at any time; the skill picks them up without code changes as long as their names follow the convention and the selection guidance below is updated.

### Headshots — for Variant B (tight close-up)

Grouped by emotional register. Many dispatches map cleanly to one register; some sit between groups, in which case pick the ref whose specific reading lands harder against the cold-open's actual phrasing.

**Neutral baseline** — use when the cold-open carries no strong emotional charge, or when the vibe scene is already doing the dramatic work.

| File | Register |
|---|---|
| `headshot-neutral-forward.png` | The anchor. Direct gaze, composed. Default when no tone signal applies. **Required file** — fallback for any missing tone-mapped ref. |
| `headshot-neutral-composed.png` | Slightly turned, more poised than dead-center. Alternative anchor when scene composition wants a touch of figure rotation. |
| `headshot-3q-neutral.png` | 3/4 angle baseline. Gives figure dimensionality when prompt scene benefits from depth. |
| `bust-neutral-front.png` | Wider crop with more shoulder/torso. Good when the vibe scene has heavy negative space the figure can sit calmly within. |

**Sardonic / dry / "of course it does"** — TCN's house register. Reach for these first when the cold-open carries dry wit, restrained incredulity, or "you can't make this up" energy.

| File | Register |
|---|---|
| `headshot-smirk.png` | The TCN signature dial. Half-smile, slight eyebrow lift implied. For dispatches where the sardonic voice is the rhetorical move. |
| `headshot-neutral-raised-eyebrow.png` | Quieter cousin of smirk. Reads as "really?" without going amused. For dispatches where the absurdity is the story but the figure shouldn't editorialize. |
| `headshot-lip-bite.png` | Restraint, suppressed reaction. "I have things to say but I'm not saying them." Niche use — when the dispatch is about something the figure would clearly have opinions on, but the thumbnail wants tension over reveal. |

**Concerned / alarmed / stern** — for dispatches where the stakes are real and the figure should signal that.

| File | Register |
|---|---|
| `headshot-concerned.png` | Furrowed brow, slight mouth downturn. "This isn't good." Default for alarm-bell dispatches. |
| `headshot-worried.png` | Close to concerned, slightly more pleading. Interchangeable — pick whichever specific facial nuance lands harder on the chosen vibe. |
| `headshot-shocked.png` | Open mouth, raised brows. For "they did WHAT" moments. High-arousal — pairs well with vibe scenes that already carry shock. |
| `headshot-stern.png` | Brow lowered, mouth tight. The "I am unimpressed and you should be too" register. For accountability dispatches that aren't quite ready for `fullbody-pointing-at-viewer`. |

**Warm / approachable** — use cautiously. These read as tonally light and may signal the wrong stakes for serious dispatches.

| File | Register |
|---|---|
| `headshot-neutral-warm.png` | Micro-smile, low-key approachable. Safest of the warm set. Good for explainer dispatches that aren't sounding alarms. |
| `headshot-neutral-slight-smile.png` | Between warm and full-smile. |
| `headshot-calm.png` | Composed, settled. "This is fine, actually." For dispatches that *push back against* alarmism. |
| `headshot-big-smile.png` | Full friendly grin, teeth visible. High CTR but tonally light — **do not use** for high-stakes or alarm dispatches. |
| `headshot-big-smile-eyes-closed.png` | Laughing moment. Rare use — only when a dispatch is genuinely absurd and you want to lean into "this is funny." |

**Looking at something** — when the dispatch concept involves observing, examining, or watching.

| File | Register |
|---|---|
| `headshot-looking-down.png` | Gaze cast downward. For "examining the document / scrolling the chart / reading the filing" framings — dispatches about leaks, evidence, screens, data. Bonus: the viewer's eye follows the figure's gaze toward the lower portion of the thumbnail, where the overlay headline often sits. |
| `headshot-3q-looking-right.png` | Gaze off to the right of frame. Good when scene context lives to the right of the figure. |
| `headshot-side-profile-left.png` | Pure side view. For "watching the chaos unfold" framings — figure as observer, not addresser. |

**Specialty — sparingly.**

| File | Register |
|---|---|
| `headshot-extreme-closeup.png` | Face fills frame, visceral, high impact. Reserve for highest-stakes visceral-reaction dispatches. Loses force if overused — once per ~5 dispatches max. |
| `headshot-wink.png` | Playful, conspiratorial. Rare use — for "yeah, we both know what's going on here" dispatches. Reads as too cute for most TCN tones. |

### Fullbody — for Variant A (wide editorial)

Grouped by posture/gesture intent.

**Neutral baseline** — for dispatches where the figure is part of the scene but not gesturing at anything specific.

| File | Register |
|---|---|
| `fullbody-standing-neutral.png` | The fullbody anchor. Standing, hands at sides. Default. **Fallback** for any missing fullbody ref. |
| `fullbody-3q-relaxed.png` | 3/4 angle, slight asymmetric weight. More natural baseline than dead-center standing. Often better than `standing-neutral` for editorial compositions. |

**Gesturing / pointing at something in the scene.**

| File | Register |
|---|---|
| `fullbody-pointing-right.png` | "Look at this" — figure positioned to the left of frame, gesturing toward subject placed in the right negative space. Excellent for "here's the chart / the filing / the situation" compositions. |
| `fullbody-pointing-up.png` | "Look above" — for dispatches about overhead things (satellites, drones, towers, leadership hierarchies, distant authority figures). |
| `fullbody-open-palm-point.png` | Softer pointing, "here's the thing" gesture. Less directional than `pointing-right` — figure presenting rather than indicating. |
| `fullbody-pointing-at-viewer.png` | Direct address, accusatory. **Sparingly** — reads preachy if overused. Save for accountability/calling-out dispatches where direct address is the rhetorical move. Limit to ~1 in 10 dispatches. |

**Reaction posture.**

| File | Register |
|---|---|
| `fullbody-shrug-open-arms.png` | "They did WHAT" / "this is absurd" / "I can't even." The TCN incredulity gesture. Pairs naturally with sardonic-register headlines on Variant B. |
| `fullbody-thumbs-gesture-smiling.png` | Positive framing — "this actually went well." Rare TCN use case (most dispatches aren't celebrations), but useful when a dispatch genuinely is good news. |

**Angle variation.**

| File | Register |
|---|---|
| `fullbody-overhead-angle.png` | Top-down camera. Reads as "observing the situation from above" — pairs well with dispatches that take a structural/systemic view rather than reacting to a single event. |

---

## Selection Guidance (interpretive)

When composing the two variants:

1. **Read the cold-open and dispatch concept before picking refs.** The cold-open's emotional charge is the strongest signal for Variant B; the dispatch concept (what the piece is *about*) is the strongest signal for Variant A.
2. **Use the vibe-adjective sniff test as a fast prior, then refine against the cold-open.** The chosen vibe at Gate 1 implies a tonal direction:
   - "moody", "noir", "conspiracy-thriller", "quiet-dread" → lean concerned/stern/worried for B; lean overhead-angle/standing-neutral for A
   - "investigative", "documentary", "analytical", "archival" → lean neutral-forward/looking-down for B; lean pointing-right/open-palm-point for A
   - "vaporwave-tech", "apocalyptic-tech", "corporate-dystopian" → lean smirk/neutral-raised-eyebrow for B; lean shrug-open-arms/overhead-angle for A
   - "dramatic" or "cinematic" alone → ambiguous; read the cold-open directly
3. **Variant B (close-up):** pick the headshot whose register matches the cold-open's emotional charge. If sardonic → `smirk`. If alarm bell → `concerned` or `worried`. If "they did WHAT" → `shocked`. If examining-evidence → `looking-down`. If no strong tone signal → `neutral-forward`.
4. **Variant A (wide editorial):** pick the fullbody whose gesture matches the dispatch concept. If "look at this evidence" → `pointing-right` with subject placed in the right negative space. If incredulity at a decision → `shrug-open-arms`. If overhead/distant authority → `pointing-up`. If structural/systemic framing → `overhead-angle`. If no strong concept signal → `3q-relaxed` or `standing-neutral`.
5. **Coherence between variants.** Both variants should feel like they belong to the same dispatch. If Variant B is `headshot-concerned`, don't pair with `fullbody-thumbs-gesture-smiling` — that's a tonal mismatch the viewer feels even without language. Pair concern with shrug or pointing-up; smirk with pointing-right or 3q-relaxed; shock with overhead-angle or shrug.
6. **Note the picks in the artifact header.** Include both filenames so a future re-run or human review can see what was picked and why.

---

## Fallback Chain

- **Missing directory entirely, OR missing `headshot-neutral-forward.png`:** halt with a setup note (where to place files, the named-by-purpose vocabulary above, link to this mapping). The neutral headshot is the irreducible-minimum file.
- **Missing specific tone-mapped ref but neutral default exists:** fall back silently:
  - Variant B fallback → `headshot-neutral-forward.png`
  - Variant A fallback → `fullbody-standing-neutral.png`
- Note the substitution in the artifact header: `**Ref substitution:** intended <picked>.png, used <fallback>.png (file not found).`

---

## Wardrobe & Style Consistency Directive (every prompt)

Every reference-image prompt the skill emits **must** include language that pins the rendered figure to the library's visual identity. The character has trained variance, but the wardrobe and style do not — if the prompt doesn't anchor them, the model can drift.

Include in every prompt:

> Match the reference image's character: salt-and-pepper brown beard, blue square-frame glasses, plaid bucket cap with red DICKIES brand patch (preserve this patch exactly — NO Supreme or other brand substitutions), olive-grey t-shirt, dark jeans, grey sneakers. Match the illustrated-portrait style — soft semi-realistic shading, illustrated editorial register, not photoreal, not flat-vector. Keep facial features and proportions consistent with the reference.

This language is **non-negotiable** — every emitted prompt includes it. Adjust only the wardrobe enumeration if you ever add wardrobe variants to the library. The DICKIES brand-patch preservation language was added after the dispatch-004 test run, where Nano Banana 2 hallucinated a "Supreme"-style patch when the prompt left brand identity to model discretion. Explicit preservation language closes that hallucination path.

---

## Character Reference Instruction (every prompt)

Every prompt includes a character-reference instruction. The skill substitutes the picked filename so the user knows which specific ref to upload alongside the prompt:

```
Use the attached reference image as the character reference. Match the character's facial features, hair, hat, glasses, beard, wardrobe, and illustrated-portrait style exactly. Place the same character into a new scene as described below.

REFERENCE IMAGE TO ATTACH: <picked-filename>.png
```

---

## Art Direction Principles (apply to every variant prompt)

Five patterns surfaced during the dispatch-004 end-to-end test as the difference between underwhelming and shippable prompts. The variant templates below incorporate all five — when extending or editing them, preserve these patterns.

1. **Named-illustrator style anchors.** Models pattern-match better to specific artist names than to abstract style descriptors. "Magazine editorial style" gets a coin-flip; "in the visual register of Brian Stauffer, Yann Legendre, or Tom Bachtell" gets you 80% of the way to the intended register. Always anchor the style register with at least one specific illustrator name.
2. **Explicit `NOT` directives.** When the model has latitude, it defaults to friendlier/safer/flatter renderings. Naming the failure modes explicitly forecloses them. Every variant prompt must include `NOT flat vector, NOT photoreal, NOT explainer-cartoon` for style register. Add per-scene `NOT` directives for the specific failure modes you anticipate (e.g., `NO hard color block seam`, `NO recognizable architectural shapes`, `NO teeth-visible smile`).
3. **Composition ratios as explicit percentages.** Abstract descriptors like "third" and "left side" get loose interpretations. Numeric ratios ("LEFT 25-30% of frame") get tight ones. State all major compositional zones in numeric percentages.
4. **Per-variant expression and gaze directives.** The model defaults to "looking at camera with neutral expression" unless told otherwise. Every variant prompt must explicitly specify (a) where the eyes look, (b) what the eyebrows do, (c) what the mouth does — and forbid the wrong default (e.g., for smirk: `closed-lipped half-smile with one eyebrow raised. Do NOT render a warm friendly smile with teeth showing`).
5. **Brand-patch preservation language.** Nano Banana 2 hallucinated a "Supreme"-style patch in the dispatch-004 test when the prompt didn't lock the cap brand. The wardrobe directive now includes `red DICKIES brand patch (preserve exactly — NO Supreme or other brand substitutions)` to close that path. Extend to any other distinctive brand-identifying detail.

---

## Variant A — Wide Editorial Composition (prompt template)

```
[CHARACTER REFERENCE INSTRUCTION above]
REFERENCE IMAGE TO ATTACH: <picked Variant A filename>

STYLE REGISTER: Editorial magazine illustration in the visual register of Brian Stauffer, Yann Legendre, or Tom Bachtell. Soft semi-realistic shading with visible illustrative brushwork, paper texture grain across the canvas, deliberate warm/cool color temperature variation. NOT flat vector. NOT photoreal. NOT explainer-cartoon.

COMPOSITION:
- LEFT 25-30% of frame: the illustrated character in [angle — three-quarter / profile / front-facing per chosen ref], [gesture description matching chosen ref — e.g., pointing across the frame to the right, hands open in shrug, hand pointing up at something overhead]. Eyes [direction — follow own pointing finger / scanning the right side of frame / looking off-camera at the scene]. Eyebrows [directive — slightly raised in amused-incredulity / furrowed in concern / lowered in stern register — match chosen ref's expression]. Mouth [directive — closed-lipped half-smile, sardonic, NOT friendly grin / OR neutral / OR concerned downturn — match chosen ref's expression]. NOT looking at camera unless the chosen ref demands it.
- RIGHT 60-65% of frame: [scene description pulled from dispatch concept + chosen vibe — be physically specific about what objects are present, their materials, their scale]. [If the dispatch's argument structure is a scale or weight contrast: name explicitly what dominates and what is dwarfed. The size contrast must be the rhetorical engine, not a subtle hint.]
- Vertical 5-10% transition zone in the middle — NOT a hard color block seam. Let lighting and scene flow across the divide.

LIGHTING:
- Key light from [direction — typically upper-left, upper-right, or overhead] in [color temperature — cool fluorescent blue-grey / warm consumer-amber / golden hour].
- [Fill / bounce description — usually the opposite color temperature from the other side of the frame].
- Subtle rim light along the top edge of the cap brim separating Justin from background.
- [If applicable: visible cast shadows from scene elements to ground their scale and position].

MOOD: [from chosen vibe adjectives]. [Register specifier — "amused-not-alarmed" / "concerned-not-shocked" / "stern-not-stoic" — name the emotional dial position precisely]. NOT alarm-bell. NOT cartoonish. NOT [other emotional defaults the model might reach for given the dispatch concept].

[WARDROBE & STYLE CONSISTENCY DIRECTIVE]

ASPECT RATIO: 16:9 (1280×720).

COMPOSITION RULES: Center 80% of frame un-busy enough that headline text overlays cleanly center-left at ~55% canvas height, identity-block elements in top-right corner.

EXCLUDE: text, words, typography anywhere in the image (including on objects, signs, screens, or labels), watermarks, logos, captions, lettering — text will be added in post. No second human figure. No flat color blocks. No literal 50/50 vertical split.
```

---

## Variant B — Tight Close-Up Composition (prompt template)

```
[CHARACTER REFERENCE INSTRUCTION above]
REFERENCE IMAGE TO ATTACH: <picked Variant B filename>

CRITICAL EXPRESSION DIRECTIVE — match the chosen ref's expression precisely. The model's default is to soften any specific expression toward "neutral friendly." Forbid that default explicitly:
- For `headshot-smirk.png`: "closed-lipped half-smile, one eyebrow slightly raised, sardonic-amused register. Do NOT render a warm friendly smile with teeth showing. The smirk is restrained, knowing, slightly conspiratorial — not friendly."
- For `headshot-concerned.png`: "furrowed brow, slight mouth downturn, alert eyes. Do NOT render a stoic or neutral expression — the concern must read."
- For `headshot-shocked.png`: "open mouth, raised brows, wide eyes. Do NOT soften toward 'surprised' or 'pleasantly startled' — this is genuine incredulity."
- For `headshot-stern.png`: "brow lowered, mouth tight, no smile. Do NOT add any warmth or hint of amusement — this is the unimpressed register."
- For `headshot-worried.png`: "brow furrowed, eyes slightly pleading, mouth slightly parted in worry. Do NOT default to neutral concern — the worry must register."
- For `headshot-neutral-forward.png`: "composed, direct gaze, neutral mouth (no smile, no frown). Do NOT default to friendly micro-smile."
- For `headshot-neutral-raised-eyebrow.png`: "neutral mouth, one eyebrow visibly raised in 'really?' register. Do NOT smooth the eyebrow back to symmetric."
- For other refs: name the expression's specific facial features and explicitly forbid the model's softening direction.

STYLE REGISTER: Editorial magazine illustration portrait in the visual register of Brian Stauffer, Yann Legendre, or Tom Bachtell. Soft semi-realistic shading with visible illustrative brushwork, paper texture grain across the canvas. NOT flat vector. NOT photoreal. NOT explainer-cartoon.

COMPOSITION:
- Close-up of the character from the upper-chest up (or face-fills-frame if the chosen ref is `headshot-extreme-closeup.png`).
- Head right-aligned, occupying the right 35-45% of the frame width. Face turned [direction — slightly toward camera-left / slightly toward camera-right / dead-center — match the chosen ref], gaze [direction — toward camera / off-camera left / downward / etc., matching the chosen ref].
- The collar of the olive-grey t-shirt is visible at the bottom of the frame; the cap fills the upper portion of the head.
- Generous negative space on the LEFT 50% of the frame reserved for headline overlay.

BACKGROUND: [Background mood description — derived from chosen vibe + dispatch concept, but ALWAYS heavily blurred and color-field only]. The transition is GRADUAL and DIFFUSE — NO hard vertical seam, NO recognizable architectural shapes, NO blurred buildings, NO blurred scene context of any kind. Background blur intensity is high enough that any underlying shapes are completely unrecognizable. Mood color field ONLY — think a heavily gaussian-blurred field of pure color, not a blurred scene with shapes.

LIGHTING:
- Key light from [direction — typically camera-right] warming the [side] of the face.
- Cool fill from [opposite direction] bringing the [other side] of the face into subtle shadow.
- Subtle rim light along the top edge of the cap brim separating the figure from background.
- Editorial portrait register — soft but DIRECTIONAL, not flat.

MOOD: [from chosen vibe adjectives]. [Register specifier matching the chosen ref's expression — e.g., "sardonic, restrained, 'let me show you something'"]. NOT alarm-bell. NOT warm-friendly. NOT [other emotional defaults the model might reach for].

[WARDROBE & STYLE CONSISTENCY DIRECTIVE]

ASPECT RATIO: 16:9 (1280×720).

COMPOSITION RULES: Face right-aligned, occupying right 35-45% of frame width. Left 50% as soft-blurred negative-space color field for overlay. Center 80% un-busy.

EXCLUDE: text, words, typography, signs, watermarks, logos, captions, lettering. No full-body shots. No multiple figures. No hard color block backgrounds. No teeth-visible smile UNLESS the chosen ref is `headshot-big-smile.png` or `headshot-big-smile-eyes-closed.png`. No specific architectural or scene context in the background blur.
```

---

## Variant A vs B — Conceptual Differentiation

Both variants share the same chosen vibe, the same chosen headline (which the prompt does *not* render — text is overlay-only, see SKILL.md §8), and the same character source library. They differ in framing and figure emphasis:

- **Variant A (wide editorial):** figure is part of a larger scene. Use a `fullbody-*.png`. Scene elements occupy 40–60% of the frame. Figure is contextualized within the dispatch's subject matter — standing in front of a chart, gesturing at a leaked document, looking up at a distant authority figure. The figure tells you whose viewpoint this is; the scene tells you what the piece is about.
- **Variant B (tight close-up):** figure dominates the frame. Use a `headshot-*.png` or `bust-*.png`. The scene is reduced to a backdrop or mood field — color, lighting, suggestion — not specific subject matter. The expression is doing the rhetorical work; the viewer is reading the figure's reaction *to* the dispatch, not the dispatch itself.

---

## Per-Tool Quirks

### Freepik / Pikaso / Mystic

- Paste the prompt into the image-generation field.
- Attach the picked reference image (Variant A's full-body ref or Variant B's headshot ref) via the "character reference" or "Pikaso character" feature.
- Set aspect to 16:9.

### Nano Banana 2 / Gemini Imagen

- Upload the picked reference image first, then paste the prompt.
- Gemini handles "use the attached reference image as character reference" natively.
- If a fixed seed is configured for the user's character (e.g., `8472`), append `Seed: <value>` to the prompt. The skill reads the seed from `~/.config/tcn/illustrated-justin-seed` if present, else omits the seed line.

### Midjourney

- Use `--cref <reference-image-URL>` at the end of the prompt, with the URL pointing to the picked reference.
- Add `--ar 16:9` for aspect, `--cw 100` for full character weight.
- The character-reference instruction at the start of the prompt becomes redundant with `--cref`; either keep both or trim to `--cref` only.
- Caveat: `--cref` accepts one ref per generation. The skill picks the single best ref per variant.

### Flux Kontext / image-to-image

- Set the picked reference image as the input image.
- Set denoise strength to ~0.7 so character is preserved but scene is regenerated.
- The character-reference instruction can be trimmed since Kontext's image-to-image flow handles character preservation automatically; keep the wardrobe/style directive as the prompt body.

---

## How the Skill Uses This File

At process step 8 (compose the two prompt variants) in reference-image mode, the skill:

1. Loads this file.
2. Verifies the refs directory exists and `headshot-neutral-forward.png` is present (halt with setup note if not).
3. Reads the cold-open and dispatch concept from the narration or transcript.
4. Uses the vibe-adjective sniff test plus the cold-open's specific phrasing to interpret tone (interpretive — no strict table).
5. Picks one headshot/bust file for Variant B and one fullbody file for Variant A. Checks variant coherence (no tonal mismatches).
6. If a picked file is missing, falls back to the neutral default and notes the substitution in the artifact header.
7. Substitutes the picked filenames into both variant prompts.
8. Fills in the bracketed scene/lighting/mood slots from the dispatch concept + chosen vibe.
9. Writes both variant prompts into the artifact file, with a one-line note on which per-tool quirks block applies (the skill doesn't know which tool the user prefers — it includes all four blocks in the artifact and lets the user pick).
10. Suppresses Gate 3 (no opt-in render in this mode — the skill doesn't know which tool the user is using).
