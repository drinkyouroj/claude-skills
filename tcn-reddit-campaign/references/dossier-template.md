# Subreddit Dossier Schema

A dossier is the cached, ground-truthed record for a single subreddit. The skill writes one
per sub at `…/workspace/reddit-campaign/dossiers/r-<sub>.md` and reuses it across articles.
Refresh a dossier (re-read the live rules via Chrome) when `last_refreshed` is older than the
freshness window (see `eligibility-rules.md` for the window).

## Schema

```
---
sub: r/<name>
last_refreshed: YYYY-MM-DD
self_promo_policy: strict | promo-friendly | discussion-heavy | promo-thread | banned | unknown
karma_gate: <number or unknown>          # karma minimum to post (note type below)
karma_gate_type: comment | post | combined | unknown
age_gate_days: <number or unknown>       # account-age minimum to post
flair_required: no | "Advice, Meta, OC"  # 'no' = none; a quoted comma-list = required, pick one
link_policy: link-post | text+comment | either | text-only
best_time_notes: <freeform — when this sub is active, mod-removal patterns, etc.>
---

## Rules summary
- <bulleted, live rules that bear on self-promo, links, flair, formatting, AI content>

## My history here
| date | article slug | framing | url | outcome |
|------|--------------|---------|-----|---------|
```

## Field notes
- `self_promo_policy` is the routing key into `self-promo-playbook.md`. When unsure, record `unknown`
  (the eligibility logic treats `unknown` conservatively).
- `karma_gate` + `karma_gate_type`: many subs gate on *comment* karma specifically. Record the type so
  the eligibility check compares against the right number.
- `link_policy: text-only` means links are banned everywhere in the sub (even in comments) — the piece
  can't be shared there at all, so it's a promotion No-go (still usable for karma-building via Mode 3).
- `outcome` in the history table is optional and filled in later (upvotes / removed? / comment count);
  it is never required to complete a session.
