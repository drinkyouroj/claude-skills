# Install / Use Guide

## What this skill does

Drop in a product image. Get back a 30-second UGC video ad with a real-looking actor holding your product. Saved to `outputs/ads/<product-slug>/`.

## What you need before you start

1. **Claude Cowork** (the desktop app)
2. **Higgsfield MCP** connected. In Cowork, open Settings → Connectors → enable Higgsfield. You'll need a Higgsfield account (free tier works for testing).
3. **A product image.** Any clean photo, lifestyle or studio. PNG or JPG.
4. **About 5 to 8 Higgsfield credits** per ad.

## Install

1. Drop the entire `product-to-ad/` folder into your Cowork skills directory:
   ```
   ~/Desktop/<your-cowork-folder>/skills/product-to-ad/
   ```
2. Restart Cowork (or reload skills).
3. Verify it loaded by typing `/product-to-ad` in Cowork. If autocomplete shows it, you're good.

## Use

In Cowork, type:
```
/product-to-ad
```
or just say:
```
turn this product into an ad
```
or paste a product image and say `make me an ad`.

Claude will then:
1. Ask you 4 quick questions (product, buyer, vibe, CTA)
2. Generate a UGC actor with Higgsfield SOUL
3. Combine actor + product into a scene
4. Write a 30-second script
5. Render the video clips
6. Save everything to `outputs/ads/<your-product-slug>/`

The whole thing takes about 3 to 5 minutes depending on your Higgsfield queue.

## Where to find your output

```
outputs/ads/<product-slug>/
  ├── brief.json          ← what you told Claude (re-edit to regenerate)
  ├── actor.png
  ├── scene.png
  ├── script.md
  ├── clip-01.mp4
  ├── clip-02.mp4
  ├── clip-03.mp4
  ├── caption.txt
  └── README.md
```

Drag the clips into your phone, your video editor, or your scheduler. Done.

## Common issues

**"Higgsfield MCP not connected."**
Open Cowork → Settings → Connectors → toggle Higgsfield on. Authenticate when prompted.

**"Can't download videos to my Desktop folder."**
Cowork's sandbox can't reach Higgsfield's CloudFront URLs directly. The skill drops a `download-urls.md` file with a curl command you paste into Terminal once. After that the videos sit in your output folder.

**"The actor looks different in every clip."**
Either (a) save the actor's Higgsfield job_id and reuse it for follow-up clips, or (b) install the `/character-locker` skill (sister skill) which automates this.

**"My product looks weird in the scene."**
Two fixes:
1. Use a cleaner product image. White or transparent background works best.
2. Re-run with a more detailed `what_it_is` field in `brief.json`.

## Want to regenerate just one piece?

Edit `brief.json`, then run `/product-to-ad regenerate clip-02`.

## Pairs well with

- `/character-locker` — save a UGC actor and reuse them across ads
- `/url-to-ad` — same pipeline but starts from a product URL instead of an image
- `/overnight-content` — schedule this skill to run every night, wake up to fresh ads

## Cost per ad

Roughly:
- 1 SOUL character generation: ~1 credit
- 1 Nano Banana Pro scene with 2 references: ~1 credit
- 3 video clips: ~3 to 5 credits

Total: ~5 to 8 Higgsfield credits per finished ad. Higgsfield's Starter plan gets you ~25 to 40 ads per month.
