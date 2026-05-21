# tcn-youtube-thumbnail — Design Spec

**Status:** Approved (2026-05-21)
**Author:** Justin Hearn (drinkYourOJ / The Civic Node)
**Implementation track:** `tcn-youtube-thumbnail` skill, to be built with `anthropic-skills:skill-creator`
**Position in ecosystem:** Step 5 of the TCN YouTube production workflow (downstream of recording, optional pre-record concepting)

---

## 1. Context — why this skill exists

The Civic Node publishes a flagship Substack article each week, plus a companion 5–7 minute YouTube trailer-format video. The YouTube video's job is to drive click-through to Substack, which makes the thumbnail one of the highest-leverage assets in the funnel: it's the gating image between every YouTube impression and any further engagement.

Two upstream skills exist (`tcn-youtube-narration`, `tcn-youtube-slideshow`) and recording happens between Step 2 and Step 3. After recording, three downstream packaging skills are planned: `tcn-youtube-title`, `tcn-youtube-description`, and this one — `tcn-youtube-thumbnail`.

Today, Justin's thumbnail process is ad-hoc: open an image-gen tool, hand-prompt a scene, hand-overlay text in Figma. The result is inconsistent in character (different faces across dispatches), inconsistent in typography, and slow to produce.

`tcn-youtube-thumbnail` automates the prompt composition. The skill is a **prompt-builder** (with an optional render step) modeled on `ai-image-prompts-skill`: it queries a curated 10,000+ prompt library for thumbnail-shaped vibe references, lets the user pick one, drafts thumbnail headline candidates, and emits two Flux prompt variants (for A/B testing) plus a text overlay spec that survives YouTube's mobile-feed crop.

Character consistency across dispatches is achieved either via a trained Flux LoRA (Justin's preferred long-term state) or via a reference image (the immediate, no-training state). The skill auto-detects which mode applies and adapts.

---

## 2. Position in the TCN ecosystem

```
Article (tcn-article-builder)
    ↓
tcn-youtube-narration  [Step 1]
    ↓
tcn-youtube-slideshow  [Step 2]
    ↓
┌─── RECORDING ───┐
    ↓
tcn-youtube-title         [Step 3 — planned]
tcn-youtube-description   [Step 4 — planned]
tcn-youtube-thumbnail     [Step 5 — this skill]
```

Recording is the cleavage point between upstream skills (which consume article prose) and downstream packaging skills (which consume the recorded transcript).

`tcn-youtube-thumbnail` is the only packaging skill that can also run pre-record, against the narration's cold-open candidate, for early thumbnail concepting. The recommended production order is: run pre-record for ideation, re-run post-record with the actual transcript for the final thumbnail.

The skill has one upstream dependency it explicitly invokes: `ai-image-prompts-skill` (used to surface 2–3 library candidates at the vibe-pick gate). It does not invoke any other skill.

---

## 3. Architectural decisions (the load-bearing ones)

These were resolved during brainstorming. Each is a fork in the road that subsequent design choices follow from.

### 3.1 Shape — library recommender, not pure prompt-builder

The skill follows the `ai-image-prompts-skill` shape — query a curated library, surface candidates with sample images, let the user pick a vibe — rather than the `tcn-youtube-slideshow` shape (deterministic prompt composition with no library lookup). Reason: thumbnails benefit from CTR-proven visual patterns, and the YouMind library already aggregates those.

### 3.2 Brand posture — CTR-first with TCN identity markers

The skill optimizes for YouTube CTR conventions (bigger faces, contrasting colors, bold text overlays) but always anchors the thumbnail with TCN identity markers: the mark, Courier Prime typography on overlay text, and the dispatch serial (`DISPATCH №NNN`). This is a deliberate deviation from the strict TCN brand austerity that governs the slideshow and substack skills. Reason: the thumbnail is a funnel gate, not a brand artifact — its job is conversion, not brand purity.

### 3.3 Character strategy — illustrated-Justin, dual-mode

The skill produces prompts that include an illustrated-Justin character. Two character-consistency mechanisms are supported, auto-detected:

- **Reference-image mode (default):** prompt references a static `illustrated-justin-ref.png`. Model-agnostic — works with any tool that accepts a character reference (Freepik, Nano Banana Pro / Gemini, Midjourney `--cref`, Flux Kontext). No render assistance from the skill.
- **LoRA mode (upgrade):** prompt references a Flux LoRA URL trained on illustrated-Justin imagery. Flux-specific. Skill offers an opt-in fal MCP render step.

Path A originally planned (Higgsfield SoulID) was rejected because Higgsfield requires a paid subscription Justin doesn't want to add. Path D (fal-trained Flux LoRA) is portable: the `.safetensors` is downloadable and works with any host running Flux.1 [dev], so the skill is not coupled to fal long-term.

### 3.4 Two-gate interaction model

The skill pauses twice for user input:

- **Gate 1 — Vibe pick.** After the library returns 2–3 candidates with sample images, user picks one (or asks for new options, or skips library entirely).
- **Gate 2 — Headline pick.** After the skill drafts 3 thumbnail headline candidates, user picks one (or asks for new options, or pastes their own).

Both gates accept override-at-invocation: if the user supplies a vibe or a headline up front, the corresponding gate is skipped.

### 3.5 Two final variants for A/B testing

The skill produces exactly two final Flux prompts per run. Same character, same chosen vibe, same headline. They differ only in composition (Variant A = wide editorial framing; Variant B = tighter close-up with stronger figure emphasis). Intent: YouTube's native thumbnail A/B test feature can pit them against each other.

### 3.6 Opt-in render

In LoRA mode, after writing the prompt artifact, the skill asks once: "Render both variants now via fal? Cost ~$0.10 total." User confirms or declines per-run. Default is to ask, not to skip. Reason: convenience for the common case (most runs the user wants the images), but explicit confirmation because each render costs money.

In reference-image mode, the render gate is suppressed — there's no service the skill knows to invoke.

---

## 4. Inputs

### 4.1 Required

- **Path to a narration file (`youtube-narration.md`) OR a recorded transcript.** Skill auto-detects: it looks for both in the supplied directory; transcript wins if both are present. If the user pastes contents directly (instead of a path), the skill saves to a temp file and proceeds.

### 4.2 Optional

- **Path to the illustrated-Justin LoRA URL store.** Lookup order, first hit wins:
  1. Explicit invocation argument (e.g., `--lora-url <url>` or natural-language equivalent)
  2. `~/.config/tcn/illustrated-justin-lora.url` (one line containing the URL)
  3. `TCN_ILLUSTRATED_JUSTIN_LORA_URL` environment variable

  Absence of all three triggers reference-image mode.

- **Path to the illustrated-Justin reference image.** Default `~/Documents/illustrated-justin-ref.png`. Used only in reference-image mode. If missing, the produced prompts contain a `{{CHARACTER_REFERENCE_IMAGE}}` placeholder and a one-line setup note.

- **Steering** — free-text guidance like "more daytime", "wide shot, not close-up", "lean apocalyptic-tech vibe", "no faces in this one".

- **Override vibe** — user names a library prompt slug or category to skip Gate 1.

- **Override headline** — user supplies the thumbnail headline directly to skip Gate 2.

---

## 5. Outputs

### 5.1 Primary artifact

Written to `workspace/drafts/<slug>/youtube-thumbnail.md`. The file structure:

```markdown
# Thumbnail prompts — TCN Dispatch №NNN

**Mode:** lora | reference-image
**Generated:** YYYY-MM-DD
**Vibe reference:** <library prompt name + URL, or "user steering only">
**Chosen headline:** "<3–6 word headline>"

---

## Variant A — wide editorial composition

[Full Flux prompt or model-agnostic reference-image prompt, with LoRA URL or reference image path embedded]

## Variant B — tight close-up composition

[Full Flux prompt or model-agnostic reference-image prompt, same character/vibe, different framing]

---

## Text overlay spec

[Full overlay specification — see §8]
```

### 5.2 Optional rendered artifacts (LoRA mode only)

If the user accepts the render gate, two PNGs are saved alongside the `.md`:

- `workspace/drafts/<slug>/thumbnail-variant-a.png`
- `workspace/drafts/<slug>/thumbnail-variant-b.png`

Both at 1280×720, generated via fal MCP (`mcp__fal-ai__run_model`) against a Flux.1 [dev] endpoint with the LoRA URL parameter set.

### 5.3 What the skill explicitly does NOT produce

- Trained LoRA files. The LoRA is a one-time setup the user performs separately via fal MCP. The skill assumes its URL is already known.
- Canonical illustrated-Justin reference images. The reference image is a one-time Freepik (or equivalent) session the user performs separately.
- Composited final thumbnails (image + overlay merged). That happens in Figma/Canva/Photoshop. Skill provides the overlay spec only.
- Substack URL embeds or CTA overlays. The text overlay is headline + identity block only.

---

## 6. The process

1. **Read narration or transcript.** Auto-detect (transcript wins if both exist). Halt with an explicit message if neither is found.

2. **Detect generation mode.** Run the LoRA-URL lookup (§4.2). Set `mode = "lora"` or `mode = "reference-image"`. Log the chosen mode to the user in one line.

3. **Extract dispatch metadata.** Pull the dispatch number from the narration's title block (or the `<slug>` directory naming convention if reading a raw transcript). Pull the cold-open candidate from the narration's Script Notes footer, or the recorded cold-open words from the transcript's first ~30 seconds.

4. **Compose the library query.** Build a TCN-flavored search string from the dispatch concept. Pattern: "illustrated editorial YouTube thumbnail, [dispatch subject in 3–6 words], dramatic composition, character-driven, magazine style, mid-shot or close-up." Full query patterns and what to avoid live in `references/vibe-query-templates.md`.

5. **GATE 1 — Vibe pick.** Invoke `ai-image-prompts-skill` with the composed query. It returns 2–3 candidate prompts with sample images. Present to the user:

   > Pick a vibe: A, B, or C. Or 'try again' for new options. Or 'skip' to compose without a library reference.

   Wait for response. If the user provided an override vibe at invocation, skip this gate entirely.

6. **Draft 3 thumbnail headline candidates.** Distill from the cold-open and article concept. See §9 for the full drafting process — drafting inputs (§9.1), acceptance criteria each candidate must pass (§9.2), pattern library reference (§9.3), retry behavior (§9.4), and Gate 2 display format (§9.5). Each candidate is 3–6 words and must pass §9.2 before being surfaced.

7. **GATE 2 — Headline pick.** Present:

   > Pick a headline: 1, 2, or 3. Or 'try again' for new options. Or paste your own.

   Wait for response. If an override headline was supplied at invocation, skip this gate.

8. **Compose the two prompt variants.** Both share the chosen vibe + chosen character source + chosen headline (which the prompts do *not* render — text is overlay-only). They differ in composition: Variant A = wide editorial framing; Variant B = tighter close-up with stronger figure emphasis.

   Each prompt:
   - Includes the illustrated-Justin character (via LoRA URL or reference image path, mode-dependent).
   - Names the dispatch subject and the chosen vibe directive.
   - Specifies 1280×720 aspect.
   - Instructs the model to keep the center ~80% of the frame un-busy (mobile safe zone for text overlay).
   - Excludes any text rendering — no in-image text at all.

   Full Flux-mode prompt template lives in `references/flux-prompt-template.md`. Full reference-image-mode template lives in `references/reference-image-prompt-template.md`.

9. **Compose the text overlay spec.** Specifies the chosen headline + the corner identity block (DISPATCH №NNN + mark.svg), with typography, positioning, and color directives sufficient for Figma/Canva/Photoshop compositing. See §8.

10. **Write the artifact file.** `workspace/drafts/<slug>/youtube-thumbnail.md` with mode header, both prompts, and overlay spec.

11. **GATE 3 — Render gate (LoRA mode only).** Ask:

    > Render both variants now via fal? Cost ~$0.10 total. yes / no / skip

    On yes: call `mcp__fal-ai__run_model` for each variant with the Flux endpoint + LoRA URL. Save PNGs (§5.2). Report paths.
    On no/skip: artifact-only output. Note in the message that the user can render manually later.
    In reference-image mode: this gate is suppressed.

12. **Final gate.** Present:

    > Thumbnail artifacts ready at `<path>`. Approve, redirect (e.g., 'tighter vibe', 'redo headline', 'swap Variant B to wide shot', 'lower contrast'), or cancel?

    Wait for response. Redirects re-enter the affected step(s) only.

---

## 7. Generation modes — what differs between LoRA and reference-image

| Concern | Reference-image mode | LoRA mode |
|---|---|---|
| Activation | No LoRA URL found | LoRA URL found in any of the three sources |
| Character source in prompt | Inline reference to `illustrated-justin-ref.png` path | Inline LoRA URL parameter |
| Prompt format | Model-agnostic — "use the attached reference image as character reference, match facial features and styling" | Flux-specific — formatted for fal MCP's `run_model` schema with Flux.1 [dev] endpoint |
| Render assist | None — user pastes prompt into their image-gen tool of choice | Opt-in: skill offers to call fal MCP and save PNGs |
| Output file header | `**Mode:** reference-image` | `**Mode:** lora` |
| Mobile safe zone directive | Same in both modes | Same in both modes |
| Aspect ratio | 1280×720 in both modes | 1280×720 in both modes |
| Text overlay spec | Identical in both modes | Identical in both modes |

---

## 8. Text overlay specification

The overlay spec section in `youtube-thumbnail.md` contains all the information needed to composite text onto the rendered image in Figma, Canva, or Photoshop. Spec includes:

- **Chosen headline**
  - The 3–6 word headline picked at Gate 2.
  - Typography: Courier Prime Bold, sentence case (matches TCN voice rule — no all-caps screaming).
  - Default size: ~120 px at 1280×720 canvas. Adjustable per overlay tool.
  - Color: slate-400 (`#557FA3`) and black (`#0D0D0F`) are both valid. The skill recommends one based on the chosen vibe's stated lighting/mood — e.g., a "dramatic night scene" vibe → slate-400 recommended; a "bright daytime editorial" vibe → black recommended. The overlay spec lists both options so the user finalizes at composite time when the actual rendered image is in front of them.
  - Optional 4–6 px stroke/halo for legibility when the illustration is busy. User-discretion at composite time.
  - Position: default center-left, baseline at ~55% of canvas height. Stays inside the center 80% (mobile safe zone).

- **Corner identity block (DISPATCH №NNN + mark)**
  - `DISPATCH №NNN` in Courier Prime Regular, wide-tracked (`0.18em`), all-caps, ~24 px at 1280×720.
  - Mark: `mark.svg` from the TCN design system, ~40 px square.
  - Default position: top-right corner, mark above the dispatch number, both anchored to the safe-zone edge.
  - Color: slate-400 on dark scenes, slate-600 (`#3A6A8F`) on light scenes.

- **Color tokens** — explicit references to `colors_and_type.css` values: `slate-400`, `slate-600`, `black`, `twilight`. No other colors.

- **Mobile safe-zone note** — repeated in the spec so the compositor doesn't forget: "All text must stay inside the center 80% of the canvas. YouTube crops mobile feed thumbnails aggressively at the edges."

Full overlay-spec template (with all sizing curves and edge cases) lives in `references/text-overlay-spec.md`.

---

## 9. Thumbnail headline distillation

Thumbnail headlines are a distinct content genre from article headlines, social hooks, or the cold-open candidate. 3–6 words has to set up a curiosity gap, anchor a concrete specific, and carry TCN voice in a fraction of a second of scrolling. This section defines the drafting process, acceptance criteria, and retry behavior — first-class design substance, not a "we'll see" note.

### 9.1 Drafting inputs

When the skill drafts candidates (process step 6, §6), it has:

- The cold-open candidate (or recorded cold open) — the dispatch's most punchable line.
- The dispatch concept — the broader article subject, extracted from the narration's structure.
- The dispatch number, slug, and any user-supplied steering.
- The full contents of `references/thumbnail-headline-patterns.md` (loaded into context at drafting time as the source of truth for voice and structural patterns).

### 9.2 Acceptance criteria (every candidate must pass)

A candidate is rejected silently and re-drafted (§9.4) if it fails any of:

- **Word count.** 3–6 words inclusive. Hyphenated compounds count as one word. Contractions count as one word. Numbers count as one word regardless of digit count.
- **No all-caps words.** Sentence case only. Genuine acronyms (FCC, ATC, FAA, DAO) are exceptions.
- **No exclamation points.** Question marks allowed sparingly, only when load-bearing for a curiosity gap.
- **No banned hype adjectives.** Explicit banned list in the patterns reference file. Initial set: SHOCKING, AMAZING, INSANE, EXPOSED, REVEALED, UNBELIEVABLE, MASSIVE, ULTIMATE, EPIC, INCREDIBLE, MIND-BLOWING, GAME-CHANGING. Case-insensitive match.
- **No banned clickbait templates.** "This One Trick…", "What They Don't Want…", "You Won't Believe…", "Here's Why…", "The Truth About…", and other generic-YouTube structures.
- **Concrete specific when supported.** If the cold-open contains a number, place name, dollar amount, year, or proper noun, at least one of the three candidates must use it. (Not all three — variety is good.)
- **Anti-AI-tell scan.** Reject candidates containing em-dashes, "delve", "tapestry", "navigate the landscape", or any token from the `tcn-text-humanizer` skill's tell list (referenced, not duplicated, in the patterns file).

The banned-word/template lists are deliberately maintained in `references/thumbnail-headline-patterns.md`, not in this spec, so they can be extended without spec churn after real dispatches surface new failure modes.

### 9.3 Pattern library (in `references/thumbnail-headline-patterns.md`)

The patterns reference file is the substantive guidance the skill reads at drafting time. Categories the file covers:

- **Proven structural patterns**, each with worked examples drawn from real or plausible TCN dispatches:
  - *Concrete Anchor + Twist* — "You Own the Hotspot"
  - *Implied Stakes* — "Nova Labs Owns It"
  - *Direct Address* — "Why You're Funding This"
  - *Specific Contradiction* — "$499 to Mine WiFi"
  - *Bare-Noun Provocation* — "The Hotspot Tax"
- **Voice anchors** — sentence-case, declarative-or-curiosity-gap, sardonic register, never-screaming, never-clickbait-shaped. Inherits from TCN's anti-AI-writing-style corpus and the `justin-hearn-voice-profile.md`.
- **Worked example walkthroughs** — for at least 2 real dispatches: cold-open → 3 drafted candidates → which one was picked and why.
- **Anti-pattern gallery** — failed candidates and the specific criterion they violated. Educational, not exhaustive.

### 9.4 Retry behavior

If any of the 3 initially drafted candidates fails the §9.2 acceptance criteria, the skill internally re-drafts the failing slot(s) up to 2 additional attempts before surfacing. If after 3 total attempts a slot still fails, the skill surfaces the best-effort candidate with a one-line note ("could not satisfy [criterion]; consider redirecting"). The user never sees a hard error — they always see 3 candidates.

Re-drafts are silent — the user doesn't see rejected attempts. Surfacing only passing candidates keeps the Gate 2 cognitive load low.

### 9.5 What the user sees at Gate 2

After successful drafting, the user sees:

```
Pick a thumbnail headline:

1. <Candidate 1>
   — <one-line rationale: pattern used, anchor, curiosity-gap mechanism>

2. <Candidate 2>
   — <rationale>

3. <Candidate 3>
   — <rationale>

Or 'try again' for new options. Or paste your own.
```

Rationales surface the *why* of each candidate, not just the words — they help the user pick on intent, not just gut feel.

---

## 10. TCN identity markers (the brand anchors)

Every thumbnail this skill produces carries these constant markers, regardless of vibe or mode:

- **The TCN mark** in the corner identity block.
- **`DISPATCH №NNN`** in the corner identity block. Zero-padded. Middle dot `·` if a sub-label is added. Mono typeface, wide-tracked, all-caps.
- **Courier Prime** as the only typeface anywhere in the overlay. Bold for the headline, regular for the dispatch serial.
- **Slate-400 / slate-600 / black / twilight** as the only colors used in the overlay text. The illustrated scene itself can use other colors (it's the CTR layer, per §3.2), but the overlay anchors stay strictly in palette.

The illustrated scene is *not* constrained to TCN brand palette — that's a deliberate trade per §3.2. CTR conventions (bright accents, dramatic lighting, expressive character work) can fully apply to the scene. The overlay carries the brand load.

---

## 11. Failure modes

- **No narration and no transcript found** → halt with an explicit message and an example path. Do not attempt to compose from nothing.

- **Narration malformed** (no Script Notes footer, no cold-open candidate, no title block) → halt and ask the user to either supply a cold-open candidate as steering or fix the narration upstream.

- **Library lookup returns nothing usable** → skip Gate 1 silently; compose without a vibe reference. Note this in the artifact file header.

- **fal MCP not installed but user has a LoRA URL** → produce the artifact in LoRA mode normally; suppress the render gate with a one-line note ("fal MCP not detected — skipping render gate; run prompts manually").

- **fal render fails** (timeout, credit exhausted, model unavailable) → keep the prompt artifact intact; surface the error message; suggest manual render via the prompt as-is.

- **Reference image missing in reference-image mode** → produce the artifact with `{{CHARACTER_REFERENCE_IMAGE}}` placeholder and a setup note (where to place the file, suggested filename, suggested specs).

- **Dispatch number missing from narration title block and not derivable from the slug** → halt and ask the user to confirm. Do not guess.

- **Combined / non-standard narration zones** → tolerate. The thumbnail only needs the cold-open and the overall dispatch concept, not the full slide structure.

- **User redirects at the final gate** → re-enter only the affected gate(s):
  - "tighter vibe" → re-enter Gate 1 with stronger steering
  - "redo headline" → re-enter Gate 2
  - "swap Variant B to wide shot" → re-compose Variant B only
  - "lower contrast" or other stylistic redirects → re-compose both prompts with the steering applied

---

## 12. Reference files (to be authored alongside the skill)

- **`references/vibe-query-templates.md`** — how to compose the TCN-flavored library query from a dispatch concept. Query patterns that work, query patterns to avoid, example transformations of cold-open → library query.

- **`references/thumbnail-headline-patterns.md`** — pattern library for the §9 candidate drafting. Voice rules, banned-word lists, banned clickbait template list, structural patterns with worked examples, anti-pattern gallery. The source of truth for headline drafting — the skill reads this file at drafting time. Maintained as a living document.

- **`references/text-overlay-spec.md`** — full typography/layout/color spec for the overlay. Courier Prime sizing curves at 1280×720 and at common Figma frame sizes. Safe-zone math (the center-80% rule explained). Mark sizing rules. Color tokens pulled from `colors_and_type.css`.

- **`references/flux-prompt-template.md`** — the Flux prompt structure for LoRA mode. Composition directives for Variant A vs Variant B. Mobile-safe-zone phrasing. Negative prompt patterns. fal MCP `run_model` parameter shape.

- **`references/reference-image-prompt-template.md`** — the model-agnostic prompt structure for reference-image mode. Phrasing that works across Freepik, Nano Banana Pro, Midjourney `--cref`, Flux Kontext. Notes on each tool's quirks.

---

## 13. What this skill is NOT

- Not a LoRA trainer. LoRA training is a one-time user task via fal MCP (or any Flux LoRA training service). The skill assumes the URL is provided.

- Not a reference-image generator. The canonical `illustrated-justin-ref.png` is a one-time Freepik (or equivalent) session.

- Not a compositor. The skill writes the overlay spec; Figma/Canva/Photoshop composite the final image.

- Not a YouTube uploader. The skill produces the artifacts; the user uploads to YouTube manually (or via a future packaging skill).

- Not a title or description generator. Those are sibling skills (`tcn-youtube-title`, `tcn-youtube-description`).

- Not an article or narration generator. Those are upstream skills.

- Not a brand-strict thumbnail (per §3.2). The illustrated scene is CTR-first; only the overlay anchors carry the brand load.

---

## 14. Companion skills and dependencies

**Upstream:**
- `tcn-youtube-narration` — produces the narration file the skill can read pre-record.
- Recording → transcript — produces the transcript the skill prefers post-record.

**Sibling (planned, not built today):**
- `tcn-youtube-title` — title generation, consumes the recorded transcript.
- `tcn-youtube-description` — description body, tags, chapter timestamps.

**Explicit invocation dependency:**
- `ai-image-prompts-skill` — invoked at Gate 1 for library candidates. Must be installed; if missing, the skill falls back to "no library reference" composition and notes this in the artifact header.

**Optional runtime dependencies:**
- `fal-ai` MCP — required only for the opt-in render gate in LoRA mode.

**Shared design-system reference:**
- `~/Documents/The Civic Node — Design System.zip` — referenced for color tokens, mark.svg, and Courier Prime sizing. The skill does not parse the zip itself; the overlay spec it produces names the canonical tokens.

---

## 15. Open questions / future work

- **LoRA training helper.** A potential sibling skill could wrap fal MCP's Flux LoRA training endpoint with TCN-specific defaults (step count, learning rate, reference-image count guidance). Deferred until after Friday recording proves the skill's value.

- **Pattern library iteration.** The §9 acceptance criteria and the patterns reference file are v1. After a few real dispatches we may discover (a) the banned-word or banned-template lists need extension, (b) new structural patterns emerge worth promoting, or (c) certain initially-banned constructions turn out to work for TCN's audience and should be allowed. Maintain by editing `references/thumbnail-headline-patterns.md` directly — no skill-code changes required.

- **Calibration via past dispatches (deferred from v1).** Initial brainstorm considered scanning sibling `youtube-thumbnail.md` files and seeding the drafting prompt with the last 3–5 chosen headlines as in-context voice examples — a feedback loop that learns from production runs. Deferred — single-dispatch quality first via §9's explicit criteria, calibration loop added if voice drift becomes a real problem.

- **A/B test winner feedback loop.** YouTube exposes A/B thumbnail performance data. A future iteration could feed that back into the vibe-query templates to learn which compositions/headline shapes win for TCN. Deferred until at least 5 dispatches have run.

- **Multi-language overlay.** Currently English-only. Not on the roadmap.

- **Static asset bundling for the overlay.** The compositor still needs to source `mark.svg` from the design-system bundle each time. A future iteration could copy the mark into `workspace/drafts/<slug>/` alongside the artifacts so the entire overlay session is self-contained.
