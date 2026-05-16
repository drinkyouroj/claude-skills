---
name: ig-carousel
description: Generate premium 4:5 Instagram carousels with a cinematic cover plus content slides that all share the same photoreal world. Use this skill when the user says "ig carousel", "instagram carousel", "make a carousel", "carousel post", "repurpose to carousel", or wants slide-based social content. This is the Higgsfield-MCP version that works inside Cowork without external API calls. Powered by Nano Banana Pro via the Higgsfield MCP.
---

# IG Carousel (Higgsfield Edition)

Cover-first cinematic carousels. Every slide lives in the same world. Built on Higgsfield Nano Banana Pro so it runs inside Cowork without any external API setup.

## What this skill does (in one breath)

1. Picks a cinematic scene that fits the topic
2. Generates the cover with `nano_banana_2`
3. Uses the cover as the style reference for every following slide
4. Saves all 6 slides to `outputs/carousels/<slug>/` and writes the caption

By the end the user has a 6-slide deck (1 cover, 4 content, 1 CTA) plus a ready-to-paste Instagram caption.

## Why this version (vs the older Gemini-direct version)

The original `ig-carousel` skill calls the Gemini API directly via a Python script. That works in Claude Code but fails inside Cowork because the sandbox cannot reach `generativelanguage.googleapis.com`. This version uses the Higgsfield MCP, which works inside Cowork.

Same visual output, same cinematic cover-first formula. Just orchestrated through MCP instead of a Python script.

## Setup the user needs

- Higgsfield MCP connected.
- About 6 to 12 Higgsfield credits per carousel (1 cover + 5 referenced slides).
- A topic. Either a free-form idea or a YouTube transcript / video to repurpose.

## Process

### Step 1: Pick the scene

The cover defines everything. Pick one cinematic scene that communicates the topic before any text is read:

| Topic family | Default scene |
|---|---|
| Learning, courses, curriculum | gothic library, leather chairs, arched windows |
| Productivity, tools, workflows | late-night architect's loft, drafting table, CRT |
| Essentials, favorites, must-haves | deserted island, palm trees, crashed plane |
| News, announcements | futuristic command center, glowing screens |
| Sleep, automation, hands-off | moonlit bedroom, midnight cityscape |
| Creator economy, content | TV studio control room, vintage broadcast desk |

Default if unsure: late-night architect's loft. Reads as professional + creative.

### Step 2: Plan the slides

Always 6 slides. Always in this order:

1. **Cover** — title in editorial serif italic + cinematic scene + CRT showing Claude + hook phrase ending in "..."
2. **What** — open journal page explaining the concept
3. **Examples** — corkboard of pinned cards showing 3-5 examples
4. **Comparison** — two journals side by side (old way vs new way)
5. **How-to** — pinned index card with the prompt or step-by-step
6. **CTA** — CRT with Claude logo glow + "Follow @aifornontechies" + Skool button

NO context slides. NO transition slides. NO "most people get this wrong" filler. The cover IS the hook. Every other slide delivers value.

### Step 3: Generate the cover

Call `mcp__8148b7eb-72e8-45e8-bb1d-864094e854c1__generate_image` with:
- `model`: `nano_banana_2`
- `aspect_ratio`: `4:5`
- `resolution`: `2k`
- `prompt`: the cinematic scene + text overlay (title + hook phrase) + footer (`@aifornontechies` left, `save for later` right)

The prompt structure should follow the template in `references/cover-prompt-template.md`.

Save the returned `job_id` — you will reuse it as the style reference for slides 2 through 6.

### Step 4: Generate slides 2 through 6

For each content slide, call `generate_image` again with:
- Same `model`, `aspect_ratio`, `resolution`
- `medias`: `[{ "role": "image", "value": "<cover-job-id>" }]`
- `prompt`: starts with "Match the cinematic cover EXACTLY..." then describes the new content element (open journal, pinned card, side-by-side journals, CRT close-up, etc.)

The slide prompts follow the templates in `references/slide-prompts.md`.

Fire all 5 in parallel (single message, multiple tool calls). They are independent and Higgsfield queues them simultaneously.

### Step 5: Wait for completion + display

After firing the 5 jobs, sleep ~40 seconds, then call `mcp__8148b7eb-72e8-45e8-bb1d-864094e854c1__job_display` with all 6 job_ids. This shows them in the Cowork UI widget so the user can see the full deck.

### Step 6: Write the caption + download urls

Save to `outputs/carousels/<slug>/`:

- `caption.txt` — Instagram caption (hook + 2-3 lines value + CTA + 5 hashtags)
- `download-urls.md` — table of slide names + Higgsfield CloudFront URLs + a one-shot curl command the user can paste into Terminal to bulk-download to the output folder

Why download-urls.md instead of saving the PNGs directly: the Cowork sandbox cannot reach Higgsfield's CloudFront URLs, so the bulk-download has to happen on the user's machine. The user pastes one command and all 6 PNGs land in the right folder.

## Output structure

```
outputs/carousels/<slug>/
  ├── caption.txt
  ├── download-urls.md
  ├── 01_cover.png            ← after user runs the curl
  ├── 02_what.png
  ├── 03_examples.png
  ├── 04_comparison.png
  ├── 05_how_to.png
  └── 06_cta.png
```

## Rules

- ALWAYS Higgsfield Nano Banana Pro (`nano_banana_2`). Never Gemini direct, never Playwright/HTML.
- ALWAYS cover first, then content slides reference the cover's job_id.
- ALWAYS 4:5 portrait, 2k resolution.
- ALWAYS warm dark tones — no cold grays, no neon, no teal/purple.
- Editorial serif italic (Playfair Display style) for headlines and accents. Monospace only when rendering code on screen.
- Salmon/orange `#DA7756` accent across all slides.
- `@aifornontechies` footer on every slide. Skool mention only on the CTA slide.
- 5th-grade reading level on viewer copy. No em dashes.
- NEVER auto-post. Ask "(1) Post now, (2) Schedule, (3) Queue to next free slot" only if the user explicitly says they want to publish.

## When NOT to use this skill

- The user wants a single static graphic — use `/explainer-graphic` or `/visual-explainer`.
- The user wants a slideshow video for YouTube — use `/slide-infographics`.
- The user wants a real PowerPoint deck — use `/pptx`.
- The user wants the Brock-stylized Claude Code Gemini-direct version — that one still exists at `.claude/skills/ig-carousel/`. This pack-version exists because the Gemini-direct version cannot run inside Cowork.
