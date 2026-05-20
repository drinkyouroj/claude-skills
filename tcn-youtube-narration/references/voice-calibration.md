# Voice Calibration — tcn-youtube-narration

*Loaded at runtime when calibrating voice register on a narration script. This file is about the dial. The canonical voice file `workspace/core/anti-ai-writing-style.md` remains the source of truth for banned vocabulary and AI-tells.*

---

## 1. The Dial

Register sits at **6-7 on a 1-10 scale**. The anchor points:

- **1 — dispatch-002 ("The Strait Is the Mandate").** TCN-Marcus, dry essayist. No concessions to general-audience pacing. Reads like a memo to other people who already know the terms.
- **4 — dispatch-004 ("You Own the Hotspot").** TCN-Marcus with the McDonald's analogy doing some accessibility work. The argument is the same, but one familiar comparison is letting a non-expert in. Still reads more like article-in-spoken-form than video essay.
- **7 — what this skill produces.** Hank-Vox blend. Sharper hooks. Willingness to drop a "vibes" once per video. Occasional one-word landings. The cleverness is foregrounded; the argument structure is the same.
- **10 — a Hank Green vlog.** Too colloquial. Concedes Marcus's respect for Marcus's accessibility. The voice has become the content.

The gradient: 1 trusts the reader to keep up. 4 offers one handhold. 7 builds a path. 10 carries the listener.

---

## 2. Reference Channels

- **Hank Green** — colloquial pacing, willingness to break the fourth wall, comedic asides, vulnerability, parenthetical jokes.
- **Vox Explained / Search Party (Westbrook) / late Vox Explained** — formal but emotional, strong narrative arc, declarative voice, intelligent-but-accessible vocabulary, cinematic structure.

The blend: **intelligent-but-accessible video essay with comedic asides and a willingness to be conversational.**

---

## 3. The Two Calibration Tests

Every slide must pass both.

### Marcus-smirk test

Would Marcus (the TCN-reader persona) smirk at the cleverness, or wince at the bait?

- **Pass:** Marcus smirks. The line earns the trick.
- **Fail signal:** Marcus winces. The line is reaching, performing, or selling. If wince, dial down.

### Hank-Vox test

Would Hank Green deliver this line without a wince? Would Vox put a key phrase on screen as a chyron?

- **Pass:** Both nod. Hank could say it. Vox could put it on screen.
- **Fail signal:** Either flinches. If Hank wouldn't say it, the line is too dry. If Vox wouldn't chyron it, the line is too colloquial. Revise.

---

## 4. Worked Example: Dialing 002 → 7

**Before — dispatch-002 Slide 1 (register 1, verbatim):**

> This piece is about a rate decision nobody voted on.
>
> In April 2026, American gasoline prices rose 37% in five weeks. The cause was geography: a 21-mile waterway in the Persian Gulf. The committee that holds the price stability mandate had no instrument for any of it.

**After — at register 7:**

```
Gas prices jumped thirty-seven percent in five weeks.

The cause was not the economy. It was a twenty-one-mile
stretch of water in the Persian Gulf.

The committee that's supposed to keep prices stable has
no tool that reaches that far. None.

So what does a mandate mean when the lever is somewhere
else?
```

**What changed:**
- Hank moves: rhetorical question to close the open ("So what does a mandate mean…"), one-word landing ("None.") used to punch the powerlessness.
- Vox moves: declarative opening hook ("Gas prices jumped thirty-seven percent in five weeks."), cinematic re-framing ("The cause was not the economy. It was…") that sets up the chyronable phrase.
- Spoken-word adaptations: numbers spelled out ("thirty-seven percent," "twenty-one-mile"), no em-dashes (the original colon and parenthetical-feeling clause were restructured into clean periods), sentences kept under 22 words, the abstract phrase "no instrument for any of it" replaced with the concrete "no tool that reaches that far."

---

## 5. Worked Example: Dialing 004 → 7

**Before — dispatch-004 Slide 01 (register 4, verbatim):**

> If you bought a McDonald's franchise, you'd read the disclosure document
> first. Federal law requires it. The pricing. The exit terms. What happens
> if McDonald's changes the menu in a way that costs you money.
>
> Three hundred eighty-five thousand people bought hardware that earns four
> to eight dollars a month, at rates someone else sets. They thought they
> were buying a business. They bought a franchise. Nobody handed them the
> disclosure document until three years later.
>
> This is what a DePIN franchise looks like when the contract gets
> documented in hindsight.

**After — at register 7 (canonical anchor from spec §5.1):**

```
Buying a McDonald's franchise comes with a 200-page disclosure document.
Federal law requires it. The pricing. The exit terms. What happens if
McDonald's changes the menu and your numbers stop working.

Three hundred eighty-five thousand people bought a Helium hotspot.

The franchise disclosure equivalent? They didn't get one.

Vibes.
```

**What changed:**
- Rhetorical question ("The franchise disclosure equivalent?") replaces a multi-clause declarative.
- One-word landing ("Vibes.") replaces the meta-summary paragraph; the joke lands and the listener picks up the implication.
- Period restructure replaces the original's comma-stacks; where dispatch-004 ran subordinate clauses, the rewrite chops into discrete short sentences a reader can deliver in one breath each.

---

## 6. Spoken-Word Adaptations Checklist

- [ ] **Sentences shorter than written prose** (max ~22 words, target 12-15) — listeners can't track long structures aurally; the ear loses the subject before the verb arrives.
- [ ] **No em-dashes in narration text** — replace with comma + restructure, or with a deliberate one-word landing. The em-dash is a visual cue; the spoken version is the pause it creates, and the pause needs its own sentence.
- [ ] **No subordinate-clause stacks** — split into two sentences. Three-clause structures are unreadable aloud.
- [ ] **Numbers spoken aloud** — write "three hundred eighty-five thousand" not "385,000" so the reader delivers naturally. The script is for the mouth, not the eye.
- [ ] **One-word landings as a feature** — "Vibes." / "Nobody overrode it." / "None." The Hank move that takes the dial from 4 to 7. One per slide max, or they stop landing.
- [ ] **Repetition is welcome** — refrains, callbacks, deliberate restatement. Written prose avoids these; spoken-word essays embrace what the ear needs to track an argument over six minutes.
- [ ] **Concrete over abstract** — visual word choices. The listener has to picture it on the first hearing, with no rewind. "Twenty-one-mile stretch of water" lands; "geography" doesn't.

---

## 7. Closing Note

This reference is consulted at runtime by `tcn-youtube-narration` when calibrating voice register on a narration script. It is purely about the dial — the 1-10 register scale, the Hank-Vox blend, the spoken-word adaptations.

The canonical voice file `workspace/core/anti-ai-writing-style.md` remains the source of truth for banned vocabulary, AI-tells, and the TCN voice as a whole. This file extends that contract for the spoken-word format; it does not replace it.
