# tcn-youtube-thumbnail Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `tcn-youtube-thumbnail` skill per the spec at [docs/superpowers/specs/2026-05-21-tcn-youtube-thumbnail-design.md](../specs/2026-05-21-tcn-youtube-thumbnail-design.md), deployable in time for Friday 2026-05-22's recording of dispatch-004 thumbnails.

**Architecture:** Markdown-based Claude Code skill mirroring the structural conventions of `tcn-youtube-narration` and `tcn-youtube-slideshow`. Source-of-truth at `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/`, runtime symlink at `~/.claude/skills/tcn-youtube-thumbnail/`. Skill is scaffolded via `anthropic-skills:skill-creator`, customized per the design spec, and validated against the dispatch-004 narration that's already on disk. Five reference files plus a SKILL.md.

**Tech Stack:** Markdown, YAML frontmatter, Bash for filesystem ops, `anthropic-skills:skill-creator` for scaffolding, `ai-image-prompts-skill` as an explicit invocation dependency, optional `mcp__fal-ai__*` MCP tools for the LoRA-mode render gate, git for atomic commits per task.

**Spec coverage map:**
- §1–§3 (context, ecosystem, architectural decisions) → SKILL.md body sections "What this skill does" + "Position in workflow" (Task 3)
- §4 (inputs) → SKILL.md body section "Inputs and outputs" + frontmatter triggers (Tasks 2–3)
- §5 (outputs) → SKILL.md body section "Inputs and outputs" + the artifact template (Task 3)
- §6 (process) → SKILL.md body section "The process" (Task 3)
- §7 (generation modes) → SKILL.md body table + `references/flux-prompt-template.md` + `references/reference-image-prompt-template.md` (Tasks 7, 8)
- §8 (text overlay spec) → SKILL.md body section + `references/text-overlay-spec.md` (Task 6)
- §9 (thumbnail headline distillation) → SKILL.md body section + `references/thumbnail-headline-patterns.md` (Task 4 — the most load-bearing reference file)
- §10 (TCN identity markers) → SKILL.md body section "TCN identity markers" (Task 3)
- §11 (failure modes) → SKILL.md body section "Failure modes" (Task 3)
- §12 (reference files) → Tasks 4–8
- §13 (what this skill is NOT) → SKILL.md body section "What this skill is NOT" (Task 3)
- §14 (companion skills) → SKILL.md body section "Companion skills" (Task 3)
- §15 (open questions) → no implementation surface; tracked in spec only

---

## Task 1: Set up skill directory + runtime symlink

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/`
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/`
- Symlink: `~/.claude/skills/tcn-youtube-thumbnail/` → top-level source

- [ ] **Step 1: Create source directory + references subdirectory**

```bash
mkdir -p /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references
```

Expected: two new directories on disk. No output is a success.

- [ ] **Step 2: Verify the runtime symlink target does not already exist**

```bash
ls ~/.claude/skills/tcn-youtube-thumbnail 2>/dev/null || echo "OK_NOT_EXISTS"
```

Expected: `OK_NOT_EXISTS`. If a non-symlink directory exists at that path, halt and ask the user — do not overwrite.

- [ ] **Step 3: Create the runtime symlink**

```bash
ln -sf /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail ~/.claude/skills/tcn-youtube-thumbnail && readlink ~/.claude/skills/tcn-youtube-thumbnail
```

Expected output: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail`

- [ ] **Step 4: No commit yet** — directory has no files. First commit lands in Task 2.

---

## Task 2: Scaffold SKILL.md via skill-creator

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/SKILL.md`

- [ ] **Step 1: Invoke the skill-creator skill to scaffold**

Use the Skill tool to invoke `anthropic-skills:skill-creator` with this prompt:

```
Scaffold a new skill at /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/

Name: tcn-youtube-thumbnail
Description (frontmatter): Step 5 of the Civic Node YouTube production workflow — produces two Flux image-prompt variants for the YouTube thumbnail (with illustrated-Justin via reference image or trained Flux LoRA) plus a text overlay spec for compositing in Figma/Canva/Photoshop. Pre- or post-record. Invoke when the user says "build the thumbnail", "thumbnail prompts for this dispatch", "make the thumbnail", "design the thumbnail for №NNN", "create thumbnail prompts", or has approved a youtube-narration.md or recorded transcript and wants thumbnails. Does NOT generate the article, narration, slideshow, title, or description (those are separate skills), and does NOT composite the final image (that's Figma/Canva/Photoshop post-processing).

Use the standard SKILL.md frontmatter format. Body can be minimal — Task 3 will fill it in.
```

Expected: a SKILL.md with valid YAML frontmatter and a placeholder body.

- [ ] **Step 2: Verify the frontmatter parses**

```bash
head -5 /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/SKILL.md
```

Expected output starts with `---` and a `name: tcn-youtube-thumbnail` line within the first 5 lines.

- [ ] **Step 3: Commit the scaffold**

```bash
git add tcn-youtube-thumbnail/SKILL.md tcn-youtube-thumbnail/ tcn-youtube-thumbnail/references/.gitkeep 2>/dev/null
git status --short
```

Then commit:

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-thumbnail/ && git commit -m "scaffold tcn-youtube-thumbnail skill via skill-creator"
```

Expected: one new commit on `main`, file added.

---

## Task 3: Fill in SKILL.md body from spec

**Files:**
- Modify: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/SKILL.md`

This is the largest single authoring task. The SKILL.md body should mirror the structure of `tcn-youtube-slideshow/SKILL.md` (already on disk for reference) but cover the thumbnail spec's content.

- [ ] **Step 1: Read the source spec to refresh context**

Read `/Users/justin/CascadeProjects/claude-skills/docs/superpowers/specs/2026-05-21-tcn-youtube-thumbnail-design.md` end-to-end. Then read `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-slideshow/SKILL.md` for structural reference.

- [ ] **Step 2: Write the SKILL.md body**

Replace the placeholder body with the following section structure. Each section's content is drawn from the spec — keep section headings consistent with the spec's numbering for traceability.

Use the Write tool to overwrite `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/SKILL.md`. Preserve the existing frontmatter from Task 2; rewrite only the body below the closing `---`.

Required body sections, in order:

1. **`# The Civic Node — YouTube Thumbnail (Step 5 of the YouTube Production Workflow)`** — top-level heading.

2. **`## What This Skill Does`** — one paragraph: prompt-builder modeled on `ai-image-prompts-skill`; produces two Flux image-prompt variants + a text overlay spec; dual-mode (reference-image default, LoRA upgrade); CTR-first with TCN identity markers on overlay only. Cite spec §1.

3. **`## Why a Prompt-Builder Plus Optional Render`** — explain the prompt-builder pattern (matching slideshow) plus the LoRA-mode opt-in render via fal MCP. Cite spec §3.6.

4. **`## Position in the YouTube Workflow`** — include the ASCII workflow diagram from spec §2 verbatim. Note recording is the cleavage point. Note this skill can run pre- or post-record.

5. **`## Inputs and Outputs`** — required input (narration OR transcript, auto-detected). Optional inputs (LoRA URL three-source lookup, reference image path, steering, override vibe, override headline). Output artifact file location and structure. Optional render outputs. Cite spec §4–§5.

6. **`## Generation Modes`** — the dual-mode table from spec §7. Reference-image mode vs LoRA mode. Activation. Prompt format. Render assist. Mode header.

7. **`## The Process`** — 12 numbered steps from spec §6. Each step gets one paragraph. Gate 1 explicitly says "Invoke `ai-image-prompts-skill` via the Skill tool with the composed query." Gate 2 references §9. Gate 3 (render) is LoRA-mode only.

8. **`## Thumbnail Headline Distillation`** — summarize spec §9. Drafting inputs (§9.1), acceptance criteria as a bulleted list (§9.2 — include the full criteria list), pattern library reference (§9.3) pointing to `references/thumbnail-headline-patterns.md`, retry behavior (§9.4), Gate 2 display format example (§9.5 — include the exact format block).

9. **`## TCN Identity Markers`** — what carries the brand load: mark, dispatch serial, Courier Prime on overlay, palette restricted to slate-400/slate-600/black/twilight on overlay only. The illustrated scene is CTR-first (not brand-restricted). Cite spec §10.

10. **`## Text Overlay Specification`** — summary of spec §8. Headline typography/position/size/color. Corner identity block. Mobile safe-zone rule (center 80%). Full details in `references/text-overlay-spec.md`.

11. **`## Failure Modes`** — list all from spec §11.

12. **`## What This Skill Is NOT`** — list from spec §13.

13. **`## Companion Skills`** — upstream (narration, transcript), sibling (title, description), invocation dependency (ai-image-prompts-skill), optional runtime dependency (fal-ai MCP). Cite spec §14.

14. **`## Reference Files`** — list all 5 files in `references/` with one-line descriptions matching spec §12.

- [ ] **Step 3: Verify the SKILL.md is well-formed**

```bash
wc -l /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/SKILL.md
head -10 /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/SKILL.md
```

Expected: 200–400 lines total. Frontmatter intact. Section headings present in order.

- [ ] **Step 4: Sanity-check spec coverage**

For each spec section §1–§14, grep the SKILL.md body for a recognizable phrase from that section. Each should appear at least once.

```bash
cd /Users/justin/CascadeProjects/claude-skills && for phrase in "Step 5 of" "auto-detect" "dual-mode" "Gate 1" "Gate 2" "Gate 3" "acceptance criteria" "mobile safe" "TCN identity markers" "fal MCP"; do
  echo -n "$phrase: "
  grep -c "$phrase" tcn-youtube-thumbnail/SKILL.md || echo "0"
done
```

Expected: every phrase appears at least once (count ≥ 1).

- [ ] **Step 5: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-thumbnail/SKILL.md && git commit -m "fill in tcn-youtube-thumbnail SKILL.md body from spec"
```

---

## Task 4: Write `references/thumbnail-headline-patterns.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md`

This is the most load-bearing reference file per spec §9.3 — the skill reads it at drafting time as the source of truth for headline voice and structure. Write this file before the other references because the SKILL.md body for §9 already points to it.

- [ ] **Step 1: Write the file with the structure below**

Use the Write tool to create the file with these top-level sections (provide actual content under each — this is not a skeleton):

````markdown
# Thumbnail Headline Patterns

Source of truth for the headline drafting step (Gate 2) in `tcn-youtube-thumbnail`. The skill reads this file at drafting time to surface 3 candidate thumbnail headlines that pass the acceptance criteria in SKILL.md §9.2.

Edit this file directly when banned-word lists, structural patterns, or anti-pattern observations need to evolve. No skill-code changes required.

## Voice anchors

Thumbnail headlines extend TCN's existing voice corpus:
- Inherits from `justin-hearn-voice-profile.md` (drinkYourOJ voice).
- Inherits from the anti-AI-writing-style rules used in `tcn-text-humanizer`.
- Constrained to the Marcus-reader visiting-friends register — talking to a smart friend, not shouting at a crowd.
- Sentence case. No screaming.
- Declarative or genuine curiosity-gap. Never clickbait-shaped.
- Sardonic and specific. Specificity = trust.

## Word-count discipline

- 3–6 words inclusive. Hyphenated compounds count as one word. Contractions count as one word. Numbers count as one word regardless of digit count.
- 3 words: punchy, works when you have a strong anchor noun.
- 4–5 words: the sweet spot for most dispatches.
- 6 words: only when every word earns its place.

## Banned hype adjectives (case-insensitive)

Any candidate containing any of these is rejected:

- SHOCKING
- AMAZING
- INSANE
- EXPOSED
- REVEALED
- UNBELIEVABLE
- MASSIVE
- ULTIMATE
- EPIC
- INCREDIBLE
- MIND-BLOWING
- GAME-CHANGING

Add new entries as future dispatches surface them. Keep the list explicit — no fuzzy matching.

## Banned clickbait templates

Any candidate matching these shapes is rejected:

- "This One Trick…" / "This Simple Trick…"
- "What They Don't Want You To Know"
- "You Won't Believe…"
- "Here's Why…" (when leading)
- "The Truth About…" (generic — fine when specific)
- "Doctors Hate This…" / any "[Group] Hate This…"
- "Number N Will Shock You"

## Anti-AI-tell tokens

Reject any candidate containing:

- em-dashes (—)
- "delve" / "delving"
- "tapestry"
- "navigate the landscape" / "the landscape of"
- "in the realm of"
- "it's worth noting"
- Any token flagged by the `tcn-text-humanizer` skill's tell list (cross-reference, don't duplicate)

## Concrete-specific requirement

If the cold-open contains any of:
- A number ($499, 11%, 23 cities)
- A place name (Helium, Austin, Reykjavík)
- A dollar amount
- A year (2024, 1996)
- A proper noun (Nova Labs, FAA, HIP-143)

…then at least ONE of the three candidates MUST use it. The other two candidates can be more abstract for variety. The point is to anchor the headline in a fact-check-able specific so the curiosity gap is earned, not invented.

## Proven structural patterns

Each pattern with worked example(s).

### Concrete Anchor + Twist

Lead with a specific named thing, then a twist that creates the curiosity gap.

- "You Own the Hotspot" — dispatch-004. Anchor: the thing the viewer paid for. Twist: implied "but…"
- "Nova Labs Owns It" — dispatch-004 alt. Anchor: named entity. Twist: contradicts what the viewer just spent $499 expecting.

### Implied Stakes

State the fact; let the stakes hang in the air. No exclamation needed.

- "The FAA Already Knows"
- "Reykjavík Tried This First"

### Direct Address

Speak to the viewer. "You" or "Your" anchors the headline.

- "Why You're Funding This"
- "Your Hotspot, Their Token"

### Specific Contradiction

Two facts in tension. Concrete on both sides.

- "$499 to Mine WiFi"
- "Public Money, Private Profit"

### Bare-Noun Provocation

One or two nouns. Pure provocation through the noun choice.

- "The Hotspot Tax"
- "The Helium Receipt"
- "The Quiet Default"

## Anti-pattern gallery

Examples of candidates that violate criteria, with the reason. Educational, not exhaustive.

- "SHOCKING Truth About Helium" — all-caps + banned word.
- "You Won't Believe What Nova Labs Did" — banned clickbait template + 8 words.
- "The Surprisingly Profitable Tapestry of Hotspots" — anti-AI-tell ("tapestry") + over-word-count + abstract.
- "An In-Depth Analysis of the Helium Network's Tokenomics" — 9 words, abstract, AI-tell shape, no curiosity gap.
- "Helium" — under word-count, no anchor.
- "Why Helium Matters" — generic, no curiosity gap, could describe any episode.

## Worked example walkthroughs

### Dispatch-004 — "You Own the Hotspot"

**Cold-open candidate:** "I bought a $499 hotspot to mine WiFi tokens. Nova Labs owns what it earns."

**3 drafted candidates with rationales:**

1. *"You Own the Hotspot"* — Direct Address + Concrete Anchor + Twist. Anchors "you" + the hardware noun. The "but…" hangs implied.
2. *"$499 to Mine WiFi"* — Specific Contradiction. Anchors dollar amount. Tension: spending money to mine something that should be free.
3. *"Nova Labs Owns It"* — Implied Stakes + named entity. The "it" is load-bearing — viewer has to click to find out what.

**Picked:** Candidate 1 — strongest curiosity gap, direct-address pulls viewer in, the implied twist is the gap.

(Add a second worked example after the second dispatch is produced. Until then, the dispatch-004 walkthrough alone is sufficient.)

## How the skill uses this file

At drafting time (process step 6, SKILL.md §9), the skill:

1. Loads this file's contents into its drafting context.
2. Extracts the cold-open candidate and dispatch concept.
3. Drafts 3 candidates following the proven patterns, with the concrete-specific requirement applied if the cold-open supports it.
4. Filters candidates against the banned-word, banned-template, and anti-AI-tell lists.
5. Re-drafts any failing slot up to 2 additional attempts.
6. Surfaces the passing candidates with one-line rationales per the Gate 2 display format.
````

- [ ] **Step 2: Verify the file structure**

```bash
wc -l /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md
grep "^## " /Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md
```

Expected: ~150–250 lines. Section headings include "Voice anchors", "Banned hype adjectives", "Proven structural patterns", "Worked example walkthroughs", "How the skill uses this file".

- [ ] **Step 3: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md && git commit -m "add thumbnail-headline-patterns reference (§9 source of truth)"
```

---

## Task 5: Write `references/vibe-query-templates.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/vibe-query-templates.md`

Per spec §6 step 4 and §12. Defines how the skill composes the search query passed to `ai-image-prompts-skill` at Gate 1.

- [ ] **Step 1: Write the file**

Use the Write tool. Top-level sections:

````markdown
# Vibe Query Templates

How the skill composes a search query for `ai-image-prompts-skill` at Gate 1. The query's job is to surface 2–3 thumbnail-shaped library candidates that match the dispatch's subject and mood.

## Query shape

```
illustrated editorial YouTube thumbnail, [dispatch subject 3–6 words], [mood adjectives 2–3], [composition hint], character-driven, magazine style
```

## Dispatch-subject extraction

Pull from the narration in this order:
1. The cold-open candidate's most punchable noun phrase.
2. The article's primary named entity if more concrete.
3. The dispatch slug if both are abstract.

Examples:
- Dispatch-004 cold open → "Helium hotspot earnings dispute"
- Dispatch about FAA + drones → "FAA drone airspace contest"
- Abstract policy dispatch → fall back to slug, e.g. "public broadband privatization"

## Mood adjective vocabulary

Pick 2–3 from this list that match the dispatch's emotional register. Do NOT invent moods outside this list — the library is best at common moods.

- dramatic
- editorial
- moody
- cinematic
- noir
- documentary
- conspiracy-thriller
- analytical
- investigative
- archival
- vaporwave-tech
- apocalyptic-tech
- corporate-dystopian
- quiet-dread

## Composition hint vocabulary

Pick one. Affects what kind of library candidate the search surfaces.

- mid-shot
- close-up portrait
- over-the-shoulder
- wide environmental
- top-down
- split-screen comparison

## Query patterns to avoid

- Too generic: "YouTube thumbnail, civic infrastructure" (returns noise).
- Single-word vibe: "moody" alone is not enough; pair with a subject.
- Brand names that the library won't have proven prompts for: "Helium-Network-specific Helium-style thumbnail" — instead use generic descriptors the library knows.
- Negations: "no clutter, no text" — library search is positive-keyword-driven.

## Example transformations

### Dispatch-004 (Helium / Nova Labs)

Cold open: "I bought a $499 hotspot to mine WiFi tokens. Nova Labs owns what it earns."

Composed query:
```
illustrated editorial YouTube thumbnail, hotspot earnings dispute, dramatic, investigative, mid-shot, character-driven, magazine style
```

### Hypothetical dispatch on FAA + drone airspace

Cold open: "The FAA quietly carved out a corridor over Austin. Nobody told the people who live under it."

Composed query:
```
illustrated editorial YouTube thumbnail, FAA drone corridor, conspiracy-thriller, moody, wide environmental, character-driven, magazine style
```

## How the skill uses this file

At step 4 (compose the library query), the skill:

1. Loads this file's contents.
2. Extracts the dispatch subject per the order above.
3. Picks 2–3 mood adjectives from the vocabulary.
4. Picks one composition hint from the vocabulary.
5. Composes the query string per the shape.
6. Passes the query to `ai-image-prompts-skill` via the Skill tool.

If the query returns zero usable candidates, the skill skips Gate 1 silently and proceeds to headline drafting (per spec §11).
````

- [ ] **Step 2: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-thumbnail/references/vibe-query-templates.md && git commit -m "add vibe-query-templates reference for thumbnail skill"
```

---

## Task 6: Write `references/text-overlay-spec.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/text-overlay-spec.md`

Per spec §8 and §12. The full typography/layout/color spec for the overlay; the SKILL.md body summarizes, this file is the authoritative source.

- [ ] **Step 1: Write the file**

Top-level sections:

````markdown
# Text Overlay Specification

The text overlay is composited onto the rendered thumbnail image in Figma/Canva/Photoshop *after* the image is generated. The skill produces this spec; the human (or future automation) executes it. The skill itself does NOT render text into the image.

## Canvas

- Source canvas: 1280 × 720 px (16:9). Match Figma/Canva frame size to this.
- Final YouTube display: variable, but the thumbnail is cropped aggressively for the mobile feed. Treat the center 80% (1024 × 576 px window, centered) as the safe zone. Anything outside that may get cropped.

## Mobile safe-zone rule

All text must stay inside the center 80%:
- Left edge of text: ≥ 128 px from canvas left.
- Right edge of text: ≤ 1152 px from canvas left.
- Top edge: ≥ 72 px from canvas top.
- Bottom edge: ≤ 648 px from canvas top.

The corner identity block exception: the dispatch number + mark may sit at ~96 px inset rather than 128 px to feel anchored to the corner. This is the only exception.

## Typeface

- Courier Prime only. Two weights used:
  - **Courier Prime Bold** — the headline.
  - **Courier Prime Regular** — the dispatch serial and any sub-line.
- Sourced from the TCN design system: `~/Documents/The Civic Node — Design System.zip` → fonts.

## Headline

- **Content:** the chosen candidate from Gate 2 (3–6 words).
- **Weight:** Courier Prime Bold.
- **Case:** sentence case. (Voice rule — no screaming.)
- **Size:** ~120 px at 1280 × 720. Scales to ~9.4% of canvas height.
- **Tracking:** -0.025em (tight, matches TCN display sizes).
- **Leading:** 1.05× size (~126 px) when the headline wraps to 2 lines.
- **Color:** slate-400 (`#557FA3`) or black (`#0D0D0F`). See "Color picking" below.
- **Optional stroke/halo:** 4–6 px stroke at 60% opacity in the opposite color (slate-400 stroke if black fill; black stroke if slate-400 fill). Use only when the underlying illustration is busy enough that flat text would lose legibility.
- **Position:** default center-left, baseline at ~55% of canvas height (~396 px from top). Left edge anchored to the safe-zone left edge (128 px in).
- **Max width:** 768 px (60% of canvas). Wrap to 2 lines if needed; never 3.

## Corner identity block

Two elements stacked:

- **Mark:** `mark.svg` from the design-system bundle.
  - Size: 40 × 40 px.
  - Color: slate-400 on dark scenes, slate-600 (`#3A6A8F`) on light scenes.
- **Dispatch serial:** `DISPATCH №NNN` (zero-padded).
  - Typeface: Courier Prime Regular.
  - Case: all-caps.
  - Tracking: 0.18em (wide, matches TCN kicker convention).
  - Size: 24 px.
  - Color: same as mark.

Stack: mark on top, dispatch serial below, 8 px gap between them.

Default position: top-right corner, both elements right-aligned. Right edge at 1184 px (96 px inset from canvas right). Top edge of mark at 72 px.

Alternative position: bottom-left, with mark above dispatch serial. Use this when the headline occupies the right half of the canvas.

## Color picking

The skill recommends a color pair (overlay-text color + optional stroke) in the artifact based on the chosen vibe's stated lighting:

- Vibe says "dark", "moody", "noir", "dramatic night", etc. → recommend slate-400 fill, no stroke.
- Vibe says "bright", "daytime", "editorial", "documentary daylight" → recommend black fill, no stroke.
- Vibe is ambiguous or mixed-lighting → recommend slate-400 fill with 4-px black stroke (works on most backgrounds).

The user can always override at composite time when looking at the actual rendered image.

## Palette restrictions

These four colors are the ONLY ones allowed on overlay text (headline, sub-line, dispatch serial, mark):

- slate-400 — `#557FA3`
- slate-600 — `#3A6A8F`
- black — `#0D0D0F`
- twilight — `#485070`

The illustrated scene (the image beneath the overlay) is NOT restricted to this palette. It can use any colors that serve CTR. The palette restriction is overlay-only — that's how the brand carries even when the scene goes loud.

## Sub-line / kicker (optional)

If the dispatch concept benefits from a context line beneath the headline (e.g., a zone or topic):

- Typeface: Courier Prime Regular.
- Case: all-caps.
- Tracking: 0.18em.
- Size: 18 px.
- Color: twilight (`#485070`).
- Position: directly below the headline, baseline at headline-baseline + 32 px.
- Length: 2–6 words max.

If the dispatch concept does NOT clearly benefit, omit. The skill should not force a sub-line.

## Spec block format (what the skill writes into youtube-thumbnail.md)

The skill writes this block into the artifact file's "Text overlay spec" section. Engineers reading this file should produce output in this shape:

```
## Text overlay spec

**Canvas:** 1280 × 720 (16:9). Center-80% safe zone.

**Headline:**
- Text: "<chosen headline>"
- Font: Courier Prime Bold, sentence case
- Size: 120 px
- Color: slate-400 #557FA3 (recommended for this vibe; black #0D0D0F also valid)
- Stroke: none recommended (4 px black if image is busier than expected)
- Position: center-left, baseline at 55% canvas height, left edge at 128 px

**Corner identity block (top-right):**
- Mark.svg: 40×40 px, slate-400
- Dispatch serial: "DISPATCH №NNN", Courier Prime Regular, 24 px, all-caps, tracking 0.18em, slate-400
- Both right-aligned at right edge 1184 px, mark top at 72 px

**Palette:** slate-400 #557FA3, slate-600 #3A6A8F, black #0D0D0F, twilight #485070. No other colors on overlay text.
```

## How the skill uses this file

At process step 9 (compose the text overlay spec), the skill:

1. Loads this file's contents.
2. Pulls the chosen headline and dispatch number.
3. Picks recommended color/stroke per the "Color picking" rules using the chosen vibe's lighting cues.
4. Writes the "Text overlay spec" block into `youtube-thumbnail.md` in the format above, substituting the chosen headline and dispatch number.
````

- [ ] **Step 2: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-thumbnail/references/text-overlay-spec.md && git commit -m "add text-overlay-spec reference for thumbnail skill"
```

---

## Task 7: Write `references/flux-prompt-template.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/flux-prompt-template.md`

Per spec §7 (LoRA mode column) and §12. The Flux prompt structure used when a LoRA URL is present.

- [ ] **Step 1: Write the file**

Top-level sections:

````markdown
# Flux Prompt Template (LoRA mode)

Active when a Flux LoRA URL is found via the §4.2 three-source lookup. Prompts produced in this mode are formatted for fal MCP's `mcp__fal-ai__run_model` call against the Flux.1 [dev] endpoint with a LoRA URL parameter.

## Variant A — wide editorial composition

```
[CHARACTER SUBJECT: illustrated character, wearing casual editorial styling, set in [SCENE DESCRIPTION pulled from dispatch concept + chosen vibe]. Wide framing, character occupies the right third of the frame. Mid-shot from the waist up. Editorial magazine-style composition with negative space on the left for text overlay.

LIGHTING: [from chosen vibe — e.g. "dramatic side-light from screen glow", "moody overcast natural", "noir single-source from off-camera"].

MOOD: [from chosen vibe adjectives].

COMPOSITION RULES: 1280×720 aspect ratio. Center 80% of frame must remain un-busy — no important detail in the corners or far edges. Negative space concentrated on the LEFT half (~768 px) for headline overlay.

NO TEXT in the image. No words, no signs, no readable typography. The text will be composited separately.

NEGATIVE PROMPT: text, words, typography, signs, watermarks, logos, captions, lettering, busy backgrounds, distracting clutter, multiple figures, low contrast.
```

**LoRA URL:** `{{ILLUSTRATED_JUSTIN_LORA_URL}}`
**LoRA strength:** 0.85
**Aspect ratio:** 16:9 (1280×720)
**Steps:** 28
**Guidance:** 3.5
**Sampler:** dpmpp_2m

## Variant B — tight close-up composition

```
[CHARACTER SUBJECT: illustrated character, close-up framing from the shoulders up, gaze [direction — toward camera / off-camera left / etc.]. Strong figure emphasis. Background [from dispatch concept] is soft-focused or partially abstract.

LIGHTING: [from chosen vibe].

MOOD: [from chosen vibe adjectives, slightly more intimate register than Variant A].

COMPOSITION RULES: 1280×720 aspect ratio. Character's face occupies the right ~40% of the frame. Center 80% must remain un-busy enough that a headline can sit at center-left without competing. Negative space on the LEFT third for text overlay.

NO TEXT in the image. No words, no signs.

NEGATIVE PROMPT: text, words, typography, signs, watermarks, logos, captions, lettering, busy backgrounds, multiple figures, low contrast, full-body shots, distant figures.
```

**LoRA URL:** `{{ILLUSTRATED_JUSTIN_LORA_URL}}`
**LoRA strength:** 0.85
**Aspect ratio:** 16:9 (1280×720)
**Steps:** 28
**Guidance:** 3.5
**Sampler:** dpmpp_2m

## fal MCP invocation shape

For the opt-in render step (Gate 3, process step 11), the skill calls:

```
mcp__fal-ai__run_model
  endpoint: fal-ai/flux-lora
  parameters:
    prompt: <the full prompt text above with [bracketed slots] filled in>
    image_size: landscape_16_9
    num_inference_steps: 28
    guidance_scale: 3.5
    loras:
      - path: <LoRA URL from §4.2 lookup>
        scale: 0.85
    num_images: 1
    enable_safety_checker: false
    output_format: png
```

One call per variant (two calls total per render gate accept).

## Negative-prompt patterns to include

- Text-rendering blockers: "text, words, typography, signs, watermarks, logos, captions, lettering"
- Composition blockers: "busy backgrounds, distracting clutter, multiple figures, low contrast"
- Variant-specific (B only): "full-body shots, distant figures"

## How the skill uses this file

At process step 8 (compose the two prompt variants) in LoRA mode, the skill:

1. Loads this file.
2. Fills in the bracketed slots from the dispatch concept + chosen vibe.
3. Writes two variant prompts into the artifact file.
4. At process step 11 (render gate), if the user accepts, invokes fal MCP per variant using the parameters above.
````

- [ ] **Step 2: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-thumbnail/references/flux-prompt-template.md && git commit -m "add flux-prompt-template reference for LoRA-mode thumbnails"
```

---

## Task 8: Write `references/reference-image-prompt-template.md`

**Files:**
- Create: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/reference-image-prompt-template.md`

Per spec §7 (reference-image mode column) and §12. Model-agnostic prompt structure for use without a LoRA.

- [ ] **Step 1: Write the file**

Top-level sections:

````markdown
# Reference-Image Prompt Template (default mode)

Active when no Flux LoRA URL is found. Prompts produced in this mode are model-agnostic — designed to work in Freepik, Nano Banana Pro / Gemini, Midjourney (with `--cref`), Flux Kontext (image-to-image), or any other tool that accepts a character reference image.

## Character reference handling

Every prompt includes an explicit instruction to use the attached reference image as the character source:

```
Use the attached reference image as the character reference. Match the character's facial features, hair, and styling exactly. Place the same character into a new scene as described below.
```

Reference image path (substituted in by the skill at runtime):
- Default location: `~/Documents/illustrated-justin-ref.png`
- If missing, the prompt contains `{{CHARACTER_REFERENCE_IMAGE}}` as a placeholder with a one-line setup note ("Generate a canonical illustrated-Justin reference image (1024×1024+) and save to this path before running.")

## Variant A — wide editorial composition

```
[CHARACTER REFERENCE INSTRUCTION from above]

SCENE: [scene description pulled from dispatch concept + chosen vibe]. Wide editorial framing. The character occupies the right third of the frame, mid-shot from the waist up. Magazine-style composition with significant negative space on the LEFT half of the frame for text overlay.

LIGHTING: [from chosen vibe].

MOOD: [from chosen vibe adjectives].

ASPECT RATIO: 16:9 (1280×720).

COMPOSITION RULES: keep the center 80% of the frame un-busy enough that a text headline can overlay center-left without competing with image detail.

EXCLUDE: text, words, typography, signs, watermarks, logos, captions, lettering. No readable characters anywhere in the image — text will be added in post.
```

## Variant B — tight close-up composition

```
[CHARACTER REFERENCE INSTRUCTION from above]

SCENE: [scene description, tighter framing]. Close-up of the character from the shoulders up. Gaze [direction — toward camera / off-camera left / etc.]. Background [from dispatch concept] is soft-focused or partially abstract.

LIGHTING: [from chosen vibe].

MOOD: [from chosen vibe adjectives, slightly more intimate register than Variant A].

ASPECT RATIO: 16:9 (1280×720).

COMPOSITION RULES: character's face occupies the right ~40% of the frame. Negative space on the LEFT third for text overlay. Keep center 80% un-busy.

EXCLUDE: text, words, typography, signs, watermarks, logos, captions, lettering. No full-body shots. No multiple figures.
```

## Per-tool quirks

### Freepik / Pikaso
- Paste the prompt into the image-generation field.
- Attach the reference image via the "character reference" or "Pikaso character" feature.
- Set aspect to 16:9.

### Nano Banana Pro / Gemini
- Upload the reference image first, then paste the prompt.
- Gemini handles "use the attached reference image as character reference" natively.

### Midjourney
- Use `--cref [reference image URL]` at the end of the prompt.
- Add `--ar 16:9` for aspect.
- The character-reference instruction at the start of the prompt becomes redundant with `--cref`; you can either keep both or trim to `--cref` only.

### Flux Kontext / image-to-image
- Set the reference image as the input image.
- Set denoise strength to ~0.7 so character is preserved but scene is regenerated.

## How the skill uses this file

At process step 8 (compose the two prompt variants) in reference-image mode, the skill:

1. Loads this file.
2. Substitutes the character reference image path (default or user-supplied).
3. Fills in the bracketed slots from the dispatch concept + chosen vibe.
4. Writes both variant prompts into the artifact file with the "Per-tool quirks" section appended as a tip block so the user knows how to adapt the prompt to their image-gen tool of choice.
5. Suppresses Gate 3 (no opt-in render in this mode — the skill doesn't know which tool the user is using).
````

- [ ] **Step 2: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-thumbnail/references/reference-image-prompt-template.md && git commit -m "add reference-image-prompt-template for default mode"
```

---

## Task 9: Validate skill against dispatch-004 narration

**Files:**
- Read: `~/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md`
- Expect-produced: `~/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-thumbnail.md`

This is the smoke test. The skill is invoked end-to-end against an existing narration. Pre-record reference-image mode is the primary validation target since no LoRA exists yet.

- [ ] **Step 1: Confirm the narration exists**

```bash
ls -la "/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md"
```

Expected: file exists, non-zero size.

- [ ] **Step 2: Confirm no LoRA URL is configured (forces reference-image mode for the test)**

```bash
ls ~/.config/tcn/illustrated-justin-lora.url 2>/dev/null && echo "LORA_CONFIG_EXISTS_UNEXPECTED" || echo "OK_NO_LORA_CONFIG"
echo "TCN_ILLUSTRATED_JUSTIN_LORA_URL=$TCN_ILLUSTRATED_JUSTIN_LORA_URL"
```

Expected: `OK_NO_LORA_CONFIG` and empty `TCN_ILLUSTRATED_JUSTIN_LORA_URL`. If a LoRA URL is already configured, unset it before the test (`unset TCN_ILLUSTRATED_JUSTIN_LORA_URL`) or stash the file temporarily.

- [ ] **Step 3: Invoke the skill end-to-end**

In a fresh Claude Code session (or by using the Skill tool to invoke `tcn-youtube-thumbnail`), provide this prompt:

```
Build the thumbnail for the dispatch-004 narration at /Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-narration.md
```

Walk through Gate 1 (pick a vibe from the surfaced candidates) and Gate 2 (pick a headline). Confirm the skill produces `youtube-thumbnail.md` in the same directory.

- [ ] **Step 4: Validate the produced artifact — checklist**

For each criterion, check the produced `youtube-thumbnail.md` file:

```bash
ARTIFACT="/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-thumbnail.md"
```

Acceptance criteria — each is a yes/no check:

  - [ ] Mode header reads `**Mode:** reference-image`.
  - [ ] Vibe reference is named (or the file says "user steering only" if Gate 1 was skipped).
  - [ ] Chosen headline is 3–6 words.
  - [ ] Chosen headline does not contain any banned hype word from `references/thumbnail-headline-patterns.md`.
  - [ ] Chosen headline does not contain an em-dash or `delve`/`tapestry`.
  - [ ] Variant A prompt exists and includes "wide" or "editorial" framing.
  - [ ] Variant B prompt exists and includes "close-up" or "tight" framing.
  - [ ] Both prompts include the character-reference instruction (the file references `illustrated-justin-ref.png` or contains `{{CHARACTER_REFERENCE_IMAGE}}`).
  - [ ] Both prompts include "no text" / "exclude text" / equivalent.
  - [ ] Both prompts include 16:9 / 1280×720 aspect.
  - [ ] Both prompts include the mobile-safe-zone rule (center 80%).
  - [ ] Text overlay spec section names the dispatch serial `DISPATCH №004`.
  - [ ] Text overlay spec names Courier Prime as the typeface.
  - [ ] Text overlay spec names exactly one of: slate-400, slate-600, black, twilight as the recommended color (no other colors named for the overlay text).
  - [ ] The "Per-tool quirks" section is appended (since this is reference-image mode).
  - [ ] No Gate 3 render gate was offered (reference-image mode suppresses it).

- [ ] **Step 5: Capture any failing criteria**

If any criterion fails, list the failures with their criterion number and observed value. Do not commit anything in this task — Task 10 handles iteration.

- [ ] **Step 6: If all criteria pass**, commit a validation marker:

```bash
cd /Users/justin/CascadeProjects/claude-skills && git commit --allow-empty -m "validate tcn-youtube-thumbnail against dispatch-004 narration (reference-image mode)"
```

---

## Task 10: Iterate on failing criteria (only if Task 9 produced failures)

**Files:**
- Modify (as needed): `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/SKILL.md`
- Modify (as needed): files under `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/references/`

- [ ] **Step 1: For each failed criterion from Task 9 Step 5, identify which file is responsible**

Use this mapping:

| Failed criterion | Likely file to edit |
|---|---|
| Mode header missing/wrong | SKILL.md (process step 2 description) |
| Vibe-reference field missing | SKILL.md (artifact template in §5.1 equivalent) |
| Headline fails word-count | `references/thumbnail-headline-patterns.md` (tighten the criterion) + SKILL.md retry-behavior wiring |
| Headline contains banned word | `references/thumbnail-headline-patterns.md` (extend banned list or fix examples) |
| Variant A/B framing wrong | `references/flux-prompt-template.md` or `references/reference-image-prompt-template.md` |
| No-text instruction missing | The active mode's prompt template file |
| Aspect ratio missing | The active mode's prompt template file |
| Safe-zone rule missing | The active mode's prompt template file |
| Dispatch serial wrong format | `references/text-overlay-spec.md` (the spec block format) |
| Typeface wrong | `references/text-overlay-spec.md` |
| Off-palette color | `references/text-overlay-spec.md` (palette restrictions section) |
| Per-tool quirks missing | `references/reference-image-prompt-template.md` |
| Gate 3 inappropriately fired | SKILL.md (process step 11 — confirm "LoRA mode only" guard) |

- [ ] **Step 2: Make the targeted edit(s)**

Use the Edit tool against each file with the minimal change needed.

- [ ] **Step 3: Re-run Task 9 Step 3 + Step 4 against the same dispatch-004 narration**

Confirm previously-failing criteria now pass and previously-passing ones still pass.

- [ ] **Step 4: Commit each iteration as a separate commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills && git add tcn-youtube-thumbnail/ && git commit -m "fix <specific criterion> in tcn-youtube-thumbnail"
```

Repeat steps 1–4 until all criteria pass.

---

## Task 11: Hand off for Friday recording

**Files:**
- Read-only: `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/SKILL.md`
- Read-only: artifact at `~/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-thumbnail.md`

- [ ] **Step 1: Print a one-line invocation cheat sheet**

The skill is now invocable in any Claude Code session. Surface this to the user:

> The `tcn-youtube-thumbnail` skill is live. Invoke with:
> - "build the thumbnail for [narration path]"
> - "thumbnail prompts for this dispatch"
> - "make the thumbnail for №004"
>
> Reference-image mode is active until a Flux LoRA URL is set at `~/.config/tcn/illustrated-justin-lora.url` (one line containing the URL).

- [ ] **Step 2: Confirm the produced artifact for dispatch-004 is usable**

Open the artifact at `~/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/youtube-thumbnail.md`. Confirm by inspection that:
- Both variant prompts read as executable in a real image-gen tool.
- The text overlay spec is concrete enough to composite in Figma without further questions.

- [ ] **Step 3: Update the project memory**

Update `/Users/justin/.claude/projects/-Users-justin-CascadeProjects-claude-skills/memory/project_tcn_youtube_workflow.md`:
- Move `tcn-youtube-thumbnail` from "What's planned" to "What's built".
- Note its actual behavior (dual-mode, two Flux variants, opt-in fal render).
- Note the reference-image-mode default and the LoRA-URL upgrade path.

- [ ] **Step 4: No commit needed** — the memory file is outside the repo. The repo's last meaningful commit was the validation in Task 9 / iteration in Task 10.

---

## Self-Review

### Spec coverage

Walked through spec §1–§15:
- §1 (context) → Task 3 (SKILL.md "What this skill does")
- §2 (ecosystem position) → Task 3 (SKILL.md "Position in workflow")
- §3 (architectural decisions) → Tasks 3, 4, 7, 8 (decisions baked into SKILL.md, headline patterns, both prompt templates)
- §4 (inputs) → Task 3 (frontmatter triggers + SKILL.md "Inputs" section)
- §5 (outputs) → Task 3 (SKILL.md "Outputs" + artifact file template)
- §6 (process) → Task 3 (SKILL.md "The process", 12 steps)
- §7 (generation modes) → Task 3 (SKILL.md mode table) + Tasks 7, 8 (prompt templates per mode)
- §8 (text overlay) → Task 6 (`references/text-overlay-spec.md`) + Task 3 (SKILL.md summary)
- §9 (headline distillation) → Task 4 (`references/thumbnail-headline-patterns.md`) + Task 3 (SKILL.md summary)
- §10 (TCN identity markers) → Task 3 (SKILL.md section)
- §11 (failure modes) → Task 3 (SKILL.md section) + Task 9 (validation surfaces real failure modes)
- §12 (reference files) → Tasks 4–8 (one task per file)
- §13 (what skill is NOT) → Task 3 (SKILL.md section)
- §14 (companion skills) → Task 3 (SKILL.md section)
- §15 (open questions) → no implementation surface; tracked in spec only

No gaps.

### Placeholder scan

Searched the plan for placeholder patterns. None found. Reference files have content templates with actual prose, examples, and category lists — not "fill in later" markers. The `{{ILLUSTRATED_JUSTIN_LORA_URL}}` and `{{CHARACTER_REFERENCE_IMAGE}}` strings are runtime substitution slots (the skill emits them when the corresponding source is missing), not plan placeholders.

### Type consistency

- File paths: consistent across tasks (`/Users/justin/CascadeProjects/claude-skills/tcn-youtube-thumbnail/...`).
- Symlink path: consistent (`~/.claude/skills/tcn-youtube-thumbnail/`).
- Mode names: `lora` and `reference-image` used uniformly (matches spec).
- Variant labels: "Variant A — wide editorial composition" and "Variant B — tight close-up composition" used uniformly across Tasks 7, 8, 9.
- Gate naming: Gate 1 (vibe), Gate 2 (headline), Gate 3 (render) used uniformly.
- Headline criteria: word-count rules (3–6 inclusive, hyphenates count as 1) consistent between spec §9.2 and Task 4 content.
