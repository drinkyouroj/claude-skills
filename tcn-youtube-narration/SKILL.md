---
name: tcn-youtube-narration
description: Step 1 of the Civic Node YouTube production workflow — converts an approved article draft into a 5-7 minute trailer-format narration script with beat markers, pacing notes, and refrain markers. Produces a beat-segmented script (8-12 scenes, 80-120 beats) where each beat is one spoken unit paired with one visual element. Calibrated to a "Hank Green meets Vox" register and written to drive Substack click-through, not to summarize the article. Invoke this skill when the user says "write the narration", "narration script", "video script from this article", "narrate this for YouTube", "do the script for Friday's video", or when the user points at a finished article draft and asks for a video script. Does NOT apply to social posts (that's tcn-post), full articles (tcn-draft), or YouTube packaging — title, description, and thumbnail come from separate skills.
---

# The Civic Node — YouTube Narration (Step 1 of the YouTube Production Workflow)

## What This Skill Does

Converts a finished Civic Node article draft into a 5-7 minute trailer-format YouTube narration script (700-1,050 words at ~140 wpm) with beat markers and a Script Notes footer. The output is structured as a trailer-funnel: it teases the article's strongest hook, names what the video deliberately does not cover, and routes viewers to read the full piece on Substack. The register sits at a 6-7 on a 1-10 dial — recognizably TCN-Marcus, but sharper, more colloquial, and tuned for a broader YouTube audience than the Substack reader base.

**Beat pacing target: 8-12 scenes, ~100-130 beats total**, calibrated for the downstream constant-motion slideshow (see `tcn-youtube-slideshow`), which renders **one slide per beat** — so beat granularity IS the on-screen motion. Same 5-7 min runtime. The motion target is a visual change every ~2-3 seconds, achieved by the **one-clause-per-beat rule** (see Per-beat rule) plus **evolving visual motifs** (see Evolving visual motifs) — never by within-slide animation. Going under 8 scenes usually means the piece is too compressed for video; going over 12 scenes usually means the cold-open angle isn't narrow enough. Landing under ~100 beats usually means beats are still carrying whole sentences instead of single clauses — the motion bug that makes a deck feel like a shuffle of static cards instead of constant motion. The dispatch-006 reference runs 109 beats across 11 scenes.

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

### Output artifacts

This skill writes **two** files on every run:

- **Primary — narration script:** `workspace/drafts/<slug>/youtube-narration.md`
  - **Contents:** Title block (article title + dispatch number + scene/beat count + format tag), 8-12 scene blocks in beat-segmented markup, Script Notes footer.
  - **Does NOT contain:** title options, YouTube description, chapter timestamps, tags, thumbnail prompt — those come from separate skills.
- **Ledger breadcrumb:** `workspace/dispatch-narration/dispatch-<NNN>-<slug>.md` — a lightweight index note written on the same pass that finalizes the script (process step 11). It records the dispatch number, slug, title, and a pointer back to the narration file. Its only job is to keep dispatch-number detection (step 9) in sync: the breadcrumb lands in the exact folder step 9 scans, so the next run counts this dispatch instead of re-suggesting a number that already shipped. Skipping this write is precisely how №005 and №006 went undetected — their scripts landed in `workspace/drafts/` but nothing was ever written back to `workspace/dispatch-narration/`, so detection froze at the last hand-placed dispatch (004).

### Gate prompt presented to user

> Narration draft complete (~[N] words, ~[M]:[SS] runtime). Approve, redirect (e.g., 'use a different hook', 'swap a middle slide', 'dial the register catchier/drier'), or cancel?

**Stop after presenting the draft.** Wait for user approval or redirect before doing anything else.

---

## The Narration Structure

Three zones, **8-12 scenes, ~100-130 beats total**, 700-1,050 words at ~140 wpm. Each beat is **one short spoken clause + one visual element** (see the Per-beat rule). The downstream `tcn-youtube-slideshow` renders one slide per beat, so the beat count is the motion budget — a beat that carries a whole sentence is a slide that sits static while you keep talking.

### Cold Open (always 2 scenes, 45-60 sec)

**Scene 1 — Hook.** A relatable analogy, surprising number, or "wait, what?" moment. No setup. No TCN-specific jargon. Earns the next 30 seconds of attention.

Example (Helium piece, calibrated to register 7 — shown here unsegmented for voice; the real script breaks this into one-clause beats):

```
**[SCENE 01 — HOOK]**

Buying a McDonald's franchise comes with a 200-page disclosure document.
Federal law requires it. The pricing. The exit terms. What happens if
McDonald's changes the menu and your numbers stop working.

Three hundred eighty-five thousand people bought a Helium hotspot.

The franchise disclosure equivalent? They didn't get one.

Vibes.
```

That example is the floor for register-7 catchiness, not the ceiling. Aim higher when the article supports it. Rhetorical questions, one-word landings, and unexpected analogies are the moves.

**Scene 2 — Thesis.** What the piece argues, distilled to one or two sentences. Often a verbatim or near-verbatim line from the article. The promise the video is making.

### Body (5-8 scenes, 3-4 min)

Read the article and pick **5-8 from this menu** by asking *which of these does this article most strongly support?* The expanded count (vs. the older 3-5 target) gives each middle slide less work to do, which keeps the per-slide visible-text budget achievable. Repeating a category is fine — `THE RECEIPT · UNIT ECONOMICS` followed by `THE RECEIPT · HIP-143` is two Receipt slides, not one overloaded Receipt slide.

- **The Receipt** — strongest concrete evidence. Numbers, dates, names. The "I can prove it" segment. **Usually mandatory.** Often appears 2× with distinct sub-labels.
- **The Frame** — the TCN lens. The way of looking at it that re-orders everything. Where refrains often live. **Usually mandatory** (one of Frame or Twist is always present).
- **The Stakes** — why Marcus and visiting friends should care. The "this affects you because" segment.
- **The Twist** — the part that genuinely surprised you and will surprise viewers.
- **The Historical Echo** — the comparison that grounds the argument in something familiar (the Volcker moment in a Fed piece; the McDonald's-FDD comparison in a DePIN piece).
- **The Verbatim** — a primary-source quote that lands harder than any paraphrase. Requires the fact-check report to source the quote.

If the article has a refrain candidate (a single sentence the article repeats or implies repeatedly), place it across 2-3 middle slides and mark each occurrence as `[REFRAIN]` in the Script Notes footer.

### Per-beat rule

Each beat is **one short spoken clause paired with one visual element**. Both halves are single: one clause out of the mouth, one thing landing on screen. This is the rule that produces constant motion. The slideshow renders one slide per beat, so a beat that carries a whole multi-sentence thought is a slide that sits static for five or six seconds while you keep talking. That reads as a card, not as motion.

**Two-part rule:**
1. **One `element:` note = one thing on screen.** If a note describes two independent things appearing at once, it is two beats. An overlay (e.g. "$400,000 lands over the left figure") counts as one element — the illustration context was established by an earlier beat.
2. **One spoken clause per beat.** If the spoken unit is a full sentence whose clauses can each carry their own visual, split it across beats. Target ~3-10 spoken words per beat; a beat over ~12 words is almost always two beats wearing a trench coat.

**Worked split** (the motion bug, fixed):

- Chunky — 1 beat, ~5.5s static: *"Ninety-seven percent were street arrests. People pulled off sidewalks, not out of jail."*
- Fixed — 3 beats, 3 visual changes: *"Ninety-seven percent were street arrests."* [97% lands] / *"People pulled off sidewalks."* [street icon] / *"Not out of jail."* [empty cell, crossed out]

**Practical effect:**

- A Receipt scene with five numbers becomes five beats — one number per beat.
- A Frame scene with a four-part argument becomes four beats — one part per beat.
- A two-sentence thought becomes two-to-four beats — one clause each.
- A Verbatim quote is one beat: the quote (or its sharpest clause) is the element.

There is no minimum word budget — "Vibes." and "Same shift." are complete beats. The ceiling is the thing to watch: when a beat runs long, split.

### Evolving visual motifs (the motion multiplier)

Finer beats get you frequent cuts. **Evolving motifs** get you motion that feels continuous instead of like a shuffle of unrelated cards. A motif is a single visual element that recurs and transforms across beats — so each beat morphs from the one before instead of replacing it with a fresh card.

This is the technique that makes the dispatch-006 deck read as one moving picture rather than a stack of stamps: two worker figures that light up, get numbers stamped over them, then reappear dim at the close; a valve a hand closes on early that the narrator has "no valve to grab" at the end; a question mark that forms, hangs as a refrain, and returns.

**How to build them:**
- Pick 1-3 motifs per script — usually the cold-open image, the refrain's visual, and one structural diagram (a split, a ledger, a map).
- In the `element:` notes, describe each motif's *next state*, not a new object: "the left figure lights up" → "$400,000 lands over it" → "the figure returns, dim, far off." The slideshow reads these as one continuous transformation.
- Bookend: plant the motif in the cold open, pay it off in the Tease/close. The valve and two-figures bookends in 006 are the model.
- Refrains are motifs by default — identical visual treatment every time, so the recurrence is legible.

Mark the primary motif(s) in the Script Notes footer under **Refrain candidate** (the slideshow uses it for rhythm planning). The `element:` note still names only *what* lands and *what state* it's in — never *how* it animates. Easing, fades, and count-ups belong to the slideshow.

### Outro (always 2 scenes, 30-45 sec)

**Scene N-1 — Tease.** Open loops. Explicitly name what the video did NOT cover. This is the funnel mechanism that converts viewers into readers.

**Scene N — End.** Disclosure (if any) + Substack CTA. **Same close every video** for channel branding:

```
**[SCENE N — END]**

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
## [N] scenes · [N] beats · beat-segmented motion format · trailer · small-screen · 5-7 min target
```

The dispatch number is detected from existing dispatches in the workspace (see step 9 of the process), or captured from the user. The format tag (`beat-segmented motion format · trailer · small-screen`) distinguishes the current format from the legacy `Part One / Part Two` format and the older 7-9-slide pre-beat-format scripts.

### Beat markup convention

Each scene opens with a scene label followed by its beat count. Each beat has three parts: beat number, one `element:` note, and one spoken unit ending in `[stop]`.

```markdown
**[SCENE NN — TITLE]** · [N] beats

▸ **B1** · *element: [one visual element — a stamp, a number, a phrase, or a motif's next state]*
"[spoken narration — one short clause]" **[stop]**

▸ **B2** · *element: [one visual element]*
"[spoken narration — one short clause]" **[stop]**

---
```

The `---` between scenes is intentional. Timing annotations (`[stop — let it sit]`, `[hold ~1.5s]`, `[REFRAIN]`) attach to the `[stop]` marker of the beat they modify.

**One clause + one element per beat.** See the Per-beat rule. If the `element:` note describes two independent things appearing at once, or the spoken unit packs two independently-visualizable clauses, split into two beats. An overlay (text landing on an existing illustration context) counts as one element.

**`[SCENE NN]` is the scene container, not a slide.** Each `[SCENE NN — TITLE]` header marks a scene (multiple beats). The downstream slideshow renders **one slide per beat** plus one scene-header slide per scene — so the scene count and the on-screen slide count are different numbers, and the narration never numbers slides. (Earlier dispatches, 002-006, labeled scenes `[SLIDE NN]`; that was a misnomer the slideshow always read as a scene marker. New scripts use `[SCENE NN]`.)

### Script Notes footer (always present)

```markdown
---

## Script Notes

**Word count:** [N]
**Beat count:** [N] across [M] scenes
**Estimated runtime:** [M]:[SS] at ~140 wpm (TCN-natural pace) + ~0.4s × [beat count] beat-stops
**Voice register:** [N]/10 (Hank-Vox blend) — verified against workspace/core/anti-ai-writing-style.md

**Refrain markers (read slow each time):**
- "[refrain line]" (Scene [NN] / B[N], callback at Scene [NN] / B[N])

**Breath / pacing cues:**
- Scene [NN] / B[N]: [cue, e.g., "hold the silence after 'Vibes.' for ~1 second"]
- Scene [NN] / B[N]: [cue]

**Supersedence (if the article has fact-corrections post-narration):**
- (none on this pass — Script Notes block surfaces corrections when present)

**Cold-open candidate** (for thumbnail / title-skill downstream use):
- [the analogy or hook the cold open uses, in one phrase]

**Refrain candidate** (for slideshow skill downstream use):
- [the refrain line, if any]

**Cuts from the article** (what we deliberately did not cover, for Tease scene reference):
- [bulleted list of major article sections not in the video]

```

The "Cold-open candidate," "Refrain candidate," and "Cuts from the article" fields are **forward-compat hooks** the slideshow + title + thumbnail skills will read later. They cost nothing to produce now and save work downstream.

---

## The Process

### 1. Voice file check

Verify `workspace/core/anti-ai-writing-style.md` exists. If missing, apply the degraded-mode fallback from the Voice & vocabulary canonical source section above — flag to the user, skip voice-aware work, but continue with the structural work this skill can still do (zone selection, slide picking, dispatch numbering, Script Notes scaffold). Do NOT fall back to generic vocabulary heuristics from training data — that risks shipping wrong substitutions.

### 2. Read the article draft

Read the finished article verbatim. If a fact-check report is supplied, read that too and check for unresolved flagged items — surface those to the user before drafting.

### 3. Identify the hook angle

Find the most relatable analogy or sharable claim in the article. If 2+ strong candidates exist, surface them to the user for selection. If one obvious choice, pick and proceed.

### 4. Identify the thesis line

Distill the article's argument to one or two sentences. Often a verbatim or near-verbatim line from the article.

### 5. Pick the middle-slide menu

Read the article's argument structure and select **5-8 from the menu** (Receipt / Frame / Stakes / Twist / Historical Echo / Verbatim). The Receipt is almost always picked, often twice with distinct sub-labels (e.g., `THE RECEIPT · UNIT ECONOMICS`, `THE RECEIPT · HIP-143`). One of Frame or Twist is almost always picked. The expanded scene count gives each scene less narrative work to do, keeping beats focused and the visual pacing tight.

### 6. Detect a refrain candidate (optional)

If the article repeats or implies a single load-bearing sentence, mark it as a refrain candidate and place it across 2-3 middle slides.

### 7. Draft the script scene-by-scene

Apply voice calibration (dial 6-7, Hank-Vox blend) and spoken-word adaptations (sentence-length cap, no em-dashes, no subordinate-clause stacks, one-word landings, numbers spelled out). Mark candidate refrain lines as `[REFRAIN]`.

For each scene, break the spoken content into **one-clause beats** (see Per-beat rule): one short spoken clause + one `element:` note per beat. Establish 1-3 **evolving motifs** (see Evolving visual motifs) and write each `element:` note as the motif's next state where one applies. Write beats in order, applying timing annotations (`[stop — let it sit]`, `[hold ~1.5s]`, `[REFRAIN]`) where the delivery calls for them. Aim for ~9-14 beats per scene; a scene under 7 beats is usually still carrying whole sentences and needs finer segmentation, a scene over 16 beats should split into two with distinct sub-labels.

### 8. Compose the Script Notes footer

Word count, runtime estimate, pacing cues, refrain markers, cold-open candidate, refrain candidate, cuts-from-article list. All fields populated — the forward-compat hooks are not optional.

### 9. Detect dispatch number and compose title block

Dispatch numbers come from **two sources that must agree**. Scan both, then take the **highest** number found across both:

1. **The ledger** — files matching `dispatch-NNN-*.md` in `workspace/dispatch-narration/` (default; configurable via steering input). Parse the leading `NNN`.
2. **Shipped narration outputs** — every `youtube-narration.md` under `workspace/drafts/*/`; parse the `## The Civic Node · Dispatch №NNN` line from each.

Suggest the next sequential integer after the highest number found across BOTH sources. Scanning the drafts outputs as well as the ledger is the safety net: a narration ships to `workspace/drafts/<slug>/` and its ledger breadcrumb (step 11) might be missing on older dispatches, so the drafts scan guarantees detection still counts it. A missing breadcrumb can never silently freeze the counter when the drafts folder is also read.

- If both sources agree, or the drafts scan is simply ahead of the ledger (the normal case before backfill), surface the suggestion with a one-line confirmation: "Suggesting Dispatch №NNN — confirm or override."
- If the two sources **disagree in a way the max can't reconcile** — a gap in the sequence, the same number used by two different slugs, or a re-record — treat detection as low-confidence and ask the user explicitly which number to use. The canonical re-record example: the Friday 2026-05-22 re-record of dispatch-004.
- If neither source has any files, ask the user.

Write the confirmed number into the title block as `Dispatch №[NNN]` (zero-padded to three digits), and carry it to step 11 for the ledger breadcrumb.

### 10. Present to user with the standard gate prompt

Use the gate prompt from the Inputs and Outputs section. Wait for approval or redirect. Do not proceed past this gate without explicit user instruction.

### 11. Write the outputs and the ledger breadcrumb

After the user approves at the gate, write **both** output artifacts:

1. The narration script to `workspace/drafts/<slug>/youtube-narration.md`.
2. The ledger breadcrumb to `workspace/dispatch-narration/dispatch-<NNN>-<slug>.md`, using the confirmed dispatch number from step 9.

The breadcrumb is **mandatory and idempotent** — overwrite it if a note for the same dispatch+slug already exists; never create a second note for the same dispatch. This write is what keeps step 9's detection honest on the next run; skipping it is what caused №005 and №006 to go undetected. Breadcrumb format:

```markdown
---
dispatch: NNN
slug: <slug>
title: "<spoken-word title from the title block>"
narration: "workspace/drafts/<slug>/youtube-narration.md"
created: YYYY-MM-DD
recorded: false
---

Dispatch ledger entry. Full narration script lives at the `narration:` path above.
This note keeps tcn-youtube-narration step 9 (dispatch-number detection) in sync — every
narration run writes one of these into workspace/dispatch-narration/.
```

If detection in step 9 revealed drift (the ledger was behind the drafts outputs), backfill the missing `dispatch-NNN-<slug>.md` breadcrumbs for the gap dispatches in the same pass, so the ledger fully re-syncs rather than only catching up by one.

---

## Failure Modes

- **Article draft missing or unreadable** — surface the failure, ask for a valid path, halt.
- **Voice canonical file missing** — apply the degraded-mode fallback used by `tcn-headline`: flag explicitly to the user, skip voice-aware work (no AI-tells cross-check, no banned-vocabulary substitutions), but continue with the structural work this skill can still do. Do NOT fall back to generic register (per the elasticity-bug failure mode documented in `tcn-headline`).
- **Article too short for a 5-7 min trailer** (less than ~800 words article-side) — surface to user: "this piece is short enough that the video would cover most of it. Confirm you want a trailer (with curiosity-gap funnel) or a near-full read-through?" Let user override.
- **Cannot pace to 8-12 scenes** — if the script lands at <8 scenes (too compressed) or >12 scenes (too sprawling), surface to user. <8 usually means the article is too thin for video. >12 usually means the cold-open angle isn't narrow enough. Don't silently exceed; ask the user whether to re-pick the hook or to accept the count.
- **Beat count outside ~100-130** — if total beats land under ~100, the beats are probably still carrying whole sentences (the motion bug) — re-segment to one clause per beat before surfacing to the user. If over ~140 (approaching the slideshow's 150-slide warning), ask whether to merge closely related beats or drop a scene. Surface the actual count either way.
- **Dispatch-number drift (detection freezes or repeats a number)** — symptom: step 9 suggests a number that already shipped (e.g., suggests №005 when a №006 narration already exists under `workspace/drafts/`). Root cause: `workspace/dispatch-narration/` is the detection source but is NOT where narration scripts land, so the ledger freezes at the last hand-placed dispatch unless a breadcrumb is written back. This is a real, observed failure — it mis-numbered №006 and would have mis-numbered №007. The fix is built into the flow: step 9 also scans `workspace/drafts/*/youtube-narration.md` (so the max can't freeze), and step 11 writes a ledger breadcrumb every run (so the ledger self-heals). If you still see drift, backfill the missing `dispatch-NNN-<slug>.md` breadcrumbs from the drafts outputs and the counter re-syncs.
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
