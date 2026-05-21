# Flux Prompt Template (LoRA mode)

Active when a Flux LoRA URL is found via the §4.2 three-source lookup. Prompts produced in this mode are formatted for fal MCP's `mcp__fal-ai__run_model` call against the Flux.1 [dev] endpoint with a LoRA URL parameter.

## Variant A — wide editorial composition

```
[CHARACTER SUBJECT: illustrated character, wearing casual editorial styling, set in [SCENE DESCRIPTION pulled from dispatch concept + chosen vibe]. Wide framing, character occupies the right third of the frame. Mid-shot from the waist up. Editorial magazine-style composition with negative space on the left for text overlay.

LIGHTING: [from chosen vibe — e.g. "dramatic side-light from screen glow", "moody overcast natural", "noir single-source from off-camera"].

MOOD: [from chosen vibe adjectives].

COMPOSITION RULES: 1280×720 aspect ratio. Center 80% of frame must remain un-busy — no important detail in the corners or far edges. Negative space concentrated on the LEFT half (~768 px) for headline overlay.

NO TEXT in the image. No words, no signs, no readable typography. The text will be composited separately.

NEGATIVE PROMPT: text, words, typography, signs, watermarks, logos, captions, lettering, busy backgrounds, distracting clutter, multiple figures, low contrast.
```

**LoRA URL:** `{{ILLUSTRATED_JUSTIN_LORA_URL}}`
**LoRA strength:** 0.85
**Aspect ratio:** 16:9 (1280×720)
**Steps:** 28
**Guidance:** 3.5
**Sampler:** dpmpp_2m

## Variant B — tight close-up composition

```
[CHARACTER SUBJECT: illustrated character, close-up framing from the shoulders up, gaze [direction — toward camera / off-camera left / etc.]. Strong figure emphasis. Background [from dispatch concept] is soft-focused or partially abstract.

LIGHTING: [from chosen vibe].

MOOD: [from chosen vibe adjectives, slightly more intimate register than Variant A].

COMPOSITION RULES: 1280×720 aspect ratio. Character's face occupies the right ~40% of the frame. Center 80% must remain un-busy enough that a headline can sit at center-left without competing. Negative space on the LEFT third for text overlay.

NO TEXT in the image. No words, no signs.

NEGATIVE PROMPT: text, words, typography, signs, watermarks, logos, captions, lettering, busy backgrounds, multiple figures, low contrast, full-body shots, distant figures.
```

**LoRA URL:** `{{ILLUSTRATED_JUSTIN_LORA_URL}}`
**LoRA strength:** 0.85
**Aspect ratio:** 16:9 (1280×720)
**Steps:** 28
**Guidance:** 3.5
**Sampler:** dpmpp_2m

## fal MCP invocation shape

For the opt-in render step (Gate 3, process step 11), the skill calls:

```
mcp__fal-ai__run_model
  endpoint: fal-ai/flux-lora
  parameters:
    prompt: <the full prompt text above with [bracketed slots] filled in>
    image_size: landscape_16_9
    num_inference_steps: 28
    guidance_scale: 3.5
    loras:
      - path: <LoRA URL from §4.2 lookup>
        scale: 0.85
    num_images: 1
    enable_safety_checker: false
    output_format: png
```

One call per variant (two calls total per render gate accept).

## Negative-prompt patterns to include

- Text-rendering blockers: "text, words, typography, signs, watermarks, logos, captions, lettering"
- Composition blockers: "busy backgrounds, distracting clutter, multiple figures, low contrast"
- Variant-specific (B only): "full-body shots, distant figures"

## How the skill uses this file

At process step 8 (compose the two prompt variants) in LoRA mode, the skill:

1. Loads this file.
2. Fills in the bracketed slots from the dispatch concept + chosen vibe.
3. Writes two variant prompts into the artifact file.
4. At process step 11 (render gate), if the user accepts, invokes fal MCP per variant using the parameters above.
