# Eligibility Rules — verdict logic + campaign defaults

> **▶ TUNE ME.** This file encodes the user's personal shadowban-risk posture. The constants and the
> decision order below are sensible defaults; the user adjusts them. Be more conservative by raising
> `KARMA_SAFETY_MARGIN` / `MIN_COMFORT_KARMA`; more aggressive by lowering them.

## Inputs
- From the dossier: `self_promo_policy`, `karma_gate`, `karma_gate_type`, `age_gate_days`,
  `flair_required` (`no`, or a quoted comma-list of flairs meaning one is required), `link_policy`.
- From the logged-in Chrome profile read (once per session): `comment_karma`, `post_karma`,
  `account_age_days`.
- From the ledger: `last_posted_to_sub_days_ago` (or `never`), `posts_today`.

Derived values:
- `relevant_karma` = the karma matching the sub's `karma_gate_type`
  (`comment`→comment_karma, `post`→post_karma, `combined`→comment+post, `unknown`→the *smaller* of the
  two, i.e. read it conservatively).
- `total_karma` = comment_karma + post_karma.

## Defaults (tunable constants)
```
COOLDOWN_DAYS       = 14     # min days before re-posting to the same sub
MAX_SUBS_PER_DAY    = 4      # max subs to post one article to in a day (bursts read as spam)
FRESHNESS_DAYS      = 30     # re-verify a dossier's rules if older than this
KARMA_SAFETY_MARGIN = 1.5    # want 1.5x the gate before "Ready" — avoids borderline auto-removal
MIN_COMFORT_KARMA   = 50     # below this total_karma, link-posts in unknown-gate strict subs are Risky
```
`FRESHNESS_DAYS` is applied by the skill's vetting step (re-read a dossier's live rules when it is
stale) — not by the verdict rules below.

## Decision (first match wins → verdict)
```
1.  self_promo_policy == banned                                  → No-go   ("self-promo prohibited")
2.  link_policy == text-only                                     → No-go   ("links banned even in comments — can't share the piece; use Mode 3 to build karma")
3.  posts_today >= MAX_SUBS_PER_DAY                              → No-go   ("daily burst cap reached — defer to tomorrow; no draft today")
4.  last_posted_to_sub_days_ago != never
       AND last_posted_to_sub_days_ago < COOLDOWN_DAYS          → No-go   ("on cooldown, N days left")
5.  age_gate_days known AND account_age_days < age_gate_days     → Locked  ("account too young: need X days")
6.  karma_gate known AND relevant_karma < karma_gate            → Locked  ("need X karma, have Y")
7.  karma_gate known
       AND karma_gate <= relevant_karma < karma_gate * KARMA_SAFETY_MARGIN
                                                                → Risky   ("just over the gate — borderline")
8.  karma_gate unknown AND total_karma < MIN_COMFORT_KARMA
       AND self_promo_policy in {strict, unknown}               → Risky   ("unknown gate, thin karma, strict sub")
9.  flair_required is a list AND no fitting flair identified     → Risky   ("flair required — confirm a fitting flair exists")
10. otherwise                                                   → Ready
```

## Verdict → action routing
- **Ready**  → framing selector + drafting engine (full paste-ready bundle).
- **Risky**  → draft *only* the most conservative archetype (value-first text, link-in-comment),
              prefixed with an explicit caution naming the risk; the user decides whether to use it.
              Never auto-promote Risky → Ready.
- **Locked** → karma-warming planner (no promo draft yet).
- **No-go**  → list with the exclusion reason; no draft.

## Cooldown / cadence enforcement
- Before drafting, read the ledger: compute `posts_today` (rows dated today) and
  `last_posted_to_sub_days_ago` per candidate. Apply rules 3–4 above.
- After the user confirms a submission and pastes the URL, append a ledger row with
  `cooldown_until = post_date + COOLDOWN_DAYS`.
