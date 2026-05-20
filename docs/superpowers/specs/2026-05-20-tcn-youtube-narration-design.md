# tcn-youtube-narration — Design Spec

**Status:** Approved (2026-05-20)
**Author:** Justin Hearn (drinkYourOJ / The Civic Node)
**Implementation track:** `tcn-youtube-narration` skill, to be built with `anthropic-skills:skill-creator`
**Position in ecosystem:** Step 1 of the TCN YouTube production workflow (upstream of recording)

---

## 1. Context — why this skill exists

The Civic Node publishes a flagship Substack article each week. Each article gets a companion 5-7 minute YouTube video that serves as a **trailer for the article, not a substitute for it**. The video's job is to drive Substack click-through, not to deliver the full argument on YouTube.

Today, narration scripts are written by hand. They follow a repeated structure (`Cover → Part One: Context → Spark → Part Two: Frame → Body → Call → End`) that the user converged on because it rendered well in Claude Design slideshows, not because the structure best serves a 5-7 min trailer. The current scripts are competent but read closer to "article in spoken form" than to "video essay that markets the article." The voice register sits around a 4 on a 1-10 dial (1 = dry essayist, 10 = Hank Green vlog); it needs to be at a 6-7 — recognizably TCN-Marcus, but with sharper hooks, willingness to drop a "vibes," and a register that broader YouTube viewers (not just existing Substack readers) will sit through.

`tcn-youtube-narration` automates this conversion: article draft in, narration script with slide markers + pacing notes out. The script is structured as a **trailer-funnel** explicitly designed to leave the viewer with a curiosity gap that resolves only by reading the article on Substack.

---

## 2. Position in the TCN ecosystem

```
Article workflow                 Video workflow                    YouTube packaging
(tcn-article-builder)            (upstream of recording)           (downstream of recording)
─────────────────────            ───────────────────────           ─────────────────────────
tcn-outline                                                         tcn-youtube-title
  ↓                                                                   ↑
tcn-outline-more                                                    tcn-youtube-description
  ↓                                                                   ↑
tcn-headline                                                        tcn-youtube-thumbnail
  ↓                                                                   ↑
tcn-opener                                                          (consumes timestamped transcript)
  ↓                                                                   ↑
tcn-draft                                                           ┌──── RECORDING ────┐
  ↓                                                                   ↑
tcn-readability                                                     tcn-youtube-slideshow
  ↓                                                                   ↑                  (not built yet)
tcn-text-humanizer                                                  (consumes narration)
  ↓                                                                   ↑
tcn-fact-check ↔ tcn-fact-reconcile                                 tcn-youtube-narration  ← THIS SKILL
  ↓                                                                   ↑
Final article draft  ──────────────────────────────────────────────  consumes the article
```

**Upstream consumers of this skill's output:**
- `tcn-youtube-slideshow` (planned) — reads slide markers and visual cues
- `tcn-youtube-title` (planned) — optionally reads "cold-open candidate" for title inspiration
- `tcn-youtube-description` (planned) — optionally reads slide-aligned chapter names
- `tcn-youtube-thumbnail` (planned) — optionally reads cold-open candidate for visual metaphor

**This skill consumes:**
- `tcn-draft` output (the finished article)
- `tcn-fact-check` output (optional — for Verbatim slide source quotes)

**Voice-rule dependency:** Loads `workspace/core/anti-ai-writing-style.md` at runtime, same contract as all other voice-aware TCN skills. No duplicated rules.

---

## 3. Scope — in and out

**IN scope (this skill produces):**
- A complete narration script (700-1,050 words at ~140 wpm spoken pace)
- Slide markers in standardized format `**[SLIDE NN — TITLE]**`
- A Script Notes footer with word count, runtime, pacing/breath cues, refrain markers
- Forward-compat fields used by sibling skills: cold-open candidate, refrain candidate, cuts-from-article list

**OUT of scope (handled by sibling skills):**
- Title options (`tcn-youtube-title`)
- YouTube description body (`tcn-youtube-description`)
- Chapter timestamps (`tcn-youtube-description`, after recording)
- Tags / hashtags (`tcn-youtube-description`)
- Thumbnail image prompt + text overlay (`tcn-youtube-thumbnail`)
- Claude Design slideshow prompts (`tcn-youtube-slideshow`, planned)
- Fact-checking new claims (`tcn-fact-check` — the article should have been fact-checked before this skill runs)
- Rewriting article prose (`tcn-text-humanizer` — that's a separate skill)

**Architectural note:** The user's existing narration documents (e.g., `dispatch-004-you-own-the-hotspot.md`) are *mega-documents* that bundled narration + title options + YouTube description + chapters + tags + thumbnail prompt into one file. The new architecture splits these into separate skill outputs, each living in `workspace/drafts/<slug>/` with the `youtube-` filename prefix.

---

## 4. Inputs and outputs (the skill's contract)

### Required input

- **Path to a finished article draft.** Typically `workspace/drafts/<slug>/05-draft-v{N}.md` (the latest version after the article workflow's fact-check loop terminates). The skill reads this file verbatim. **Acceptable fallback:** if the user pastes article contents directly rather than supplying a path, the skill saves the pasted contents to a temp file and proceeds.

### Optional inputs

- **Path to fact-check report** (`workspace/drafts/<slug>/08-fact-check-v{N}.md`) — if present, the skill surfaces verified primary-source quotes for use in a Verbatim middle-slide. If the fact-check report has unresolved flagged items, the skill warns the user before drafting.
- **Length override** — defaults to 5-7 min target. User can pass "make it 4 min" or "make it 8 min" and the skill recalibrates compression.
- **Steering** — free-text guidance like "lean into the historical-echo angle" or "keep the McDonald's analogy as the hook" or "no Verbatim slide this time."

### Output artifact

- **File:** `workspace/drafts/<slug>/youtube-narration.md`
- **Contents:**
  - Title block (article title + dispatch number + slide count + format tag)
  - 7-9 slide blocks in standardized markup
  - Script Notes footer (always present, after final slide)
- **Does NOT contain:** title options, YouTube description, chapter timestamps, tags, thumbnail prompt

### Gate prompt presented to user

> Narration draft complete (~[N] words, ~[M]:[SS] runtime). Approve, redirect (e.g., 'use a different hook', 'swap a middle slide', 'dial the register catchier/drier'), or cancel?

---

## 5. The narration structure

Three zones, 7-9 slides total, 700-1,050 words at ~140 wpm.

### 5.1 Cold Open (always 2 slides, 45-60 sec)

**Slide 1 — Hook.** Cold open. A relatable analogy, surprising number, or "wait, what?" moment. **No setup. No TCN-specific jargon.** Earns the next 30 seconds of attention.

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

*Note: this example is the floor for register-7 catchiness, not the ceiling. The skill should aim higher when the article supports it. Rhetorical questions, one-word landings, and unexpected analogies are the moves; this example uses one of each.*

**Slide 2 — Thesis.** What the piece argues, distilled to one or two sentences. Often a verbatim or near-verbatim line from the article. The promise the video is making.

Example:

```
**[SLIDE 02 — THESIS]**

They thought they were buying a business. They bought a franchise.
The hardware is theirs. The pricing authority is not.
```

### 5.2 Body (3-5 slides, 3-4 min)

The skill picks from this menu by reading the article and asking *which of these does this article most strongly support?*

- **The Receipt** — strongest concrete evidence. Numbers, dates, names. The "I can prove it" segment. **Usually mandatory.**
- **The Frame** — the TCN lens. The way of looking at it that re-orders everything. Where refrains often live. **Usually mandatory** (one of Frame or Twist is always present).
- **The Stakes** — why Marcus + visiting friends should care. The "this affects you because" segment.
- **The Twist** — the part that genuinely surprised you and will surprise viewers.
- **The Historical Echo** — the comparison that grounds the argument in something familiar (the Volcker-equivalent moment in a Fed piece; the McDonald's-FDD comparison in a DePIN piece).
- **The Verbatim** — a primary-source quote that lands harder than any paraphrase. Requires the fact-check report to source the quote.

If the article has a refrain candidate (a single sentence the article repeats or implies repeatedly), the skill places it across 2-3 middle slides and marks each occurrence as `[REFRAIN]` in the Script Notes footer.

### 5.3 Outro (always 2 slides, 30-45 sec)

**Slide N-1 — Tease.** Open loops. Explicitly name what the video did NOT cover. This is the funnel mechanism that converts viewers into readers.

Example:

```
**[SLIDE N-1 — TEASE]**

The piece names four disclosures that would have caught Helium in 2021
and missed Datagram. We didn't get to Datagram. The article does.

Every number you saw is sourced. Vote records, proposal text, financial
reports. All linked.
```

**Slide N — End.** Disclosure (if any) + Substack CTA. **Same close every video** for channel branding:

```
**[SLIDE N — END]**

The Civic Node. Subscribe free at drinkyouroj.substack.com.
Weekly. No hype.
```

---

## 6. Voice calibration

### 6.1 The dial

Register sits at **6-7 on a 1-10 scale** where:
- **1** = dispatch-002 ("The Strait Is the Mandate") — TCN-Marcus, dry essayist, no concessions to general-audience pacing
- **4** = dispatch-004 ("You Own the Hotspot") — TCN-Marcus with the McDonald's analogy doing some accessibility work
- **7** = the calibrated register this skill produces — Hank-Vox blend, sharper hooks, willingness to drop a "vibes" once per video, occasional one-word landings
- **10** = a Hank Green vlog — too colloquial; concedes Marcus's respect for Marcus's accessibility

### 6.2 Reference channels

- **Hank Green** — colloquial pacing, willingness to break the fourth wall, comedic asides, vulnerable, parenthetical jokes
- **Vox Explained / Search Party (Westbrook) / late Vox Explained** — formal but emotional, strong narrative arc, declarative, intelligent-but-accessible vocabulary, cinematic structure

The blend = "intelligent-but-accessible video essay with comedic asides and a willingness to be conversational."

### 6.3 Calibration tests (every slide must pass both)

1. **Marcus would get it** — would Marcus (the TCN-reader persona) smirk at the cleverness, or wince at the bait? If wince, dial down.
2. **Hank-Vox test** — would Hank deliver this line without a wince? Would Vox put a key phrase on screen as a chyron? If either flinches, revise.

### 6.4 Spoken-word adaptations applied to TCN voice

- **Shorter sentences than written prose.** Max ~22 words, target 12-15.
- **No em-dashes.** Replace with comma + restructure, or with a deliberate one-word landing.
- **No subordinate-clause stacks.** Split into two sentences. Listeners can't track three-clause structures aurally.
- **Numbers spoken aloud.** Write "three hundred eighty-five thousand" not "385,000" in the script — easier for the reader to deliver naturally.
- **One-word landings as a feature.** "Vibes." / "Nobody overrode it." / "Same protocol. Different revenue ladder." These are the Hank move that takes the dial from 4 to 7.
- **Repetition is welcome.** Refrains, callbacks, and deliberate restatement. Written prose avoids these; spoken-word essays embrace them.
- **Concrete over abstract.** Visual word choices. The listener has to picture it on the first hearing.

### 6.5 Canonical voice file

Loads `workspace/core/anti-ai-writing-style.md` at runtime. Same contract as `tcn-headline`, `tcn-draft`, etc. No duplicated banned-words lists. Fallback message if missing: halt with the same instruction `tcn-headline` uses.

---

## 7. Output format (canonical examples)

### 7.1 Title block

```markdown
# [Article Title in Spoken-Word Friendly Form]
## The Civic Node · Dispatch №[NNN]
## [N] slides · trailer-format · 5-7 min target
```

The dispatch number is captured from the user (or inferred from existing dispatches in the workspace). The format tag (`trailer-format`) distinguishes new-format scripts from the legacy `Part One/Part Two` format.

### 7.2 Slide markup

```markdown
**[SLIDE NN — SLIDE TITLE]**

[narration text — short sentences, no em-dashes, one-word landings welcome]

[blank line between paragraphs to mark a breath point]

---
```

The `---` between slides is intentional — it gives the reader visual separation when reading aloud.

### 7.3 Script Notes footer (always present)

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

## 8. Skill process (internal steps)

1. **Voice file check** — verify `workspace/core/anti-ai-writing-style.md` exists. Halt if missing with the standard TCN fallback message.
2. **Read the article draft** + (if present) the fact-check report.
3. **Identify the hook angle** — find the most relatable analogy or sharable claim in the article. If 2+ strong candidates exist, surface to user for selection. If one obvious choice, pick and proceed.
4. **Identify the thesis line** — distill the article's argument to one or two sentences. Often a verbatim or near-verbatim line from the article.
5. **Pick the middle-slide menu** — read the article's argument structure and select 3-5 from the menu (Receipt / Frame / Stakes / Twist / Historical Echo / Verbatim). Receipt is almost always picked; one of Frame or Twist is almost always picked.
6. **Detect a refrain candidate** (optional) — if the article repeats or implies a single load-bearing sentence, mark it as a refrain candidate and place it across 2-3 middle slides.
7. **Draft the script slide-by-slide** — apply voice calibration (§6) and spoken-word adaptations. Mark candidate refrain lines.
8. **Compose the Script Notes footer** — word count, runtime estimate, pacing cues, refrain markers, cold-open candidate, refrain candidate, cuts-from-article list.
9. **Present to user with the standard gate prompt** (§4).

---

## 9. Failure modes & fallbacks

- **Article draft missing or unreadable** — surface the failure, ask for a valid path. Halt.
- **Voice canonical file missing** — halt with the same message used by `tcn-headline`. Do not fall back to generic register (per the elasticity-bug failure mode documented in `tcn-headline`).
- **Article too short for a 5-7 min trailer** (less than ~800 words article-side) — surface to user: "this piece is short enough that the video would cover most of it. Confirm you want a trailer (with curiosity-gap funnel) or a near-full read-through?" Let user override.
- **No obvious hook angle** (rare) — present 2-3 candidate cold-open frames and ask user to pick.
- **Fact-check report has flagged unresolved items** — surface those to the user before drafting. A trailer can't safely include claims the fact-check skill flagged. Let user override only if they explicitly accept the editorial risk.
- **User redirects** — re-invoke the relevant step:
  - "new hook" → re-draft Slide 01 + 02
  - "swap a middle slide" → ask which slide, generate replacement from menu
  - "dial catchier/drier" → re-draft full script at adjusted register
  - "shorter/longer runtime" → recalibrate compression and re-draft

---

## 10. Relationship to companion skills

**This skill is the first step in the YouTube production workflow.** Downstream skills consume its output:

| Skill | Status | Reads from this skill |
|-------|--------|------------------------|
| `tcn-youtube-slideshow` | Planned (next brainstorm) | Slide markers + slide-visual cues + refrain markers — produces Claude Design slideshow prompts |
| `tcn-youtube-title` | Planned | Cold-open candidate (Script Notes footer) — optional title inspiration |
| `tcn-youtube-description` | Planned | Slide markers (semantic chapter names better than raw transcript chunking) — optional, after recording |
| `tcn-youtube-thumbnail` | Planned | Cold-open candidate — optional visual-metaphor input |

**This skill consumes:**

| Source | Required? | Used for |
|--------|-----------|----------|
| Article draft (`tcn-draft` output) | Yes | The argument and prose to compress |
| Fact-check report (`tcn-fact-check` output) | Optional | Verbatim slide source quotes; pre-flight check for unresolved flagged items |
| `workspace/core/anti-ai-writing-style.md` | Yes | Voice rules — banned words, AI-tells, vocabulary cliff, closing-line abstraction |

---

## 11. Test criteria (definition of done)

The skill is working correctly when:

1. **Runs end-to-end on the Friday article** and produces a `youtube-narration.md` with the correct structure (Cold Open + Flex Middle + Outro), the right word count (700-1,050), and a complete Script Notes footer.
2. **The cold-open passes the Hank-Vox test** — at least one tester (the user) reads it aloud and confirms Hank could deliver it without a wince.
3. **The cold-open passes the Marcus-smirk test** — Marcus (the TCN-reader persona) would smirk, not wince.
4. **Refrain markers are correctly placed** if a refrain candidate was detected.
5. **The Script Notes footer is complete** — word count, runtime, pacing cues, cold-open candidate, refrain candidate, and cuts-from-article are all populated.
6. **The Tease slide explicitly names article content the video did not cover** — the funnel mechanism is present.
7. **The End slide uses the canonical close verbatim** — same close every video.
8. **No em-dashes appear in narration prose.** (Em-dashes inside *primary-source quoted material* on a Verbatim slide are acceptable if the reader can naturally pause on them.) No subordinate-clause stacks in narration prose. Sentences average under 16 words.
9. **The skill halts gracefully** when voice file is missing, article is missing, or fact-check has unresolved items.

---

## 12. Implementation track

This spec hands off to:

1. **`superpowers:writing-plans`** — produces an implementation plan for the skill
2. **`anthropic-skills:skill-creator`** — produces the actual `SKILL.md` (and any `references/` files) following the conventions used by the rest of the TCN skill family
3. **Test pass** — run the skill against `workspace/drafts/<slug>/05-draft-v{N}.md` for Friday's video and verify all test criteria pass

**Source-of-truth location:** `/Users/justin/CascadeProjects/claude-skills/tcn-youtube-narration/SKILL.md`
**Runtime copy:** `~/.claude/skills/tcn-youtube-narration/SKILL.md` (symlink — per repo conventions documented in `feedback_claude_skills_source_of_truth.md`)

---

## 13. Out of scope for this spec (deferred to separate brainstorms)

- **`tcn-youtube-slideshow`** — converts narration to Claude Design slideshow prompts. Next brainstorm session.
- **`tcn-youtube-title`** — title generation. Brainstorm largely complete; will resume after Friday recording.
- **`tcn-youtube-description`** — description body + tags. Brainstorm largely complete; will resume after Friday recording.
- **`tcn-youtube-thumbnail`** — image prompt + text overlay spec. Brainstorm largely complete; will resume after Friday recording.
- **`tcn-youtube-shorts`** — Shorts variant. Future skill.
- **`tcn-youtube-pinned-comment`** — pinned comment generator. Future skill.
- **`tcn-youtube-end-screen`** — end-screen CTA script. Future skill.
