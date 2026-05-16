# claude-skills

Centralized library of custom Claude Code skills. Skills live here once and are symlinked into any project that needs them — edit in one place, update everywhere with `git pull`.

## How it works

Claude Code loads skills from a project's `.claude/skills/` directory. Instead of copying skill files into each project, you symlink them back to this repo. When you pull updates here, every linked project sees them instantly.

```
~/CascadeProjects/claude-skills/    ← you edit here
    tcn-post.skill
    tcn-content-plan.skill
    tcn-content-plan/               ← companion reference dir

~/CascadeProjects/my-project/.claude/skills/
    tcn-post.skill → ~/CascadeProjects/claude-skills/tcn-post.skill
    tcn-content-plan.skill → ~/CascadeProjects/claude-skills/tcn-content-plan.skill
    tcn-content-plan → ~/CascadeProjects/claude-skills/tcn-content-plan/
```

---

## Installing skills into a project

```bash
# 1. Go to the project you want to enable skills in
cd ~/CascadeProjects/my-project

# 2. Make sure the skills directory exists
mkdir -p .claude/skills

# 3. Set a variable pointing to this repo (adjust path if needed)
SKILLS_REPO=~/CascadeProjects/claude-skills

# 4. Symlink the skills you want (see catalog below for what's available)
ln -s $SKILLS_REPO/tcn-post.skill .claude/skills/tcn-post.skill
```

For skills that have a **companion directory** (reference files Claude reads alongside the skill), symlink both:

```bash
ln -s $SKILLS_REPO/tcn-content-plan.skill .claude/skills/tcn-content-plan.skill
ln -s $SKILLS_REPO/tcn-content-plan       .claude/skills/tcn-content-plan
```

For **skill packs** (subdirectory bundles like Higgsfield), symlink each sub-skill individually:

```bash
ln -s $SKILLS_REPO/higgsfield-cowork-pack/skills/product-to-ad .claude/skills/product-to-ad
ln -s $SKILLS_REPO/higgsfield-cowork-pack/skills/character-locker .claude/skills/character-locker
# ...etc
```

### Updating all skills

```bash
cd ~/CascadeProjects/claude-skills
git pull
```

That's it. All symlinked projects pick up changes automatically — no reinstall, no copying.

---

## Skill catalog

### The Civic Node (drinkYourOJ)

Skills built for The Civic Node Substack newsletter and Justin Hearn's brand voice.

| Skill file | What it does |
|---|---|
| `tcn-post.skill` | Writes tweets, threads, and social posts for X, LinkedIn, and Facebook using the Marcus reader persona and Civic Node viral post process |
| `tcn-substack-notes.skill` + `tcn-substack-notes/` | Generates Substack Notes calibrated to convert feed readers into subscribers — single Notes, article harvests, multi-day batches |
| `tcn-content-plan.skill` + `tcn-content-plan/` | Manages TCN daily and monthly content planning — check today's plan, generate 30-day maps, draft standalone post options |
| `tcn-text-humanizer.skill` | Strips AI writing patterns and rewrites text in Justin Hearn's dry, sardonic, opinionated voice |
| `publish-timing.skill` | Analyzes a draft article and determines the optimal Substack publish date and time by scanning live news cycles and upcoming events |
| `story-conversation.skill` | Conducts a structured writing conversation to extract personal stories and observations for Substack articles |

### General purpose

| Skill file | What it does |
|---|---|
| `project-md-generator.skill` | Generates a repo-root `CLAUDE.md` for any coding project — git flow, testing conventions, Docker config, adversarial agent protocol |
| `ai-image-prompts-skill.skill` | Recommends proven prompts from a 10,000+ real-world image generation library, compatible with any model (Midjourney, DALL-E, Flux, Nano Banana Pro, etc.) |

---

## Skill packs

Self-contained bundles with multiple related skills and shared reference files.

### `higgsfield-cowork-pack/`

End-to-end UGC ad and content pipeline via the Higgsfield MCP. Requires Claude Cowork with the Higgsfield MCP connected.

| Skill | What it does |
|---|---|
| `setup-higgsfield-project` | One-time project init — generates a `CLAUDE.md` that locks brand voice, character, output folders, and model defaults |
| `character-locker` | Saves a UGC actor as a reusable character profile (face, outfit, vibe) via Higgsfield SOUL |
| `product-to-ad` | Drops a product image, returns a finished UGC video ad — actor, script, MP4 |
| `url-to-ad` | Pastes a product URL, scrapes it, and chains into `product-to-ad` |
| `ig-carousel` | Generates premium 4:5 Instagram carousels with a cinematic cover and photoreal slides |
| `overnight-content` | Schedules the full ad pipeline to run unattended and drops finished ads each morning |

Install all Higgsfield skills at once:

```bash
SKILLS_REPO=~/CascadeProjects/claude-skills
for skill in setup-higgsfield-project character-locker product-to-ad url-to-ad ig-carousel overnight-content; do
  ln -s $SKILLS_REPO/higgsfield-cowork-pack/skills/$skill .claude/skills/$skill
done
```

### `video-use-main/`

Conversational video editing — transcribe, cut, color grade, generate overlay animations, burn subtitles. Works for talking heads, montages, tutorials, interviews. Uses ffmpeg and PIL under the hood.

```bash
ln -s $SKILLS_REPO/video-use-main/skills/manim-video .claude/skills/manim-video
```

---

## Reference files

These files live at the repo root and are used by skills or as standalone context.

| File | Purpose |
|---|---|
| `justin-hearn-voice-profile.md` | Full voice and brand profile for drinkYourOJ / The Civic Node |
| `civic-node-viral-social-process.md` | The Civic Node's documented process for writing viral social content |
| `.agents/social-media-context-sms.md` | Social media context configuration for the drinkYourOJ brand |

---

## Adding a new skill

1. Add the `.skill` file (and companion directory if needed) to this repo root
2. `git add` and `git commit`
3. `git push`
4. Symlink from any project that needs it

Skills added here are immediately available to any project — just symlink and go.
