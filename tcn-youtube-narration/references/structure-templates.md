# Structure Templates — tcn-youtube-narration

Canonical templates for slide markup, the three narration zones (Cold Open / Body / Outro), the Script Notes footer, and the title block. Loaded at runtime when instantiating a slide. Skim, do not memorize.

---

## 1. Slide markup format

**Format:** `**[SLIDE NN — TITLE]**` — two-digit zero-padded slide number, em-dash separating from the slide title.

**Rationale:** matches the format used in dispatch-004 ("You Own the Hotspot"). Visually distinct from prose. Easy to grep. The em-dash inside the bracket is a STRUCTURAL marker, not narration content, so it does not violate the no-em-dashes-in-narration rule.

**Slide separator:** `---` on its own line between consecutive slides. Provides visual breathing room when reading aloud.

**Worked example:**

```
**[SLIDE 03 — THE RECEIPT]**

The vote passed 41,000 to 12,000. Eight wallets held 60 percent of the yes side.

---

**[SLIDE 04 — THE FRAME]**
```

---

## 2. Cold Open templates

The Cold Open is always 2 slides, 45-60 sec. Earns the next 30 seconds of attention.

### Slide 1 — Hook

Cold open. A relatable analogy, surprising number, or "wait, what?" moment. No setup. No TCN-specific jargon.

**Example (verbatim from spec §5.1, register 7):**

```
**[SLIDE 01 — HOOK]**

Buying a McDonald's franchise comes with a 200-page disclosure document.
Federal law requires it. The pricing. The exit terms. What happens if
McDonald's changes the menu and your numbers stop working.

Three hundred eighty-five thousand people bought a Helium hotspot.

The franchise disclosure equivalent? They didn't get one.

Vibes.
```

**Hank-Vox moves present in this example:**
- **Concrete number:** "200-page disclosure," "Three hundred eighty-five thousand" (spoken-aloud form, not "385,000")
- **Rhetorical question:** "The franchise disclosure equivalent?"
- **Period structure replacing em-dash:** "The pricing. The exit terms." instead of "the pricing — the exit terms"
- **One-word landing:** "Vibes."

This example is the floor for register-7 catchiness, not the ceiling. Aim higher when the article supports it.

### Slide 2 — Thesis

What the piece argues, distilled to one or two sentences. Often a verbatim or near-verbatim line from the article. The promise the video is making.

**Example (verbatim from spec §5.1):**

```
**[SLIDE 02 — THESIS]**

They thought they were buying a business. They bought a franchise.
The hardware is theirs. The pricing authority is not.
```

**What makes a good thesis line:** it's the *sharable core* of the article, not the topic. A reader could text it to a friend without context and the friend would understand the stakes.

---

## 3. Body slide menu

The Body is 3-5 slides, 3-4 min. The skill picks from this menu by asking *which of these does this article most strongly support?*

All examples below are **invented hypothetical articles** — they are not drawn from any real TCN dispatch.

### The Receipt

Strongest concrete evidence. Numbers, dates, names. The "I can prove it" segment. **Usually mandatory.**

**Example phrasing:**

```
**[SLIDE 03 — THE RECEIPT]**

The pension fund sold 18 percent of its small-cap holdings in March.
The same month the board added two private-credit allocations.
The minutes name the consultants. The fee schedule is in Appendix C.
```

### The Frame

The TCN lens. The way of looking at it that re-orders everything. Where refrains often live. **Usually mandatory** (one of Frame or Twist is always present).

**Example phrasing:**

```
**[SLIDE 04 — THE FRAME]**

This isn't a budget shortfall. It's a transfer.
The same dollars move. They just stop having a name attached to them.
```

### The Stakes

Why Marcus + visiting friends should care. The "this affects you because" segment.

**Example phrasing:**

```
**[SLIDE 05 — THE STAKES]**

If you live in this district, your school's per-pupil number drops 4 percent next year.
That is not a forecast. That is the line item.
```

### The Twist

The part that genuinely surprised you and will surprise viewers.

**Example phrasing:**

```
**[SLIDE 06 — THE TWIST]**

The auditor flagged the same line item in 2019. And 2021. And 2023.
Three reports. Same finding. Nobody overrode it. Nobody acted on it either.
```

### The Historical Echo

The comparison that grounds the argument in something familiar. The Volcker-equivalent moment.

**Example phrasing:**

```
**[SLIDE 07 — THE HISTORICAL ECHO]**

The 1986 savings-and-loan rules were written after the fact, not before it.
Every name on the post-crisis hearings had been quoted in a trade journal three years earlier.
The warning was public. The action wasn't.
```

### The Verbatim

A primary-source quote that lands harder than any paraphrase. Requires the fact-check report to source the quote.

**Example phrasing:**

```
**[SLIDE 08 — THE VERBATIM]**

From the committee transcript, page 47:
"We are not pretending this is sustainable. We are asking what comes after."
The vote was 9 to 2. The "after" never came.
```

**Closing note on the menu:** the skill picks 3-5 of these per article. The Receipt is almost always chosen. At least one of Frame or Twist is almost always chosen. Stakes, Historical Echo, and Verbatim slot in based on what the article actually supports.

---

## 4. Outro templates

The Outro is always 2 slides, 30-45 sec.

### Slide N-1 — Tease

Open loops. Explicitly name what the video did NOT cover. The funnel mechanism that converts viewers into readers.

**Example (verbatim from spec §5.3):**

```
**[SLIDE N-1 — TEASE]**

The piece names four disclosures that would have caught Helium in 2021
and missed Datagram. We didn't get to Datagram. The article does.

Every number you saw is sourced. Vote records, proposal text, financial
reports. All linked.
```

**What makes a strong Tease:** it names SPECIFIC content that's in the article and NOT in the video. Vague teases ("the article has more!") don't convert.

### Slide N — End

Disclosure (if any) + Substack CTA. **Same close every video** for channel branding.

**Verbatim:**

```
**[SLIDE N — END]**

The Civic Node. Subscribe free at drinkyouroj.substack.com.
Weekly. No hype.
```

This close is CANONICAL — same wording every video for channel branding. Do not vary it per piece.

---

## 5. Script Notes footer template

Always present at the end of the script. Verbatim from spec §7.3:

```
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

**Forward-compat fields.** The last three bulleted fields cost nothing to produce now and save work downstream:

- **Cold-open candidate** → consumed by `tcn-youtube-title` (title inspiration) and `tcn-youtube-thumbnail` (visual metaphor).
- **Refrain candidate** → consumed by `tcn-youtube-slideshow` (slide rhythm planning).
- **Cuts from the article** → consumed by `tcn-youtube-description` (description content) and reused by the Tease slide itself.

Populate every field even when the value is "none on this pass." Empty fields read as a bug downstream; explicit "none" reads as a decision.

---

## 6. Title block template

Verbatim from spec §7.1:

```markdown
# [Article Title in Spoken-Word Friendly Form]
## The Civic Node · Dispatch №[NNN]
## [N] slides · trailer-format · 5-7 min target
```

**Notes:**

- **"Spoken-word friendly"** — the title may differ slightly from the article title to be easier to deliver aloud. Drop a colon. Use a shorter version. The article title is the canonical record; the video title is the spoken adaptation.
- **`Dispatch №[NNN]`** — zero-padded to three digits, populated by the dispatch-number detection step (skill process step 9). The skill scans `workspace/dispatch-narration/` for existing `dispatch-NNN-*.md` files and suggests the next integer.
- **`trailer-format`** — the format tag distinguishes new-format scripts from the legacy Part-One/Part-Two skeleton. Always present on new scripts.
