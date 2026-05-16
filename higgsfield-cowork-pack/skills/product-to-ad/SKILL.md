---
name: product-to-ad
description: Turn any product image into a finished UGC video ad. Drop a product photo in a folder, give Claude a few details, and get back a UGC actor holding your product, a 30-second script, and a rendered MP4 ready to post. Use this skill when the user says "product to ad", "make me an ad", "UGC ad", "turn this product into an ad", "ad video", "create a video ad", "I have a product, make an ad", or pastes a product image and asks for a marketing video. Powered by Higgsfield (SOUL for the actor, Nano Banana Pro for the scene, Higgsfield video for motion). Always orchestrated through the Higgsfield MCP, never through external API calls.
---

# Product to Ad

Drop in a product image. Get back a finished UGC video ad. Saved to a folder. Ready to post.

## What this skill does (in one breath)

1. Looks at the product image
2. Picks a UGC actor who matches the buyer
3. Generates a scene of that actor holding the product
4. Writes a 30-second UGC script
5. Renders the video with Higgsfield
6. Saves everything to `outputs/ads/<product-slug>/`

By the end the user has a folder they can drag straight into their phone or schedule on Blotato.

## Setup the user needs (check before generating)

- Higgsfield MCP connected. If `balance` returns an error, stop and tell them to connect it in Cowork settings.
- A product image. Any clean photo of the product works best (white background, lifestyle shot, both fine). Ask for the file path or have them drop it in `inputs/products/`.
- 5 minutes of credits. A full ad uses around 4 to 8 Higgsfield credits depending on video length.

## Process

### Step 1: Brief the user with AskUserQuestion

Always call AskUserQuestion before generating. Even if the user gave a topic in chat, the brief locks in the four things you need. Ask all four in one batch.

1. **Product** — "Which product file should I use?" Options: paths from `inputs/products/`, plus an "Other" path option.
2. **Buyer** — "Who buys this product?" Options: 4 archetypes that fit the product (pulled from `references/character-archetypes.md`). Default options: gym-bro twenties, busy-mom thirties, gen-z creator, white-collar professional.
3. **Vibe** — "What tone do you want?" Options: excited and high-energy, calm and educational, sarcastic and funny, soft and aspirational.
4. **CTA** — "What should viewers do?" Options: visit website, use code at checkout, follow for more, comment "YES" for a link.

Save the answers to `outputs/ads/<slug>/brief.json` (use the template in `templates/ad-brief.json`).

### Step 2: Read the product image

Use Claude vision to describe the product in 2 sentences. Pull out: what it is, what color it is, what it does, what kind of person uses it. This becomes the seed for the rest of the prompts.

### Step 3: Generate the UGC actor (Higgsfield SOUL)

Call `mcp__8148b7eb-72e8-45e8-bb1d-864094e854c1__generate_image` with model `soul_cast` (text-to-image character). Build the prompt from `references/character-archetypes.md` matching the buyer the user picked.

Aspect ratio: `9:16` (TikTok / Reels native).
Resolution: `2k`.
Save the image as `outputs/ads/<slug>/actor.png`. Save the Higgsfield job_id too — you will reuse it as a reference.

If the user previously ran the `/character-locker` skill, look in `characters/` first. If a saved character profile exists for this brief, use that instead and skip this step.

### Step 4: Generate the scene (actor + product together)

Call `generate_image` with model `nano_banana_2` (Nano Banana Pro is best at multi-reference compositing).

Pass two reference medias:
- The actor image (job_id from step 3)
- The product image (upload via `media_upload`, then pass the media_id)

Prompt template:
```
The exact actor from reference image 1 holding the exact product from reference image 2 in a {ugc-setting from visual-prompts-pack}. Natural UGC lighting, slight handheld feel, talking-to-camera framing, casual smile. Photorealistic, not staged. 9:16 vertical.
```

Aspect ratio: `9:16`. Resolution: `2k`. Save as `outputs/ads/<slug>/scene.png`.

If the sandbox cannot upload the product image to Higgsfield (network restrictions), fall back to describing the product in detail in the prompt and rely on Nano Banana Pro to render it. Tell the user this happened so they know the product likeness may drift.

### Step 5: Write the 30-second UGC script

Use `references/ugc-script-formula.md`. Structure: Hook (0 to 3s), Demo (3 to 25s), CTA (25 to 30s). Match the vibe the user picked. Write it in the voice of the buyer archetype, not in a marketing voice.

Save as `outputs/ads/<slug>/script.md` with timestamps and on-screen text directions.

### Step 6: Generate the video

Call `mcp__8148b7eb-72e8-45e8-bb1d-864094e854c1__generate_video`.

Use the scene image (job_id from step 4) as the start frame. Pass the script's hook line plus a motion direction as the prompt. Example:
```
The actor lifts the product to camera and smiles. Subtle handheld camera shake. Soft natural daylight. 5-second clip.
```

Aspect ratio: `9:16`. Length: 5 to 8 seconds for the hero shot.

For a full 30-second ad, generate 3 to 5 short clips (hook, demo angle 1, demo angle 2, CTA), each starting from a slightly different scene image. Save each as `outputs/ads/<slug>/clip-XX.mp4`.

### Step 7: Save the package

Final folder layout:
```
outputs/ads/<product-slug>/
  ├── brief.json          ← inputs from step 1
  ├── actor.png           ← UGC character
  ├── scene.png           ← actor + product hero shot
  ├── script.md           ← 30-second script
  ├── clip-01.mp4         ← hero clip
  ├── clip-02.mp4         ← demo clip
  ├── clip-03.mp4         ← CTA clip
  ├── caption.txt         ← Instagram / TikTok caption + hashtags
  └── README.md           ← what each file is, how to assemble
```

Always also write `caption.txt` (5th-grade tone, hook + value + CTA + 5 hashtags) and a small `README.md` explaining the file map.

### Step 8: Show the user what they got

End with the file links the user can click. Do not auto-post. Ask: "Want me to (1) regenerate any clip, (2) write a longer script, or (3) schedule this on Blotato?"

## Rules

- ALWAYS use Higgsfield via the MCP. Never call Gemini, OpenAI, or any external image API directly. The sandbox cannot reach external endpoints, and the user has Higgsfield credits to use.
- ALWAYS check `balance` before starting a long generation. If credits are below 10, warn the user.
- ALWAYS write to `outputs/ads/<slug>/`. Slug from product name, lowercase, kebab-case.
- ALWAYS download generated assets via the Higgsfield UI widget. The sandbox cannot download CloudFront URLs to disk, so leave them in the Higgsfield account and provide a `download-urls.md` file with curl commands the user can paste.
- 9:16 vertical for everything. This is for TikTok and Reels, not YouTube.
- 5th-grade reading level on every piece of viewer-facing copy (script, caption). Short sentences. Plain words.
- No em dashes anywhere. No "this isn't just X, it's Y" cadence. Sound like a person.
- No revenue claims, no "I made $X" hooks. Pattern-interrupt or curiosity hooks only.
- Save the brief to `brief.json` so the user can re-run a variation by editing one file.

## Output checklist (before handing off)

- [ ] `brief.json` saved
- [ ] `actor.png` rendered, looks like a real person
- [ ] `scene.png` rendered, product is recognizable
- [ ] `script.md` reads naturally, fits 30 seconds at normal speaking pace
- [ ] At least 1 video clip rendered
- [ ] `caption.txt` written, 5 hashtags, no em dashes
- [ ] `README.md` explains the folder
- [ ] Computer:// links shown to the user at the end

## When NOT to use this skill

- The user wants a long-form (60s+) video. Use a different workflow.
- The user only wants images, not video. Use Higgsfield image generation directly.
- The user wants a polished brand commercial. UGC ads are deliberately casual; a brand commercial needs storyboarding and is out of scope.
