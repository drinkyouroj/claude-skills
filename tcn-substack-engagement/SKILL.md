---
name: tcn-substack-engagement
description: >
  Read-only daily Substack engagement preparer for The Civic Node (TCN). Use this skill whenever the
  user wants to handle, prepare, or run today's Substack engagement — comments, restacks, and new
  follows — including phrases like "do today's Substack engagement", "run my engagement", "prep my
  comments and restacks", "who should I engage today", "draft my Substack comments", "engagement
  worksheet", "restacks for today", "what should I restack", or "follow some accounts for the
  algorithm". It reads today's content-plan note's Engagement section, uses the Claude-for-Chrome
  extension as a READ-ONLY sensor to dedup against the user's own recent activity (Likes & Replies AND
  the user's own Notes published today) and to find who is actually posting the day's beat, then
  produces a paste-ready worksheet (comments + restack addenda + follow list) that the user executes by
  hand. It NEVER submits, comments, restacks, follows, likes, votes, or clicks any button on the
  account — the user takes every action. Does NOT write the content plan (tcn-content-plan), Substack
  Notes (tcn-substack-notes), X/LinkedIn/Facebook copy (tcn-post / tcn-facebook-post), or Reddit posts
  (tcn-reddit-campaign).
---

# tcn-substack-engagement

A daily, read-only engagement preparer. It consumes today's content-plan Engagement assignment, uses
the Chrome extension as a sensor to dedup and discover who is live on the beat, drafts every comment and
restack addendum in Justin Hearn's voice, and hands back a paste-ready worksheet. "Act independently"
means this skill does all the cognitive labor (dedup, discovery, ranking, drafting); the user does only
the final clicks. Its doctrine sibling is `tcn-reddit-campaign` (read-only sensor, human executes,
durable ledger) — applied to a recurring daily surface instead of a per-article campaign.

## Hard constraints (never violate)
1. **Read-only on the account.** Claude-for-Chrome is a *sensor*, never a submit button. Never type into
   a composer; never click Reply / Restack / Post / Submit / Follow / Like / vote. The worksheet is the
   only output. Every action is the user's.
2. **Account check is a precondition.** Verify the logged-in account is `@drinkyouroj` before any read
   that informs drafting. If it is not, stop and report — do nothing.
3. **Dedup is a hard gate (including cross-surface).** Before drafting, read the user's Likes & Replies
   AND the user's own Notes published today. Dedup at four levels: same note, same author, same
   analytical angle, and same as the user's own already-published framing today. A comment must never
   blatantly repeat what the user already said in the day's Notes. See
   `references/dedup-and-targeting.md`.
4. **Honest, voice-true authorship.** First-person, truthful; never astroturf. All drafted copy passes
   `~/Documents/substack-research/Substack Research/workspace/core/anti-ai-writing-style.md`. No
   template-stamping — each comment answers what the target actually said.
5. **Stay in the day's authorized lane.** Inherit the plan's spend/hold boundaries. Comments must not
   spend material the plan is holding for the flagship.

## Mode
| User intent | Mode |
|---|---|
| "run today's engagement" / "prep my comments and restacks" / "engagement worksheet" | **Run today's engagement** (the only mode) |

If no content-plan note exists for today, see Fallbacks before proceeding.

## Browsing sensor policy (read-only)
- **Chrome is the ground-truth sensor only for, in this order:** (a) the `@drinkyouroj` login check;
  (b) the dedup reads — `substack.com/@drinkyouroj/likes` (Likes & Replies) and the `@drinkyouroj`
  profile's Notes tab (own posts today); (c) live topic discovery — `substack.com/search` (Top +
  Recent); (d) each candidate note's actual text; (e) the user's existing follows. Use
  `mcp__Claude_in_Chrome__*`. Full recipe in `references/browser-recipe.md`.
- **Never a write button.** The extension reads. It never types, clicks Reply/Restack/Follow/Like, or
  submits. (Hard constraint 1.)
- **If Chrome is unavailable / not logged in / wrong account:** degrade gracefully — stop and tell the
  user what is needed (connect the extension, log in as `@drinkyouroj`). Never fall back to computer-use
  clicking a browser (browsers are read-only under computer-use). Never guess live state silently.

## State bootstrap
Worksheets live at `~/Documents/substack-research/Substack Research/workspace/engagement/`. On first run,
if the directory does not exist, create it (the `README.md` there documents the worksheet format). Each
run writes `workspace/engagement/YYYY-MM-DD-worksheet.md`; that dated file doubles as the next day's
local dedup ledger.

## Run flow — "run today's engagement"
1. **Preconditions.** Confirm the Chrome extension is connected. Navigate to `substack.com`; verify the
   logged-in account is `@drinkyouroj` (stop + report if not). Locate today's plan note at
   `~/Documents/substack-research/Substack Research/workspace/notes/YYYY-MM-DD-*-options.md`. If none,
   see Fallbacks.
2. **Load context.** Parse the plan's **Engagement** section (comment targets + angles, restack targets
   + addenda), the `duplication_audit` frontmatter (`spent_this_week`, `fresh_today`), and the hold list
   (it lives in the `live_news` frontmatter under a 'HELD for the … flagship' entry and/or inline in the
   Engagement preamble). Load the voice anchor. Read prior worksheets from the last `LEDGER_LOOKBACK_DAYS` days in
   `workspace/engagement/` if present (the local dedup ledger).
3. **Dedup read (hard gate).** Read Likes & Replies; read the user's own Notes published today; build the
   **spent set** at four levels (note / author / angle / own-published-framing). Merge two supplements:
   the prior worksheet's targets, and the plan note's recommended default pairing / `fresh_today` (a
   fallback signal for what was posted if the live Notes read is thin). Live reads win on conflict. See
   `references/dedup-and-targeting.md`.
4. **Live discovery.** Search the day's topic (Top + Recent) and scan the feed for who is actually
   posting the beat now. Treat the plan's named Tier-1 list as aspirational seeds, not a checklist —
   verify handles. Rank per `references/dedup-and-targeting.md`.
5. **Target-confirm gate (human checkpoint).** Present the ranked list as *live poster → which plan
   angle → the note permalink*, plus the proposed follow list (~3–5). The user prunes. Draft **only the
   survivors.**
6. **Draft.** For each confirmed comment: write the paste-ready reply from the plan's angle **against
   the note's actual content**. For each restack: the one-sentence added-analysis addendum. Then run
   three passes over all drafted prose: (a) voice check against the anchor file; (b) cross-surface
   distinctness — if a draft merely restates the day's own published Notes framing, rewrite it to add a
   distinct angle or engage the target's specific point, or cut it; (c) lane discipline — drop/rewrite
   anything that spends held material.
7. **Output the worksheet.** Write `workspace/engagement/YYYY-MM-DD-worksheet.md` per the Output
   contract and surface it in chat. The user executes by hand.

## Output contract — the worksheet
Write `workspace/engagement/YYYY-MM-DD-worksheet.md`. Header records: date · plan note it was built from
· account verified (`@drinkyouroj`) · a one-line dedup summary (what was already-spent and skipped,
including any angle dropped because it echoed the day's own Notes).

Then three checklists. **Each comment item:** `- [ ]` · target author + handle · note permalink · the
note's gist (1 line) · the paste-ready comment text · "why this target" (1 line: which plan angle, why
unspent). **Each restack item:** `- [ ]` · note permalink + author · the note's gist (1 line) · the
paste-ready one-sentence addendum. **Each follow item:** `- [ ]` · account name + profile link ·
rationale (1 line). The README template at `workspace/engagement/README.md` is authoritative for the
exact field labels and header format (including the `**Date:**` line) — use its labels verbatim.

## Fallbacks (skip-not-halt unless a hard gate)
- **No plan note for today** → offer to invoke `tcn-content-plan` (Mode 1), or take a topic from the
  user. If both declined, abort.
- **Wrong account / not logged in** (hard gate) → stop; report; take no action.
- **Chrome extension not connected** (hard gate) → ask the user to connect it; never fall back to
  computer-use clicking a browser.
- **No live on-topic posters** → widen to adjacent beats; report a "thin day" with what surfaced. Never
  force weak targets to hit a number.
- **A plan target is already spent** (dedup hit) → skip it; record it in the worksheet's dedup summary;
  pivot to an unspent lane/author per the plan.
- **Missing voice anchor file** → skip the AI-tell pass; keep structurally-correct drafts; note the skip
  (ecosystem skip-not-halt convention).

## What this skill owns
- Daily dedup (incl. cross-surface vs. own Notes), live target discovery + ranking, voice-true comment
  and restack drafting, follow recommendation, and the durable dated worksheet that doubles as a local
  dedup ledger.

## What this skill does NOT own
- Any write action on Substack — comments, restacks, follows, likes, votes (the user does these, by hard
  constraint).
- The content plan + its Engagement assignment (`tcn-content-plan`).
- Substack Notes (`tcn-substack-notes`), X/LinkedIn/Facebook copy (`tcn-post`, `tcn-facebook-post`),
  Reddit (`tcn-reddit-campaign`).
- Headless/autonomous runs (needs the user's logged-in session — out of scope for v1).

## Related skills
- `tcn-content-plan` — produces the Engagement section this skill consumes. Invoke it (Mode 1) if no
  plan note exists for today.
- `workspace/core/anti-ai-writing-style.md` — the canonical voice anchor (shared across the ecosystem;
  loaded, never duplicated).
- `tcn-reddit-campaign` — the read-only-sensor doctrine sibling (per-article rather than daily).

## References
- `references/browser-recipe.md` — the read-only Chrome interaction recipe + the forbidden-actions list.
- `references/dedup-and-targeting.md` — four-level dedup, spent-lane pivot, aspirational-Tier-1 caveat,
  ranking + follow-selection heuristics, tunable defaults.
