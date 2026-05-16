# Naming Conventions

Names matter more than they look. Pick something memorable, kebab-case-friendly, and easy to say in a chat prompt.

## Good names

- `Maya` — short, common, works across many archetypes
- `Big Mike` — descriptive nickname, instantly conveys archetype
- `Coach Sam` — role-based, signals expertise
- `Mom Jenna` — archetype-coded but personal
- `Trainer T` — initial-based, fast to type

## Bad names

- `UGC Actor 1` — generic, will drift in your memory
- `Test` — placeholder energy, you will create 12 of these
- `MariaJoseRodriguezPerez` — too long, hard to type in chat
- `Actor #34` — numbered, breaks emotional connection

## Slug rules

The skill auto-generates a kebab-case slug from the name:

- `Maya` → `maya`
- `Big Mike` → `big-mike`
- `Coach Sam` → `coach-sam`
- `Mom Jenna` → `mom-jenna`

The slug becomes the folder name and the JSON filename: `characters/big-mike.json` and `characters/big-mike/portrait.png`.

## Reserved slugs

Don't use these (they conflict with system folder patterns):

- `default`
- `current`
- `last`
- `temp`
- Any word starting with `_` or `.`

## When to make a new character vs edit an existing one

**Make a new one when:**
- Different archetype (busy-mom vs gym-bro)
- Different vibe (warm friendly vs cool professional)
- Different default scene that wouldn't make sense to swap
- You want to A/B test two faces against the same product

**Edit an existing one when:**
- Same person, refining the prompt for tighter likeness
- Adding tags so you can find them later
- Updating the default scene without changing the face

## Naming for campaigns

If you're running 10+ characters, group them with a prefix:

```
characters/
  ├── ad-maya.json
  ├── ad-big-mike.json
  ├── ad-coach-sam.json
  ├── carousel-jenna.json
  └── carousel-david.json
```

Use the prefix when calling: "use ad-maya" or "rotate through all ad-* characters."
