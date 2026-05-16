# Install / Use Guide

## What this skill does

Save a UGC actor as a reusable character profile. Generate the face once. Reuse the exact same person across every ad you ever make.

## Why this matters

The biggest hidden problem with AI-generated UGC ads is character drift. Every time you run a fresh generation, the actor looks slightly different. Your audience picks up on it. Your brand stops feeling cohesive.

`/character-locker` solves this by saving the Higgsfield job_id plus the full SOUL prompt to a profile file. Every future skill in the pack can pull that profile by name and the same face appears, frame for frame.

## What you need

- **Claude Cowork** desktop app
- **Higgsfield MCP** connected (Settings → Connectors → Higgsfield)
- About **1 to 2 Higgsfield credits** to generate a fresh actor (or zero if you import an existing job_id)

## Install

The skill is part of the `higgsfield-cowork-pack` plugin. Install the plugin and `/character-locker` shows up automatically.

## Use

In Cowork, type:
```
/character-locker
```
or
```
save a character
```

Claude will ask you to pick a path (Generate / Import / List), then ask for:
- **Name** — what to call the character
- **Archetype** — gym-bro, busy-mom, gen-z creator, white-collar pro, outdoorsy, senior
- **Specifics** — your free-text overrides (skin tone, age, hair, vibe)
- **Default scene** — where they appear by default

Claude builds the SOUL prompt, generates the face, and saves the profile.

## Where to find your output

```
characters/
  ├── maya.json
  └── maya/
      └── portrait.png
```

The JSON profile contains:
- `name`, `slug`, `created_at`
- `archetype`, `specifics`, `default_scene`
- `higgsfield.job_id` and `higgsfield.raw_url`
- `soul_prompt` (full text, for re-roll if the job ever expires)
- `tags` (search keywords)

## Reusing the character

Once saved, just say "use Maya" inside any other skill in the pack:

```
/product-to-ad — use Maya for this product image.
```

```
/url-to-ad https://amazon.com/dp/B0XXX — use Maya, vibe sarcastic.
```

```
/overnight-content — rotate between Maya and Big Mike for the next 30 days.
```

## Editing or regenerating

- **Edit any field** — open `characters/<slug>.json` and change it. The next generation will use the new fields.
- **Regenerate the face** — run `/character-locker` again with the same name. Claude asks if you want to overwrite. If yes, it re-renders the SOUL portrait with the saved prompt.
- **Delete a character** — just delete the JSON file. The Higgsfield job stays in your account.

## Common issues

**"Higgsfield MCP not connected."**
Open Cowork → Settings → Connectors → toggle Higgsfield on.

**"The face looks wrong."**
Run the skill again with more specific overrides. The `specifics` field is your strongest knob. Add details like "hair color, skin tone, age, slight smile, neutral background" and the SOUL model will lock in tighter.

**"I want to use my own face."**
SOUL is for synthetic actors. For your real face, use Higgsfield SOUL 2 with a face reference photo (different model, separate workflow).

## Pairs well with

- `/product-to-ad` — passes the saved character into every ad
- `/url-to-ad` — same, from a URL
- `/overnight-content` — rotate through multiple saved characters nightly

## Cost per character

About 1 to 2 Higgsfield credits per generation. Most users save 3 to 5 characters total (one per buyer archetype) and reuse them indefinitely.
