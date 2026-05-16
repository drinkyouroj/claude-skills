# Install / Use Guide

## What this skill does

Generate a 6-slide cinematic Instagram carousel where every slide lives in the same photoreal world. Cover renders first, every other slide uses it as the style reference.

## Why this matters

Most "AI-generated carousels" look like flat templates with stock icons. This one runs on Higgsfield Nano Banana Pro and produces editorial-quality cinematic scenes (gothic library, late-night office, deserted island, command center). The cover-first style locking means slides 2 through 6 inherit the cover's lighting, palette, and atmosphere automatically. Same world, different angles.

## Why this version (vs the original Gemini-direct skill)

Brock's original `ig-carousel` skill at `.claude/skills/ig-carousel/` calls the Gemini API directly via a Python script. That works in Claude Code but fails inside Cowork because the sandbox can't reach external endpoints.

This pack version uses the Higgsfield MCP, which works inside Cowork. Same visual output, different orchestration.

If you're in Claude Code, use the original. If you're in Cowork, use this one.

## What you need

- **Claude Cowork** desktop app
- **Higgsfield MCP** connected
- A **topic** (free-form idea or YouTube transcript to repurpose)
- About **6 to 12 Higgsfield credits per carousel** (1 cover + 5 referenced slides)

## Install

The skill is part of the `higgsfield-cowork-pack` plugin. Install the plugin and `/ig-carousel` shows up automatically.

## Use

In Cowork, type:
```
/ig-carousel
```
or
```
make a carousel about X
```

Claude will ask you for:
- **Topic** (what the carousel teaches)
- **Scene** (cinematic world — pick from the menu in `references/scene-library.md`)
- **Hook** (cover phrase, ends in "...")

Claude picks the cinematic scene, generates the cover, then renders 5 content slides using the cover as the style reference.

## Where to find your output

```
outputs/carousels/<topic-slug>/
  ├── 01_cover.png
  ├── 02_what.png
  ├── 03_examples.png
  ├── 04_comparison.png
  ├── 05_how_to.png
  ├── 06_cta.png
  ├── caption.txt
  └── download-urls.md
```

## Important: the download step

The Cowork sandbox cannot reach Higgsfield's CloudFront URLs to download the PNGs to your folder automatically. Instead, the skill drops a `download-urls.md` file with a one-shot curl command. Paste it into Terminal once and all 6 PNGs land in the right place.

This is a known limitation of running through Cowork. The original Gemini-direct skill writes PNGs directly to disk because Claude Code has no sandbox restriction.

## Common issues

**"The cover style didn't carry through to the content slides."**
The skill passes the cover's job_id as the style reference for slides 2-6. If those slides drift, two possible causes:
1. Higgsfield queue restarted between cover and content (rare). Re-run.
2. The content prompts were too descriptive of a different scene. Trim the slide prompts to "match the cinematic cover EXACTLY" plus only the new element being added.

**"Text on the cover came out garbled."**
Nano Banana Pro is excellent at rendering text but not perfect. If the title text is fuzzy:
1. Reduce the number of text overlays per slide. One title + one subtitle + one hook is the max that renders reliably.
2. Specify the font weight clearly: "bold italic serif" works better than "fancy script."
3. Re-run with a shorter hook phrase.

**"Slide 6 (CTA) doesn't show the Skool button correctly."**
The CTA prompt asks for a "small ivory pill-shaped letterpress button." Sometimes Nano Banana renders it as a generic rectangle. Re-run that single slide with a tighter button description, or accept the result and overlay the button manually in Canva / Figma.

**"My topic doesn't fit any of the preset scenes."**
Pick the closest match and override with custom scene language. The skill accepts free-form scene descriptions, not just the preset library.

## Pairs well with

- `/character-locker` — for ads, not carousels (carousels don't use UGC actors)
- `/product-to-ad` — different output format, different goal
- The original Gemini-direct `ig-carousel` skill in `.claude/skills/` — same thing, different runtime

## Cost reference

- 1 cover (Nano Banana Pro, 4:5, 2k): ~1 credit
- 5 content slides (Nano Banana Pro, with cover as ref): ~1 credit each = 5 credits
- Total per carousel: 6 credits minimum, 12 if you re-roll any slides

The Higgsfield Starter plan covers ~12 to 25 carousels per month.

## Privacy note

Topic and slide content stay local until you post the carousel. Nothing is uploaded except the rendering jobs to Higgsfield (which respects their account-private storage policy).
