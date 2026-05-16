# Install / Use Guide

## What this skill does

Paste any product URL. Wake up to a finished UGC video ad. Claude scrapes the page, pulls the hero image plus the product copy, and chains directly into the `/product-to-ad` pipeline. No manual brief filling.

## Why this matters

The slowest part of running ad campaigns is moving information between tabs. You open the product page, copy the name, save the image, paste it into a brief, type the price into your CRM. `/url-to-ad` does all of that in one step.

Pair it with a saved character via `/character-locker` and you go from URL to finished MP4 in five minutes.

## What you need

- **Claude Cowork** desktop app
- **Higgsfield MCP** connected
- A **public product URL** (not behind login)
- Same Higgsfield credit cost as `/product-to-ad`: roughly **5 to 8 credits per ad**

## Install

The skill is part of the `higgsfield-cowork-pack` plugin. Install the plugin and `/url-to-ad` shows up automatically.

## Use

In Cowork, type:
```
/url-to-ad
```
or just paste the URL:
```
/url-to-ad https://www.amazon.com/dp/B0XXX
```

Claude will:
1. Fetch the page
2. Extract the product (name, hero image, price, features)
3. Auto-fill the brief
4. Ask you only for **vibe** and **CTA** (and confirm the inferred buyer)
5. Run the rest of `/product-to-ad` with everything pre-filled
6. Save the package to `outputs/ads/<product-slug>/`

## Where to find your output

```
outputs/ads/<product-slug>/
  ├── source.json         ← URL extraction (provenance)
  ├── source-hero.png     ← downloaded hero image
  ├── from-url.md         ← receipt with the original link
  ├── brief.json          ← auto-filled brief
  ├── actor.png
  ├── scene.png
  ├── script.md
  ├── clip-01.mp4
  ├── clip-02.mp4
  ├── clip-03.mp4
  ├── caption.txt
  └── README.md
```

The first three (`source.json`, `source-hero.png`, `from-url.md`) are unique to this skill. Everything else is the standard `/product-to-ad` output.

## Supported domains

Best-supported (parser fills in all fields automatically):

- **Amazon** — `amazon.com/*/dp/*` and short links
- **Shopify stores** — `*.myshopify.com` plus any custom domain with `/products/` URL pattern
- **TikTok Shop** — public product pages
- **eBay** — listing pages

Unknown domains will work but the parser may miss fields. Claude will flag what it couldn't extract and ask you to fill in the gaps.

## Common issues

**"Couldn't fetch the page."**
The URL is behind a login or paywall. Either the page returns a 403 (blocked) or 401 (auth required). Two options:

1. Open the page yourself, copy the title plus first paragraph, and pass that to `/product-to-ad` directly with the saved hero image.
2. Use the Chrome MCP if you have it connected: `mcp__Claude_in_Chrome__navigate` works on logged-in pages.

**"The hero image came back small or low-res."**
Some product pages serve a tiny thumbnail as `og:image`. The parser falls back to the first large `<img>` near the headline. If both are small, the rendered scene will have a blurry product. Fix: download the high-res image manually and pass it to `/product-to-ad` directly.

**"The script makes claims that aren't true about the product."**
The script is generated from the page's marketing copy. If the page has misleading or vague copy, the script inherits the issue. Edit the script in `script.md` before recording, or constrain it by editing `brief.json` and re-running.

**"The buyer archetype it picked doesn't match the actual audience."**
The skill infers the buyer from the product category, then asks you to confirm. If you skipped the confirmation prompt or accepted a wrong default, edit `brief.json` and re-run with the right archetype.

## Pairs well with

- `/character-locker` — pass a saved character: `use Maya for this URL`
- `/product-to-ad` — `/url-to-ad` is just `/product-to-ad` with the brief auto-filled
- `/overnight-content` — feed a list of URLs as the source for nightly runs

## Cost per ad

Same as `/product-to-ad`: about **5 to 8 Higgsfield credits per finished ad**. The URL fetch itself is free.

## Privacy note

The skill saves the original URL plus the extracted page snapshot to `source.json`. If you don't want that paper trail (some affiliates have weird rules about caching product pages), delete `source.json` after the ad renders. The video itself doesn't reference the URL.
