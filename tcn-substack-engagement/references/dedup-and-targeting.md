# Dedup & Targeting

> **▶ TUNE ME.** The counts and window below are sensible defaults from the content plan; the user
> adjusts them. They are not hard limits — honesty about a thin day beats padding to a number.
>
> - `COMMENT_TARGET_COUNT` = 6–8 per day
> - `RESTACK_TARGET_COUNT` = 1–2 per day (each with one sentence of added analysis)
> - `FOLLOW_COUNT` = 3–5 per day
> - `LEDGER_LOOKBACK_DAYS` = 7 (how far back prior worksheets supplement the live dedup read)

## The four dedup levels (hard gate — run before drafting)
A candidate is **spent** (skip it) if it matches the user's recent activity at any level:
1. **Same note** — the user already replied to or restacked this exact note (from Likes & Replies).
2. **Same author** — the user already engaged this author recently on this beat (a second comment to the
   same person in a few days reads as a double-dip).
3. **Same analytical angle** — the user already made this analytical point recently, even to a different
   author. Dedup the *idea*, not just the target.
4. **Same as own published framing today (cross-surface)** — the drafted comment would merely restate
   what the user already published in today's own Notes. A comment must add a distinct angle or apply the
   framing to the target's specific point — never echo Justin's own Note back to the feed.

**Source of truth:** the live reads (Likes & Replies for levels 1–3; the user's own Notes tab for level
4) win over any local supplement. Supplements: the prior worksheet (last `LEDGER_LOOKBACK_DAYS` days) and
the plan note's recommended default pairing / `fresh_today`.

## Spent-lane pivot
When one lane of the flagship's thesis is already spent across the week (e.g., the labor lane was
blitzed earlier), move engagement to the **unspent** lane (e.g., the grid/cost lane). The plan's
`duplication_audit` (`spent_this_week`) names what is burned; honor it. Hold material the plan reserves
for the flagship out of all comments.

## Aspirational-Tier-1 caveat
The plan's named Tier-1 accounts are **seeds, not a checklist.** Several are frequently not posting the
day's beat, and some handles are wrong (e.g., the Substack handle `@noahsmith` is a CS academic with a
handful of subscribers, **not** Noahpinion). Verify every handle live. The live, on-topic conversation
is usually among mid-tier writers surfaced by a topic search — weight toward whoever is actually in it.

## Comment-target ranking (highest first)
1. **In the live conversation** — actively posting the beat now (Recent tab / recent feed).
2. **Maps to a plan angle** — the plan's angles are the analytic payload; a live poster is a target only
   if Justin has something specific to add.
3. **Not deduped** — clears all four levels above.
4. **Account fit** — audience overlap and engagement likelihood; mid-tier writers in the live topic
   usually outperform chasing exact Tier-1 handles.

If no live on-topic posters surface: widen to adjacent beats, then report a **"thin day"** with whatever
was found. Do not pad with weak targets.

## Follow-selection heuristic
Candidate pool (~`FOLLOW_COUNT`/day), deduped against accounts the user already follows:
1. Authors engaged with today (comment or restack targets) the user does not already follow.
2. Live-topic discoveries on the beat that fit the audience but were not selected as comment targets.

Follows always land on the worksheet for the user to click — never auto-clicked (hard constraint 1).
Each follow ships with a one-line rationale tying it to building the audience-aligned algorithm.
