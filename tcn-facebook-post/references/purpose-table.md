# Facebook Purpose Table — Reference

Canonical mapping for FB post purpose → shape → image source → voice notes → CTA rule. This is the single source of truth referenced by `tcn-facebook-post/SKILL.md` and `tcn-content-plan/references/posting-rules.md`.

## The four purposes

| Purpose | Shape | Image source | Voice notes | CTA rule |
|---|---|---|---|---|
| **Awareness** | Caption (≤30 words) | AI-generated (via `ai-image-prompts-skill`) | Soft, observational. Drop closed em dashes entirely. One warmth-marker max ("honestly," / "look," / "the thing is"). No edge. | No link |
| **Engagement** | Caption (≤30 words) | AI-generated | Question-framing or "tell me in the comments" pattern. Active second person OK. Designed for FB algorithm comment-signal. | No link |
| **Soft funnel** | Paragraph (50-80 words) | Substack article hero from the older piece referenced (URL specified in monthly plan's `Brief note` cell, or surfaced by `tcn-content-plan` Step 1 prompt when no monthly entry) — AI-generated fallback only if no usable hero exists | Slight authority. 1 closed em dash max. Plain-English summary of the older piece's argument. | Soft link: "wrote about this back in [month] — [link]" |
| **Flagship CTA** | Paragraph (50-80 words) | Substack article hero (today's piece) | Slight authority. Plain-English tagline of the flagship's argument. No "predictably," "naturally," "of course." | Hard link at end: "Full piece: [link]" |

## Shape rules

### Caption (Awareness, Engagement)

- ≤30 words total
- Image is **required** — no caption ships without an image
- Closed em dashes: forbidden (read as trying-too-hard at this length)
- Sentences: 1-3 short ones
- No CTA, no link
- One warmth-marker max ("honestly," / "look," / "the thing is")

### Paragraph (Soft funnel, Flagship CTA)

- 50-80 words total (hard fail outside this range)
- Image is recommended (Substack hero preferred); not strictly required if no hero exists
- Closed em dashes: max 1 per post
- Sentences: 2-4
- CTA placement: end of post, on its own line for Flagship CTA; inline for Soft funnel

## Image source rules

### AI-generated (Awareness, Engagement)

Invoke `ai-image-prompts-skill` to draft the prompt. The prompt must:
- Be ≤80 words
- Reference the post's subject concretely (numbers visible, scene specific)
- Avoid generic stock-photo language ("business people in a meeting," "abstract concept of growth")
- Be safe for Facebook's content policies (no political party logos, no copyrighted figures by name without context)

### Substack hero (Soft funnel, Flagship CTA)

- Flagship CTA: the article's published hero image, fetched from the published article URL
- Soft funnel: the older referenced piece's hero, URL specified in monthly plan
- If hero image not available, fall back to AI-generated (surface the gap in the recommendation)

### Stock-photo fallback

Triggered only if:
- `ai-image-prompts-skill` is not available
- Substack hero not retrievable

Format: a one-line search-query suggestion ("freeway gridlock at dusk, no logos") that Justin pastes into Unsplash/Pexels.

## Weekday rotation (default)

Used by `tcn-content-plan` Step 3 when the monthly plan's `FB:` cell is absent.

| Day | Purpose | Rationale |
|---|---|---|
| Monday | Awareness | Week opens soft — plain observation about weekend or week ahead. |
| Tuesday | Engagement | Tuesday FB engagement historically strong; comment signal early in the week. |
| Wednesday | Awareness | Mid-week observation. Wednesday is also paid Substack note day — deliberately not funneling so the two don't compete. |
| Thursday | Soft funnel | Tease Friday's flagship — "writing about X for Friday." |
| Friday | Flagship CTA | Article link + plain-English tagline. Hard funnel. |
| Saturday | Awareness | Weekend FB usage high but cognitive load low. |
| Sunday | Soft funnel | Resurface older Substack piece relevant to the week's news. |

## Posting time defaults

| Purpose | Default posting time | Fallback |
|---|---|---|
| Awareness | 09:00 ET | 19:00-21:00 ET |
| Engagement | 09:00 ET (high engagement window) | 19:00-21:00 ET |
| Soft funnel | 09:00 ET | 19:00-21:00 ET |
| Flagship CTA | 11:00-13:00 ET (must be after article publishes) | Same-day evening if AM missed |

Hard rule: never post Flagship CTA before the article is live. Out-of-order publishing breaks the funnel.
