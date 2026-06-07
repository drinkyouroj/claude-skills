---
name: tcn-youtube-shorts
description: "Use this skill to write YouTube Shorts metadata — a separate title and description for each short vertical clip in a batch. Whenever a request mentions Shorts, vertical clips, vertical cuts, reels, or 9:16 / 9x16 clips that need titles or descriptions, prefer THIS skill over the single-video title or description skills: the giveaway is many clips each getting their own metadata, not one set for a whole video. Trigger on intents like 'package the shorts', 'shorts titles for these clips', 'titles and descriptions for the vertical cuts', 'what goes in the title/description field for each short', 'youtube shorts for №NNN', or 'one file per clip before uploading'. Produces one paste-ready file per clip — clip-native title, hook, Substack CTA, and #Shorts hashtags drawn from each clip's spoken transcript. Not for cutting or rendering clips, making thumbnails, uploading, writing tweets or Substack notes, or writing the single long-form title or description for the full-length video (those are separate skills)."
---

# The Civic Node — YouTube Shorts Packaging (Step 6 of the YouTube Production Workflow)

## What This Skill Does

Packages a batch of finished 9:16 vertical clips — already cut and rendered from a recorded TCN dispatch — into per-clip YouTube Shorts metadata. For each clip it produces a clip-native title (a short declarative line, ≤60 characters, distilled from what the clip actually says) and a compact description (a 1–2 line hook, a Substack article CTA with the bare URL, and a hashtag line led by `#Shorts`). Output is one paste-ready `youtube-shorts-clip-NN.md` file per clip, gated one clip at a time so a weak transcript match never ships silently.

The skill is batch-first and reuses what the dispatch already produced. It slices the dispatch's master `.srt` transcript per clip, so each Short's copy comes from the words spoken on screen rather than a fresh invention that may drift from the clip. It inherits the Substack article URL and the channel hashtags from the long-form package rather than regenerating them.

It does **not** produce thumbnails. A Short plays in a vertical feed that auto-selects a frame, so a custom cover is optional; it is deferred to a later version. And this is **not** a `--shorts` mode bolted onto the long-form `tcn-youtube-description` skill — Shorts invert that skill's load-bearing assumptions (no chapters, terse copy, one output per *clip* rather than one per dispatch), so they get a dedicated skill instead of a forked one.

---

## Voice & vocabulary canonical source

This skill MUST load `workspace/core/anti-ai-writing-style.md` from the active project's root before making any voice, vocabulary, substitution, or AI-tells decision. That file is the single source of truth for the audience vocabulary list and always-gloss-on-first-use rule, the banned-words list, dead phrases / transitions / engagement bait / hype language, the negative-parallelism rule, tribal-coded crypto cringe and operational shibboleths, the dismissal-label rule, the vocabulary cliff rules including the meaning-preservation sub-principle, the closing-line abstraction rule, the broader AI writing patterns to avoid, and the anti-overfitting guide.

This skill MUST NOT maintain its own duplicate copy of any of the following:
- The audience vocabulary list
- Substitution examples
- Banned words
- Voice patterns
- AI-tells checklists

If a vocabulary or substitution decision is needed mid-task, resolve it by referring to the canonical file at runtime, not by relying on a copy embedded in this spec.

**Why these rules bite hardest in short form.** A Shorts title is six words and a hook is two lines. There is no room to spend a third of the budget on a sentence that points at meaning instead of carrying it. The highest-value rules for this skill, by section:
- **§3H.1 (dismissal labels)** — "X is just theater / a press release / optics" hands the viewer a verdict without the mechanism that earns it. In a 6-word title there is no room to earn it back. Name the concrete thing.
- **§3H.2 (pointing-and-labeling)** — "That's the gap / here's the move / this is the mechanism." Litmus: if you deleted the pointing sentence, would the copy lose any information? In a two-line hook it almost never does. Note that the *spoken slice itself* sometimes carries this anti-pattern (a narrator's "that gap is the whole story" closer); a literal lift of that line into a title fails this check, so filter the slice, don't just transcribe it.
- **§3J / §3K (closing-line abstraction, cold-read failure)** — applies to **both** the title and the description hook's closer, since both are read in search out of context. A Short's last line wants a concrete image, not an abstract noun phrase. "No valve to grab" lands; "the asymmetry of leverage" does not. A verb/imperative closer ("and make it stick") is fine — the rule bans abstract *nouns*, not action.
- **§3F (false-symmetry reframe)** — an asymmetry hook ("his raise didn't pay your bill") tends toward the banned "it's not X, it's Y" reframe. Split it into two plain sentences naming each side on its own terms instead.
- **§1 (keystone vocabulary, gloss-on-first-use)** — a Short has no glossary and no above-the-fold room to define a term, so any unglossed insider word is a hard stop. Prefer the spoken-on-screen phrasing the viewer just heard. The one exception is a genuine acronym the title can't avoid (PJM, UAW, TSMC); the gloss rule is waived for the title field and applied, if at all, only in the hook.

**Fallback when the canonical file is missing.** If `workspace/core/anti-ai-writing-style.md` is not present in the current project, this skill must:
1. Flag explicitly to the user — "no voice file found at workspace/core/anti-ai-writing-style.md; skipping voice calibration."
2. Skip all voice-related work — no AI-hit-list cross-check on candidate titles or hooks.
3. NOT apply generic vocabulary heuristics from training data — those risk shipping wrong substitutions (the elasticity-bug failure mode).
4. Continue with non-voice work this skill can still do: still locate clips and order them, still slice the transcript per clip, still derive the Substack URL, still assemble the hashtag line and the file structure. Flag "voice rules pass" as not enforced in each artifact's metadata.

---

## Position in the YouTube Workflow

```
Article (tcn-article-builder)
    ↓
tcn-youtube-narration   [Step 1]
    ↓
tcn-youtube-slideshow   [Step 2]
    ↓
┌─── RECORDING ───┐
    ↓                              ↓
the 16:9 master video         the same footage, re-cut
    ↓                              into short vertical clips
tcn-youtube-title       [Step 3]   ↓
tcn-youtube-description [Step 4]   tcn-youtube-shorts  [Step 6 — this skill]
tcn-youtube-thumbnail   [Step 5]
```

Shorts is a **parallel** packaging track, not a downstream step (the "Step 6" label is for family numbering only). The 16:9 packaging cluster (Steps 3–5) consumes the recording as one long video and produces one set of metadata for the dispatch. This skill consumes the same recording re-cut into short vertical clips and produces one metadata file per clip. It reads the same master `.srt` transcript the description skill reads, which is why a Short's copy can come from the words actually spoken on screen. It is purely **post-record**: run it after the clips are cut and rendered.

---

## Inputs and Outputs

### Required input

- **Dispatch directory** — e.g. `workspace/drafts/samsungs-400000-bonus-and-the-4000-one/`. The skill auto-detects the master `.srt` transcript here. **SRT selection is deterministic:** of the `.srt` files present, use the one whose name carries no aspect/cut qualifier (`1x1`, `9x16`, `square`, `social`) — that is the 16:9 master, and its script is shared with the vertical cuts. If two qualify, or none clearly does, halt and ask which to use. (Cue count and duration are a sanity check only — reject an SRT with under half the expected cue count — never the primary selector; on a typical dispatch the master and the social cut differ by a handful of cues, which is not a signal.) Halt with an explicit message and example path if no `.srt` is found.
- **Clip source** — either a directory (e.g. `/Volumes/D10/`) the skill globs for the dispatch's vertical clips, or an explicit list of filenames. Clip detection rules:
  - **Video extensions only.** Match `.mp4`/`.mov`/`.m4v`. A dispatch directory is full of non-video siblings that share the prefix — editor project files (`.cmproj`, `.llc`, `.audiate`), `.wav` audio, `.png` frames. Never treat those as clips.
  - **De-dup render variants.** When two video files share a beat (differing only by a suffix like `-polished`, `-final`, `-captioned`, `-v2`, or a numeric collision suffix), keep the most recently modified and warn once which you dropped. (Real example: `…-100to1-ai-boom-short-clip.mp4` and `…-100to1-ai-boom-short-clip-polished.mp4` are the same beat — package one.)
  - **Confirm the count before drafting.** After detection and de-dup, surface `Found N clips for Dispatch №NNN — confirm before I package?` with the ordered list. An over- or under-count (the naive glob found 10; you expected 9) gets caught here, not silently shipped as an extra file.

### Optional inputs

- **Substack URL override** — bypasses URL derivation.
- **Steering** — free-text like `"punchier hooks"`, `"clip 03 title needs the number in it"`, `"skip clip 07"`, `"shorter descriptions across the board"`.
- **Clip order override** — an explicit ordering when filename slugs don't sort cleanly.
- **SRT override** — a specific transcript path when auto-detect picks the wrong one.

### Primary output artifact

One file per clip: `workspace/drafts/<slug>/youtube-shorts-clip-NN.md`, where `NN` is the clip's zero-padded position in canonical order (Process step 2) — `01` is the first clip, not a 0-based index. The file maps 1:1 onto the YouTube Studio Shorts upload screen: the two `▶` blocks are paste targets (one field each), the rest is a checklist for the fields you set by hand.

```markdown
# YouTube Shorts — TCN Dispatch №NNN · Clip NN

**Clip file:** <clip filename>.mp4
**Generated:** YYYY-MM-DD
**Transcript source:** <srt filename> (match: high | low — fallback: article)

---

## ▶ TITLE — paste into the Title field

<chosen title>

## ▶ DESCRIPTION — paste into the Description field

<hook line 1>
<hook line 2>

→ Full piece on Substack:
https://drinkyouroj.substack.com/p/<slug>

#<DispatchTag1> #<DispatchTag2> #Shorts #TheCivicNode #drinkYourOJ

---

## Upload settings (screen fields, not paste targets)

- **Playlist:** Shorts
- **Audience:** Not made for kids
- **Thumbnail:** skip — a custom Shorts cover is mobile-app only (deferred to a later skill version)
- **Visibility:** your call — Public, or Schedule

---

## Alternate titles (NOT for upload — pick-one reference only)

- <candidate 2>
- <candidate 3>
```

There is exactly **one** Title field and **one** Description field on the upload screen, so the file commits to a single chosen title in the `▶ TITLE` block and demotes the other two candidates to the reference footer — they are alternatives the user can swap in, not additional paste material. The `▶ DESCRIPTION` block carries no Markdown — YouTube descriptions render none. The CTA glyph is always `→` (a Unicode arrow, not an em-dash); the only allowed substitute is a literal `>` if a paste target strips Unicode. **No hashtags in the title** — they live in the description (see Hashtags).

### Gate prompt presented to user

The skill gates **once per clip**, not once for the whole batch, because the transcript-slice quality varies clip to clip and a per-clip gate is where a weak match gets caught. See Process step 4 for the gate format and Failure Modes for the skip path.

---

## Shorts Packaging Anatomy

The block-level rules, char/line budgets, the structural-pattern menu to draw titles from, the hashtag-selection logic, and a full worked Dispatch №006 example all live in `references/shorts-anatomy.md` — read it at drafting time. The essentials:

### Title (the `## Title` field)
- A short **declarative line**, ≤60 characters total, distilled from the clip's transcript slice. An internal period is fine (`Profit jumped 755%. The workers asked for a cut.`); what's banned is the long-form `tcn-youtube-title` "Specific Anchor. Twist." stop *calibrated to desktop-feed truncation* — that math doesn't apply, because the Shorts feed hides the title until the viewer leaves the feed.
- **3 candidates per clip**, surfaced at the gate with a one-line rationale each.
- **Anchors come from the slice, not the article.** Draw the title from words actually spoken on screen. Article passages are enrichment context for *you*, not source material for the title — don't put a proper noun in a title that the clip never says (e.g. the clip says "Korea", the article says "Pyeongtaek"; the title uses Korea).
- **Concrete-anchor rule:** if the slice contains a number, dollar amount, place name, year, or proper noun, at least one of the three candidates must use it. If the slice carries none of those (some beats are all common nouns), anchor at least one candidate on the clip's strongest concrete noun in its spoken plain-language form (`the memory every AI chip needs`, not the `HBM` acronym).
- Sentence case (genuine acronyms excepted). No exclamation points. No em-dashes.
- Structural patterns and the enforced banned-word / banned-template / anti-AI-tell lists all live in `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` (under `## Proven structural patterns` and the banned-list sections). Read it; don't keep a copy here.

### Description (the `## Paste this into YouTube` block)
Fixed order: **hook → blank line → article CTA → blank line → hashtags.**
- **Hook** — 1–2 lines, a fresh restatement of the clip's core claim that runs a **different angle than the chosen title** (locked to a non-title angle regardless of which candidate the user picks). The hook's closer is subject to the same §3J/§3K concreteness check as the title — it's read in search.
- **Article CTA** — one line `→ Full piece on Substack:` then the bare URL on its own line.
- **Hashtags** — see below.

### Hashtags
- `#Shorts` **always first** — the classifier signal that tells YouTube to treat the upload as a Short.
- **2–4 dispatch-specific** tags. Prefer proper nouns; prefer ones **spoken in the slice** (`#Samsung`, `#Butler`) over article-only names (`#ClevelandCliffs`), and over abstract categories (`#Economy`). When the clip is proper-noun-poor, one or two topical anchors (`#AIBoom`, `#GridStrain`) are allowed to reach the floor. If you must cut to stay in range, cut article-only names before spoken ones.
- **`#TheCivicNode #drinkYourOJ`** always last (channel-evergreen) — lifted verbatim from the dispatch's `youtube-description.md` when present.
- Total **5–7** tags (`#Shorts` + 2–4 dispatch-specific + 2 channel). Sentence case / PascalCase, no all-caps, nothing outside `[A-Za-z0-9_]` after the `#`. Re-roll the dispatch-specific selection silently if the total falls outside 5–7.

---

## The Process

**Input hygiene (applies to every glob, read, and selection below).** Ignore any file whose basename matches the macOS sync-collision pattern — a literal space followed by an integer immediately before the extension (e.g. `05-draft-v8 2.md`, `youtube-description 2.md`, `006-03 2.png`). These are iCloud/Dropbox conflict copies; never read, write, or count them. A live dispatch directory is full of them, and they will otherwise pollute clip detection, SRT selection, draft selection, and the URL grep.

### 1. Locate inputs

Find the master `.srt` in the dispatch directory (deterministic rule in Inputs). Detect the clip files at the clip source (video-extension-only, de-dup variants, confirm the count). If either is missing, halt with an explicit message and an example path — do not compose from nothing. Read the voice file (or run the missing-file fallback).

### 2. Establish canonical clip order

Sort numbered clips by the index in their filename slug: `clip-02-…` → 02, `clip-09-…` → 09.

The cold open is often exported without a `clip-NN` prefix (e.g. `Dispatch 006-100to1-ai-boom-short-clip.mp4`). Handle it by **beat coverage, not by filename shape**: if a `clip-NN`-prefixed video already covers that beat, use its number; only when no numbered clip covers the cold open does it take position 01 by default. (Note that an editor project file like `clip-01-cold-open-…llc` is NOT a clip — it's excluded by the video-extension rule — so don't let it claim the 01 slot or the cold-open beat.) If **any** unnumbered clip sits alongside numbered ones, surface the proposed order and ask the user to confirm before drafting. Do not rely on filesystem sort order; it is platform-dependent.

### 3. Derive the Substack URL (confirmation gate)

1. If the dispatch's `youtube-description.md` exists, grep it for the article URL and use that exact string — most reliable, already confirmed, no slug drift. (This is the preferred source; it also supplies the channel-evergreen hashtags.)
2. Otherwise construct `https://drinkyouroj.substack.com/p/<slug>` from the directory name.
3. Surface: `Article URL: <URL>. Confirm or paste an override:`
4. Empty / "yes" / "confirm" accepts; a pasted URL overrides.
5. If the slug fails sanity checks (>80 chars, underscores, uppercase, or characters outside `[a-z0-9-]`), surface it with a flag and require an explicit override.

This URL is constant across the batch; resolve it once before the per-clip loop.

### 4. Per-clip loop

For each clip, in canonical order:

**a. Slice the transcript.** Fuzzy-match the clip's beat key-terms (from its filename slug — `clip-03-755-percent` → `755`, `percent`) against the `.srt` content, matching both digit and spelled-out number forms, and pull the verbatim spoken passage (1–4 sentences) for that beat. Trim to sentence boundaries around the anchor, and **drop a trailing meta/aside clause even when it shares a cue** (a spoken "…I kept the rest for the article" is the narrator's housekeeping, not the on-screen claim). Classify the match:
- **High** — key terms land in a tight cluster of cues. Use the slice as the copy source.
- **Low** — terms scattered or absent (some beat slugs are narration phrasing that never appears verbatim). Warn in one line (`"weak transcript match for clip NN — falling back to the article section"`), fall back to the matching section of the **final** article draft, and mark the artifact `match: low — fallback: article`. The final draft is the highest `NN` in `05-draft-vNN.md` (ignoring collision copies and `-lean`/qualifier variants) — `05-draft-v8.md` beats `v7`, `v1-lean`, and `05-draft-v8 2.md`. Never silently ship low-confidence copy. If no draft file is found, surface the clip with no copy and ask for a one-line steer rather than inventing the beat.

**b. Draft 3 title candidates** from the slice, per the Title rules. Each must pass the banned-word / banned-template / anti-AI-tell checks before it is surfaced. Re-draft a failing slot silently up to 2 more times (3 attempts total); if it still fails, surface the best effort with a one-line note on which criterion it missed.

**c. Draft the description** — hook, article CTA, hashtags — per the Description and Hashtag rules.

**d. Present the per-clip gate:**

> ```
> Clip NN — <beat slug>  (<duration>s, <width>×<height> if known)
> Transcript match: high | low (fallback: article)
>
> Title candidates:
>   1. <candidate>   — <pattern · anchor · why it lands>
>   2. <candidate>   — <rationale>
>   3. <candidate>   — <rationale>
>
> Description preview:
> ---
> <full paste-ready description block>
> ---
>
> approve [1/2/3] · redirect (e.g. 'title needs the number', 'punchier hook', 'redo the whole clip', 'swap #Economy for #PJM') · skip
> ```

**Stop after presenting each clip's draft.** Wait for the user's response before writing the file or advancing. (In a non-interactive / batch invocation where no user turn is available, emit the full gate payload — 3 candidates + recommended index + paste-ready description — as the deliverable for that clip and move on.)

- **approve [N]** — write `youtube-shorts-clip-NN.md` with candidate N as the chosen title; advance.
- **redirect [steering]** — re-draft the affected surface (title, hook, or hashtags), or all surfaces if the steering is blanket ("redo this clip"); re-present the gate for this clip.
- **skip** — write the file with `**STATUS: skipped — not packaged**` in place of the title and description; advance. (A placeholder, so the file set stays complete and the clip is easy to find later.)

If an override title or description was supplied for a clip at invocation, skip drafting that surface and present it pre-filled at the gate for a yes/no.

### 5. Closing summary

After the last clip, print a compact upload-order list to the conversation (not a file — the per-clip files are the artifacts): each clip's `NN`, filename, and chosen title, in order, so the upload session in YouTube Studio can go top to bottom. Note any clips that were skipped or fell back to the article.

---

## Failure Modes

- **No `.srt` found in the dispatch directory** — halt with an explicit message and example path. Do not compose from nothing.
- **No clip files found at the clip source** — halt with an explicit message and the glob that was tried.
- **Clip count doesn't match expectation** (naive glob caught a render variant or a project file) — the video-extension filter and variant de-dup should prevent it; the count-confirmation gate in Inputs is the backstop. Surface the de-duped list and the dropped files; do not package a `-polished` twin or a `.cmproj` as a clip.
- **More than one master-eligible `.srt`, or none clearly unqualified** — halt and ask which transcript to use. Do not guess from cue counts.
- **Weak transcript match for a clip** — warn in one line, fall back to the final article draft's matching section, mark `match: low — fallback: article`. Never silent.
- **Final article draft not found (needed for a low-match fallback)** — surface the clip with no copy and ask the user for a one-line steer rather than inventing the beat.
- **An unnumbered clip sits alongside numbered ones** — surface the proposed order and confirm before drafting. Do not guess.
- **Voice file missing** — flag explicitly, skip the AI-tells pass, continue with slicing / URL / hashtags / file structure; mark "voice rules pass: not enforced" in metadata.
- **`thumbnail-headline-patterns.md` not resolvable** — flag, fall back to conservative inline heuristics (sentence case, no exclamation points, none of the obvious hype words SHOCKING/AMAZING/INSANE/MASSIVE/EPIC), continue.
- **Slug fails sanity checks** — flag the constructed URL and require an explicit override. Do not ship a malformed URL across the batch.
- **Title candidate still fails acceptance after 3 attempts** — surface the best-effort candidate with a one-line note on the unmet criterion; let the user redirect.
- **Hashtag count drifts outside 5–7** — silently re-roll the dispatch-specific selection; never surface a count-violating block.
- **User skips a clip** — write a placeholder file and continue the batch.
- **User redirects at a clip's gate** — re-draft only the affected surface (or all, on blanket steering); re-present that clip's gate.

---

## What This Skill Is NOT

- Not a clip cutter or renderer. The user's video editor produces the clip files; this skill packages the metadata around them.
- Not a thumbnail generator. Shorts auto-play a frame; a vertical cover spec is deferred to a later version. The long-form 16:9 thumbnail is `tcn-youtube-thumbnail`.
- Not the long-form description generator. That is `tcn-youtube-description` — chapters, 1,500–2,500-char body, one output per dispatch. Shorts are the inverse shape, which is why this is a separate skill, not a mode flag.
- Not a long-form title generator. That is `tcn-youtube-title` (the "Anchor. Twist." desktop-feed pattern). Shorts titles are clip-native declaratives.
- Not a transcript transcriber. It slices an existing `.srt`; it does not generate one.
- Not a YouTube uploader. It produces paste-ready files; the user pastes each into YouTube Studio.
- Not a TikTok / Facebook / Reels packager. Those surfaces share the same vertical clips but have different description and hashtag conventions; v1 is YouTube Shorts only.
- Not an article, narration, or slideshow generator. Those are upstream skills.

---

## Companion Skills

**Upstream (this skill reads from):**
- Recording → `.srt` transcript — the master transcript the skill slices per clip.
- The dispatch's vertical clips — cut and rendered in the user's editor.
- `tcn-youtube-description` — if its `youtube-description.md` is present, the skill lifts the confirmed Substack URL and the channel-evergreen hashtags from it rather than re-deriving them.
- The final article draft in the dispatch dir — read only as the low-match fallback copy source.

**Sibling (no direct interaction):**
- `tcn-youtube-title`, `tcn-youtube-thumbnail`, `tcn-youtube-narration`, `tcn-youtube-slideshow` — the long-form 16:9 track.

**Shared canonical sources (read at runtime, not duplicated):**
- `workspace/core/anti-ai-writing-style.md` — voice file.
- `../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` — banned hype words, banned clickbait templates, anti-AI-tell tokens, and the structural-pattern library used for title and hook drafting.

---

## Reference Files

- `references/shorts-anatomy.md` — the block-by-block spec: title rules and the structural-pattern menu, the description block order with line budgets, hashtag-selection logic, the transcript-slicing method (fuzzy-match, confidence classes, fallback), and one full worked Dispatch №006 example walking from transcript slice → 3 title candidates → chosen description for two real clips. The draft-time source of truth; read it at every batch.
