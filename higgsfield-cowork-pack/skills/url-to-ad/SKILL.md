---
name: url-to-ad
description: Paste any product URL. Get back a finished UGC video ad. Claude scrapes the product page, pulls the hero image plus the marketing copy, then chains into the /product-to-ad pipeline to render the actor, scene, script, and video. Use this skill when the user says "url to ad", "make an ad from this link", "this product page", "Amazon link to ad", "Shopify URL to ad", "scrape this product", or pastes a product URL and asks for a marketing video. Powered by Higgsfield via the MCP.
---

# URL to Ad

Paste a product URL. Wake up to an ad. End-to-end. Zero copy-paste between tabs.

## What this skill does (in one breath)

1. Fetches the product page
2. Pulls the hero image, name, price, and bullet features
3. Hands the package off to `/product-to-ad` with everything pre-filled
4. Saves the finished ad to `outputs/ads/<slug>/`

By the end the user has the same finished folder as `/product-to-ad`, with no manual brief filling.

## Setup the user needs

- Higgsfield MCP connected.
- The product URL must be public (not behind login or paywall).
- Same Higgsfield credit cost as `/product-to-ad` (5 to 8 credits).

## Process

### Step 1: Take the URL

The user will either paste a URL directly into chat or invoke `/url-to-ad <url>`. If no URL is provided, ask via AskUserQuestion (one open text question).

Validate the URL:
- Must start with `https://`
- Domain should be on the supported list: Amazon (`amazon.com/*/dp/*`), Shopify stores (`*.myshopify.com` or any store with `/products/`), TikTok Shop, eBay, plus generic e-commerce. If the domain is unknown, proceed but warn the user that the parser may miss fields.

### Step 2: Fetch the page

Use `mcp__workspace__web_fetch` to load the URL. If the host is on the egress allowlist, this works directly. If not, fall back to:
- `mcp__Claude_in_Chrome__navigate` + `read_page` if the user has the Chrome extension connected
- Or ask the user to open the page and paste the title + description manually

### Step 3: Extract the product data

From the page HTML, pull:
- **Product name** — meta `og:title` or `<h1>`
- **Hero image URL** — meta `og:image` or the first large `<img>` near the title
- **Price** — look for `$` followed by digits, or schema.org `Product/offers`
- **Description / features** — meta `og:description`, plus the first 5 bullet points
- **Brand** — meta `product:brand` or domain name
- **Color / variant** — first variant option if present

If the hero image URL is not on Higgsfield's allowed import hosts, download it (via `web_fetch` if allowlisted, or ask the user to download and re-upload).

Save the extraction to `outputs/ads/<slug>/source.json`:

```json
{
  "url": "https://...",
  "fetched_at": "2026-04-29T13:00:00Z",
  "product": {
    "name": "...",
    "hero_image_url": "...",
    "hero_image_local_path": "outputs/ads/<slug>/source-hero.png",
    "price": "$24.99",
    "description": "...",
    "features": ["...", "...", "..."],
    "brand": "..."
  }
}
```

### Step 4: Pre-fill the product-to-ad brief

Build the brief from `source.json` so the user does NOT have to fill it again:

- `product.name` → product name from URL
- `product.image_path` → local path to the downloaded hero
- `product.what_it_is` → first sentence of the description
- `product.what_it_does` → outcome inferred from the features (Claude writes this)
- `product.price` → price string
- `buyer.archetype` → inferred from the product category (e.g. supplement → gym-bro-twenties; baby gear → busy-mom-thirties). Confirm with user before generating.
- `vibe` → ask the user, do not infer.
- `cta.type` → default to `link-in-bio` for influencer-style ads, but ask.

### Step 5: Hand off to /product-to-ad

Trigger `/product-to-ad` with the pre-filled brief. Skip the four-question intake (Step 1 of that skill) since this skill already filled everything in. Resume at Step 2 (vision check on the product image).

The output folder is the same: `outputs/ads/<slug>/`. The brief shows the `source.json` reference so the user can trace back.

### Step 6: Add the URL receipt to the package

Append a small `from-url.md` file to the output folder:

```markdown
# Ad Source

This ad was generated from:
**[Product Name](https://...)**

- Brand: ...
- Price: $24.99
- Fetched: 2026-04-29

Original page snapshot saved to `source.json`.
```

This gives the user provenance if they ever need to verify claims in the ad against the product page.

## Rules

- ALWAYS save `source.json` so the brief can be re-used.
- ALWAYS warn the user if the page domain is unknown — the parser may miss fields.
- NEVER make claims in the script that are not supported by the product page (price, features, ingredients). The script can be playful, but specific claims must trace back to `source.json`.
- NEVER scrape pages behind a login or paywall. If `web_fetch` returns 401 or 403, stop and ask the user to copy-paste the product details.
- 9:16 video, same as `/product-to-ad`.

## Output structure

```
outputs/ads/<slug>/
  ├── source.json         ← full extraction from URL
  ├── source-hero.png     ← downloaded hero image
  ├── from-url.md         ← provenance receipt
  ├── brief.json          ← pre-filled brief (handed to product-to-ad)
  ├── actor.png
  ├── scene.png
  ├── script.md
  ├── clip-01.mp4
  ├── clip-02.mp4
  ├── clip-03.mp4
  ├── caption.txt
  └── README.md
```

## When NOT to use this skill

- The user already has a clean product image on disk — go straight to `/product-to-ad`.
- The product is custom or local (not on a website) — `/product-to-ad`.
- The page is behind login — copy-paste the description into `/product-to-ad` instead.
