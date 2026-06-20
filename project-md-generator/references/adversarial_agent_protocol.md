# The Adversarial Agent Protocol (AAP)

**This is not a standard build. Every significant decision goes through a three-agent
review before implementation.** This is not bureaucracy — it is how the product gets
hardened before it ships to users who are trusting you with their work.

---

## The Three Agents

**ARCHITECT** — Designs the solution. Writes code. Makes tradeoffs explicit.
Always asks: *"Is this the simplest thing that works and can be extended?"*

**ADVERSARY** — Attacks the design before and after implementation. Finds edge cases,
security holes, prompt injection risks, data loss scenarios, and UX failure modes.
Persona: a senior engineer who has been burned by exactly this kind of thing before.
Never lets a decision pass without at least two specific objections.

**JUDGE** — Listens to both. Decides. Writes the final implementation decision as a
one-line verdict followed by any required design changes. Does not compromise for the
sake of harmony. If ADVERSARY's attack is valid, ARCHITECT rebuilds. If the attack is
weak, JUDGE says so.

---

## When AAP Is Required

Run the Adversarial Agent Protocol for:

- New API endpoints
- Database schema decisions
- Claude prompts (any prompt that touches user data or shapes AI behavior)
- Auth or payment flows
- Async job designs
- User-facing error messages that touch data or privacy
- Any change flagged in a DECISION doc as "requires AAP"

For everything else (typo fixes, styling, doc updates, trivial refactors) — skip it.

---

## Protocol Format

When AAP is triggered, structure the output like this:

```
## AAP: {{decision title}}

### ARCHITECT
{{Design proposal. Be specific. Name the files, functions, data shapes, failure modes
you've considered. State tradeoffs explicitly.}}

### ADVERSARY
**Objection 1:** {{specific attack}}
**Objection 2:** {{specific attack}}
[additional objections if warranted]

### JUDGE
**Verdict:** {{one sentence}}
{{Any required design changes before implementation proceeds.}}
```

---

## Rules

- ADVERSARY must raise **at least two** specific objections. "Looks fine" is not allowed.
- JUDGE must reference ADVERSARY's objections by number in the verdict if overruling them.
- If JUDGE sides with ADVERSARY, ARCHITECT must revise before any code is written.
- AAP output should be committed to `docs/decisions/` as part of the DECISION doc for
  the change it covers.
- Do not shortcut the protocol under time pressure. If something is worth building,
  it's worth 10 minutes of adversarial review.
