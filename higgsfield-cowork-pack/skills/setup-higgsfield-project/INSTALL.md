# Install / Use Guide

## What this skill does

Generates a tailored CLAUDE.md for your Higgsfield content project. One file that locks in your brand voice, default character, output folders, and model preferences so every other skill in the pack runs on autopilot.

## Why this is the most important skill in the pack

The CLAUDE.md is the secret to making AI workflows feel custom. Without it, every skill runs with vanilla defaults and asks you the same setup questions every time. With it, the pack knows YOU — your voice, your folders, your character, your vibe — and only asks about the thing that changes per generation.

This is the single highest-leverage move in the entire pack. Run this skill first. Once.

## What you need

- **Claude Cowork** desktop app
- A **project folder** on your computer where you'll keep this work
- About **2 minutes** to answer 7 questions

## Install

The skill is part of the `higgsfield-cowork-pack` plugin. Install the plugin and `/setup-higgsfield-project` shows up automatically.

## Use

In Cowork, type:
```
/setup-higgsfield-project
```
or
```
set up my project
```

Claude will ask you:
1. Project name
2. What you're making (ads / carousels / both / experimenting)
3. Brand voice (4 presets + free-text override)
4. Default platform (TikTok / Instagram / Shorts / multi)
5. Default character (saved slug or "later")
6. Brand accent color
7. Output folder structure

Then writes a CLAUDE.md to your project root.

## Where to find your output

```
<your-project-folder>/
  └── CLAUDE.md
```

Open it. Read it. If anything looks wrong, edit the file directly. The next skill that runs in this folder reads from it.

## What changes after setup

Before:
```
You: /product-to-ad
Claude: Which product? What buyer? What vibe? What CTA? What aspect ratio?
        What output folder? Should I use a saved character?...
```

After:
```
You: /product-to-ad — here's the product image
Claude: Got it. Running with Maya, sarcastic vibe, link-in-bio CTA,
        9:16, outputs/ads/. Sound right?
You: yep
[ad renders]
```

## Re-running

You can re-run `/setup-higgsfield-project` anytime to update defaults. Claude shows you the current values and only asks about what you want to change.

Common reasons to re-run:
- You saved a better default character
- Your brand voice shifted
- You added a new platform target
- You renamed the project

## Common issues

**"It overwrote my existing CLAUDE.md."**
The skill is supposed to ask before overwriting. If it didn't, you can recover from the previous version (most editors keep undo history). To prevent: always say "no" or "merge" when asked about the existing file.

**"The default character it suggested doesn't exist yet."**
You have to save the character first via `/character-locker`. Run that, then re-run setup with the saved name in step 5.

**"My brand voice doesn't match any of the 4 presets."**
Use the free-text override in question 3. Anything you write there gets injected verbatim into the voice section of CLAUDE.md.

## Pairs well with

- `/character-locker` — natural follow-up. Set up project, then save your first character.
- All other skills in the pack — every single one reads CLAUDE.md before asking anything.

## Cost

Zero. This skill writes a local file. No Higgsfield credits, no API calls, no subscription.

## What goes in a typical CLAUDE.md

After running setup, your file looks like this:

```markdown
# Higgsfield Content Project — [Your Name]
Generated: 2026-04-29

## Goal
Running daily UGC ads on TikTok and Instagram for an e-commerce brand.

## Defaults
- Aspect ratio: 9:16
- Resolution: 2k
- Default character: Maya
- Default vibe: sarcastic-funny
- Brand accent: #DA7756

## Voice
- Sarcastic-witty
- 5th-grade reading level
- No em dashes ever

## Output structure
- Ads → outputs/ads/<product-slug>/
- Carousels → outputs/carousels/<topic-slug>/
- Overnight runs → outputs/morning/<date>/

## Models pinned
- Actor: SOUL
- Scene: Nano Banana Pro
- Video: Higgsfield Video
- Carousels: Nano Banana Pro

## Hard rules
- Never auto-post
- Never use em dashes
- Always 5th-grade reading level
```

That's the whole magic. Read it once. Update it as your brand evolves. Forget about defaults forever.
