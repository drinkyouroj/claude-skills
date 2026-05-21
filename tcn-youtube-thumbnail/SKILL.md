---
name: tcn-youtube-thumbnail
description: "Step 5 of the Civic Node YouTube production workflow — produces two Flux image-prompt variants for the YouTube thumbnail (with illustrated-Justin via reference image or trained Flux LoRA) plus a text overlay spec for compositing in Figma/Canva/Photoshop. Pre- or post-record. Invoke when the user says 'build the thumbnail', 'thumbnail prompts for this dispatch', 'make the thumbnail', 'design the thumbnail for №NNN', 'create thumbnail prompts', or has approved a youtube-narration.md or recorded transcript and wants thumbnails. Does NOT generate the article, narration, slideshow, title, or description (those are separate skills), and does NOT composite the final image (that's Figma/Canva/Photoshop post-processing)."
---

# The Civic Node — YouTube Thumbnail (Step 5 of the YouTube Production Workflow)

## What This Skill Does

Produces YouTube thumbnail artifacts for a TCN dispatch: two Flux image-prompt variants (one wide-editorial, one tight close-up — both same character, vibe, and chosen headline) plus a text overlay spec. The skill is a prompt-builder modeled on `ai-image-prompts-skill`: it queries a curated library for thumbnail-shaped vibe references, lets the user pick one, drafts thumbnail headline candidates, and emits two Flux prompts plus the overlay spec. It runs in **dual-mode** — reference-image mode by default, LoRA mode when a trained Flux LoRA URL is configured. Output is CTR-first; the illustrated scene is not brand-restricted, but the text overlay carries TCN identity markers (mark, dispatch serial, Courier Prime, restricted palette). See spec §1.

---

## Why a Prompt-Builder Plus Optional Render

The skill matches the slideshow-skill pattern: it does not own image generation. It composes the precise prompt and overlay spec, and the user (or, in LoRA mode, fal MCP via an opt-in gate) renders the image. In LoRA mode, after writing the artifact, the skill asks once: "Render both variants now via fal? Cost ~$0.10 total." Default is to ask, not skip. In reference-image mode, the render gate is suppressed because the skill cannot know which downstream tool (Freepik, Nano Banana Pro, Midjourney `--cref`, Flux Kontext) the user will paste the prompt into. See spec §3.6.

---

## Position in the YouTube Workflow

```
Article (tcn-article-builder)
    ↓
tcn-youtube-narration  [Step 1]
    ↓
tcn-youtube-slideshow  [Step 2]
    ↓
┌─── RECORDING ───┐
    ↓
tcn-youtube-title         [Step 3 — planned]
tcn-youtube-description   [Step 4 — planned]
tcn-youtube-thumbnail     [Step 5 — this skill]
```

Recording is the cleavage point between upstream skills (which consume article prose) and downstream packaging skills (which consume the recorded transcript). This skill is the only packaging skill that can also **run pre-record**, against the narration's cold-open candidate, for early concepting. Recommended production order: run pre-record for ideation, re-run post-record with the actual transcript for the final thumbnail.

---

## Inputs and Outputs

### Required input

- **Path to a narration file (`youtube-narration.md`) OR a recorded transcript.** The skill auto-detects: it looks for both in the supplied directory; transcript wins if both are present. If the user pastes contents directly, save to a temp file and proceed. Halt with an explicit message and example path if neither is found.

### Optional inputs

- **Illustrated-Justin LoRA URL.** Lookup order, first hit wins:
  1. Explicit invocation argument (e.g., `--lora-url <url>` or natural-language equivalent)
  2. `~/.config/tcn/illustrated-justin-lora.url` (one-line file containing the URL)
  3. `TCN_ILLUSTRATED_JUSTIN_LORA_URL` environment variable

  Absence of all three triggers reference-image mode.

- **Illustrated-Justin reference image path.** Default `~/Documents/illustrated-justin-ref.png`. Used only in reference-image mode. If missing, the produced prompts contain a `{{CHARACTER_REFERENCE_IMAGE}}` placeholder and a one-line setup note.
- **Steering** — free-text guidance like "more daytime", "wide shot, not close-up", "lean apocalyptic-tech vibe", "no faces in this one".
- **Override vibe** — user names a library prompt slug or category to skip Gate 1.
- **Override headline** — user supplies the thumbnail headline directly to skip Gate 2.

### Primary output artifact

- **File:** `workspace/drafts/<slug>/youtube-thumbnail.md`
- **Structure:**

```markdown
# Thumbnail prompts — TCN Dispatch №NNN

**Mode:** lora | reference-image
**Generated:** YYYY-MM-DD
**Vibe reference:** <library prompt name + URL, or "user steering only">
**Chosen headline:** "<3–6 word headline>"

---

## Variant A — wide editorial composition
[Full Flux prompt or model-agnostic reference-image prompt]

## Variant B — tight close-up composition
[Full Flux prompt or model-agnostic reference-image prompt]

---

## Text overlay spec
[Full overlay specification — see §8]
```

### Optional rendered outputs (LoRA mode only)

If the user accepts the render gate, two PNGs are saved alongside the artifact, both at 1280×720 via `mcp__fal-ai__run_model` against a Flux.1 [dev] endpoint with the LoRA URL parameter:

- `workspace/drafts/<slug>/thumbnail-variant-a.png`
- `workspace/drafts/<slug>/thumbnail-variant-b.png`

See spec §4–§5.

---

## Generation Modes

The skill ships dual-mode. Same artifact shape in both modes — only the prompt format and the render gate differ.

| Concern | Reference-image mode | LoRA mode |
|---|---|---|
| Activation | No LoRA URL found in any of the three sources | LoRA URL found in any source |
| Character source in prompt | Inline reference to `illustrated-justin-ref.png` path | Inline LoRA URL parameter |
| Prompt format | Model-agnostic — "use the attached reference image as character reference, match facial features and styling" | Flux-specific — formatted for fal MCP's `run_model` schema with Flux.1 [dev] endpoint |
| Render assist | None — user pastes prompt into their image-gen tool of choice | Opt-in: skill offers to call fal MCP and save PNGs |
| Output file header | `**Mode:** reference-image` | `**Mode:** lora` |
| Mobile safe-zone directive | Identical | Identical |
| Aspect ratio | 1280×720 | 1280×720 |
| Text overlay spec | Identical | Identical |

See spec §7.

---

## The Process

### 1. Read narration or transcript

Auto-detect in the supplied directory: transcript wins if both exist. Halt with an explicit message and example path if neither is found.

### 2. Detect generation mode

Run the LoRA-URL lookup (invocation argument → `~/.config/tcn/illustrated-justin-lora.url` → `TCN_ILLUSTRATED_JUSTIN_LORA_URL` env var). Set `mode = "lora"` or `mode = "reference-image"`. Log the chosen mode to the user in one line.

### 3. Extract dispatch metadata

Pull the dispatch number from the narration's title block (or the `<slug>` directory naming convention if reading a raw transcript). Pull the cold-open candidate from the narration's Script Notes footer, or the recorded cold-open words from the transcript's first ~30 seconds. If the dispatch number is missing from both sources, halt and ask the user to confirm. Do not guess.

### 4. Compose the library query

Build a TCN-flavored search string from the dispatch concept. Pattern: "illustrated editorial YouTube thumbnail, [dispatch subject in 3–6 words], dramatic composition, character-driven, magazine style, mid-shot or close-up." Full query patterns and what to avoid live in `references/vibe-query-templates.md`.

### 5. GATE 1 — Vibe pick

Invoke `ai-image-prompts-skill` via the Skill tool with the composed query. It returns 2–3 candidate prompts with sample images. Present:

> Pick a vibe: A, B, or C. Or 'try again' for new options. Or 'skip' to compose without a library reference.

Wait for response. If the user provided an override vibe at invocation, skip this gate entirely. If the library lookup returns nothing usable, skip the gate silently, compose without a vibe reference, and note this in the artifact header.

### 6. Draft 3 thumbnail headline candidates

Distill from the cold-open and dispatch concept per §9 below: drafting inputs (§9.1), acceptance criteria (§9.2), pattern library (§9.3), retry behavior (§9.4), and Gate 2 display format (§9.5). Each candidate is 3–6 words and must pass §9.2 before being surfaced.

### 7. GATE 2 — Headline pick

Present:

> Pick a headline: 1, 2, or 3. Or 'try again' for new options. Or paste your own.

Wait for response. If an override headline was supplied at invocation, skip this gate.

### 8. Compose the two prompt variants

Both variants share the chosen vibe, chosen character source, and chosen headline (which the prompts do *not* render — text is overlay-only). They differ only in composition: Variant A = wide editorial framing; Variant B = tighter close-up with stronger figure emphasis. Each prompt:

- Includes the illustrated-Justin character (via LoRA URL or reference image path, mode-dependent).
- Names the dispatch subject and the chosen vibe directive.
- Specifies 1280×720 aspect.
- Instructs the model to keep the center ~80% of the frame un-busy (mobile safe zone for text overlay).
- Excludes any in-image text — no rendered text at all.

Full Flux-mode prompt template lives in `references/flux-prompt-template.md`. Full reference-image-mode template lives in `references/reference-image-prompt-template.md`.

### 9. Compose the text overlay spec

Specifies the chosen headline + the corner identity block (DISPATCH №NNN + mark.svg), with typography, positioning, and color directives sufficient for Figma/Canva/Photoshop compositing. See §8 below.

### 10. Write the artifact file

Write `workspace/drafts/<slug>/youtube-thumbnail.md` with mode header, both prompts, and overlay spec.

### 11. GATE 3 — Render gate (LoRA mode only)

Gate 3 runs only in LoRA mode. Ask:

> Render both variants now via fal? Cost ~$0.10 total. yes / no / skip

On **yes**: call `mcp__fal-ai__run_model` for each variant with the Flux.1 [dev] endpoint + LoRA URL parameter. Save PNGs (§5.2 above). Report paths. On **no/skip**: artifact-only output; note in the message that the user can render manually later. **In reference-image mode Gate 3 is suppressed.** If fal MCP is not installed but the user has a LoRA URL, produce the artifact in LoRA mode and suppress the render gate with a one-line note ("fal MCP not detected — skipping render gate; run prompts manually").

### 12. Final gate

Present:

> Thumbnail artifacts ready at `<path>`. Approve, redirect (e.g., 'tighter vibe', 'redo headline', 'swap Variant B to wide shot', 'lower contrast'), or cancel?

Wait for response. Redirects re-enter only the affected step(s).

---

## Thumbnail Headline Distillation

Thumbnail headlines are a distinct content genre from article headlines, social hooks, or the cold-open. 3–6 words must set up a curiosity gap, anchor a concrete specific, and carry TCN voice in a fraction of a second of scrolling. See spec §9.

### Drafting inputs (§9.1)

When drafting candidates at process step 6, the skill has:

- The cold-open candidate (or recorded cold-open) — the dispatch's most punchable line.
- The dispatch concept — the broader article subject, extracted from the narration's structure.
- The dispatch number, slug, and any user-supplied steering.
- The full contents of `references/thumbnail-headline-patterns.md` (loaded into context at drafting time as the source of truth for voice and structural patterns).

### Acceptance criteria (every candidate must pass)

A candidate is rejected silently and re-drafted if it fails any of:

- **Word count.** 3–6 words inclusive. Hyphenated compounds count as one word. Contractions count as one word. Numbers count as one word regardless of digit count.
- **No all-caps words.** Sentence case only. Genuine acronyms (FCC, ATC, FAA, DAO) are exceptions.
- **No exclamation points.** Question marks allowed sparingly, only when load-bearing for a curiosity gap.
- **No banned hype adjectives.** Explicit banned list in the patterns reference file. Initial set: SHOCKING, AMAZING, INSANE, EXPOSED, REVEALED, UNBELIEVABLE, MASSIVE, ULTIMATE, EPIC, INCREDIBLE, MIND-BLOWING, GAME-CHANGING. Case-insensitive match.
- **No banned clickbait templates.** "This One Trick…", "What They Don't Want…", "You Won't Believe…", "Here's Why…", "The Truth About…", and other generic-YouTube structures.
- **Concrete specific when supported.** If the cold-open contains a number, place name, dollar amount, year, or proper noun, at least one of the three candidates must use it. (Not all three — variety is good.)
- **Anti-AI-tell scan.** Reject candidates containing em-dashes, "delve", "tapestry", "navigate the landscape", or any token from the `tcn-text-humanizer` skill's tell list (referenced, not duplicated, in the patterns file).

The banned-word and banned-template lists are maintained in `references/thumbnail-headline-patterns.md`, not in this skill, so they can be extended without skill-code changes.

### Pattern library (§9.3)

The substantive guidance for candidate drafting lives in `references/thumbnail-headline-patterns.md`. It covers proven structural patterns (Concrete Anchor + Twist, Implied Stakes, Direct Address, Specific Contradiction, Bare-Noun Provocation), voice anchors (sentence-case, declarative-or-curiosity-gap, sardonic, never-screaming), worked example walkthroughs for at least 2 dispatches, and an anti-pattern gallery. Read this file at drafting time.

### Retry behavior (§9.4)

If any of the 3 initially drafted candidates fails the acceptance criteria, internally re-draft the failing slot(s) up to 2 additional attempts before surfacing. If after 3 total attempts a slot still fails, surface the best-effort candidate with a one-line note ("could not satisfy [criterion]; consider redirecting"). The user always sees 3 candidates. Re-drafts are silent — the user does not see rejected attempts.

### Gate 2 display format (§9.5)

After successful drafting, the user sees:

```
Pick a thumbnail headline:

1. <Candidate 1>
   — <one-line rationale: pattern used, anchor, curiosity-gap mechanism>

2. <Candidate 2>
   — <rationale>

3. <Candidate 3>
   — <rationale>

Or 'try again' for new options. Or paste your own.
```

Rationales surface the *why* of each candidate, not just the words.

---

## TCN Identity Markers

Every thumbnail this skill produces carries these constant markers, regardless of vibe or mode:

- **The TCN mark** in the corner identity block.
- **`DISPATCH №NNN`** in the corner identity block. Zero-padded. Middle dot `·` if a sub-label is added. Mono typeface, wide-tracked, all-caps.
- **Courier Prime** as the only typeface anywhere in the overlay. Bold for the headline, regular for the dispatch serial.
- **Palette restricted to slate-400 / slate-600 / black / twilight** for all overlay text. No other colors.

The illustrated scene itself is *not* constrained to TCN brand palette — that is a deliberate CTR-first trade. Bright accents, dramatic lighting, expressive character work can all apply to the scene. The overlay carries the brand load. See spec §10.

---

## Text Overlay Specification

The overlay spec section in `youtube-thumbnail.md` contains everything needed to composite text onto the rendered image in Figma, Canva, or Photoshop:

- **Chosen headline** — Courier Prime Bold, sentence case (TCN never screams in all-caps). Default ~120 px at 1280×720 canvas, adjustable per tool. Color: slate-400 (`#557FA3`) or black (`#0D0D0F`) — the spec lists both options; recommend one based on the chosen vibe's lighting/mood ("dramatic night scene" → slate-400; "bright daytime editorial" → black). Optional 4–6 px stroke/halo for legibility on busy illustrations, user discretion at composite time. Default position: center-left, baseline at ~55% of canvas height. Stays inside the center 80% mobile safe zone.

- **Corner identity block** — `DISPATCH №NNN` in Courier Prime Regular, wide-tracked (`0.18em`), all-caps, ~24 px at 1280×720. Mark: `mark.svg` from the TCN design system, ~40 px square. Default position: top-right corner, mark above the dispatch number, both anchored to the safe-zone edge. Color: slate-400 on dark scenes, slate-600 (`#3A6A8F`) on light scenes.

- **Color tokens** — explicit references to `colors_and_type.css` values: `slate-400`, `slate-600`, `black`, `twilight`. No other colors.

- **Mobile safe-zone note** — repeated in the spec so the compositor does not forget: "All text must stay inside the center 80% of the canvas. YouTube crops mobile feed thumbnails aggressively at the edges."

Full overlay-spec template (sizing curves, edge cases, mark sizing rules) lives in `references/text-overlay-spec.md`.

---

## Failure Modes

- **No narration and no transcript found** — halt with an explicit message and an example path. Do not attempt to compose from nothing.
- **Narration malformed** (no Script Notes footer, no cold-open candidate, no title block) — halt and ask the user to either supply a cold-open candidate as steering or fix the narration upstream.
- **Library lookup returns nothing usable** — skip Gate 1 silently; compose without a vibe reference. Note this in the artifact file header.
- **fal MCP not installed but user has a LoRA URL** — produce the artifact in LoRA mode normally; suppress the render gate with a one-line note ("fal MCP not detected — skipping render gate; run prompts manually").
- **fal render fails** (timeout, credit exhausted, model unavailable) — keep the prompt artifact intact; surface the error message; suggest manual render via the prompt as-is.
- **Reference image missing in reference-image mode** — produce the artifact with `{{CHARACTER_REFERENCE_IMAGE}}` placeholder and a setup note (where to place the file, suggested filename, suggested specs).
- **Dispatch number missing from narration title block and not derivable from the slug** — halt and ask the user to confirm. Do not guess.
- **Combined / non-standard narration zones** — tolerate. The thumbnail only needs the cold-open and the overall dispatch concept, not the full slide structure.
- **User redirects at the final gate** — re-enter only the affected gate(s):
  - "tighter vibe" → re-enter Gate 1 with stronger steering
  - "redo headline" → re-enter Gate 2
  - "swap Variant B to wide shot" → re-compose Variant B only
  - "lower contrast" or other stylistic redirects → re-compose both prompts with the steering applied

---

## What This Skill Is NOT

- Not a LoRA trainer. LoRA training is a one-time user task via fal MCP (or any Flux LoRA training service). The skill assumes the URL is provided.
- Not a reference-image generator. The canonical `illustrated-justin-ref.png` is a one-time Freepik (or equivalent) session.
- Not a compositor. The skill writes the overlay spec; Figma/Canva/Photoshop composite the final image.
- Not a YouTube uploader. The skill produces the artifacts; the user uploads manually (or via a future packaging skill).
- Not a title or description generator. Those are sibling skills (`tcn-youtube-title`, `tcn-youtube-description`).
- Not an article or narration generator. Those are upstream skills.
- Not a brand-strict thumbnail. The illustrated scene is CTR-first; only the overlay anchors carry the brand load.

---

## Companion Skills

**Upstream (this skill reads from):**
- `tcn-youtube-narration` — produces the narration file the skill reads pre-record.
- Recording → transcript — produces the transcript the skill prefers post-record.

**Sibling (planned, not built today):**
- `tcn-youtube-title` — title generation, consumes the recorded transcript.
- `tcn-youtube-description` — description body, tags, chapter timestamps.

**Explicit invocation dependency:**
- `ai-image-prompts-skill` — invoked at Gate 1 for library candidates. Must be installed; if missing, the skill falls back to "no library reference" composition and notes this in the artifact header.

**Optional runtime dependency:**
- `fal-ai` MCP — required only for the opt-in render gate in LoRA mode. Absence in LoRA mode triggers a suppressed render gate with a one-line note (see Failure Modes).

**Shared design-system reference:**
- `~/Documents/The Civic Node — Design System.zip` — referenced for color tokens, `mark.svg`, and Courier Prime sizing. The skill does not parse the zip; the overlay spec names the canonical tokens.

See spec §14.

---

## Reference Files

- `references/vibe-query-templates.md` — how to compose the TCN-flavored library query from a dispatch concept. Query patterns that work, patterns to avoid, example transformations of cold-open → library query.
- `references/thumbnail-headline-patterns.md` — pattern library for §9 candidate drafting. Voice rules, banned-word list, banned clickbait template list, structural patterns with worked examples, anti-pattern gallery. The source of truth for headline drafting — the skill reads this file at drafting time. Living document.
- `references/text-overlay-spec.md` — full typography/layout/color spec for the overlay. Courier Prime sizing curves at 1280×720 and at common Figma frame sizes. Safe-zone math (center-80% rule explained). Mark sizing rules. Color tokens pulled from `colors_and_type.css`.
- `references/flux-prompt-template.md` — Flux prompt structure for LoRA mode. Composition directives for Variant A vs Variant B. Mobile-safe-zone phrasing. Negative prompt patterns. fal MCP `run_model` parameter shape.
- `references/reference-image-prompt-template.md` — model-agnostic prompt structure for reference-image mode. Phrasing that works across Freepik, Nano Banana Pro, Midjourney `--cref`, Flux Kontext. Notes on each tool's quirks.
