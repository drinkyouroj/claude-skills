# CLAUDE.md Template

This is the template for the wiki schema file. When creating a new wiki, customize every section for the user's domain. Remove this header when writing the actual file.

---

```markdown
# {Wiki Name} — Schema & Agent Instructions

## Purpose
{One paragraph describing what this wiki is for, what knowledge it accumulates, and the user's goal.}

## Domain
{The subject matter. Be specific. E.g., "AI research with a focus on agentic systems, evals, and frontier labs" not just "AI".}

## Source Types
{List the kinds of sources this wiki ingests. E.g., research papers, blog posts, podcast transcripts, book chapters, personal notes.}

---

## Directory Structure

{wiki-root}/
├── CLAUDE.md              ← this file
├── index.md               ← content catalog (update on every ingest)
├── log.md                 ← append-only operation log
├── raw/                   ← immutable source files (user manages)
│   └── assets/            ← downloaded images
└── wiki/
    ├── overview.md        ← evolving synthesis / main thesis
    ├── entities/          ← people, orgs, products, projects
    ├── concepts/          ← ideas, frameworks, methods, terms
    ├── sources/           ← one page per ingested source
    └── analyses/          ← filed query outputs

---

## Frontmatter Spec

Every wiki page must include YAML frontmatter:

```yaml
---
title: "{Page Title}"
type: source | entity | concept | analysis | overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
sources: [source-slug-1, source-slug-2]   # for entity/concept pages
source_count: N                             # for entity/concept pages
---
```

---

## Page Format Conventions

### Source Pages (`wiki/sources/{slug}.md`)
- **Header**: Title, author, date, source type, URL or file path
- **Summary**: 300-500 word synthesis in the agent's own words
- **Key Claims**: Bulleted list of 5-10 specific claims or data points
- **Connections**: Inbound and outbound links to entity/concept pages
- **Contradictions**: Note any conflict with existing wiki content

### Entity Pages (`wiki/entities/{name}.md`)
- **Header**: Name, type (person/org/product/project), brief descriptor
- **Summary**: What this entity is and why it matters to the domain
- **Key Facts**: Bulleted list of notable attributes, claims, or data points
- **Sources**: All source pages that mention this entity (with brief context per source)
- **Related**: Links to related entities and concepts

### Concept Pages (`wiki/concepts/{term}.md`)
- **Header**: Term, brief one-line definition
- **Definition**: 100-200 word explanation in plain language
- **Key Properties**: What makes this concept important or distinct
- **Examples**: Concrete instances from the sources
- **Sources**: All source pages where this concept appears
- **Related**: Links to related concepts and entities

### Analysis Pages (`wiki/analyses/{slug}.md`)
- **Header**: Question asked, date, source pages consulted
- **Answer**: Full synthesis with citations to wiki pages
- **Caveats**: What the wiki can't yet answer; gaps to fill
- **Next Steps**: Suggested sources or follow-up questions

### Overview (`wiki/overview.md`)
- **Thesis**: The current working synthesis — what do we believe about this domain?
- **Key Findings**: Top 5-10 conclusions supported by the wiki
- **Open Questions**: What we don't know yet
- **Source Count**: How many sources have been ingested
- **Last Updated**: Date of last revision

---

## Ingest Workflow

When the user provides a source:

1. Read the source carefully
2. Ask the user if there's anything to emphasize, deprioritize, or flag
3. Write `wiki/sources/{slug}.md`
4. Update relevant entity pages in `wiki/entities/`
5. Update relevant concept pages in `wiki/concepts/`
6. Update `wiki/overview.md` if the thesis shifts
7. Update `index.md` — add new and updated pages
8. Append to `log.md`: `## [{date}] ingest | {Source Title}`

Typical ingest: 8-15 pages touched.

---

## Query Workflow

When the user asks a question:

1. Read `index.md` to identify relevant pages
2. Read those pages
3. Synthesize an answer with citations to wiki pages (not raw sources)
4. Offer to file the answer to `wiki/analyses/{slug}.md` if it's substantive
5. Append to `log.md`: `## [{date}] query | {brief question description}`

---

## Lint Checklist

Run periodically or on demand:

- [ ] Contradictions between pages
- [ ] Stale content superseded by newer sources
- [ ] Orphan pages (no inbound links)
- [ ] Missing pages (concepts/entities mentioned but not created)
- [ ] Missing cross-references between related pages
- [ ] Data gaps (questions the wiki can't answer)
- [ ] Suggested new sources to find

---

## Cross-Reference Rules

- Use `[[WikiLinks]]` for all internal links
- Every entity and concept mentioned in a page should be linked
- Source pages link out to entities and concepts
- Entity and concept pages link back to all source pages that reference them
- Never leave an entity or concept as plain text if a page exists for it

---

## Naming Conventions

- Source slugs: `{author-last-name}-{year}-{short-title}` or `{publication}-{year}-{short-title}`
- Entity slugs: `{name-kebab-case}` (e.g., `dario-amodei`, `anthropic`, `claude-3-5`)
- Concept slugs: `{term-kebab-case}` (e.g., `constitutional-ai`, `chain-of-thought`)
- Analysis slugs: `{YYYY-MM-DD}-{short-question}`

---

## Domain-Specific Notes

{Add any domain-specific conventions here. E.g., for AI research: always note the lab/institution behind a paper; for reading notes: always note chapter and page numbers; for self-improvement: always link personal observations to relevant concepts.}
```
