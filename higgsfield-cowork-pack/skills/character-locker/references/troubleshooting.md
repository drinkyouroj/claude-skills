# Troubleshooting

Quick fixes for the issues that come up most often. If you hit something not on this list, the SKILL.md describes the full workflow and where each step happens.

## "The job_id verification failed."

You imported a Higgsfield job_id that the API can't find. Two causes:

1. **The job is older than 90 days.** Higgsfield expires raw URLs after 90 days. The job still exists in your account, but the import path can't fetch it. Re-render with the saved soul_prompt instead.
2. **You typo'd the UUID.** Double-check you copied the full job_id, no leading or trailing characters.

## "The portrait looks completely different than the archetype."

The archetype provides the seed prompt. Your `specifics` field overrides it. If you wrote specifics that contradict the archetype, the specifics win.

Example: if you pick `gym-bro-twenties` (which assumes athletic, lean, 25-y-o) but write `specifics: 50-year-old businessman in a suit`, you get a 50-year-old in a suit, not a gym bro.

Fix: either pick a different archetype or pull the contradiction out of specifics.

## "The face changes between generations even though I called the saved character."

Three possible causes:

1. **You're not actually passing the saved job_id.** Confirm by checking the chat log. The skill should reference `characters/<slug>.json` before generating.
2. **The job_id expired** (see first issue).
3. **The downstream skill is composing the saved face with another reference image** (e.g. /product-to-ad uses both the actor and the product). Some drift between scene compositions is normal. The face should still feel like the same person.

If you want pixel-perfect consistency, generate a few scenes with the saved actor and pin one job_id to use as the locked composition reference for all future ads.

## "I saved the character but other skills don't recognize them by name."

The other skills look in `characters/<slug>.json` (kebab-case). If your name was `Big Mike`, the slug is `big-mike` and you'd say "use big-mike" or "use Big Mike" — both work because the skill normalizes the name to slug before lookup.

If still no match, list what's saved:
```
/character-locker — list my saved characters
```

## "The soul_prompt I saved looks generic."

The skill generates the prompt by combining the archetype block from `references/archetypes-quick.md` with your `specifics`. If your specifics were sparse, the prompt is sparse.

Fix: edit `characters/<slug>.json` directly. Replace the `soul_prompt` field with a richer prompt. The next regeneration uses your updated prompt.

## "I want to A/B test two faces against the same product."

Save both characters. Run `/product-to-ad` twice with the same product image, once with each character. Compare the outputs side by side.

## "Can the skill generate a character from a real photo?"

Not with the default `soul_cast` model (text-only). For real-face UGC, use Higgsfield SOUL 2 (which accepts a face reference photo) — that's a different workflow, not handled by this skill. You'd:
1. Upload your face photo to Higgsfield manually
2. Run a SOUL 2 generation with the face as a reference
3. Take the resulting job_id
4. Use the import path of `/character-locker` to save it as a profile

## "The portrait was perfect but I lost the file."

If the JSON is gone:
- Check `characters/` for any `.json` files
- Check Higgsfield's web app — every job is in your account history forever (even if the URL expires)
- Take the job_id from Higgsfield's UI and use the import path to save a fresh profile

If the PNG is gone but the JSON exists:
- The `higgsfield.raw_url` in the JSON points to the original. If it's still within 90 days, download it.
- If past 90 days, run `/character-locker` regenerate to render a fresh portrait from the saved soul_prompt.
