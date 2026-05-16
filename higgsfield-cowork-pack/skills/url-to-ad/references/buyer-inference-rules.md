# Buyer Inference Rules

Claude infers the buyer archetype from the product category, then asks you to confirm. This file lists the inference logic so you know what to expect.

## Inference table

| Product category signals | Inferred buyer |
|---|---|
| Supplements, protein powder, pre-workout, BCAA | gym-bro-twenties |
| Workout clothing, athletic wear, gym gear | gym-bro-twenties |
| Mens grooming, beard care, mens skincare | gym-bro-twenties |
| Baby products, diapers, bottles, strollers | busy-mom-thirties |
| Kitchen gadgets, meal prep, cookware | busy-mom-thirties |
| Womens skincare, beauty, makeup | busy-mom-thirties (default) or gen-z-creator (depends on price tier) |
| Wellness, supplements for mood/sleep | busy-mom-thirties |
| Tech gadgets, gaming, niche internet products | gen-z-creator |
| Books (especially fiction or self-help under $20) | gen-z-creator |
| Software subscriptions, courses, productivity tools | white-collar-professional |
| Finance products, investment apps, B2B services | white-collar-professional |
| Travel gear, hiking, camping equipment | outdoorsy-thirties |
| Pet products | varies (skill asks user) |

## How the inference works

The skill reads `source.json` and looks for category signals in:
1. The product name (e.g. "protein" → gym-bro)
2. The first 200 characters of the description
3. The brand name (some brands signal a category instantly)

If two archetypes both match, the skill picks the one with the strongest signal and tells you the alternative as a "consider also" option.

## Beauty products are the trickiest

Beauty has the widest age and demographic range of any category. The parser tries to pick up signals:

- **Mentions of "anti-aging" or skincare routines** → busy-mom-thirties
- **TikTok-coded packaging or under-$25 price** → gen-z-creator
- **Premium price ($50+) or luxury brand cues** → could be either, defaults to busy-mom-thirties

If you disagree with the inference, override it in the confirmation step. Or pre-empt the question by passing the buyer in your initial prompt: "/url-to-ad URL — buyer is gen-z-creator."

## When to override

The inference is a default. Override when:

- You know the actual customer doesn't match the obvious category (e.g. you're targeting men with a beauty product)
- The brand is repositioning (e.g. a supplement company going after busy moms instead of gym bros)
- You're testing a new audience and want different framing

## When to accept the inference

For a first-pass test ad, just accept the inferred buyer and see what comes out. If the script lands flat, re-run with a different archetype. The credit cost of one re-run is lower than the time cost of overthinking the targeting.
