# Voice Archetypes

Four pre-built brand voices the user can pick from in step 3. Each one expands into a specific block in the generated CLAUDE.md.

## warm-friendly

Best for: lifestyle, wellness, parenting, beauty, food brands.

```
- Talk to the reader like a friend over coffee
- Warm, encouraging, never judgmental
- Use "we" and "us" sometimes, but mostly "you"
- Soft humor, never sarcasm
- Lead with empathy, then solution
```

## sarcastic-witty

Best for: gen-z products, niche internet, anything where the audience is in on the joke.

```
- Self-aware about being an ad
- Drop pop-culture references when natural
- Punch up, never down
- Short sentences, sharp asides
- "Tell me why I just bought this" energy
```

## calm-educational

Best for: courses, books, tools, B2B, anything where the buyer needs to feel smart.

```
- Authority without arrogance
- Lead with the insight, then the product
- Cite specifics: numbers, names, timelines
- Never hype-y, never vague
- Treat the reader as already informed
```

## professional-polished

Best for: software, finance, services, premium brands.

```
- Confident but not loud
- Plain English with occasional industry term (defined)
- Lead with the outcome, not the process
- Short paragraphs, scannable bullets
- No exclamation points, no all-caps
```

## free-text override

If the user picks "none of these fit, let me describe it," capture their words verbatim and inject them into the voice block of CLAUDE.md. Do NOT editorialize or expand.

Example user override:
> "Like a hot best friend with a degree in marketing"

Goes into CLAUDE.md as:
```
- Voice: Like a hot best friend with a degree in marketing
- Hard voice rules from the pack still apply (no em dashes, 5th-grade reading level, etc.)
```

## Why preset

Most users don't know how to describe a brand voice. Picking from 4 named archetypes is faster, more accurate, and produces better CLAUDE.md output than asking them to free-write. The override exists for users who already have a clear voice locked in.
