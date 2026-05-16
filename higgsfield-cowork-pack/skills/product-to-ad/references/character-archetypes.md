# UGC Character Archetypes (SOUL Prompts)

Match the character to the buyer. The closer the actor looks like the target customer, the higher the conversion.

Use these as the seed prompt for `soul_cast` (text-to-image character). Tweak the specifics (skin tone, region, age) to match the audience.

## How to use

When the user picks a buyer in the brief, drop the matching archetype block into the SOUL prompt. Add the product setting at the end. Aspect ratio always `9:16`. Resolution `2k`.

---

## Gym-bro twenties

Best for: supplements, workout gear, mens grooming, athletic apparel, nutrition products.

```
A 25-year-old man, athletic build, fitted gray gym tank, short messy
brown hair, light stubble, friendly relaxed smile, slight tan,
holding a phone arm's length to record himself. Standing in a clean
modern home gym with soft natural window light. Casual UGC style,
9:16 vertical, photorealistic, slight handheld feel. No filter look.
```

Variants: switch to "30-year-old", "Black", "Latino", "South Asian", etc. to match the audience.

---

## Busy-mom thirties

Best for: kitchen gadgets, parenting products, household, beauty, supplements, organization.

```
A 34-year-old woman, warm friendly face, hair in a low messy bun,
oversized cream cardigan over a simple t-shirt, light makeup, slight
tired-but-happy expression, holding her phone arm's length. Standing
in a sunlit kitchen with a coffee cup on the counter behind her.
Casual UGC style, 9:16 vertical, photorealistic, slight handheld
feel. No filter look.
```

Variants: switch the setting to bathroom mirror, car driver seat, walking the kids in, etc.

---

## Gen-Z creator

Best for: tech, fashion, beauty, food, niche internet products.

```
A 22-year-old, expressive face, slight smirk, layered necklaces,
oversized vintage band t-shirt, baggy jeans, dyed hair (pick one:
soft pink, platinum, dark brown with chunky highlights), sitting
cross-legged on a bed in a bedroom with string lights, posters, and
a Lava lamp. Holding phone arm's length. Casual UGC style, 9:16
vertical, photorealistic, slight handheld feel. Slight Gen-Z fish-
eye lens vibe.
```

Variants: car selfie angle, bathroom mirror, coffee shop window seat.

---

## White-collar professional

Best for: software, productivity tools, books, courses, finance products, B2B.

```
A 32-year-old, neat appearance, fitted button-up in a neutral color
(white, light blue, or oat), thin-framed glasses, hair styled but
relaxed, sitting in a modern home office with a clean desk, a plant,
and a monitor visible behind them. Holding phone arm's length, soft
overhead daylight. Casual but polished UGC style, 9:16 vertical,
photorealistic. Less handheld shake than other archetypes.
```

Variants: standing in front of a brick wall, leaning against a
kitchen island in a nice apartment, walking through a co-working
space.

---

## Outdoorsy thirties

Best for: travel gear, camping, wellness, hiking, fitness apps,
recovery products.

```
A 31-year-old, weathered tan, sun-bleached hair, simple performance
t-shirt and a vest, standing on a hiking trail or rooftop with
mountain or city skyline in the background, golden hour light,
slight wind in the hair. Holding phone arm's length. UGC style, 9:16
vertical, photorealistic, soft handheld feel.
```

---

## Kid / teen (USE WITH CAUTION)

Skip this archetype unless the product is explicitly for under-18s
(school supplies, sports equipment, etc.). For most products, use
the "gen-z creator" archetype with a 19+ specification instead.

---

## Senior

Best for: health products, mobility, hobbies, gardening, kitchen
gadgets that "just work".

```
A 67-year-old, kind expression, simple polo shirt or cardigan,
neatly combed hair, holding phone with two hands at chest level (not
arm's length, more deliberate), sitting in a sunlit living room or
kitchen with personal touches (family photos, plants, a tea cup).
UGC style but slower, more grounded camera. 9:16 vertical,
photorealistic.
```

---

## Diversity defaults

By default, generate a mix of skin tones, body types, and ages
across an ad campaign. Never default the actor to white unless the
product is geographically specific. The buyer prompt in the brief
overrides everything.

## Consistency tip

Once you generate an actor you like, save the Higgsfield job_id in
`characters/<archetype>-<name>.json` so the next ad in the same
campaign can reuse the exact face. This is what `/character-locker`
does. Until that skill ships, you can hand-save the job_id by
writing it to a file yourself.
