# Browser Recipe — read-only Substack sensor

The Chrome extension (`mcp__Claude_in_Chrome__*`) is used here **only to read**. Every pattern below
observes state; none of them writes. The user takes every action from the worksheet.

## Forbidden actions (never do these)
- Never click **Reply**, **Restack**, **Post**, **Submit**, **Follow**, **Like**, or any vote control.
- Never type into a comment composer, a restack-note composer, or any input that posts to the account.
- Never fall back to computer-use to click a browser (browsers are read-only under computer-use anyway).
- If a step would require a write to make progress, **stop and report** instead. Never guess live state.

## 0. Preconditions
- Confirm a browser is connected via the extension.
- Navigate to `substack.com`. Confirm the visible logged-in account is **`@drinkyouroj`** (avatar /
  account menu). If it is not `@drinkyouroj`, stop and tell the user — take no further action.

## 1. Acting on a specific note reliably
The Notes feed lazy-loads and reorders, so screenshot-coordinate clicks drift. To target a specific
note:
1. Use `find` to get the element ref for the note's text.
2. Open its permalink by clicking the **note body** (read-only navigation), or read the body in place.
3. Capture the permalink URL for the worksheet (the user needs it to act).
Reading reply context: opening the comment view to read existing replies is fine (read-only). **Never
open the reply composer.** If reply content is not fully visible, scroll the comment *thread* view (not a
composer) to read it.

## 2. External dedup read — Likes & Replies
- Navigate to `substack.com/@drinkyouroj/likes`.
- Read recent **replies** and **restacks**. For each, capture: target author/handle, the note's gist,
  the analytical angle used, and (if visible) the permalink.
- This is the authoritative "what have I already engaged externally" source.

## 3. Cross-surface dedup read — the user's own Notes today
- Navigate to the `@drinkyouroj` profile's **Notes** tab (the user's own published Notes/posts).
- Capture the framing the user has already published **today** across surfaces (the day's Notes).
- Purpose: a comment must not echo what Justin already said in his own Note. This feeds dedup level 4
  (own already-published framing). If the live read is thin, fall back to the plan note's recommended
  default pairing / `fresh_today` as a signal of what was posted.

## 4. Live topic discovery
- Go to `substack.com/search`; query the day's beat. Read **Top** and **Recent** tabs.
- Also scan the home / Notes feed for live posters on the beat.
- For each candidate, capture: author/handle, note gist, permalink, and an approximate freshness/size
  read. Verify handles — the plan's named Tier-1 list is aspirational (e.g., `@noahsmith` is a CS
  academic, not Noahpinion).

## 5. Existing-follows read (for follow recommendations)
- From the `@drinkyouroj` profile / following list, read who the user already follows so the worksheet's
  follow recommendations exclude them. If the following list is not readily readable, note the
  uncertainty in the worksheet rather than guessing.

## Degrade rules
- Extension not connected, not logged in, or wrong account → **stop and report** (hard gates).
- A page won't load a needed read → report which read failed and continue with what is available, marking
  the gap in the worksheet. Never silently omit a gap.
