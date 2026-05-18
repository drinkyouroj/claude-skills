# Page Format Reference

Full format specifications for each wiki page type. These are the canonical templates — follow them exactly when writing wiki pages.

---

## Source Page

**Path**: `wiki/sources/{slug}.md`

```markdown
---
title: "{Full Article/Paper Title}"
type: source
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
author: "{Author Name(s)}"
published: {YYYY-MM-DD or YYYY}
source_type: article | paper | transcript | book-chapter | note | report
url: "{URL or file path}"
tags: [tag1, tag2, tag3]
---

# {Title}

**Author**: {Author} | **Published**: {Date} | **Source**: [{source_type}]({url})

---

## Summary

{300-500 word synthesis written entirely in the agent's own words. Cover the main argument, methodology (if applicable), evidence, and conclusions. Do not quote extensively — paraphrase and synthesize. This should read as a confident distillation, not a neutral abstract.}

---

## Key Claims

- {Specific, falsifiable claim or data point from the source}
- {Another claim}
- {Continue for 5-10 total}

---

## Connections

**Entities mentioned**: [[entity-1]], [[entity-2]]  
**Concepts referenced**: [[concept-1]], [[concept-2]]

---

## Contradictions / Tensions

{Note any claims that conflict with existing wiki pages, or where this source complicates the current thesis. If none, write "None identified." Do not leave this section blank.}

---

## Notes

{Any additional context: why this source was added, what question it was trying to answer, caveats about the source's credibility or bias.}
```

---

## Entity Page

**Path**: `wiki/entities/{slug}.md`

```markdown
---
title: "{Entity Name}"
type: entity
entity_type: person | organization | product | project | place
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
tags: [tag1, tag2]
sources: [source-slug-1, source-slug-2]
source_count: N
---

# {Entity Name}

**Type**: {entity_type} | **Domain relevance**: {one-line descriptor}

---

## Summary

{100-200 words describing what this entity is and why it matters to the wiki's domain.}

---

## Key Facts

- {Notable attribute, claim, or data point}
- {Another fact}
- {Continue for 5-8 total}

---

## In the Sources

| Source | Context |
|--------|---------|
| [[source-slug-1]] | {Brief note on how this entity appears in this source} |
| [[source-slug-2]] | {Brief note} |

---

## Related

**Entities**: [[related-entity-1]], [[related-entity-2]]  
**Concepts**: [[related-concept-1]]
```

---

## Concept Page

**Path**: `wiki/concepts/{slug}.md`

```markdown
---
title: "{Concept Term}"
type: concept
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
tags: [tag1, tag2]
sources: [source-slug-1, source-slug-2]
source_count: N
---

# {Concept Term}

> {One-sentence plain-language definition.}

---

## Definition

{100-200 words explaining the concept in plain language. Assume the reader is intelligent but not a specialist. Focus on what makes this concept useful or important in this domain.}

---

## Key Properties

- {What distinguishes this concept}
- {How it differs from related concepts}
- {When/where it applies}

---

## Examples from Sources

| Example | Source |
|---------|--------|
| {Concrete instance of this concept} | [[source-slug]] |
| {Another example} | [[source-slug]] |

---

## In the Sources

| Source | Context |
|--------|---------|
| [[source-slug-1]] | {How this concept appears} |

---

## Related

**Concepts**: [[related-concept-1]], [[related-concept-2]]  
**Entities**: [[related-entity-1]]
```

---

## Analysis Page

**Path**: `wiki/analyses/{slug}.md`

```markdown
---
title: "{Question or Analysis Title}"
type: analysis
created: {YYYY-MM-DD}
tags: [tag1, tag2]
sources_consulted: [source-slug-1, source-slug-2]
pages_consulted: [entity-slug, concept-slug]
---

# {Question}

**Asked**: {YYYY-MM-DD} | **Confidence**: high | medium | low

---

## Answer

{Full synthesis answering the question. Cite wiki pages inline using [[WikiLinks]]. This should be substantive — the reason it's being filed is that it's worth keeping.}

---

## Caveats

{What the wiki can't yet answer. Gaps in the evidence. Uncertainties.}

---

## Next Steps

- {Source to find that would fill a gap}
- {Follow-up question to investigate}
```
