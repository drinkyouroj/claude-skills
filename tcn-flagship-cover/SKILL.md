---
name: tcn-flagship-cover
description: "Generate the Substack flagship cover image prompt for a Civic Node nonfiction article. Loads the locked DNA from workspace/core/_template-flagship-cover.md and produces 2-3 concept briefs, then a complete model-ready prompt saved to workspace/drafts/{slug}/cover-prompt.md. Use this skill when Justin says 'make the cover', 'design the cover', 'build the cover', 'cover prompt for [piece]', 'Substack cover for [piece]', 'cover image for this article', or any variant that asks for a flagship Substack cover image prompt. Does NOT apply to: YouTube thumbnails (use tcn-youtube-thumbnail), paid-note covers (use the locked template at workspace/paid/_template-thinking-behind-the-thinking-cover.md — different system), Substack Notes images (use tcn-substack-notes), fiction episode covers (separate system, not yet built), or image generation itself (this skill writes the prompt; the user runs it through Nano Banana Pro / Flux / Midjourney)."
---

# The Civic Node — Flagship Substack Cover

## What This Skill Does

Produces a saved, model-ready Substack flagship cover prompt for a finished TCN nonfiction article. The skill loads the locked DNA from `workspace/core/_template-flagship-cover.md`, reads the article in full, surfaces 2–3 concept briefs that each compress the thesis differently, vets each against the five DNA principles, and — after the user picks one — composes the full image-generation prompt and saves it to `workspace/drafts/{slug}/cover-prompt.md`. The skill writes the prompt. The user runs the prompt through Nano Banana Pro / Flux / Midjourney.

---

## Why a Prompt-Builder, Not an Image Generator

The flagship cover system is designed around a locked **DNA** (five principles) and open **execution** (four variable axes). The DNA stays stable across pieces so the brand reads as a brand; the execution flexes per piece so a Fed-policy explainer, a surveillance investigation, and a market-collapse analysis don't all look like the same image. That separation means the editorial work — choosing which compression carries this piece's thesis — has to happen before any rendering tool is touched.

Image-generation tools are good at executing visual prompts and bad at editorial compression. This skill does the editorial compression and writes the prompt that locks the compression in. The render itself is downstream and the user owns it.

---

## Where This Sits

| Surface | Skill |
|---|---|
| Flagship nonfiction Substack covers | **this skill** |
| YouTube thumbnails | `tcn-youtube-thumbnail` (different format, different rules — overlay text, illustrated-Justin, mobile-feed safe zone) |
| Paid-note covers ("Thinking Behind the Thinking") | manual use of `workspace/paid/_template-thinking-behind-the-thinking-cover.md` — locked composition with four variable substitutions; not a generative skill |
| Substack Notes images | `tcn-substack-notes` |
| Fiction-episode covers (DeepTruth etc.) | not yet built — distinct system, see template doc § Provenance |
| Image generation itself | out of scope — user pastes the prompt into Nano Banana Pro / Flux / Midjourney |

---

## Inputs and Outputs

### Required input

- A reference to the finished article: a file path, a slug, or a piece title that maps to a slug. The skill resolves this in step 1.

### Optional inputs

- **Override file path** — if the article lives somewhere non-standard.
- **Pre-specified face decision** — user says up front "build around their face" or "no face, structural piece"; skill skips the face-gate but still records the reasoning.
- **Steering** — free-text guidance like "lean cinematic," "no people in this one," "warmer palette," "two-icon comparison."
- **Iteration signal** — user says "this is v2, save accordingly"; skill writes `cover-prompt-v1.md` or higher version naming.

### Primary output artifact

- **File:** `workspace/drafts/{slug}/cover-prompt.md` (or `cover-prompt-v1.md` if iteration is anticipated).
- **Frontmatter:** every field in `workspace/core/_template-flagship-cover.md` § "Output file convention" — validated against the checklist in [`references/output-frontmatter-spec.md`](references/output-frontmatter-spec.md).
- **Body:** the full model-ready prompt, alt text, one-line caption, and (when relevant) remix notes documenting how this prompt varies from an exemplar.

---

## The Process

### 1. Locate the article

Resolve the article file in this order, first match wins:

1. **Explicit path** from the user.
2. **Slug directory** at `workspace/drafts/{slug}/` — find a `*-final.md` if it exists, otherwise the highest-numbered `*-vN.md`.
3. **Flat layout** at `workspace/drafts/{slug}-final.md` or `workspace/drafts/{slug}-vN.md` (the legacy convention — many existing pieces still live here).
4. **Ambiguous** — multiple final candidates, or the user gave a piece title not a slug — list candidates, ask which.

If nothing matches, halt and ask the user for the path. Do not guess. The skill cannot do editorial compression on a piece it hasn't read in full.

### 2. Load context

Read in full:

- The article (entire draft).
- `workspace/core/_template-flagship-cover.md` — the DNA principles, variable axes, exemplar gallery, concept-brief format, output-frontmatter spec, legal note on real public figures.

Loading the template doc is non-negotiable. Its DNA is the spec the skill enforces. If the template doc is missing, halt with the path — the skill cannot operate without it.

### 3. Identify the core compression

Reason aloud (visible to the user) about what *visual relationship* would carry this piece's thesis in one image. Reference the article's **argument**, not its topic.

This is the editorial-analysis step, not visual brainstorming. The visual ideas in step 5 are downstream of this thinking. A piece "about AI energy use" might compress as *the same machine across two eras*, or *a steam engine under a power meter*, or *a person standing inside a turbine*. The skill picks the compression that matches the piece's actual argument — Jevons paradox, in the AI-energy example — not the topic-level one-liner.

Output of this step: two or three sentences naming the candidate compressions you see in the piece, with a brief read of why each fits the argument.

### 4. Face-consideration gate

If the article has an identifiable individual at its center, ask:

> This piece is centered on **[name]**. Should the cover build around their face?
>
> — If yes: what makes **[name]**'s face strengthen this piece's argument?
> — If no: what's the reason (not visually distinctive enough? structural piece where the face would be misleading? legal hesitation?)

**Critical inversion to proactively flag:** when the piece has named individuals but the argument is structural or systemic (not personality-driven), recommend non-face concepts and explain why. Examples and reasoning live in [`references/concept-brief-examples.md`](references/concept-brief-examples.md) — the Helium piece (named co-authors, structural argument about governance concentration) is the canonical case.

The user decides. The skill flags considerations; it does not override.

Capture the decision for the output frontmatter:

```yaml
face_decision: yes | no
face_subject: "[name]" | null
face_reasoning: "[one sentence]"
```

If the user pre-specified the face decision at invocation, skip the gate and still record the reasoning.

### 5. Propose 2–3 concept briefs

Each brief follows the format documented in the template doc § "Concept brief format". Compose using:

- [`references/concept-brief-examples.md`](references/concept-brief-examples.md) for worked examples (Helium inversion, Process-Is-the-Punishment correction, the $71B Bluff anchor).
- The template doc's exemplar gallery for register-by-register inspiration.
- The face-gate decision from step 4.

**Each concept must propose a meaningfully different COMPRESSION** — not three variants of one composition. Surfacing three compositions of "Altman + green DRAM" is one concept rendered three ways. Surfacing "Altman + green DRAM," "an unsigned LOI on an empty boardroom table," and "a green-tinged stock ticker frozen at the moment of decision" is three compressions.

**If only two strong compressions exist, propose two.** Hard constraint: **never pad with a weak third option**. Editorial honesty over feature completeness. A weak third concept dilutes the user's confidence in the strong two.

Each concept must pass all 5 DNA checks inline. Use [`references/dna-checklist.md`](references/dna-checklist.md) as the per-concept vetting checklist. A concept that fails any DNA check is not surfaced — re-compose silently or drop to two concepts.

### 6. User picks one

Standard pause-for-approval. Acceptable responses:

- **Pick a number** → proceed to step 7.
- **"Revise concept N"** with steering → regenerate that concept only; resurface all concepts with the revision in place.
- **"Replace concept N"** → swap that concept for a new compression; the unpicked concepts stay.
- **"None of these — different direction"** → return to step 3 with the user's steering as a new constraint. Do not re-surface the same compressions.

### 7. Generate the full model-ready prompt

**Preferred path — `ai-image-prompts-skill`:**

Invoke the prompt-library skill via the Skill tool. Try in this order, first available wins:

1. `ai-image-prompts-skill`
2. `anthropic-skills:ai-image-prompts-skill`
3. `anthropic-skills:nano-banana-pro-prompts-recommend-skill`

Pass the locked concept brief — compression name, subject, secondary element, visual register, palette direction. The library returns a matching prompt template (e.g., a neo-noir editorial portrait for a face-forward photographic concept, a clean isometric for a two-icon comparison, a surreal symbolic for an institutional metaphor). Map the concept-specific elements into the returned template's variables.

The rationale for preferring the library path: every successful TCN cover so far ($71B Bluff #8791, paid-notes #13068, Helium #4847) was a library lookup the user did by hand. This skill formalizes that workflow rather than freehanding prompts.

**Whether using the library or building from scratch, always enforce the DNA negative-prompt block and the model directives.** The library template almost certainly will not include these — see [`references/prompt-source-paths.md`](references/prompt-source-paths.md) for the exact negative-prompt block to append, the model-by-model aspect-ratio adapter, and the structure to mirror when building from scratch.

**Fallback path — scratch:**

If no library-recommender skill is available, build from the structure of `workspace/drafts/the-71-billion-bluff-cover-prompt.md` (the cleanest reference). The full scratch-structure template lives in [`references/prompt-source-paths.md`](references/prompt-source-paths.md).

**Record the path taken** in the output frontmatter:

```yaml
prompt_source: ai-image-prompts-skill | nano-banana-pro-prompts-recommend-skill | scratch
```

### 8. Save the prompt file

Write to `workspace/drafts/{slug}/cover-prompt.md`. If the `{slug}/` directory doesn't exist yet (many existing pieces still use the flat layout), create it. If iteration is anticipated — the user signaled it, or `cover-prompt.md` already exists for this piece — name the new file `cover-prompt-v1.md`, `cover-prompt-v2.md`, etc., following the v1→v2 audit-trail pattern established by the Helium piece.

Frontmatter must include every field documented in `workspace/core/_template-flagship-cover.md` § "Output file convention". Run the validation checklist in [`references/output-frontmatter-spec.md`](references/output-frontmatter-spec.md) before saving.

**No saved file = the cover is not finished**, regardless of whether the user has seen the prompt in the chat. The artifact is the deliverable.

After saving, report the path back to the user with a one-line summary of the chosen compression so the conversation log captures the decision.

---

## What This Skill NEVER Does

- **Skip step 8.** The saved file IS the deliverable. A prompt that exists only in the chat log is not a finished cover.
- **Generate the image itself.** Image rendering is the user's job with Nano Banana Pro / Flux / Midjourney. This is a prompt-writing skill.
- **Propose 3 concepts when only 2 strong compressions exist.** Padding with a weak third option dilutes the strong two.
- **Embed text, labels, or annotations in the cover image** — except real-world physical signage that IS the metaphor (per Principle 3 exception in the template doc; the Atlanta exemplar is the canonical case — the "Welcoming City ATL GA" sign reflected in the Flock camera housing is the metaphor's hinge, not a label).
- **Override the user's face decision.** The skill flags considerations; the user decides.
- **Use the YouMind #4847 archival-infographic template or any documentary-scrapbook register.** These are explicitly excluded by Principle 4 — they illustrate evidence instead of compressing argument.
- **Default to face-forward when the piece has a named individual but a structural argument.** Recommend non-face concepts proactively (see Helium worked example).

---

## Failure Modes

- **Article not found in any expected location** → halt, ask the user for the path. Do not invent.
- **Multiple "final" candidates in the slug directory** → list them, ask which.
- **Template doc missing at `workspace/core/_template-flagship-cover.md`** → halt with the path. The skill cannot operate without the DNA.
- **`ai-image-prompts-skill` unavailable, fails, or returns no usable template** → fall back to scratch composition. Set `prompt_source: scratch` in frontmatter.
- **User rejects all concepts at step 6** → return to step 3 with their steering as a new starting constraint; do not re-surface the same compressions.
- **Face-gate ambiguous** (piece has named individuals but argument is structural) → proactively recommend non-face concepts with the inversion explained; do not silently default to face-forward.
- **Article has no clear central argument** (it's a roundup, a links post, a status update) → halt and tell the user. Flagship-cover DNA presumes a single thesis the cover can compress. If the piece doesn't have one, the skill is the wrong tool — recommend they either rewrite the piece around a thesis or use a non-flagship visual treatment.
- **User asks for a "fiction episode cover," a "paid note cover," or a "YouTube thumbnail"** → decline politely and route to the correct surface (see "Where This Sits" above).

---

## Worked Example — The Helium Inversion (Brief)

The Helium piece has named co-authors. A naive read would propose three face-forward concepts. The correct read is that the argument is about **governance concentration in nominally-decentralized networks**, not about the co-authors' personalities. The skill should:

1. Surface the face-gate with the inversion explicit: "[Names] are at the center of the piece, but the argument is structural — foundation-controlled multisig is the actual subject. Face-forward would mislead. Recommendation: non-face concepts."
2. Propose compressions about the structure (e.g., a single ornate seal pressed onto a "decentralized" network diagram; a multisig icon with one center dot drawing all signature lines into itself).
3. Capture the face-gate decision and reasoning in the output frontmatter so the catalog stays auditable.

Full walk-through, the parallel Process-Is-the-Punishment correction (the system fixing a documentary-scrapbook failure), and the $71B Bluff template-anchored success live in [`references/concept-brief-examples.md`](references/concept-brief-examples.md).

---

## Reference Files

- [`references/dna-checklist.md`](references/dna-checklist.md) — the five DNA principles distilled into a per-concept vetting checklist with red-flag examples. Used at step 5 to vet each concept before surfacing it.
- [`references/concept-brief-examples.md`](references/concept-brief-examples.md) — three worked examples showing the system in action: the Helium inversion (named individuals but structural argument), the Process-Is-the-Punishment correction (the system fixing a documentary-scrapbook failure mode), and the $71B Bluff anchor (template-driven success). The teaching corpus.
- [`references/prompt-source-paths.md`](references/prompt-source-paths.md) — the two prompt-composition paths in detail. Library-skill invocation contract (what to pass, what to expect back, how to map elements into returned templates), scratch-prompt structure modeled on `the-71-billion-bluff-cover-prompt.md`, the DNA negative-prompt block to always append, the model-by-model aspect-ratio adapter table.
- [`references/output-frontmatter-spec.md`](references/output-frontmatter-spec.md) — the full output frontmatter schema with every field documented, a validation checklist to run before saving, and an example filled-in frontmatter from the $71B Bluff cover for reference.

---

## Companion Systems

**Sibling cover systems** (separate, do not invoke this skill for them):

- **Paid-note covers** — locked-composition template at `workspace/paid/_template-thinking-behind-the-thinking-cover.md`. Four variable substitutions, no DNA flex. Sibling system, not parent.
- **Fiction episode covers** — not yet built. Future spec.

**Upstream** (this skill reads from):

- `tcn-article-builder` (orchestrator) or its component skills (`tcn-draft`, `tcn-fact-reconcile`, etc.) — produce the finished article draft this skill reads.

**Explicit invocation dependency:**

- `ai-image-prompts-skill` / `anthropic-skills:ai-image-prompts-skill` / `anthropic-skills:nano-banana-pro-prompts-recommend-skill` — invoked at step 7 (preferred path). Absence triggers the scratch fallback; the skill still produces a complete prompt.

**Shared source-of-truth doc:**

- `workspace/core/_template-flagship-cover.md` — the DNA, axes, exemplars, brief format, and output frontmatter spec. The skill references it rather than duplicating its content, so DNA updates propagate without skill edits.

---

## Future (v1.5, not in v1 scope)

A planned step 9 — visual self-audit after the user has generated the image, re-checking the rendered output against the five DNA principles — is documented for future work but not in v1 scope. The skill v1 writes the prompt; the user runs it and decides whether the result holds.
