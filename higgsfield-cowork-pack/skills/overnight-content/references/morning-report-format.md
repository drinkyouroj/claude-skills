# Morning Report Format

The first thing you read every morning. Has to be scannable in 30 seconds. Below is the exact format the scheduled task generates each night.

## Template

```markdown
# Morning Report — <YYYY-MM-DD>

## Summary
- <N> ads ✅ rendered
- <M> ads ❌ failed
- <X> Higgsfield credits used
- <Y> credits remaining

## Ads ready to post

### 1. <Ad Title> (<vibe>)
**Hook:** <first line of script.md>
**Files:** [scene.png] [clip-01.mp4] [clip-02.mp4] [clip-03.mp4] [caption.txt]
**Folder:** outputs/morning/<date>/<ad-slug>/

### 2. <Ad Title> (<vibe>)
...

## Failures (if any)

### <Ad Title>
**Why:** <error message>
**Action:** <suggested fix>

## What to do next
1. Pick your favorite ad of the morning
2. Drag the clips into your phone
3. Schedule the post (Blotato, manual, whatever)
```

## Why each section matters

**Summary** — One-line gut check. Is the campaign healthy? Anything to worry about?

**Ads ready to post** — Each entry leads with the **hook** because that's what tells you instantly if the ad is worth posting. If the hook is weak, skim the others before diving in. The folder path makes it copy-paste-able.

**Failures** — Every failure logs *why* and *what to do*. Common failures:
- Higgsfield rate-limited → wait an hour and re-run manually
- Source product image was corrupt → fix the product and re-run
- Character profile was deleted → restore from backup or regenerate

**What to do next** — Three concrete actions. Not five, not ten. Three.

## Why morning-report.md is markdown

So you can preview it in any editor (VS Code, Obsidian, the Finder Quick Look pane) without opening Cowork. Even if Cowork is closed, you can still read what happened overnight and grab the clips.

## Auto-generated, do not edit

This report is rebuilt every morning by the scheduled task. If you edit it, your changes get overwritten the next night.

If you want to keep notes about an ad, put them in a different file (e.g. `outputs/morning/<date>/notes.md`). The scheduled task only owns `morning-report.md`.

## Customizing the format

If you want to change the report structure (e.g. add CTR predictions, or sort by hook strength), edit `references/nightly-prompt.md` in this skill. The nightly scheduled task uses that prompt to write the report.
