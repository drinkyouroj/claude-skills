---
name: tcn-facebook-post
description: >
  Draft a daily Facebook post for The Civic Node (TCN) — one post per day, plain-English
  voice, image-forward, image-required on caption-shape posts. Sister skill invoked by
  tcn-content-plan Step 7.5. Use this skill whenever the user (or the orchestrator) asks
  for "the FB post", "facebook copy", "today's facebook post", "draft the FB for [date]",
  "facebook caption", "facebook paragraph", or any TCN Facebook content. Also use when the
  orchestrator delegates Step 7.5 of Mode 2 with a purpose label. Produces 2-3 options per
  slot, each tagged Safe / News-dependent, each with concrete image guidance (AI prompt,
  Substack hero URL, or screenshot recommendation). Does NOT own the weekday rotation
  (tcn-content-plan does), does NOT own the monthly-plan override (tcn-content-plan does),
  does NOT replace tcn-post or tcn-substack-notes (those run on different surfaces).
---

# tcn-facebook-post

The Facebook drafting skill for The Civic Node. One FB post per day, seven days a week. Plain-English voice, low cognitive load, image-forward — calibrated for an audience used to scrolling kitten pictures, not parsing analytical takes.

This skill is invoked by `tcn-content-plan` Step 7.5 in Mode 2 (Create Daily Plan). It can also be invoked directly if the user just wants today's FB post without a full daily plan.

## What this skill owns

- FB-Explainer voice rules (see `references/voice-register.md`)
- Purpose → shape mapping (caption vs. paragraph)
- Purpose → image-source mapping (see `references/purpose-table.md`)
- Option generation (2-3 options per slot)
- Shelf-life labeling (Safe / News-dependent — two-state, NOT the three-state Frame-forward/Data-forward/Conditional used for X and Notes)
- Image prompt drafting (delegates to `ai-image-prompts-skill` for AI-generated; constructs prompt text directly)

## What this skill does NOT own

- The weekday rotation lookup (`tcn-content-plan` owns)
- The monthly-plan `FB:` override (`tcn-content-plan` reads this from the 30-day map)
- The X copy, Substack Note copy, or LinkedIn copy
- The schedule table or Status block formatting (`tcn-content-plan` owns the daily plan file)
- Voice-passes on other surfaces — `tcn-text-humanizer` handles X/Notes; this skill is self-contained on voice
