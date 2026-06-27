## `technical` preset

> STATUS: documented stub — not built in first release

Intended for engineering blogs, developer tutorials, technical deep-dives, and how-to guides that assume a practitioner audience. Accuracy and reproducibility take precedence over broad accessibility.

---

### Steps that differ from `general`

| Step | Change from `general` |
|---|---|
| `outline` | Structure selection includes tutorial (problem → setup → walkthrough → outcome), reference-doc, and architecture-explainer templates in addition to standard angle/hook + structure selection |
| `headline` | Headline audit checks that the title communicates the concrete task or concept, not just the topic area |
| `opener` | Opens with the problem being solved or the capability being demonstrated; reader-persona pre-assessment focuses on assumed prerequisite knowledge |
| `readability` | Density/comprehension audit permits high information density; flags undefined acronyms and missing prerequisite links rather than simplifying prose |
| `humanizer` | Constrained: preserve technical precision; do not introduce ambiguity in the name of voice |
| `fact-check` | Code samples, version numbers, command syntax, and API signatures verified against documentation |
| `fact-reconcile` | Outdated commands or deprecated APIs flagged with recommended replacements |

All other steps inherit `general` defaults.

---

### Framing vocabulary additions

| Concept | Term used in this preset |
|---|---|
| Angle/hook + structure selection | **problem framing + tutorial/reference structure selection** |
| Reader-persona pre-assessment | **prerequisite and audience-level check** |
| Density/comprehension audit | **precision and prerequisite-gap audit** |
