# Higgsfield Content Project — {{PROJECT_NAME}}
Generated: {{DATE}}
Pack version: 0.4.0

## Goal
{{PROJECT_GOAL}}

## Defaults

| Setting | Value |
|---|---|
| Aspect ratio | {{ASPECT_RATIO}} |
| Resolution | 2k |
| Default character | {{DEFAULT_CHARACTER}} |
| Default vibe | {{DEFAULT_VIBE}} |
| Brand accent | {{BRAND_ACCENT}} |
| Default platform | {{PLATFORM}} |

## Voice

{{VOICE_RULES}}

Hard rules that apply regardless of voice:
- 5th-grade reading level on every viewer-facing line
- Short sentences, plain words
- No em dashes (use commas, periods, or rephrase)
- Talk to one person, not a room
- Never sound like an ad

## Output structure

```
{{PROJECT_NAME_SLUG}}/
  ├── inputs/
  │   ├── products/        ← drop product images here
  │   └── urls.md          ← list URLs for /url-to-ad
  ├── characters/          ← saved character profiles
  ├── outputs/
  │   ├── ads/             ← /product-to-ad output
  │   ├── carousels/       ← /ig-carousel output
  │   └── morning/         ← /overnight-content output
  └── CLAUDE.md            ← this file
```

## Models pinned

| Job | Model |
|---|---|
| UGC actor face | Higgsfield SOUL |
| Actor + product scene | Higgsfield Nano Banana Pro |
| Video clips | Higgsfield Video |
| Instagram carousels | Higgsfield Nano Banana Pro |

## Skills installed (higgsfield-cowork-pack)

- `/setup-higgsfield-project` — this skill
- `/character-locker` — save reusable UGC actors
- `/product-to-ad` — turn a product image into a UGC video ad
- `/url-to-ad` — same pipeline, starts from a URL
- `/overnight-content` — schedule the pipeline to run nightly
- `/ig-carousel` — build cinematic Instagram carousels

## Workflow rules

When the user runs any skill in this folder:
- Auto-fill all defaults from this file. Never re-ask the user about aspect ratio, resolution, voice, output folder, or default character unless they explicitly want to change it for this run.
- If a saved character profile is named in the user's prompt, load it from `characters/<slug>.json` before any generation.
- For `/url-to-ad`: extract the product page first, save to `source.json`, then chain into `/product-to-ad` with the brief auto-filled.
- For `/overnight-content`: never run without first checking Higgsfield credit balance against the budget calculation.

## Hard rules

- Never auto-post any generated content. Save to disk, then ask the user to review.
- Never overwrite a saved character profile without confirmation.
- Never use em dashes anywhere in scripts, captions, or chat output.
- Never make up product features or claims that aren't supported by the actual product page or user-provided brief.
- Never store Higgsfield credentials, API keys, or anything sensitive in this file.

## When in doubt

The user's preferences (in chat) override this file. This file is a default, not a hard constraint. If the user explicitly asks for a different aspect ratio, vibe, or character for one specific run, use what they asked for and don't re-ask why.
