---
name: tcn-youtube-narration
description: Step 1 of the Civic Node YouTube production workflow — converts an approved article draft into a 5-7 minute trailer-format narration script with slide markers, pacing notes, and refrain markers. Calibrated to a "Hank Green meets Vox" register and explicitly written to drive Substack click-through, not to summarize the article. Invoke this skill when the user says "write the narration", "narration script", "video script from this article", "narrate this for YouTube", "do the script for Friday's video", or when the user points at a finished article draft and asks for a video script. Does NOT apply to social posts (that's tcn-post), full articles (tcn-draft), or YouTube packaging — title, description, and thumbnail come from separate skills.
---

# The Civic Node — YouTube Narration (Step 1 of the YouTube Production Workflow)

## What This Skill Does

Converts a finished Civic Node article draft into a 5-7 minute trailer-format YouTube narration script (700-1,050 words at ~140 wpm) with standardized slide markers and a Script Notes footer. The output is structured as a trailer-funnel: it teases the article's strongest hook, names what the video deliberately does not cover, and routes viewers to read the full piece on Substack. The register sits at a 6-7 on a 1-10 dial — recognizably TCN-Marcus, but sharper, more colloquial, and tuned for a broader YouTube audience than the Substack reader base.

---

## Voice & vocabulary canonical source

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule (§ 1), the banned-words list (§ 3A), dead phrases / transitions / engagement bait / hype language (§ 3B–§ 3E), the negative-parallelism rule (§ 3F), tribal-coded crypto cringe and operational shibboleths (§ 3G), the dismissal-label rule (§ 3H), the vocabulary cliff rules including the meaning-preservation sub-principle (§ 3I), the closing-line abstraction rule (§ 3J), the broader AI writing patterns to avoid (§ 4), and the anti-overfitting guide (§ 5).

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on a copy embedded in this spec. Any short examples cited here are illustrative only — the canonical file is authoritative.

**Fallback when the canonical file is missing.** If `workspace/core/anti-ai-writing-style.md` is not present in the current project, this skill must:
1. Flag explicitly to the user — "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip all voice-related work — no AI-hit-list cross-check on candidate narration scripts.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still structure the script as Cold Open / Body / Outro, still pick from the middle-slide menu, still compose the Script Notes footer, still run the spoken-word adaptations (sentence-length cap, no em-dashes, no subordinate-clause stacks, one-word landings). Flag "voice rules pass" as not enforced in the recommendation. Better to do less than to do harm with stale or generic guidance.

---

## Why a Trailer, Not a Translation

The YouTube video is a trailer for the article, not a video version of it. Its job is to drive Substack click-through.

That framing is load-bearing because it inverts the default impulse. The default impulse — the one the legacy narration documents reached for — is to take the article and read it out loud, lightly compressed. That produces a script that fully resolves the argument on YouTube, which leaves the viewer with no reason to click through. A satisfied viewer is a lost reader.

A trailer does the opposite. It opens the loop, lands the strongest hook, surfaces enough evidence that the viewer believes the article will deliver, and then explicitly names what the video did NOT cover. The Tease slide is the funnel mechanism. The article resolves the curiosity gap; the video creates it.

Every structural decision in this skill flows from that framing.

---

## Position in the YouTube Workflow

This skill is **Step 1 of the YouTube production workflow** — it runs after the article is finalized and before any recording happens.

**Upstream sources (what this skill reads):**
- The finished article draft (`tcn-draft` output, typically `workspace/drafts/<slug>/05-draft-v{N}.md`)
- The fact-check report (`tcn-fact-check` output, optional — for Verbatim slide source quotes)
- `workspace/core/anti-ai-writing-style.md` (voice rules)

**Downstream consumers (what reads this skill's output):**
- `tcn-youtube-slideshow` (planned) — consumes slide markers + visual cues to produce slideshow prompts
- `tcn-youtube-title` (planned) — optionally reads the cold-open candidate for title inspiration
- `tcn-youtube-description` (planned) — optionally reads slide-aligned chapter names
- `tcn-youtube-thumbnail` (planned) — optionally reads the cold-open candidate for visual metaphor

The full ecosystem diagram lives in the design spec at `docs/superpowers/specs/2026-05-20-tcn-youtube-narration-design.md`.

---

## Inputs and Outputs

### Required input

- **Path to a finished article draft.** Typically `workspace/drafts/<slug>/05-draft-v{N}.md`. The skill reads this verbatim. If the user pastes the article contents directly instead of supplying a path, save the paste to a temp file and proceed.

### Optional inputs

- **Path to the fact-check report** (`workspace/drafts/<slug>/08-fact-check-v{N}.md`) — if present, surfaces verified primary-source quotes for use in a Verbatim middle-slide. If the report has unresolved flagged items, warn the user before drafting.
- **Length override** — defaults to 5-7 min target. Accepts "make it 4 min" or "make it 8 min"; recalibrate compression.
- **Steering** — free-text guidance like "lean into the historical-echo angle," "keep the McDonald's analogy as the hook," "no Verbatim slide this time."

### Output artifact

- **File:** `workspace/drafts/<slug>/youtube-narration.md`
- **Contents:** Title block (article title + dispatch number + slide count + format tag), 7-9 slide blocks in standardized markup, Script Notes footer.
- **Does NOT contain:** title options, YouTube description, chapter timestamps, tags, thumbnail prompt — those come from separate skills.

### Gate prompt presented to user

> Narration draft complete (~[N] words, ~[M]:[SS] runtime). Approve, redirect (e.g., 'use a different hook', 'swap a middle slide', 'dial the register catchier/drier'), or cancel?

**Stop after presenting the draft.** Wait for user approval or redirect before doing anything else.

---

## The Narration Structure

Three zones, 7-9 slides total, 700-1,050 words at ~140 wpm.

### Cold Open (always 2 slides, 45-60 sec)

**Slide 1 — Hook.** A relatable analogy, surprising number, or "wait, what?" moment. No setup. No TCN-specific jargon. Earns the next 30 seconds of attention.

Example (Helium piece, calibrated to register 7):

```
**[SLIDE 01 — HOOK]**

Buying a McDonald's franchise comes with a 200-page disclosure document.
Federal law requires it. The pricing. The exit terms. What happens if
McDonald's changes the menu and your numbers stop working.

Three hundred eighty-five thousand people bought a Helium hotspot.

The franchise disclosure equivalent? They didn't get one.

Vibes.
```

That example is the floor for register-7 catchiness, not the ceiling. Aim higher when the article supports it. Rhetorical questions, one-word landings, and unexpected analogies are the moves.

**Slide 2 — Thesis.** What the piece argues, distilled to one or two sentences. Often a verbatim or near-verbatim line from the article. The promise the video is making.

### Body (3-5 slides, 3-4 min)

Read the article and pick from this menu by asking *which of these does this article most strongly support?*

- **The Receipt** — strongest concrete evidence. Numbers, dates, names. The "I can prove it" segment. **Usually mandatory.**
- **The Frame** — the TCN lens. The way of looking at it that re-orders everything. Where refrains often live. **Usually mandatory** (one of Frame or Twist is always present).
- **The Stakes** — why Marcus and visiting friends should care. The "this affects you because" segment.
- **The Twist** — the part that genuinely surprised you and will surprise viewers.
- **The Historical Echo** — the comparison that grounds the argument in something familiar (the Volcker moment in a Fed piece; the McDonald's-FDD comparison in a DePIN piece).
- **The Verbatim** — a primary-source quote that lands harder than any paraphrase. Requires the fact-check report to source the quote.

If the article has a refrain candidate (a single sentence the article repeats or implies repeatedly), place it across 2-3 middle slides and mark each occurrence as `[REFRAIN]` in the Script Notes footer.

### Outro (always 2 slides, 30-45 sec)

**Slide N-1 — Tease.** Open loops. Explicitly name what the video did NOT cover. This is the funnel mechanism that converts viewers into readers.

**Slide N — End.** Disclosure (if any) + Substack CTA. **Same close every video** for channel branding:

```
**[SLIDE N — END]**

The Civic Node. Subscribe free at drinkyouroj.substack.com.
Weekly. No hype.
```

Full slide templates and zone-by-zone examples live in `references/structure-templates.md`.

---

## Voice Calibration

### The dial

Register sits at **6-7 on a 1-10 scale** where:

- **1** — dispatch-002 ("The Strait Is the Mandate"). TCN-Marcus, dry essayist, no concessions to general-audience pacing.
- **4** — dispatch-004 ("You Own the Hotspot"). TCN-Marcus with the McDonald's analogy doing some accessibility work.
- **7** — the calibrated register this skill produces. Hank-Vox blend, sharper hooks, willingness to drop a "vibes" once per video, occasional one-word landings.
- **10** — a Hank Green vlog. Too colloquial; concedes Marcus's respect for accessibility.

### Reference channels

- **Hank Green** — colloquial pacing, willingness to break the fourth wall, comedic asides, vulnerable, parenthetical jokes.
- **Vox Explained / late Vox / Search Party (Westbrook)** — formal but emotional, strong narrative arc, declarative, intelligent-but-accessible vocabulary, cinematic structure.

The blend is "intelligent-but-accessible video essay with comedic asides and a willingness to be conversational."

### Calibration tests (every slide must pass both)

1. **Marcus-smirk test** — would Marcus (the TCN-reader persona) smirk at the cleverness, or wince at the bait? If wince, dial down.
2. **Hank-Vox test** — would Hank deliver this line without a wince? Would Vox put a key phrase on screen as a chyron? If either flinches, revise.

### Spoken-word adaptations applied to TCN voice

- **Shorter sentences than written prose.** Max ~22 words, target 12-15.
- **No em-dashes.** Replace with comma + restructure, or with a deliberate one-word landing.
- **No subordinate-clause stacks.** Split into two sentences. Listeners can't track three-clause structures aurally.
- **Numbers spoken aloud.** Write "three hundred eighty-five thousand" not "385,000" — easier for the reader to deliver naturally.
- **One-word landings as a feature.** "Vibes." / "Nobody overrode it." / "Same protocol. Different revenue ladder." These are the Hank move that takes the dial from 4 to 7.
- **Repetition is welcome.** Refrains, callbacks, and deliberate restatement. Written prose avoids these; spoken-word essays embrace them.
- **Concrete over abstract.** Visual word choices. The listener has to picture it on the first hearing.

Full dial worked examples, register-comparison side-by-sides, and the spoken-word adaptations checklist live in `references/voice-calibration.md`.

---

## Output Format

### Title block

```markdown
# [Article Title in Spoken-Word Friendly Form]
## The Civic Node · Dispatch №[NNN]
## [N] slides · trailer-format · 5-7 min target
```

The dispatch number is detected from existing dispatches in the workspace (see step 9 of the process), or captured from the user. The format tag (`trailer-format`) distinguishes new-format scripts from the legacy `Part One / Part Two` format.

### Slide markup convention

```markdown
**[SLIDE NN — SLIDE TITLE]**

[narration text — short sentences, no em-dashes, one-word landings welcome]

[blank line between paragraphs to mark a breath point]

---
```

The `---` between slides is intentional. It gives the reader visual separation when reading aloud.

### Script Notes footer (always present)

```markdown
---

## Script Notes

**Word count:** [N]
**Estimated runtime:** [M]:[SS] at ~140 wpm (TCN-natural pace)
**Voice register:** [N]/10 (Hank-Vox blend) — verified against workspace/core/anti-ai-writing-style.md

**Refrain markers (read slow each time):**
- "[refrain line]" (Slides [list], callback in Slide [N])

**Breath / pacing cues:**
- Slide [NN]: [cue, e.g., "hold the silence after 'Vibes.' for ~1 second"]
- Slide [NN]: [cue]

**Supersedence (if the article has fact-corrections post-narration):**
- (none on this pass — Script Notes block surfaces corrections when present)

**Cold-open candidate** (for thumbnail / title-skill downstream use):
- [the analogy or hook the cold open uses, in one phrase]

**Refrain candidate** (for slideshow skill downstream use):
- [the refrain line, if any]

**Cuts from the article** (what we deliberately did not cover, for Tease slide reference):
- [bulleted list of major article sections not in the video]
```

The "Cold-open candidate," "Refrain candidate," and "Cuts from the article" fields are **forward-compat hooks** the slideshow + title + thumbnail skills will read later. They cost nothing to produce now and save work downstream.

---

## The Process

### 1. Voice file check

Verify `workspace/core/anti-ai-writing-style.md` exists. If missing, halt with the standard TCN fallback message (see Voice & vocabulary canonical source section above). Do not fall back to generic vocabulary heuristics.

### 2. Read the article draft

Read the finished article verbatim. If a fact-check report is supplied, read that too and check for unresolved flagged items — surface those to the user before drafting.

### 3. Identify the hook angle

Find the most relatable analogy or sharable claim in the article. If 2+ strong candidates exist, surface them to the user for selection. If one obvious choice, pick and proceed.

### 4. Identify the thesis line

Distill the article's argument to one or two sentences. Often a verbatim or near-verbatim line from the article.

### 5. Pick the middle-slide menu

Read the article's argument structure and select 3-5 from the menu (Receipt / Frame / Stakes / Twist / Historical Echo / Verbatim). The Receipt is almost always picked; one of Frame or Twist is almost always picked.

### 6. Detect a refrain candidate (optional)

If the article repeats or implies a single load-bearing sentence, mark it as a refrain candidate and place it across 2-3 middle slides.

### 7. Draft the script slide-by-slide

Apply voice calibration (dial 6-7, Hank-Vox blend) and spoken-word adaptations (sentence-length cap, no em-dashes, no subordinate-clause stacks, one-word landings, numbers spelled out). Mark candidate refrain lines as `[REFRAIN]`.

### 8. Compose the Script Notes footer

Word count, runtime estimate, pacing cues, refrain markers, cold-open candidate, refrain candidate, cuts-from-article list. All fields populated — the forward-compat hooks are not optional.

### 9. Detect dispatch number and compose title block

Scan the user's dispatch-narration archive (default: `workspace/dispatch-narration/` relative to the active project root; configurable via steering input) for existing files matching `dispatch-NNN-*.md` and parse out the dispatch numbers. Suggest the next sequential integer (e.g., if `dispatch-002`, `dispatch-003`, `dispatch-004` exist, suggest `005`).

- If detection succeeds with high confidence, surface the suggestion to the user with a one-line confirmation: "Suggesting Dispatch №005 — confirm or override."
- If detection fails (no existing files, ambiguous numbering, gap in sequence) **or** the user is re-recording an existing dispatch (the canonical example: the Friday 2026-05-22 re-record of dispatch-004), ask the user explicitly which dispatch number to use.

Write the number into the title block as `Dispatch №[NNN]` (zero-padded to three digits).

### 10. Present to user with the standard gate prompt

Use the gate prompt from the Inputs and Outputs section. Wait for approval or redirect. Do not proceed past this gate without explicit user instruction.

---

## Failure Modes

- **Article draft missing or unreadable** — surface the failure, ask for a valid path, halt.
- **Voice canonical file missing** — halt with the standard fallback message used by `tcn-headline`. Do not fall back to generic register (per the elasticity-bug failure mode).
- **Article too short for a 5-7 min trailer** (less than ~800 words article-side) — surface to user: "this piece is short enough that the video would cover most of it. Confirm you want a trailer (with curiosity-gap funnel) or a near-full read-through?" Let user override.
- **No obvious hook angle** (rare) — present 2-3 candidate cold-open frames and ask the user to pick.
- **Fact-check report has flagged unresolved items** — surface those before drafting. A trailer can't safely include claims the fact-check skill flagged. Override only if the user explicitly accepts the editorial risk.
- **User redirects** — re-invoke the relevant step:
  - "new hook" → re-draft Slides 01 and 02
  - "swap a middle slide" → ask which slide, generate replacement from menu
  - "dial catchier/drier" → re-draft full script at adjusted register
  - "shorter/longer runtime" → recalibrate compression and re-draft

---

## What This Skill Is NOT

- This skill does **not** generate YouTube titles. That's `tcn-youtube-title` (planned).
- This skill does **not** write the YouTube description body, chapter timestamps, or tags. That's `tcn-youtube-description` (planned, runs after recording for chapter timestamps).
- This skill does **not** produce thumbnail image prompts or text overlays. That's `tcn-youtube-thumbnail` (planned).
- This skill does **not** generate Claude Design slideshow prompts. That's `tcn-youtube-slideshow` (planned).
- This skill does **not** fact-check the article. The article should have been fact-checked via `tcn-fact-check` ↔ `tcn-fact-reconcile` before this skill runs.
- This skill does **not** rewrite or humanize the article prose. That's `tcn-text-humanizer`.
- This skill does **not** write social media posts. That's `tcn-post`.

---

## Companion Skills

**Upstream (this skill reads from):**
- `tcn-draft` — the finished article draft is the primary input.
- `tcn-fact-check` — optional, for Verbatim slide source quotes and pre-flight unresolved-items check.

**Downstream (these skills will read this skill's output, once built):**
- `tcn-youtube-slideshow` — converts slide markers into Claude Design slideshow prompts.
- `tcn-youtube-title` — reads cold-open candidate for title inspiration.
- `tcn-youtube-description` — reads slide markers as semantic chapter names.
- `tcn-youtube-thumbnail` — reads cold-open candidate for visual metaphor.

All voice-aware TCN skills load `workspace/core/anti-ai-writing-style.md` at runtime as their single source of truth for voice rules. There is no duplication across skills.

---

## Reference Files

- `references/voice-calibration.md` — dial scale, calibration tests, worked examples, spoken-word adaptations checklist
- `references/structure-templates.md` — slide markup, zone templates, Script Notes footer, title block
