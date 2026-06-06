# Self-Promo Playbook — framing map + Reddit culture rules

## Hard rules (non-negotiable — repeated from SKILL.md)
- **Honest authorship only.** First-person, truthful attribution. Never pose as a third party who
  "found" the piece. Never astroturf.
- **No manipulation.** No vote brigading, no sockpuppets, no ban evasion, no posting where a sub
  bans self-promotion outright (`eligibility-rules.md` enforces this as rule 1).
- **Member first.** Reddit's norm is roughly the 9:1 / 10% rule — your own links should be a small
  fraction of your activity in a community. A link from an account with no history in the sub reads
  as spam and is often auto-removed.

## Framing archetypes
- **transparent-author** — open "I wrote a piece on X" framing, link as the post itself.
- **thread-targeted** — post into the sub's recurring self-promo / share thread, transparently.
- **question-led** — lead with the article's sharpest finding as a genuine discussion prompt; put the
  link in your own first comment, framed as "I went deeper on this here."
- **value-first** — a self-contained, genuinely useful text post that stands alone even if nobody
  clicks; link in a first comment as a footnote, not the headline.

## ▶ TUNE ME — policy → archetype map
> This map encodes how aggressive the user is willing to be per rule signal. These are working
> defaults; the user adjusts the right-hand column.

```
self_promo_policy   →  archetype           link placement
-----------------------------------------------------------------
promo-friendly      →  transparent-author   link as post
promo-thread        →  thread-targeted      link in the self-promo thread
discussion-heavy    →  question-led         link in first comment
strict              →  value-first          link in first comment
unknown             →  value-first          link in first comment   (treat as strict until confirmed)
banned              →  (no draft)           —                       (No-go; see eligibility-rules.md)
```

## Link placement respects `link_policy`
The archetype's default link placement above is a *preference*, not an override. Reconcile it with the
dossier's `link_policy` before drafting, per archetype:
- **transparent-author** wants a top-level link-post — allowed only when `link_policy` is `link-post`
  or `either`. If `link_policy` is `text+comment`, downgrade to a text post with the link in your own
  first comment (and draft that comment — see below).
- **thread-targeted** posts a comment *inside* the sub's share thread, so the link always goes in that
  comment; it is not a top-level submission, so `link-post` vs `text+comment` does not apply.
- **question-led** and **value-first** already place the link in a first comment by design.
- `text-only` (links banned even in comments) → eligibility already marks this No-go (see
  `eligibility-rules.md`); don't draft a promo post.

## Link-in-comment tactic (why it exists)
Many subs auto-filter link-posts from low-history accounts but allow text posts. Leading with a text
post that delivers value, then dropping the Substack link in your own first comment, both respects the
community and survives spam filters. Whenever a bundle's link placement is "link in first comment" —
the archetype default (question-led, value-first) or a `text+comment` downgrade of transparent-author —
draft that first comment as part of the bundle.

## What the skill must show the user
For each Ready/Risky sub, state which archetype was selected **and the rule signal that selected it**
(e.g. "strict no-self-promo rule → value-first, link-in-comment"). The user approves before posting.
