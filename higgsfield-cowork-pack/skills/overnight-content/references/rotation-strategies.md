# Rotation Strategies

How to pick what gets generated each night when you have multiple products, multiple characters, and multiple vibes.

## The four rotation knobs

Each campaign config has four things that can rotate:

1. **Product** (which item gets the ad)
2. **Character** (which face holds it)
3. **Vibe** (excited, calm, sarcastic, soft)
4. **Scene** (kitchen, bathroom, gym, etc.)

The skill rotates them independently. So a 30-night campaign with 4 vibes, 5 characters, and 10 products can produce 200+ unique combinations without repeating.

## Three rotation modes

### Round-robin (default)
Walks through the source list in order, day by day. Predictable, easy to debug.

```json
"source": { "type": "products-folder", "products_folder": "inputs/products/" },
"ads_per_night": 1
```

Day 1: product 1. Day 2: product 2. Day 3: product 3. Wraps when the list ends.

### Random
Picks randomly from the source pool. Better for split-testing because you avoid systematic biases.

```json
"rotation_mode": "random",
"random_seed": "campaign-slug-2026-04"
```

Use a fixed `random_seed` so reruns are reproducible. Don't use real random — debugging "why did Tuesday produce two of the same product" is annoying.

### Weighted
Prioritize certain products or characters. Useful if you have one hero product and a few secondary products.

```json
"rotation_mode": "weighted",
"weights": {
  "ice-roller": 5,
  "pillow-mist": 2,
  "hand-cream": 1
}
```

Day 1 to 5: ice-roller (5x weight). Day 6 to 7: pillow-mist (2x). Day 8: hand-cream (1x). Cycle repeats.

## Character rotation

### Single character (lock-in)
Best for: brand consistency, building a recognizable face.
```json
"characters": { "mode": "saved", "saved_slug": "maya" }
```

### Rotate through a saved pool
Best for: testing which face converts best, or running multi-persona campaigns.
```json
"characters": {
  "mode": "rotate-saved",
  "rotation_pool": ["maya", "big-mike", "coach-sam"]
}
```

### Generate fresh each night
Best for: variety-driven campaigns where character drift is a feature, not a bug.
```json
"characters": { "mode": "new-each-night" }
```
Costs an extra credit per night for the SOUL generation.

## Vibe rotation

Almost always rotate. Variety in tone is what makes a campaign feel alive vs spammy.

```json
"vibes": ["excited-high-energy", "sarcastic-funny", "calm-educational"]
```

Day 1: excited. Day 2: sarcastic. Day 3: calm. Day 4: excited. And so on.

If you only want one tone, list one. The skill won't complain.

## Anti-patterns

**Don't rotate everything at once with a small pool.** If you have 3 products, 2 characters, and 3 vibes, rotation gives you 18 combinations but you'll see the same product+character+vibe within 18 days. Either grow the pool or accept the repetition.

**Don't rotate scenes if the product needs a specific setting.** A pre-workout supplement filmed in a sunlit kitchen looks weird. If your product has a clear scene match, fix it in the brief and only rotate the vibe.

**Don't generate fresh characters every night for a 30-day campaign.** That's 30 different faces. Your audience won't form recognition. Save 2 to 4 characters and rotate them.

## Practical defaults

For most users, this config works:
```json
{
  "rotation_mode": "round-robin",
  "ads_per_night": 1,
  "characters": { "mode": "saved", "saved_slug": "maya" },
  "vibes": ["excited-high-energy", "sarcastic-funny"],
  "schedule": { "run_time_local": "02:00" }
}
```

One ad per night, locked character, rotated vibe. Predictable, brand-consistent, varied tone.

Only get fancy with weights and random when you have data showing the simple version isn't working.
