---
name: character-locker
description: Save a UGC actor as a reusable character profile so every future video uses the exact same face, outfit, and vibe. Use this skill when the user says "save this character", "lock this actor", "make this person reusable", "save my UGC character", "character locker", "create a character profile", "reuse this actor", or wants consistency across multiple ads. Pairs with /product-to-ad, /url-to-ad, and /overnight-content. Powered by Higgsfield SOUL via the MCP.
---

# Character Locker

Save a UGC actor once. Reuse them forever. Stop the character-drift problem where every ad has a different face.

## What this skill does (in one breath)

1. Generates or accepts an existing UGC actor (Higgsfield SOUL)
2. Saves the profile to `characters/<name>.json` (job_id + descriptor + tags)
3. Lets every other skill in the pack pull the same actor by name

By the end the user has a named character file they can call by saying "use Maya" in any future ad.

## Setup the user needs

- Higgsfield MCP connected.
- A clear idea of the actor they want, OR an existing Higgsfield job_id to import.
- About 1 to 2 Higgsfield credits to generate a fresh actor.

## Process

### Step 1: Ask what the user wants to do

Use AskUserQuestion. One question, three options:

1. **Generate a new actor** — start from scratch with SOUL.
2. **Import an existing actor** — they already generated a face they like, and want to save the job_id.
3. **List my saved actors** — show what's already in `characters/`.

If option 3, read every `characters/*.json` file, print a one-line summary of each (name, archetype, age, vibe), then stop.

### Step 2a: Generate path

Ask 4 quick follow-ups via a single AskUserQuestion batch:
- **Name** — what should we call this character? (e.g. "Maya", "Big Mike"). Used as the filename.
- **Archetype** — pick from `references/archetypes-quick.md` (gym-bro, busy-mom, gen-z-creator, etc.)
- **Specifics** — free-text override (skin tone, hair, age, vibe twist, anything else)
- **Default scene** — the setting they normally appear in (kitchen, gym, bathroom mirror, car, bedroom, etc.)

Build a SOUL prompt by combining the archetype block from `references/archetypes-quick.md` with the specifics. Aspect ratio `9:16`, resolution `2k`, model `soul_cast` (text-to-image character).

Save the rendered PNG to `characters/<slug>/portrait.png`. Save the Higgsfield job_id.

### Step 2b: Import path

Ask the user for:
- **Name** — what to call the character.
- **Higgsfield job_id** — paste from a previous generation or the Higgsfield UI.
- **Archetype + specifics** (same as 2a, used for tagging and future regeneration if the saved face ever needs a refresh).

Verify the job_id exists by calling `mcp__8148b7eb-72e8-45e8-bb1d-864094e854c1__job_display` with that ID. If it returns a non-image or errors, stop and tell the user.

### Step 3: Write the character profile

Save to `characters/<slug>.json`:

```json
{
  "name": "Maya",
  "slug": "maya",
  "created_at": "2026-04-29T13:00:00Z",
  "archetype": "busy-mom-thirties",
  "specifics": "warm latina mom, 32, hair in a low bun, oversized cream cardigan",
  "default_scene": "sunlit kitchen counter",
  "higgsfield": {
    "job_id": "76712ea7-6e56-42c0-810a-2513b74d1c4c",
    "model": "soul_cast",
    "raw_url": "https://d8j0ntlcm91z4.cloudfront.net/...png"
  },
  "soul_prompt": "FULL TEXT OF THE PROMPT USED, so it can be regenerated identically if needed",
  "tags": ["mom", "warm", "kitchen", "skincare", "wellness"]
}
```

Use `templates/character-profile.json` as the template. Always include `soul_prompt` — that is the fallback if the job_id ever expires.

### Step 4: Confirm and hand off

Show the user:
- The portrait (computer:// link to the PNG)
- The profile path (computer:// link to the JSON)
- The instruction: "Now in any other skill just say 'use Maya' and the same actor will appear."

End with a prompt suggestion: "Want me to use this character to make an ad now?" (if yes, hand off to `/product-to-ad` with `saved_character_id` already filled in).

## How other skills use saved characters

When `/product-to-ad`, `/url-to-ad`, or `/overnight-content` start, they always check `characters/` first.

If the user mentions a name that matches a saved character (e.g. "make an ad with Maya for this product"), they:
1. Read `characters/<slug>.json`
2. Skip Step 3 (actor generation) of `/product-to-ad`
3. Pass the `higgsfield.job_id` directly as the actor reference in Step 4 (scene compositing)
4. Use the saved `default_scene` unless the user overrides

This is the consistency play. Same face. Same vibe. Across every ad in a campaign.

## Editing or deleting

- **Edit** — open `characters/<slug>.json` and change any field. Specifics + soul_prompt drive future regenerations.
- **Regenerate face** — run the skill again with the same name; ask if the user wants to overwrite. Re-render with the saved soul_prompt for an identical-but-fresh portrait.
- **Delete** — just delete the JSON file. The Higgsfield job stays in their account and can be re-imported later.

## Output structure

```
characters/
  ├── maya.json
  ├── maya/
  │   └── portrait.png
  ├── big-mike.json
  └── big-mike/
      └── portrait.png
```

## Rules

- ALWAYS save `soul_prompt` in the profile. Job_ids can become stale; the prompt cannot.
- ALWAYS use kebab-case for the slug.
- ALWAYS verify the job_id exists before saving (Step 2b).
- NEVER overwrite an existing profile without asking.
- NEVER store anything sensitive — this is a creative profile, not a personal record.
- 9:16 vertical for the portrait, even if the user only plans square use. Easier to crop down than up.

## When NOT to use this skill

- The user wants a one-off ad with a face they will never reuse — skip `/character-locker`, just let `/product-to-ad` generate and forget.
- The user wants to use their own face. SOUL works best with synthetic actors. For real-face UGC, use a different model (Higgsfield Soul 2 with a face reference photo).
