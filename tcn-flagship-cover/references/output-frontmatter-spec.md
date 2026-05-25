# Output Frontmatter Spec — Schema + Validation Checklist

Every cover prompt saved by this skill must include a complete frontmatter block before the body of the prompt. This file documents the schema, defines every field, and provides a pre-save validation checklist.

The canonical schema lives in `workspace/core/_template-flagship-cover.md` § "Output file convention". This file is the **enforcement layer** — the validation the skill runs before saving.

---

## Full schema

```yaml
---
title: "Cover Prompt — [Article Title]"
type: image-prompt
article: "[relative or absolute path to the final article draft]"
model: Nano Banana Pro | Flux | Midjourney | other
aspect_ratio: "16:9 (1456 × 816)"
based_on: "[library template id (e.g., 'YouMind id: 8791 — Neo-Noir Fashion Portrait') or 'flagship-dna' for scratch]"
prompt_source: ai-image-prompts-skill | nano-banana-pro-prompts-recommend-skill | scratch
compression: "[compression name from the picked concept brief]"
register: "[visual register, e.g., 'editorial poster' / 'clean technical illustration']"
palette: "[palette description, e.g., 'B&W subject + saturated green backdrop']"
dna_checks:
  compression: yes
  two_elements_or_fewer: yes
  no_embedded_text: yes
  cinematic_or_technical_register: yes
  contrast_carries_argument: yes
face_decision: yes | no
face_subject: "[name]" | null
face_reasoning: "[one sentence explaining the choice]"
created: YYYY-MM-DD
---
```

---

## Field-by-field definitions

### `title`

Format: `"Cover Prompt — [Article Title]"`. The article title matches the title of the linked draft, not a shortened version. If the article title is itself long, keep it long — this is a working filename, not a Substack-feed line.

### `type`

Always `image-prompt`. Distinguishes cover prompts from other artifact types in the catalog.

### `article`

Path to the article file the cover prompt was built from. Prefer relative paths from the workspace root (e.g., `drafts/the-71-billion-bluff-v10.md`); fall back to absolute if the article lives outside the workspace. The path must point at the **specific version** the cover was composed against, not a generic `*-final.md` symlink — when the article goes through another edit pass, the cover may need a re-cover, and the version trail matters.

### `model`

Which image-generation tool the prompt is written for. If the user has not specified a target model, list the compatible ones: `Nano Banana Pro | Flux | Midjourney`. The prompt body should include the rendering directives for all listed models (per `prompt-source-paths.md` § Step A.6).

### `aspect_ratio`

Always `"16:9 (1456 × 816)"` for Substack flagship covers. Substack hero image renders at this ratio; deviation creates cropping artifacts on the feed.

### `based_on`

What the prompt was structurally derived from:

- **Library template id**, when Path A was used — e.g., `"Neo-Noir Fashion Portrait with High Contrast (YouMind id: 8791)"`. Include both the human-readable name and the catalog id.
- **`"flagship-dna"`**, when Path B (scratch) was used — indicating the prompt was composed directly from the DNA without a library scaffold.

### `prompt_source`

Which path produced the prompt body:

- `ai-image-prompts-skill` — Path A succeeded via the primary library skill.
- `nano-banana-pro-prompts-recommend-skill` — Path A succeeded via the Nano-Banana-specific recommender.
- `scratch` — Path B was used (no library skill available, or both library skills returned nothing usable).

Recording this lets the catalog audit over time which paths produced which quality of cover.

### `compression`

The picked concept brief's compression name, exactly as it appeared in step 5. Example: `"One signature, falling market"` (the $71B Bluff compression).

This is the **single most important field for catalog auditability**. Future searches across the catalog ("which face-forward neo-noir compressions worked?", "do we have a precedent for two-icon-comparison covers?") rely on consistent compression naming.

### `register`

The visual register the cover sits in. Must be one of the permitted registers from the DNA (or the picked concept's specific variant):

- editorial poster
- surreal symbolic illustration
- photographic with reflection device
- clean technical illustration
- narrative scene (specify the cultural idiom if relevant — e.g., "narrative scene, ukiyo-e")

Free text within those families is fine; the register names are not strictly enumerated.

### `palette`

Short prose description of the palette and the contrast it carries. Examples:

- `"B&W subject + saturated green backdrop"` ($71B Bluff)
- `"Cold steel-blue exterior + warm amber reflection"` (Atlanta)
- `"White background + industrial charcoal/steel-blue/brass"` (Cheaper AI)

### `dna_checks`

Five booleans, one per DNA principle. **Every check must be `yes` before saving.** If any check is `no` or `unsure`, do not save — return to step 5 and re-vet the concept. The point of the DNA is that an unmet check disqualifies the cover; recording `no` defeats the purpose.

The booleans correspond to the five principles in `workspace/core/_template-flagship-cover.md`:

- `compression` — Principle 1, metaphor compression not evidence illustration
- `two_elements_or_fewer` — Principle 2, ≤2 primary visual elements
- `no_embedded_text` — Principle 3, no embedded text (or photographed-signage exception applies)
- `cinematic_or_technical_register` — Principle 4, permitted register
- `contrast_carries_argument` — Principle 5, named carrying contrast

### `face_decision`

`yes` if the cover builds around an identifiable individual's face; `no` otherwise.

### `face_subject`

The named individual when `face_decision: yes`; `null` otherwise. Use the person's commonly-known name, not a formal title — `"Sam Altman"`, not `"Mr. Samuel H. Altman, CEO of OpenAI"`.

### `face_reasoning`

One sentence explaining the face decision. This is the audit-trail field — read across the catalog, the `face_reasoning` lines should make the editorial logic of face-vs-structure decisions legible over time.

Examples:

- **face_decision: yes** — `"Named executive in the editorial piece's headline event; his face anchors the piece to the specific public-record decision being reported."` ($71B Bluff)
- **face_decision: no** — `"Named co-authors are vectors for the structural critique, not its subject. Face-forward would mislead the reader into reading the piece as about people instead of about governance concentration."` (Helium)
- **face_decision: no** — `"Structural piece about the cost of litigation. No single human anchor; the argument is about the system, not a person."` (Process Is the Punishment, corrected)

### `created`

ISO date `YYYY-MM-DD`. The date the cover prompt was composed, not the article's publication date.

---

## Pre-save validation checklist

Run this checklist before writing the file. If any item fails, do not save — fix the issue and re-run.

1. **`title` matches the article title.** Not shortened, not paraphrased.
2. **`article` points at a specific version**, not a generic `*-final.md` symlink. The version trail matters for re-cover audits.
3. **`model` is set** (single value or pipe-separated list of compatible models). Not blank.
4. **`based_on` is set.** Either a library template id (Path A) or `flagship-dna` (Path B).
5. **`prompt_source` is set** to one of the three valid values — `ai-image-prompts-skill`, `nano-banana-pro-prompts-recommend-skill`, or `scratch`. Not blank.
6. **`compression` matches the picked concept brief exactly.** Copy from step 6's locked brief.
7. **`register`** is one of the permitted register families.
8. **`palette` names a specific contrast**, not generic ("warm tones," "high contrast" — too vague; "B&W subject + saturated green backdrop" — specific).
9. **All five `dna_checks` are `yes`.** If any is not, return to step 5.
10. **`face_decision` is explicitly `yes` or `no`** — never blank, never `tbd`.
11. **`face_subject` is `null` if `face_decision: no`**, named individual if `face_decision: yes`.
12. **`face_reasoning` is a complete sentence** — not "n/a", not blank. Even for non-face concepts, the reasoning explains *why* face-forward was rejected.
13. **`created` is today's date** in `YYYY-MM-DD` format.

If any of these fail, the artifact is not saveable — fix the issue and re-validate before writing.

---

## Reference: $71B Bluff frontmatter

The cleanest worked example, including all required fields for a face-forward Path-A composition:

```yaml
---
title: "Cover Prompt — The $71 Billion Bluff"
type: image-prompt
article: "drafts/the-71-billion-bluff-v10.md"
model: Flux | Nano Banana Pro | Midjourney
aspect_ratio: "16:9 (1456 × 816)"
based_on: "Neo-Noir Fashion Portrait with High Contrast (YouMind id: 8791)"
prompt_source: ai-image-prompts-skill
compression: "One signature, falling market"
register: "editorial poster / neo-noir"
palette: "B&W subject + saturated green backdrop"
dna_checks:
  compression: yes
  two_elements_or_fewer: yes
  no_embedded_text: yes
  cinematic_or_technical_register: yes
  contrast_carries_argument: yes
face_decision: yes
face_subject: "Sam Altman"
face_reasoning: "Named executive in the editorial piece's headline event; his face anchors the piece to the specific public-record decision being reported."
created: 2026-04-12
---
```

Note: the existing on-disk version at `workspace/drafts/the-71-billion-bluff-cover-prompt.md` predates this skill and has a shorter frontmatter (`title`, `type`, `article`, `model`, `aspect_ratio`, `based_on`, `created` only). New covers produced by this skill use the full schema above. The legacy file does not need to be retrofitted; it stays as a reference.
