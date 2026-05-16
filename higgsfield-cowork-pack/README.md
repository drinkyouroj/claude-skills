# Higgsfield Cowork Pack

End-to-end UGC ad and content pipeline powered by Higgsfield via the Higgsfield MCP. Designed to run inside Claude Cowork with zero external API setup.

## What's inside

| Skill | What it does |
| --- | --- |
| `setup-higgsfield-project` | One-time project init — generates a tailored `CLAUDE.md` that locks brand voice, default character, output folders, models, and aspect ratios. Run this first. |
| `character-locker` | Save a UGC actor as a reusable character profile so every future ad uses the exact same face, outfit, and vibe. |
| `product-to-ad` | Drop in a product image. Get back a finished UGC video ad — actor, scene, script, MP4. |
| `url-to-ad` | Paste a product URL. Claude scrapes the page and chains into the `product-to-ad` pipeline. |
| `ig-carousel` | Premium 4:5 Instagram carousels with a cinematic cover plus content slides that share the same photoreal world. |
| `overnight-content` | Schedule the full ad pipeline to run while you sleep. Wake up to a folder of fresh ads every morning. |

## Requirements

- Claude Cowork
- Higgsfield MCP connected (provides SOUL, Nano Banana Pro, and Higgsfield Video)

## Recommended order

1. `setup-higgsfield-project` — lock your project defaults
2. `character-locker` — save your hero UGC actor
3. `product-to-ad` or `url-to-ad` — make ads
4. `ig-carousel` — repurpose to social
5. `overnight-content` — automate the whole loop

## Install

Upload the zipped plugin folder into Claude Cowork as-is — do not unzip first.
