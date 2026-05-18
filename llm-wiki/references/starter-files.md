# Starter Files

Exact content to write when initializing a new wiki. Customize the header and domain description.

---

## index.md (starter)

```markdown
# {Wiki Name} — Index

> Content catalog. Updated on every ingest. Read this first when answering queries.

**Stats**: {N} sources | {N} entity pages | {N} concept pages | {N} analyses

---

## Overview

| Page | Description |
|------|-------------|
| [[wiki/overview]] | Evolving synthesis and working thesis |

---

## Sources

| Slug | Title | Date Ingested | Tags |
|------|-------|---------------|------|
| *(empty — first source goes here)* | | | |

---

## Entities

| Slug | Type | Description |
|------|------|-------------|
| *(empty)* | | |

---

## Concepts

| Slug | Definition (one line) |
|------|-----------------------|
| *(empty)* | |

---

## Analyses

| Slug | Question | Date |
|------|----------|------|
| *(empty)* | | |
```

---

## log.md (starter)

```markdown
# {Wiki Name} — Operation Log

> Append-only. One entry per ingest, query, or lint pass.
> Format: `## [{YYYY-MM-DD}] {operation} | {description}`
> Tip: `grep "^## \[" log.md | tail -10` gives the last 10 entries.

---

## [{YYYY-MM-DD}] setup | Wiki initialized

- Domain: {domain}
- Source types: {source types}
- Structure created: CLAUDE.md, index.md, log.md, raw/, wiki/
```

---

## wiki/overview.md (starter)

```markdown
---
title: "Overview"
type: overview
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
tags: []
---

# {Wiki Name} — Overview

> Evolving synthesis. Updated as sources are ingested and the thesis develops.

**Sources ingested**: 0  
**Last updated**: {YYYY-MM-DD}

---

## Working Thesis

*(No sources ingested yet. Thesis will develop here.)*

---

## Key Findings

*(None yet.)*

---

## Open Questions

*(Add questions you want the wiki to eventually answer.)*
```
