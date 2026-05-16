# Supported Domains

Detailed parser behavior per domain. Use this to predict what the skill will extract before you run it.

## Tier 1: full extraction (every field auto-fills)

### Amazon
- **URL patterns**: `amazon.com/*/dp/*`, `a.co/*` (short links)
- **Extracts**: name, price, hero image, bullet features, brand
- **Notes**: Price comes from the buy box. If the product has variants (size, color) the parser picks the default-selected one. Bullet features come from the "About this item" section.

### Shopify stores
- **URL patterns**: `*.myshopify.com/products/*`, plus any custom domain with `/products/<slug>` (most D2C brands)
- **Extracts**: name, price, hero image, description, brand (from store name)
- **Notes**: Description comes from the product page body, often longer than Amazon bullets. The parser truncates to the first 5 sentences for the brief.

### TikTok Shop
- **URL patterns**: `shop.tiktok.com/view/product/*`
- **Extracts**: name, price, hero image, brand, ratings count
- **Notes**: TikTok Shop pages are quite minimal. The parser fills the brief from the headline and one-liner.

### eBay
- **URL patterns**: `ebay.com/itm/*`
- **Extracts**: name, price, hero image, condition (new vs used)
- **Notes**: eBay is a marketplace so product copy is seller-written and often inconsistent. Sanity-check the extracted name before generating.

## Tier 2: partial extraction (most fields, may miss bullets or features)

These domains have inconsistent metadata. The parser pulls what it can:

- **Etsy** (`etsy.com/listing/*`) — name, hero image, price reliably; description may be empty
- **Walmart** (`walmart.com/ip/*`) — name, price, hero image; specs section often missed
- **Target** (`target.com/p/*`) — name, hero, price; deeper specs missed
- **Best Buy** (`bestbuy.com/site/*`) — name, hero, price, brand; review highlights missed

## Tier 3: best-effort (may miss the hero image)

For everything else, the parser:
1. Reads `<meta property="og:title">` for the product name
2. Reads `<meta property="og:image">` for the hero
3. Reads `<meta property="og:description">` for the body
4. Falls back to the first `<h1>` and first large `<img>` if og tags are missing

If a custom site has none of those tags, the parser will warn you and ask for manual input.

## Unsupported domains

These will fail or return junk:

- **Login-walled pages** (Costco member pricing, wholesale catalogs, B2B portals)
- **Paywalled pages** (anything behind a subscription)
- **Pages that aggressively client-side render** (some new-school sites where the product info is loaded after the page load via JavaScript). The parser only sees the initial HTML.

For these, use the Chrome MCP if connected, or paste the product details directly into `/product-to-ad`.

## Reading the parser output

After fetch, Claude saves `source.json`. Open it before approving the ad. Key fields to sanity-check:

- `product.name` — should match the actual product, not the page title which sometimes includes "(Pack of 4)" or other clutter
- `product.hero_image_url` — open it in your browser. If it's a placeholder or thumbnail, swap in a better image manually
- `product.price` — should be the real price, not a strikethrough or list price
- `product.features` — the first 5 bullets. If they're irrelevant or empty, the script will be weak

If any of those look wrong, edit `source.json` directly and re-run. The brief auto-fills from `source.json`.
