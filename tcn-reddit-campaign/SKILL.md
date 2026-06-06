---
name: tcn-reddit-campaign
description: >
  Standing-aware Reddit promotion manager for The Civic Node (TCN). Use this skill whenever the user
  wants to find subreddits for a Substack article, check subreddit rules, draft Reddit posts to
  promote a piece, or manage their Reddit promotion over time — including phrases like "plan Reddit
  for this piece", "where should I post this on Reddit", "find subreddits for my article", "promote
  this on Reddit", "draft a Reddit post for X", "reddit campaign", "what's my Reddit status", "what
  should I post on Reddit next", "which subreddits can I post to", or "help me build karma in r/X".
  The skill discovers topic-relevant subreddits, vets them against their rules AND the user's account
  standing, and produces per-subreddit paste-ready posts with the framing each sub's self-promo rules
  allow. It NEVER submits anything: it is read-only on the account and hands the user paste-ready
  drafts to post manually. Does NOT write the article (that's tcn-draft / tcn-article-builder), and
  does NOT write X/LinkedIn/Facebook social copy (that's tcn-post / tcn-facebook-post).
---

# tcn-reddit-campaign

A campaign manager for promoting TCN articles on Reddit without getting shadowbanned. It turns a
published Substack URL into a vetted, per-subreddit posting plan with paste-ready drafts, and it
remembers — caching subreddit dossiers and logging what was posted where, so it never re-researches a
sub, never breaks a cooldown, and always knows the next move.

## Hard constraints (never violate)
1. **Read-only on the account.** Claude-for-Chrome is a *sensor*, never a submit button. Never post,
   comment, vote, or DM. Output is always paste-ready for the user to submit.
2. **Honest authorship only.** First-person, truthful attribution. Never pose as a third party; never
   astroturf.
3. **Respect the rules.** Honor each sub's rules and Reddit sitewide rules. No vote manipulation, no
   ban evasion, no posting where self-promo is banned outright.
4. **Human-in-the-loop on every submission.** The user submits; then optionally pastes the URL back so
   the ledger updates.

## Modes
| User intent | Mode |
|---|---|
| Gives a published article URL / "plan Reddit for this piece" | **Mode 1 — Plan a piece** |
| "what's my Reddit status" / "what should I post next" (no article) | **Mode 2 — Campaign status** |
| "help me build standing in r/X" (a named sub) | **Mode 3 — Build standing** |

Identify the mode from the request; if ambiguous, ask.

## Browsing sensor policy (hybrid)
- **Discovery uses no browser:** Claude's subreddit knowledge + `audience-profiles` (Marcus persona) +
  WebSearch (`site:reddit.com <topic>`).
- **Chrome is the ground-truth sensor only for:** the live rules page of finalist subs, and the user's
  logged-in karma/account-age (read once per session). Use `mcp__Claude_in_Chrome__*`.
- If Chrome is unavailable/not logged in: degrade gracefully — ask the user to paste the rules page and
  report their karma. Never guess gates silently.

## State bootstrap
Campaign state lives at `~/Documents/substack-research/Substack Research/workspace/reddit-campaign/`.
On first run, if it does not exist, create:
- `reddit-campaign/dossiers/` (empty dir)
- `reddit-campaign/ledger.md` with this header:
  `| date | sub | article slug | framing | url | cooldown_until | outcome |`
  `|------|-----|--------------|---------|-----|----------------|---------|`
- `reddit-campaign/targets.md` (created lazily by Mode 3).

## Mode 1 — Plan a piece (the main flow)
1. **Intake.** Take the published Substack URL + slug. Read the canonical article at
   `~/Documents/substack-research/Substack Research/workspace/drafts/<slug>/10-final.md` for title +
   body (or, if absent, the highest-numbered draft in that folder, e.g. `05-draft-v{N}.md`); extract
   the topic and the 2–3 sharpest "hook" findings. If the slug is not given, derive it from the URL or
   ask. If no draft file exists, ask the user to paste the article text.
2. **Discovery (no browser).** Generate ~10–15 candidate subreddits (knowledge + Marcus persona +
   WebSearch), each with a one-line "why Marcus is here / why this article fits" rationale. Dedupe
   against existing dossiers in `reddit-campaign/dossiers/`.
3. **Vet (Chrome).** For each finalist without a fresh dossier (or one older than `FRESHNESS_DAYS`),
   read the live rules page and write/refresh `dossiers/r-<sub>.md` per `references/dossier-template.md`.
   Read the user's karma/account-age once.
4. **Eligibility.** Apply `references/eligibility-rules.md` → verdict per sub
   (Ready / Risky / Locked / No-go), cross-checked against the ledger for cooldown/burst caps.
5. **Frame + draft.** For Ready (and conservatively, Risky) subs, select the archetype via
   `references/self-promo-playbook.md`, then draft in the `references/reddit-voice.md` register. Run the
   AI-tell pass per `references/reddit-voice.md` § Anchor. Emit one **paste-ready bundle** per sub (see Output contract).
6. **Warming.** For Locked subs, produce a short karma-warming plan: 2–3 genuine comment opportunities
   (real current threads, via Chrome) or one native non-promo text-post idea that earns the standing to
   unlock the sub.
7. **Ledger stub.** Present the plan. When the user confirms a submission and pastes its URL, append a
   ledger row with `cooldown_until = post_date + COOLDOWN_DAYS`.

## Output contract — the paste-ready bundle
Every Ready/Risky draft ships with all of:
- **target sub** · **post type** (link / text) · **title** · **body** · **flair to select** ·
  **the exact rule it satisfies** · **link placement** (body or first comment — the comment is drafted
  too if applicable) · **suggested post time**.
Risky bundles are prefixed with an explicit caution naming the risk. No-go subs are listed with the
exclusion reason and no draft.

## Mode 2 — Campaign status / what's next
No article. Read `ledger.md` + dossiers → report: subs currently on cooldown (and when they clear),
Locked subs closest to unlocking, the user's karma progress, and a recommended set of this week's moves
(which warming comments to leave, which subs are now Ready). Karma progress is reused from the last
session's recorded value and may be stale — do a quick Chrome karma read if the user wants it current.
No drafting unless asked.

## Mode 3 — Build standing in a sub
Given a named sub, read/refresh its dossier, then produce a deeper warming plan (genuine participation
ideas grounded in current threads) to move it Locked → Ready. Record progress in `targets.md` (create
it if absent) — one row per warmed sub: `| sub | current karma | gate to clear | last warming action | last updated |`.

## Fallbacks
- Missing `10-final.md` and no draft file in the slug folder → ask for pasted text; continue.
- Chrome unavailable → ask user to paste rules + karma; continue.
- `audience-profiles` unavailable → use unaided knowledge of the Marcus persona; note the degrade (skip-not-halt).
- Ambiguous rules → classify **Risky**, surface the ambiguity, never auto-upgrade to Ready.
- Missing voice anchor file → skip AI-tell pass, keep structural output; note the skip.
- Sub private/banned/not found → **No-go** with reason; no draft.

## What this skill owns
- Subreddit discovery, rule vetting, standing/eligibility judgment, per-sub framing, Reddit-native
  drafting, karma-warming plans, and the persistent dossier + ledger.

## What this skill does NOT own
- Writing the article (`tcn-draft`, `tcn-article-builder`).
- X / LinkedIn / Facebook social copy (`tcn-post`, `tcn-facebook-post`).
- Submitting anything to Reddit (the user does this manually — by hard constraint).

## Related skills
- `audience-profiles` — the Marcus persona that seeds discovery. Invoke it via the Skill tool (or read
  `audience-profiles/references/marcus-profile.md`); if unavailable, fall back to unaided knowledge of
  the Marcus persona (skip-not-halt) and note it.
- `workspace/core/anti-ai-writing-style.md` — the canonical voice anchor (shared across the ecosystem).
- Future: callable as a post-publish step from `tcn-content-plan` / `tcn-article-builder`. Standalone today.

## References
- `references/dossier-template.md` — per-sub dossier schema.
- `references/eligibility-rules.md` — verdict logic + cadence defaults (user-tunable).
- `references/self-promo-playbook.md` — policy→framing map + culture rules (user-tunable).
- `references/reddit-voice.md` — the Reddit-native voice register.
