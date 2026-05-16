---
name: setup-higgsfield-project
description: Generate a tailored CLAUDE.md for a Higgsfield content workflow. Locks in brand voice, default character, output folders, model preferences, and aspect ratios so every future generation in this project follows them automatically without you re-specifying. Use this skill when the user says "setup higgsfield", "create CLAUDE.md", "set up my project", "lock my defaults", "configure my project", "first-time setup", "project init", or wants a one-time setup so the rest of the pack runs on autopilot.
---

# Setup Higgsfield Project

The single highest-leverage move you can make before running any other skill in the pack. Spend 90 seconds answering questions. Get back a CLAUDE.md that locks every default in for the entire project.

## Why this matters

Without a CLAUDE.md, every time you run `/product-to-ad` or any other skill, Cowork has to ask you the same questions: aspect ratio, vibe, default character, output path, brand voice. Most of those answers don't change run-to-run. They're project-level, not ad-level.

A project CLAUDE.md tells Cowork "for everything in this folder, here are the answers." Now `/product-to-ad` only asks about THIS product, not the whole brand.

## What this skill does (in one breath)

1. Asks you 7 questions about your project, brand, and defaults
2. Generates a tailored CLAUDE.md
3. Saves it to the project root (or wherever you specify)
4. Confirms with the user and offers to chain into the first ad

## What you need

- **Claude Cowork** desktop app
- **Higgsfield MCP** connected (recommended but not required for setup)
- A **project folder** on your machine where you'll keep this work

## Process

### Step 1: Ask the user 7 questions (one AskUserQuestion batch where possible)

1. **Project name** — what should we call this content workspace? (free-text, used in the file header)
2. **What you're making** — ads only / carousels only / both / experimenting (multi-select)
3. **Brand voice** — pick from 4 archetypes (warm-friendly, sarcastic-witty, calm-educational, professional-polished) plus optional free-text override
4. **Default platform** — TikTok / Instagram / YouTube Shorts / multi-platform (this drives aspect ratio defaults)
5. **Default character** — already-saved character slug, or "I'll save one later", or "rotate through saved pool"
6. **Brand accent color** — terracotta `#DA7756` (default), or hex code free-text
7. **Output folder structure** — confirm or override the default `outputs/ads/`, `outputs/carousels/`, `outputs/morning/`

### Step 2: Build the CLAUDE.md content

Use the template in `templates/claude-md-template.md` as the scaffold. Substitute in the user's answers.

The CLAUDE.md should include:

- **Header** — project name, generated date, version
- **Project goal** — what they told you they're making
- **Defaults** — aspect ratio (from platform), resolution (always 2k), default character, default vibe, brand accent
- **Voice** — explicit rules pulled from the brand voice archetype, plus the user's overrides
- **Output structure** — where each skill writes its outputs
- **Models pinned** — SOUL for actors, Nano Banana Pro for scenes, Higgsfield Video for clips, Nano Banana Pro for carousels
- **Skills installed** — list of the 6 skills in the higgsfield-cowork-pack
- **Workflow rules** — how the skills should chain together (e.g. "/url-to-ad always pre-fills brief.json from source.json before running /product-to-ad")
- **Hard rules** — no em dashes, 5th-grade reading level, no auto-posting

### Step 3: Save the file

Default save path: `<project-root>/CLAUDE.md`. Ask the user to confirm the path before writing.

If a CLAUDE.md already exists, never overwrite silently. Show a diff of the differences and ask the user to choose: replace, merge, or keep existing.

### Step 4: Confirm + offer the next step

Show the user the saved file path. Ask if they want to:
1. Save a character now (chain into `/character-locker`)
2. Run their first ad (chain into `/product-to-ad`)
3. Just confirm, they'll come back later

End with a 1-sentence summary of what changed: "From now on, every Higgsfield skill in this folder uses these defaults. You'll only be asked about the specific product or topic, never about the brand."

## Output structure

```
<project-root>/
  └── CLAUDE.md          ← the generated config
```

That's it. One file. The whole pack now reads from it.

## Re-running

Run `/setup-higgsfield-project` again any time you want to update defaults. Common reasons:
- New brand voice
- New default character (you saved a better one)
- New platform (e.g. moving from TikTok-only to multi-platform)
- New output folder structure

The skill will load the existing CLAUDE.md, show you the current values, and only ask about fields you want to change. You don't have to re-answer all 7 questions.

## Rules

- ALWAYS ask before overwriting an existing CLAUDE.md.
- NEVER hard-code Higgsfield credentials, API keys, or anything sensitive into the CLAUDE.md. Those belong in Cowork's connector settings.
- The CLAUDE.md is shared with every Cowork conversation in this project — keep it under 200 lines so it doesn't bloat the context window.
- Use the user's exact wording for project name and voice overrides. Do not editorialize.
- If the user picks "experimenting" for project goal, generate a flexible CLAUDE.md with looser defaults (no locked character, vibe rotation, multiple aspect ratios).

## When NOT to use this skill

- The user's project already has a working CLAUDE.md they're happy with.
- The user wants a one-off generation, not a long-running project. (For one-offs, the skill defaults are fine without a CLAUDE.md.)
- The user is in someone else's project folder. Setup CLAUDE.md belongs to the project owner, not visiting collaborators.

## Pairs well with

- `/character-locker` — the natural first follow-up after setup
- `/product-to-ad` — uses the saved CLAUDE.md defaults to skip questions
- All 5 other skills in the pack — every single one reads from CLAUDE.md before asking the user anything
