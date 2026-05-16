# Nightly Prompt Template

This is the prompt the scheduled task receives every night when it fires. Do NOT show this to the user during setup. Build it programmatically inside `/overnight-content` Step 3.

## Template

```
You are running the nightly batch for the "<campaign_slug>" campaign.

1. Load the campaign config:
   /Users/brockmesarich/Desktop/Claude Code Short System/campaigns/<campaign_slug>/config.json

2. Today's date is <DATE>. Create the output folder:
   /Users/brockmesarich/Desktop/Claude Code Short System/outputs/morning/<DATE>/

3. Pick today's batch:
   - Pick `ads_per_night` items from the source pool (round-robin index keyed off the day-of-year)
   - Pick today's vibe from `vibes` (rotation by day)
   - Pick today's character per `characters.mode`

4. Check Higgsfield balance. If credits < ads_per_night * 8, abort and log "insufficient credits" in morning-report.md.

5. For each item in today's batch:
   a. If source.type == "products-folder" or "single-product-variations": run /product-to-ad with the pre-filled brief
   b. If source.type == "urls": run /url-to-ad with that URL
   c. Save outputs to outputs/morning/<DATE>/<ad-slug>/

6. After all items finish (or fail), write morning-report.md following the format in /character-locker SKILL.md Step 6.

7. End the run silently. Do NOT chat back to the user. The morning-report.md IS the chat.
```

## Variable substitution

When building the prompt, replace:
- `<campaign_slug>` — from config
- `<DATE>` — `date +%Y-%m-%d` at run time

## Failure modes the prompt handles

- Higgsfield down: log + skip
- Source URL 404: log + skip that one product, continue with the rest
- Character profile deleted: regenerate from saved soul_prompt
- Output folder permission error: write to /tmp/morning-fallback/ and log the move

## Why this is a separate file

The nightly prompt is the brain of the scheduled task. Keeping it in a reference makes it easy to update without touching SKILL.md, and gives the user something to inspect if they want to know what their scheduled task is actually doing.
