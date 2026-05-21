# Reference-Image Prompt Template (default mode)

Active when no Flux LoRA URL is found. Prompts produced in this mode are model-agnostic — designed to work in Freepik, Nano Banana Pro / Gemini, Midjourney (with `--cref`), Flux Kontext (image-to-image), or any other tool that accepts a character reference image.

## Reference-image library

The skill expects a directory of tone-mapped illustrated-Justin reference images, sourced one-time from Freepik (or wherever the canonical character is generated). The directory location comes from the SKILL.md §4.2 inputs lookup (default `~/Pictures/tcn-justin-references/`).

### Expected filenames (named-by-purpose convention)

The skill references files by their intent, not arbitrary names. The following filenames are the canonical vocabulary — the skill looks for these specific files based on dispatch tone + variant framing.

**Headshots (Variant B — close-up):**
- `headshot-neutral-forward.png` — default; eye-line forward; calm/explanatory tone
- `headshot-smirk.png` — sardonic register; dry-twist dispatches
- `headshot-concerned.png` — cautionary register; "this is worse than you think" dispatches

**Full-body (Variant A — wide editorial):**
- `fullbody-standing-neutral.png` — default; arms-relaxed; explanatory tone
- `fullbody-pointing-right.png` — directive register; "look at this" / accusation dispatches
- `fullbody-shrug-open-arms.png` — sardonic register; "how is this real" dispatches

Add more files to the library as future dispatch tones emerge — extend the vocabulary, don't rename existing files.

## Tone-to-file mapping

The skill picks the per-variant reference image from this table, based on the dispatch tone (derived from the chosen vibe at Gate 1).

| Dispatch tone | Variant A (wide) ref | Variant B (close-up) ref |
|---|---|---|
| Neutral / explanatory | `fullbody-standing-neutral.png` | `headshot-neutral-forward.png` |
| Sardonic / dry-twist | `fullbody-shrug-open-arms.png` | `headshot-smirk.png` |
| Concerned / cautionary | `fullbody-standing-neutral.png` | `headshot-concerned.png` |
| Directive / "look at this" | `fullbody-pointing-right.png` | `headshot-neutral-forward.png` |

Tone is derived from the chosen vibe adjectives:
- "moody", "noir", "conspiracy-thriller", "quiet-dread" → Concerned / cautionary
- "investigative", "documentary", "analytical", "archival" → Neutral / explanatory
- "vaporwave-tech", "apocalyptic-tech", "corporate-dystopian" → Sardonic / dry-twist
- "dramatic" or "cinematic" alone (no other strong adjective) → ambiguous; default Neutral

If tone is ambiguous, default to Neutral.

## Fallback behavior

- **Missing directory entirely, OR missing `headshot-neutral-forward.png`:** halt with a setup note (where to place files, the named-by-purpose vocabulary above, link to this mapping table). The neutral headshot is the irreducible-minimum file.
- **Missing specific tone-mapped ref but neutral default exists:** fall back silently to `headshot-neutral-forward.png` (for Variant B) or `fullbody-standing-neutral.png` (for Variant A). Note the substitution in the artifact's header so the user knows which expected file was missing.

## Character reference instruction (every prompt)

Every prompt includes:

```
Use the attached reference image as the character reference. Match the character's facial features, hair, and styling exactly. Place the same character into a new scene as described below.
```

The skill substitutes the picked filename into the prompt's "attach this file" instruction so the user knows which specific ref to upload alongside the prompt.

## Variant A — wide editorial composition

```
[CHARACTER REFERENCE INSTRUCTION from above]
[REFERENCE IMAGE TO ATTACH: <picked Variant A filename from "Tone-to-file mapping">]

SCENE: [scene description pulled from dispatch concept + chosen vibe]. Wide editorial framing. The character occupies the right third of the frame, mid-shot from the waist up. Magazine-style composition with significant negative space on the LEFT half of the frame for text overlay.

LIGHTING: [from chosen vibe].

MOOD: [from chosen vibe adjectives].

ASPECT RATIO: 16:9 (1280×720).

COMPOSITION RULES: keep the center 80% of the frame un-busy enough that a text headline can overlay center-left without competing with image detail.

EXCLUDE: text, words, typography, signs, watermarks, logos, captions, lettering. No readable characters anywhere in the image — text will be added in post.
```

## Variant B — tight close-up composition

```
[CHARACTER REFERENCE INSTRUCTION from above]
[REFERENCE IMAGE TO ATTACH: <picked Variant B filename from "Tone-to-file mapping">]

SCENE: [scene description, tighter framing]. Close-up of the character from the shoulders up. Gaze [direction — toward camera / off-camera left / etc.]. Background [from dispatch concept] is soft-focused or partially abstract.

LIGHTING: [from chosen vibe].

MOOD: [from chosen vibe adjectives, slightly more intimate register than Variant A].

ASPECT RATIO: 16:9 (1280×720).

COMPOSITION RULES: character's face occupies the right ~40% of the frame. Negative space on the LEFT third for text overlay. Keep center 80% un-busy.

EXCLUDE: text, words, typography, signs, watermarks, logos, captions, lettering. No full-body shots. No multiple figures.
```

## Per-tool quirks

### Freepik / Pikaso
- Paste the prompt into the image-generation field.
- Attach the picked reference image (Variant A's full-body ref or Variant B's headshot ref) via the "character reference" or "Pikaso character" feature.
- Set aspect to 16:9.

### Nano Banana Pro / Gemini
- Upload the picked reference image first, then paste the prompt.
- Gemini handles "use the attached reference image as character reference" natively.

### Midjourney
- Use `--cref [reference image URL]` at the end of the prompt, with the URL pointing to the picked reference.
- Add `--ar 16:9` for aspect.
- The character-reference instruction at the start of the prompt becomes redundant with `--cref`; you can either keep both or trim to `--cref` only.

### Flux Kontext / image-to-image
- Set the picked reference image as the input image.
- Set denoise strength to ~0.7 so character is preserved but scene is regenerated.

## How the skill uses this file

At process step 8 (compose the two prompt variants) in reference-image mode, the skill:

1. Loads this file.
2. Verifies the refs directory exists and `headshot-neutral-forward.png` is present (halt with setup note if not).
3. Derives the dispatch tone from the chosen vibe adjectives using the rules in "Tone-to-file mapping".
4. Picks the per-variant reference filenames from the mapping table.
5. If a specific tone-mapped file is missing, falls back to the neutral default and notes the substitution in the artifact header.
6. Substitutes the filenames into both variant prompts.
7. Fills in the bracketed scene/lighting/mood slots from the dispatch concept + chosen vibe.
8. Writes both variant prompts into the artifact file, with the "Per-tool quirks" section appended as a tip block.
9. Suppresses Gate 3 (no opt-in render in this mode — the skill doesn't know which tool the user is using).
