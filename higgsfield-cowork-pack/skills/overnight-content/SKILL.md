---
name: overnight-content
description: Schedule the full ad pipeline to run while you sleep. Drops a folder of ready-to-post ads, captions, and image variations on your desktop every morning. Use this skill when the user says "overnight content", "while I sleep", "schedule ads", "auto-generate ads", "morning content drop", "automate my UGC", "schedule this nightly", or wants a hands-off content pipeline. Wraps /product-to-ad and /url-to-ad in a Cowork scheduled task.
---

# Overnight Content

Set it once. Wake up to a folder of fresh ads every morning.

## What this skill does (in one breath)

1. Reads a "campaign config" (which products, which characters, how many ads)
2. Schedules a Cowork task to run nightly at midnight
3. Each night, generates 1 to N finished ads using `/product-to-ad`
4. Saves to `outputs/morning/<YYYY-MM-DD>/` so the user wakes up to a dated folder
5. Writes a small `morning-report.md` summarizing what was made

By the end the user has a recurring, hands-off content engine.

## Setup the user needs

- Higgsfield MCP connected with enough credits for the planned run rate (each ad is ~5 to 8 credits — a 30-day month at 1 ad/night is ~150 to 240 credits).
- At least one saved character via `/character-locker` (recommended, not required).
- The Cowork scheduled-tasks feature available (this skill uses `mcp__scheduled-tasks__create_scheduled_task`).

## Process

### Step 1: Build the campaign config

Use AskUserQuestion to collect:

1. **Source** — where are the products?
   - "Folder of product images" (path under `inputs/products/`)
   - "List of URLs" (paste them, this skill will use `/url-to-ad` per night)
   - "Single product, vary the ads" (run multiple ad variations off the same product)
2. **Volume** — how many ads per night? 1, 3, or 5.
3. **Character** — saved character name, or "rotate through all" or "generate a new one each time".
4. **Vibes** — pick 1 or more from: excited-high-energy, calm-educational, sarcastic-funny, soft-aspirational. If multiple, the skill rotates through them.
5. **Run window** — start date and end date. Default: tonight to 30 days out.
6. **Time** — what hour of the night? Default: 02:00 local time. Avoid US peak Higgsfield hours (8 to 11 PM ET) so jobs queue faster.

Save to `campaigns/<slug>/config.json`. Use `templates/campaign-config.json`.

### Step 2: Verify credit budget

Math check:
- ads_per_night × nights × ~7 credits = total credits needed
- Call `mcp__8148b7eb-72e8-45e8-bb1d-864094e854c1__balance` and compare.
- If short, warn the user with the exact number they need to top up.

### Step 3: Create the scheduled task

Call `mcp__scheduled-tasks__create_scheduled_task` with:
- **Schedule** — daily at the user's chosen time, between start and end dates.
- **Prompt** — a templated prompt that loads the campaign config and runs one night's batch (see `references/nightly-prompt.md`).
- **Working directory** — the user's Cowork project root.

The prompt the scheduled task receives looks like this (do not show this to the user, just create it):

```
Run the overnight-content nightly batch for campaign "<slug>".
1. Load campaigns/<slug>/config.json
2. Pick today's products + vibes per the rotation rules
3. For each, run /product-to-ad (or /url-to-ad if source=urls) silently
4. Save outputs to outputs/morning/<YYYY-MM-DD>/<ad-slug>/
5. Write outputs/morning/<YYYY-MM-DD>/morning-report.md summarizing what was made
6. If any generation failed, log it in morning-report.md but keep going
```

### Step 4: Show the user the schedule

Confirm:
- Task name
- Run time + run window
- Total ads expected
- Estimated total credits
- Output folder pattern

End with a prompt suggestion: "Want me to test-run tonight's batch right now so you can see the output?"

### Step 5: Daily run (this is what the scheduled task does, NOT what the user invokes)

When the scheduled task fires:

1. Read `campaigns/<slug>/config.json`
2. Pick the next product (round-robin through the source list, or shuffle if the user picked random)
3. Pick today's vibe (round-robin)
4. Pick today's character (saved profile, rotate, or generate fresh per config)
5. Run `/product-to-ad` (or `/url-to-ad` if source is URLs) with everything pre-filled
6. Save the output to `outputs/morning/<YYYY-MM-DD>/<ad-slug>/`
7. Append to `morning-report.md`:
   ```markdown
   ## <ad-slug>
   - Product: ...
   - Character: Maya
   - Vibe: sarcastic-funny
   - Hook: "Tell me why I just bought a $30 ice roller"
   - Files: clip-01.mp4, clip-02.mp4, clip-03.mp4
   - Status: ✅ rendered
   ```
8. If anything errors (Higgsfield credits exhausted, Chrome extension disconnected, etc.), log the error in morning-report.md and skip to the next item. Do NOT abort the whole run.

### Step 6: Morning report

`outputs/morning/<YYYY-MM-DD>/morning-report.md` should be the first thing the user sees each morning. Make it scannable:

```markdown
# Morning Report — 2026-04-29

## What got made tonight
- 3 ads ✅
- 0 failures
- 21 Higgsfield credits used
- Total credits remaining: 134

## Ads ready to post

### 1. Ice Roller (sarcastic-funny)
[scene.png] [clip-01.mp4] [clip-02.mp4] [clip-03.mp4] [caption.txt]
Hook: "Tell me why I just paid $30 for an ice cube on a stick"

### 2. ...

## What to do next
1. Pick your favorite ad
2. Drag the clips into your phone
3. Post to TikTok / Reels (or use /schedule-blotato)
```

## Rules

- NEVER auto-post. Even with `/schedule-blotato` available, this skill stops at "saved to folder". Posting is a separate user action.
- NEVER overrun the user's credit budget. Calculate before scheduling, not after.
- NEVER run more than 5 ads per night by default. The user can override but this skill warns at 6+.
- ALWAYS write `morning-report.md` even if nothing succeeded — the user needs to know what happened.
- ALWAYS dated folders. Never overwrite previous mornings.
- ALWAYS log failures with the actual error so the user can fix the campaign config.

## When NOT to use this skill

- The user only wants 1 to 2 ads, one time. Just run `/product-to-ad`.
- The user wants the ads to autoposted. Use `/schedule-blotato` separately after reviewing.
- The user wants the same exact ad every night. They want a duplicate, not a campaign — just save the original.

## Output structure

```
campaigns/
  └── <campaign-slug>/
      └── config.json

outputs/morning/
  ├── 2026-04-29/
  │   ├── morning-report.md
  │   ├── ice-roller-sarcastic/
  │   │   └── (full /product-to-ad output)
  │   └── ...
  ├── 2026-04-30/
  │   └── ...
```
