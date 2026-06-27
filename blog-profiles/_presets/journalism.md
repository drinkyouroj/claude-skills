## `journalism` preset

> STATUS: documented stub — not built in first release

Intended for news-style and investigative blogs: breaking coverage, in-depth features, and reported opinion pieces that prioritize timeliness, attribution, and editorial standards.

---

### Steps that differ from `general`

| Step | Change from `general` |
|---|---|
| `outline` | Structure selection draws from inverted-pyramid, nut-graf, and narrative-feature templates before angle/hook selection |
| `headline` | Headline audit adds news-style conventions: active voice, avoidance of question headlines, verb-forward construction |
| `fact-check` | Elevated priority — source attribution and quotation accuracy checked before any other readability pass |
| `fact-reconcile` | Claims without traceable primary or named secondary sources are flagged for removal, not just softened |
| `readability` | Density/comprehension audit also checks reading level against a general-public baseline (≤ grade 10) |
| `humanizer` | Constrained: do not sand off the direct, declarative register characteristic of reported journalism |

All other steps inherit `general` defaults.

---

### Framing vocabulary additions

| Concept | Term used in this preset |
|---|---|
| Angle/hook selection | **news angle + story framing** |
| Reader-persona pre-assessment | **audience and platform context check** |
| Density/comprehension audit | **readability and attribution pass** |
