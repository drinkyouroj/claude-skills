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

---

## Inputs

When invoked by `tcn-content-plan` Step 7.5, this skill receives:

1. **`purpose`** — one of: `Awareness`, `Engagement`, `Soft funnel`, `Flagship CTA`. Required. The orchestrator derives this from the day's `facebook_purpose:` frontmatter (set in Step 3 of Mode 2).
2. **`source_material`** — conditional on purpose:
   - **Funnel/Flagship:** the day's X standalone option text (from Step 5 output) + flagship article URL + flagship article tagline (when available)
   - **Awareness/Engagement:** today's live news (from Step 1 of Mode 2) + FRESH list (from Step 2 duplication audit)
3. **`spent_list`** — the SPENT list from Step 2 of Mode 2. Required. Used to avoid echoing what other surfaces already said.
4. **`flagship_url`** — present only on Flagship CTA and Soft funnel days. The full URL of the article being linked.
5. **`date`** — today's date (YYYY-MM-DD) for the schedule slot.

When invoked directly (not via the orchestrator), prompt the user for any missing inputs before drafting.

## Outputs

A markdown block in the following structure, returned to the orchestrator for insertion into the daily plan file under `## Facebook`:

```markdown
**Purpose:** [Awareness | Engagement | Soft funnel | Flagship CTA]
**Shape:** [Caption | Paragraph]
**Posting time:** [HH:MM ET]

### Option A — [Safe | News-dependent]
[FB post prose]

**Image:** [concrete instruction — AI prompt text, Substack hero URL, or screenshot recommendation]

### Option B — [Safe | News-dependent]
[FB post prose]

**Image:** [concrete instruction]

### Option C — [Safe | News-dependent]
[FB post prose]

**Image:** [concrete instruction]

**Recommendation:** [one sentence — default option + conditional logic if any option is News-dependent]
```

Always produce 2-3 options. Single-option output is a quality-bar failure.
