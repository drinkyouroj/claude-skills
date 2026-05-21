# Vibe Query Templates

How the skill composes a search query for `ai-image-prompts-skill` at Gate 1. The query's job is to surface 2–3 thumbnail-shaped library candidates that match the dispatch's subject and mood.

## Query shape

```
illustrated editorial YouTube thumbnail, [dispatch subject 3–6 words], [mood adjectives 2–3], [composition hint], character-driven, magazine style
```

## Dispatch-subject extraction

Pull from the narration in this order:
1. The cold-open candidate's most punchable noun phrase.
2. The article's primary named entity if more concrete.
3. The dispatch slug if both are abstract.

Examples:
- Dispatch-004 cold open → "Helium hotspot earnings dispute"
- Dispatch about FAA + drones → "FAA drone airspace contest"
- Abstract policy dispatch → fall back to slug, e.g. "public broadband privatization"

## Mood adjective vocabulary

Pick 2–3 from this list that match the dispatch's emotional register. Do NOT invent moods outside this list — the library is best at common moods.

- dramatic
- editorial
- moody
- cinematic
- noir
- documentary
- conspiracy-thriller
- analytical
- investigative
- archival
- vaporwave-tech
- apocalyptic-tech
- corporate-dystopian
- quiet-dread

## Composition hint vocabulary

Pick one. Affects what kind of library candidate the search surfaces.

- mid-shot
- close-up portrait
- over-the-shoulder
- wide environmental
- top-down
- split-screen comparison

## Query patterns to avoid

- Too generic: "YouTube thumbnail, civic infrastructure" (returns noise).
- Single-word vibe: "moody" alone is not enough; pair with a subject.
- Brand names that the library won't have proven prompts for: "Helium-Network-specific Helium-style thumbnail" — instead use generic descriptors the library knows.
- Negations: "no clutter, no text" — library search is positive-keyword-driven.

## Example transformations

### Dispatch-004 (Helium / Nova Labs)

Cold open: "I bought a $499 hotspot to mine WiFi tokens. Nova Labs owns what it earns."

Composed query:
```
illustrated editorial YouTube thumbnail, hotspot earnings dispute, dramatic, investigative, mid-shot, character-driven, magazine style
```

### Hypothetical dispatch on FAA + drone airspace

Cold open: "The FAA quietly carved out a corridor over Austin. Nobody told the people who live under it."

Composed query:
```
illustrated editorial YouTube thumbnail, FAA drone corridor, conspiracy-thriller, moody, wide environmental, character-driven, magazine style
```

## How the skill uses this file

At step 4 (compose the library query), the skill:

1. Loads this file's contents.
2. Extracts the dispatch subject per the order above.
3. Picks 2–3 mood adjectives from the vocabulary.
4. Picks one composition hint from the vocabulary.
5. Composes the query string per the shape.
6. Passes the query to `ai-image-prompts-skill` via the Skill tool.

If the query returns zero usable candidates, the skill skips Gate 1 silently and proceeds to headline drafting (per spec §11).
