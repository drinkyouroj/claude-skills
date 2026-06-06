# Shorts Packaging Anatomy — draft-time source of truth

Read this at every batch. The `SKILL.md` carries the workflow and the summary; this file carries the block-level rules and a worked example. Living document.

---

## Table of contents

1. Transcript slicing — method, confidence classes, fallback
2. Title — rules, the structural-pattern menu, acceptance checks
3. Description — block order and line budgets
4. Hashtags — selection logic
5. Worked example — Dispatch №006, two real clips end to end

---

## 1. Transcript slicing

Each clip is a window of the dispatch's recording, and the `.srt` is the transcript of that recording. The job is to recover the window so the title and hook come from the words the viewer actually hears.

**Method:**
1. Extract beat key-terms from the clip's filename slug. Strip `Dispatch NNN-`, `clip-NN-`, `-short-clip`, `.mp4`. What remains is the beat: `755-percent` → `755`, `percent`; `no-valve-to-grab` → `valve`, `grab`; `14-billion-never-voted` → `14 billion`, `never voted`.
2. Scan the `.srt` cues for the tightest cluster containing those terms (numbers may be spelled out in speech — "seven hundred and fifty five percent" — so match digit *and* spelled forms).
3. Pull the verbatim spoken text for that cluster, 1–4 sentences. Trim to the sentence boundaries around the anchor — and **drop a trailing meta/aside clause even when it shares a cue** with the anchor. A spoken "…I kept the rest for the article" is the narrator's housekeeping, not the on-screen claim; the slice is what the viewer watches happen, not the voiceover's bookkeeping.

**Confidence classes:**
- **High** — the key terms land in one tight cluster of cues. Use the slice as the copy source.
- **Low** — terms are scattered across the transcript, or absent (a beat slug like `bonus-is-the-receipt` may be narration phrasing that never appears verbatim). Fall back to the matching section of the **final** article draft, mark the artifact `match: low — fallback: article`, and warn the user in one line. The final draft is the highest `NN` in `05-draft-vNN.md`, ignoring any macOS collision copy (`… 2.md`) and any qualifier variant (`-lean`): `05-draft-v8.md` wins over `v7`, over `05-draft-v1-lean.md`, and over `05-draft-v8 2.md`. Never ship low-confidence copy silently.

The beat slug is a strong hint but not the title. Draft from the *content* of the slice, not from the slug.

---

## 2. Title

A Shorts title is read in three places: the channel's Shorts grid, search results, and the share/endscreen card. It is *not* the in-feed click driver — the feed auto-plays the video and hides the title behind an info tap. So the long-form `tcn-youtube-title` "Specific Anchor. Twist." two-part stop, calibrated to the 16:9 browse feed's desktop truncation, does not apply. A Shorts title wants to be a single clean declarative line that holds up in search. (An *internal period* is still fine — `Profit jumped 755%. The workers asked for a cut.` — what's banned is the desktop-truncation *calibration*, not the punctuation.)

**Rules:**
- **≤60 characters** total, including spaces.
- **Declarative line**, sentence case (genuine acronyms — PJM, UAW, TSMC, CWA — excepted). An internal period is allowed.
- **Drawn from the slice, not the slug, and not the article.** Use words actually spoken on screen. Article passages are enrichment context for *you*, never source material for the title: if the clip says "Korea" and the article says "Pyeongtaek," the title says Korea.
- **3 candidates** per clip, each surfaced with a one-line rationale (which pattern, which anchor, why it lands).
- **Concrete-anchor rule:** if the slice carries a number, dollar amount, place name, year, or proper noun, at least one candidate must use it. If the slice carries none of those (some beats are all common nouns), anchor at least one candidate on the clip's strongest concrete noun in its spoken plain-language form — `the memory every AI chip needs`, not the `HBM` acronym.
- **No** exclamation points, **no** em-dashes, **no** all-caps words.

**Structural-pattern menu** (full library, with worked examples, under `## Proven structural patterns` in `../../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md`):
- **Concrete Anchor + Twist** — lead with the hard specific, turn it. *"755% in a year. The workers asked for a cut."*
- **Implied Stakes** — name the thing and let the consequence hang. *"One mill makes the steel the whole grid needs."*
- **Specific Contradiction** — two facts that shouldn't both be true. *"Same shift, same plant. A hundred to one."*
- **Bare-Noun Provocation** — a flat noun phrase that begs the question. *"No valve to grab."*
- **Direct Address** — put the viewer in it. *"You never voted on the data center."*

**Acceptance checks** (every candidate, before it is surfaced — re-draft a failing slot silently up to 2 more times, then surface best-effort with a note):
- Word/char budget (≤60 chars).
- No banned hype adjective, no banned clickbait template, no anti-AI-tell token. The **enforced lists are the canonical ones** in `../../tcn-youtube-thumbnail/references/thumbnail-headline-patterns.md` — read them there; do not keep a copy here. (Illustrative only, non-exhaustive: hype like `SHOCKING`/`INSANE`/`GAME-CHANGING`; templates like "You Won't Believe…"/"The Truth About…"; tells like em-dash, "delve", "tapestry".)
- Passes the voice file's §3H.1 (no dismissal label), §3H.2 (no pointing-and-labeling), and §3J/§3K (no abstract-noun closer — a concrete-noun or verb/imperative closer is fine).

---

## 3. Description

Fixed order. YouTube renders no Markdown in the description, so the paste-ready block is plain text.

```
[HOOK]            1–2 lines. Fresh restatement of the clip's core claim.
                  A different angle than the title — not a repeat.
                  This is the SEO body and the above-fold for a "more" tap.

[BLANK LINE]

[ARTICLE CTA]     → Full piece on Substack:
                  https://drinkyouroj.substack.com/p/<slug>

[BLANK LINE]

[HASHTAGS]        #<Tag1> #<Tag2> [#<Tag3>] #Shorts #TheCivicNode #drinkYourOJ
```

Hashtags live **in the description, never in the title.** The title stays a clean declarative line (§2); YouTube surfaces the leading description hashtags for discovery, so a clean title and a tagged description give the discovery benefit without spending title characters or undercutting the voice.

**Budgets:** hook ≤220 chars across its 1–2 lines; CTA is one sentence + the bare URL on its own line; hashtags one line. The whole block stays compact — a Short's description is rarely read in full, so its job is the hook (for the *more* tap and for search) plus the funnel link plus the classifier signal, not a full essay.

**The `→` arrow** is the CTA glyph — use it on every clip in the batch (the output template and both worked examples use `→`). The only substitute is a literal `>`, and only if a paste target strips Unicode; never mix the two within a batch. No em-dashes anywhere in output copy.

The long-form `-- THE CIVIC NODE --` channel link block is **omitted** on Shorts — the channel identity rides on the `#TheCivicNode #drinkYourOJ` hashtags and the Substack URL, which is enough for a surface this terse.

---

## 4. Hashtags

Hashtags go in the **description, never the title.** Order matters: YouTube surfaces the *leading* description hashtags for discovery, so lead with the strongest, not with boilerplate.

- **Lead with 2–4 dispatch-specific** tags, mined from the clip's anchors. Prefer proper nouns, and within those prefer ones **spoken in the slice** (`#Samsung`, `#PJM`, `#Butler`) over article-only names (`#ClevelandCliffs`, `#SKHynix` — fine to use, just second-priority), and both over abstract categories (`#Economy`, `#AInews`). Lead the run with the strongest spoken proper noun. When the clip is proper-noun-poor, one or two topical anchors (`#AIBoom`, `#GridStrain`) are allowed to reach the floor. If you must cut to stay in range, cut article-only names before spoken ones.
- **`#Shorts` after the dispatch-specific run.** Include it (an explicit Shorts signal is harmless), but it does not need to lead — vertical + sub-3-minute already auto-classifies, and a leading `#Shorts` wastes the most-visible slot on a generic tag.
- **`#TheCivicNode #drinkYourOJ` last**, always (channel-evergreen). Lifted verbatim from the dispatch's `youtube-description.md` when present.
- **Total 5–7.** That is 2–4 dispatch-specific + `#Shorts` (1) + channel (2). Re-roll the dispatch-specific selection silently if the total lands outside 5–7.
- Sentence case / PascalCase, no all-caps, no characters outside `[A-Za-z0-9_]` after the `#`.

---

## 5. Worked example — Dispatch №006 ("Samsung's $400,000 Bonus, and the $4,000 One")

Article URL (confirmed, reused verbatim): `https://drinkyouroj.substack.com/p/samsungs-400000-bonus-and-the-4000-one`
Master transcript: `Dispatch 006_en.srt`

### Clip 03 — `755-percent`  (match: high)

**Transcript slice:**
> "Their profit had jumped seven hundred and fifty five percent in a year, so the workers asked for a cut, and they got it. Ten and a half percent of the division's profit… every year for ten years."

**Anchors:** 755%, 10.5%, ten years, division's profit, SK Hynix (article-only).

**3 title candidates** (this is the gate-time menu; the file commits to one and demotes the rest):
1. `Profit jumped 755%. The workers asked for a cut.` (48 chars) — Concrete Anchor + Twist; leads on the hard number, turns to the human move. *Recommended.*
2. `755% in a year, and the union had a template.` (45 chars) — Implied Stakes; hints there was a playbook (SK Hynix) without spending the words.
3. `10.5% of the profit, every year for a decade.` (45 chars) — Bare-Noun Provocation on the terms of the deal.

**Final file** (field-mapped to the upload screen — title clean, no em-dashes in the copy, hashtags led by the strongest spoken anchor):
```
## ▶ TITLE — paste into the Title field

Profit jumped 755%. The workers asked for a cut.

## ▶ DESCRIPTION — paste into the Description field

Samsung's chip division booked a 755% profit jump in a year. Its unionized workers had a product nobody could substitute, so they took 10.5% of the profit, every year for a decade.

→ Full piece on Substack:
https://drinkyouroj.substack.com/p/samsungs-400000-bonus-and-the-4000-one

#Samsung #AIBoom #SKHynix #Shorts #TheCivicNode #drinkYourOJ
```
(Hook runs the *leverage* angle, a different beat than the title's profit-number, so the two don't repeat. Hashtags lead with the spoken proper noun `#Samsung`; `#SKHynix` is article-only so it sits behind the spoken/topical tags; `#Shorts` after the dispatch run. 6 total.)

### Clip 08 — `no-valve-to-grab`  (match: high)

**Transcript slice:**
> "Even the four thousand dollar guy had a union and a vote. He was still inside the deal. The person opening that power bill was never inside it. The chip workers had a hand on the valve, and they turned it. The rest of us are still standing somewhere with no valve to grab."

**Anchors:** $4,000, union and a vote, the ratepayer, the valve.

**3 title candidates:**
1. `Even the $4,000 guy was inside the deal.` (40 chars) — Specific Contradiction; the one who came up short still had leverage the ratepayer didn't. *Recommended.*
2. `The chip workers had a valve. You don't.` (40 chars) — Direct Address; lands the asymmetry on the viewer.
3. `No valve to grab.` (17 chars) — Bare-Noun Provocation; the clip's own closing image, naked.

**Final file:**
```
## ▶ TITLE — paste into the Title field

Even the $4,000 guy was inside the deal.

## ▶ DESCRIPTION — paste into the Description field

The Samsung worker with the small bonus still had a union and a vote, so he was inside the deal. The person opening a higher power bill never was. One side had a hand on the valve and turned it. The other has nothing to grab.

→ Full piece on Substack:
https://drinkyouroj.substack.com/p/samsungs-400000-bonus-and-the-4000-one

#Samsung #PowerBill #AIBoom #Shorts #TheCivicNode #drinkYourOJ
```

Note both titles obey the voice file: no dismissal label, no pointing-and-labeling ("the asymmetry here is…"), and each closer is a concrete image (`the deal`, `nothing to grab`) rather than an abstract noun phrase. Neither description copy uses an em-dash.
