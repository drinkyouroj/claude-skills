# Install / Use Guide

## What this skill does

Schedule the full ad pipeline to run while you sleep. Set the campaign once. Wake up to a dated folder of fresh ads, captions, and a morning report telling you what got made.

## Why this matters

Even the fastest manual `/product-to-ad` run takes 5 minutes of your attention. If you want to run 30 ads a month, that's 2.5 hours of "watching Higgsfield render." `/overnight-content` removes you from the loop entirely. Set it Monday morning, check folders Tuesday through the rest of the month.

## What you need

- **Claude Cowork** desktop app
- **Higgsfield MCP** connected
- **Cowork's scheduled-tasks feature** (the skill uses `mcp__scheduled-tasks__create_scheduled_task`)
- At least **one saved character** via `/character-locker` (recommended, not strictly required)
- **Higgsfield credit budget** — calculate based on `ads_per_night × nights × ~7 credits`

## Install

The skill is part of the `higgsfield-cowork-pack` plugin. Install the plugin and `/overnight-content` shows up automatically.

## Use

In Cowork, type:
```
/overnight-content
```
or
```
schedule ads while I sleep
```

Claude will ask you for:
- **Source** (folder of products, list of URLs, or single product variations)
- **Volume** (1, 3, or 5 ads per night)
- **Character** (saved name, rotation, or generate fresh nightly)
- **Vibes** (1 or more, rotated through nights)
- **Run window** (start date, end date, time of night)

Claude saves the campaign config, calculates the credit budget, and creates the scheduled task.

## Where to find your output

Each night the scheduled task creates a dated folder:

```
outputs/morning/
  ├── 2026-04-30/
  │   ├── morning-report.md          ← read this first
  │   ├── ice-roller-sarcastic/
  │   │   └── (full /product-to-ad output)
  │   ├── pillow-mist-calm/
  │   │   └── (full output)
  │   └── ...
  ├── 2026-05-01/
  │   └── ...
```

The `morning-report.md` is your one-page summary: what got made, what failed, credits used, hooks for each ad.

## Recommended first run

Before committing to 30 days, run a one-night test:

```
/overnight-content — single night test for tonight, one ad, use Maya, vibe sarcastic.
```

This burns 5 to 8 credits. Check the morning folder tomorrow. If it looks right, schedule the full campaign. Don't burn 200 credits validating a config that has a typo in it.

## Common issues

**"The scheduled task didn't fire."**
Three things to check:

1. Cowork has to be running (or set to auto-start) at the scheduled time. If your Mac is asleep at 2 AM, the task is paused.
2. Higgsfield credits are below the per-ad threshold. The skill checks balance at the start of each run and aborts if low.
3. The Cowork scheduled-tasks MCP isn't connected. Settings → Connectors.

**"The morning report says everything failed."**
Open the report and look at the error column. The most common failure: Higgsfield is rate-limiting you because you queued too many at once. Fix: lower `ads_per_night` to 1 or 2.

**"All my ads use the same character."**
That's the saved-character behavior. If you want rotation, edit the campaign config and set `characters.mode` to `rotate-saved` with a `rotation_pool` array of slugs.

**"I want to stop the campaign mid-run."**
Run `/overnight-content stop campaign-slug` (Claude will list active scheduled tasks and confirm before deleting). The dated folders from past nights stay; only the future runs are cancelled.

**"Can it run during the day?"**
Yes. The "overnight" is a default, not a requirement. You can schedule for any hour. Just avoid US peak Higgsfield hours (8 to 11 PM ET) so jobs queue faster.

## Pairs well with

- `/character-locker` — save 2 to 5 characters, rotate them in the config
- `/product-to-ad` — what each nightly run actually invokes
- `/url-to-ad` — alternative source mode (URLs instead of local product images)

## Cost reference

| Setup | Total credits |
|---|---|
| 1 ad/night for 7 nights | ~35 to 56 |
| 1 ad/night for 30 nights | ~150 to 240 |
| 3 ads/night for 30 nights | ~450 to 720 |
| 5 ads/night for 30 nights | ~750 to 1,200 |

Always check Higgsfield balance before scheduling. The skill warns you if your budget exceeds your credits.

## Privacy note

The campaign config and morning reports stay local on your machine. Nothing is uploaded except the ad generations themselves to Higgsfield (which is the same as running `/product-to-ad` manually).
