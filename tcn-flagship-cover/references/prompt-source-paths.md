# Prompt Source Paths — Library vs. Scratch

The skill composes the full model-ready prompt via two paths. The library path is preferred (every successful TCN cover so far was a library lookup done by hand; the skill formalizes that workflow). The scratch path is the fallback.

Both paths produce the same artifact shape. Both paths must enforce the DNA negative-prompt block and the model directives. Only the source of the structural template differs.

The path taken is recorded in the output frontmatter via `prompt_source: ai-image-prompts-skill | nano-banana-pro-prompts-recommend-skill | scratch`.

---

## Path A — Library lookup (preferred)

### Step A.1: Invoke the prompt-library skill

Try via the Skill tool, first available wins:

1. `ai-image-prompts-skill`
2. `anthropic-skills:ai-image-prompts-skill`
3. `anthropic-skills:nano-banana-pro-prompts-recommend-skill`

If none of these are available, fall through to Path B (Scratch).

### Step A.2: What to pass

Pass the **locked concept brief** — the one the user picked at step 6. Specifically:

- **Compression name** — the metaphor strategy in 3–5 words.
- **Subject** — the primary visual element, described with enough specificity that the library can match it (not "a man," but "a senior executive in a B&W three-piece suit at a conference table"; not "a wallet," but "a worn leather wallet photographed close on a dark table").
- **Secondary element** — the thing the subject relates to (the backdrop, reflection, second icon, absence).
- **Visual register** — photographic / surreal symbolic / clean technical illustration / narrative scene / editorial poster.
- **Palette direction** — what contrast carries the argument.

This is the same information the user already approved. Do not re-write it for the library invocation — pass it verbatim so the path is auditable.

### Step A.3: What you'll get back

The library returns a recommended prompt template. For TCN-shaped concepts these tend to be one of three families:

| Concept shape | Likely returned template family |
|---|---|
| Face-forward photographic (named executive, named official) | Neo-noir / editorial portrait (the $71B Bluff path — YouMind #8791) |
| Two-icon comparison (structural argument across domains) | Clean isometric (the Cheaper AI path — isometric on white background) |
| Symbolic-object-built-from-materials | Surreal symbolic / collage-illustration (the System Functioning Correctly path) |
| Photographic with reflection device | Editorial photography with embedded reflection (the Atlanta path) |
| Narrative scene in a distinct cultural idiom | Style-specific illustrated tableau (the ukiyo-e / Wrong Protagonist path) |

The skill is not required to predict which family the library will return. The library does the matching; the skill maps the concept-specific elements into whatever template comes back.

### Step A.4: Map concept elements into template variables

For each variable in the returned template, substitute the concept-specific value. Use the $71B Bluff mapping table as a worked example of how this looks:

| Template variable (Neo-Noir #8791) | $71B Bluff value |
|---|---|
| Subject | unnamed model → **Sam Altman, B&W three-piece suit** |
| Prop | gun → **fountain pen + unsigned document** |
| Setting | (default) → **long polished black conference table** |
| Backdrop | crimson red → **saturated green + cascading DRAM modules** |
| Framing | 4:5 portrait → **16:9 landscape, 1456 × 816 for Substack hero** |

The mapping is **deliberate replacement**, not "keep the template and add stuff." If the template has a "prop" slot and the concept has a different prop, the template's prop is replaced — not augmented.

### Step A.5: Append the DNA negative-prompt block

The library template will almost certainly **not** include the DNA-specific negative prompts. Always append:

```
Negative prompts:
- no embedded text in the image
- no annotation labels
- no chart titles
- no sticky-note callouts
- no document captions
- no stamped editorial words
- no documentary-scrapbook elements
- no labeled blueprints
- no cork-board / pinboard layouts
- no UPC codes, barcodes, or magazine furniture
- no multi-panel layouts (single image only)
- no encyclopedic infographic styling
```

**Single exception:** if the picked concept's metaphor *requires* real-world physical signage (the Atlanta "Welcoming City ATL GA" sign reflected in the Flock camera housing is the canonical case), then the "no embedded text" line is replaced with a positive directive naming the specific signage and treating it as a photographed element of the world, not as added annotation. Add a note in the prompt body explicitly: "the [sign] is photographed real-world signage, not an editorial overlay; it appears as a small element within the reflection."

### Step A.6: Append model directives

The 16:9 hero spec needs different phrasing per model. Apply whichever matches the user's chosen render target (or apply all if the user is undecided):

| Model | Aspect-ratio directive |
|---|---|
| **Midjourney** | append `--ar 16:9` to the prompt |
| **Nano Banana Pro** | append `--ar 16:9` |
| **DALL-E 3** | include phrase "wide landscape, 1792 × 1024" |
| **Stable Diffusion / Flux** | set width 1456, height 816 explicitly |
| **GPT Image 1.5 / Seedream 5.0** | include phrase "16:9 aspect ratio, 1456 × 816 px" |

If the user hasn't specified a model, default to including the Midjourney/Nano Banana Pro `--ar 16:9` and the explicit "1456 × 816" pixel callout — both together cover most models. Set `model: Nano Banana Pro | Flux | Midjourney` in the frontmatter as a multi-option list.

### Step A.7: Generate alt text and caption

- **Alt text:** one-sentence description of what's in the image, in the voice you'd write actual accessibility alt text. Not a tagline — a description. Pattern from $71B Bluff: *"A man in a black suit sits at a dark conference table holding a pen over an unsigned document, rendered in black and white, while green-lit memory chips cascade behind him like a collapsing market."*
- **Caption:** one-line editorial tagline. The voice you'd use to caption the cover in the Substack publishing UI. Pattern from $71B Bluff: *"One signature. No obligation. $71 billion in damage."*

### Step A.8: Record path in frontmatter

```yaml
prompt_source: ai-image-prompts-skill   # or nano-banana-pro-prompts-recommend-skill
based_on: "[returned template name + id, e.g., 'Neo-Noir Fashion Portrait with High Contrast (YouMind id: 8791)']"
```

---

## Path B — Scratch (fallback)

Use this path only when no library-recommender skill is available — Path A is preferred.

### Scratch structure (modeled on `the-71-billion-bluff-cover-prompt.md`)

```markdown
---
[full frontmatter — see references/output-frontmatter-spec.md]
---

# Cover Image Prompt: [Article Title]

## Prompt

[Full model-ready prompt. Multi-paragraph if needed. Structure:
 - paragraph 1: the main subject and primary action / pose / scene
 - paragraph 2: the secondary element / backdrop / reflection
 - paragraph 3: lighting, palette, register, style references, film grain, etc.
 - final line: aspect ratio and rendering directives]

## Alt text

[One-sentence accessibility description.]

## Caption

[One-line editorial tagline.]

## Remix notes

- [What this prompt varies from an exemplar, if relevant]
- [Specific prop / backdrop / framing choices and their rationale]
- [Core DNA preserved: the contrast, the register, the compression]
```

### What to include even in scratch composition

Even when building from scratch, **always**:

- Lead with subject specificity matching the locked concept brief.
- Name the visual register explicitly (e.g., "editorial poster," "clean isometric illustration," "photographic with reflection device").
- Name the palette and the carrying contrast.
- Include lighting direction (single hard key light, soft directional, ambient, etc. — register-dependent).
- Append the DNA negative-prompt block from Step A.5.
- Append the model directive from Step A.6.
- Write alt text and caption per Step A.7.

### What the scratch path forfeits

The library path gives you a structurally-tested prompt skeleton that the recommender knows will produce good output for that register. Scratch composition reinvents that skeleton from the article's needs. The output can be just as good, but the floor is lower — a slightly underspecified scratch prompt produces noticeably worse renders than a well-mapped library template.

This is why the skill **prefers** Path A and records the source. Over time the skill's catalog will show which prompts came from which path; that record helps surface patterns about when scratch produced equal-quality output vs. when it underperformed.

---

## The negative-prompt block — why it matters

Image generators default toward including text when the prompt mentions concepts that involve text (documents, signage, titles, charts). They also default toward documentary-scrapbook aesthetics when the prompt mentions "investigation," "report," "evidence," or "documents."

Both defaults break the DNA. Principles 1 (compression-not-evidence) and 3 (no embedded text) are the principles most frequently violated by image generators *because the user's prompt didn't explicitly forbid them*. The negative-prompt block isn't optional belt-and-suspenders. It's the operational mechanism that enforces two of the five DNA principles at the rendering stage.

If the negative-prompt block were dropped from a prompt produced by this skill, the resulting cover would have a meaningfully higher chance of failing the DNA at render time, regardless of how well the positive prompt was composed.

---

## What this file is NOT

- Not a prompt library — the curated prompt library lives in `ai-image-prompts-skill`. This file documents how to **invoke** that library, not what's in it.
- Not a model comparison — the aspect-ratio table covers rendering directives, not which model produces the best output for which register. (That comparison is a separate concern; the user picks the model.)
- Not a writing-style guide for the prompt prose — model-ready prompts are descriptive and specific; the voice of the prompt is the model's voice, not TCN's. TCN voice goes in the article and the caption, not in the prompt body.
