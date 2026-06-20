---
name: project-md-generator
description: >
  Generates a committed, repo-root project instructions file — AGENTS.md or CLAUDE.md —
  for programming and Claude Code/Cowork projects. Defaults to AGENTS.md for greenfield
  repos (the portable, cross-agent convention) and otherwise updates whichever file the
  repo already has. Use this skill whenever a user asks to create or update an AGENTS.md
  or CLAUDE.md, set up Claude Code conventions for a project, scaffold a new project's
  agent instructions, or wants to establish git flow, adversarial agent protocol, docker
  config, testing conventions, or documentation standards for a codebase. Trigger even if
  the user says something loose like "set up my AGENTS.md", "make a CLAUDE.md", "get
  Claude Code ready for this project", "add your instructions to the repo", or "configure
  Claude for this project". Always use this skill rather than freehand-writing an AGENTS.md
  or CLAUDE.md.
---

# Project Instructions File Generator (AGENTS.md / CLAUDE.md)

Generates a complete, committed project instructions file — `AGENTS.md` or `CLAUDE.md` —
for a programming project. The output is a permanent repo artifact, not a session prompt,
so it should be durable, precise, and project-specific.

Both filenames carry the same content and the same section structure; only the name and a
couple of self-references differ. **Step 1.5 decides which to write.** The short version:
default to `AGENTS.md` for a greenfield repo, and otherwise update whichever file the
project already has.

---

## Step 1: Gather Project Context

**Infer first, then confirm gaps.**

From the current conversation, open files, and any uploaded material, try to extract:

| Field | What to look for |
|---|---|
| `project_name` | Repo name, app name, mentions in conversation |
| `purpose` | One-sentence description of what this builds |
| `tech_stack` | Languages, frameworks, databases, infra tools mentioned |
| `test_framework` | pytest, vitest, jest, etc. — any test tooling mentioned |
| `docker_used` | Any docker-compose, Dockerfile, container references |
| `port_assignments` | Any ports already in use or mentioned |
| `modules_to_skip` | Anything the user has explicitly opted out of |

### Step 1.5: Choose the target filename (AGENTS.md vs CLAUDE.md)

This skill writes **one** instructions file. Decide its name before generating — the
content is identical either way, so this is only about which filename the repo should carry:

- **`AGENTS.md`** — the cross-agent open convention ([agents.md](https://agents.md)). One
  file that any coding agent reads, Claude Code included. Because it's portable, it's the
  greenfield default.
- **`CLAUDE.md`** — Claude Code's original, Claude-specific name. Still fully supported.

Apply the first rule that matches:

1. **The user named one** ("set up my AGENTS.md", "write a CLAUDE.md") → use exactly that.
2. **A file already exists at the repo root** → update that one; don't create a competing
   second file. If *both* exist, treat `AGENTS.md` as the source of truth and ask what the
   `CLAUDE.md` should become (usually deleted, or reduced to a one-line pointer at AGENTS.md).
3. **Greenfield** — neither exists and the user didn't say → default to **`AGENTS.md`**.
   Claude Code reads it too, so nothing is lost by choosing the portable name, and any other
   agent the project later adopts gets the same guidance for free.

Carry the result as `{{instructions_filename}}` and use it everywhere below.

Present a short **Context Confirmation Block** to the user before generating:

```
Here's what I've gathered — confirm or correct before I generate:

- Target file: <AGENTS.md (default) or CLAUDE.md>
- Profile: <Lean (default) or Full — sets which heavyweight process modules are on>
- Project: <name>
- Purpose: <one-liner>
- Stack: <tech list>
- Tests: <framework or "not specified">
- Docker: <yes/no/unknown>
- Skipping modules: <none or list>

Good to go?
```

Only proceed once the user confirms (or corrects and confirms).

---

## Step 2: Select Active Modules

Start from a **project profile**, then adjust. The profile decides whether the heavyweight
process modules are on — they earn their keep on a multi-agent product build but are pure
friction on a small static site or a solo script, so don't impose them by reflex.

- **Lean** (default) — small / solo / static / marketing / early-stage repos. Core modules
  only: `tech_stack_env`, `git_flow`, `testing`, `documentation`, and `project_specific_notes`
  (plus `docker` when the project actually uses it).
- **Full** — multi-agent builds, or any service touching data, auth, payments, or async jobs.
  Lean **plus** the process apparatus: `adversarial_agent_protocol`, `build_log` +
  `DECISION docs`, and `architecture.md`.

Infer the profile from the project — a static marketing site is Lean; a backend with a
database and auth is Full — and confirm it in the Context Confirmation Block. Whatever the
profile, any individual module can be toggled on or off on request.

| Module Key | Default | On when | Off / skip when |
|---|---|---|---|
| `tech_stack_env` | ✅ | always | no stack info after the context step |
| `git_flow` | ✅ | always | user says "no git flow" / "simple commits only" |
| `testing` | ✅ | a test framework exists or is wanted | no tests in the project |
| `documentation` | ✅ | always (scaled to profile — see the module) | user says "no doc conventions" |
| `project_specific_notes` | ✅ | always | genuinely nothing non-obvious to record |
| `docker` | ➖ | the project uses Docker | no Docker in project |
| `adversarial_agent_protocol` | Full only | Full profile, or the user asks for it | Lean profile / "solo/fast project" |
| `build_log` + `DECISION docs` | Full only | Full profile, or the user asks for it | Lean profile |
| `architecture.md` | Full only | Full profile, or non-trivial system topology | Lean profile / single-component repo |

---

## Step 3: Generate the instructions file

Assemble the file in this section order, including only the modules the profile and context
turned on (Step 2). Each section heading is shown below with its full canonical content;
substitute `{{placeholders}}` with project-specific values, and delete any `{{…}}` row or
line you have no real value for rather than shipping an empty placeholder.

---

### File Header

```markdown
# {{instructions_filename}} — {{project_name}}

> This file is the authoritative guide for Claude Code and any AI agent working in this
> repository. Read it fully before taking any action. It is committed to the repo root
> and applies to every session.

**Project:** {{project_name}}
**Purpose:** {{purpose}}
**Live:** {{production URL / host + which branch ships there — e.g. "Cloudflare Pages; production tracks `main`". Omit for a library or a not-yet-deployed repo.}}
**Preview:** {{staging / review environment, if any — e.g. "the `preview` branch is the client-review deploy". Omit if there's no staging step.}}
**Last updated:** {{YYYY-MM-DD}}
```

---

### MODULE: tech_stack_env

```markdown
## Environment & Stack

**Language(s):** {{languages}}
**Framework(s):** {{frameworks}}
**Database(s):** {{databases}}
**Key dependencies:** {{notable libs}}
**Runtime:** {{e.g. Python 3.12, Node 20}}

### Setup

```bash
# Install dependencies
{{install command — e.g. pip install -r requirements.txt or npm install}}

# Run locally
{{run command}}

# Run tests
{{test command}}
```

> Always verify the environment is set up before suggesting code changes.
> Never assume a dependency is installed.
```

---

### MODULE: docker

```markdown
## Docker

### Safety Block

**Never run `docker system prune`, `docker volume prune`, or any destructive Docker
command without explicit user confirmation in the chat.** These are irreversible.

### Port Assignments

| Service | Port |
|---|---|
{{| service_name | port |}} ← populate from project context, or leave template row

> Before adding a new service, check this table. Never assign a port already in use.
> Add new assignments to this table as part of the PR that introduces the service.

### Compose

```bash
# Start all services
docker compose up -d

# Rebuild after dependency changes
docker compose up -d --build

# Tear down (data volumes preserved)
docker compose down
```
```

---

### MODULE: testing

```markdown
## Testing Conventions

**Framework:** {{test_framework}}

### Rules

- Every new function or endpoint gets a test in the same PR that introduces it.
- Tests live in `tests/` mirroring the source structure.
- Test names follow `test_<what>_<condition>_<expected>` — e.g. `test_parse_empty_input_returns_none`.
- No PR merges to `develop` with failing tests.
- Prefer narrow unit tests over broad integration tests unless the integration is the thing under test.

### Running Tests

```bash
# All tests
{{test command}}

# Specific file
{{test command}} tests/path/to/test_file.py

# With coverage
{{test command with coverage flag}}
```

### Eval Harness (if applicable)

If this project includes a Claude prompt eval harness, it lives in `evals/`.
Run it with `{{eval command}}` before any prompt change is merged.
```

Then add a Verification section. Fill the table with the project's real commands; the
rightmost column matters because some checks need a fresh build first. The limits note is
what stops a green check from being mistaken for "done" — keep it honest and specific.

```markdown
## Verification

How to *prove* a change is good, and which layer to run for which change.

| Command | Checks | Build first? |
|---|---|---|
| {{unit test command}} | {{fast logic checks}} | no |
| {{build / integration test}} | {{build-output or integration checks}} | yes |
| {{a11y / lint / type command}} | {{accessibility, lint, types}} | {{yes/no}} |
| {{full gate command}} | {{builds once, runs everything; the pre-merge / pre-release gate}} | — |

### What the automated checks *don't* catch

Automated gates are necessary, not sufficient. Spell out where human judgment is still
required so nobody reads a green check as "done":

- Name the coverage gaps (e.g. *"axe catches ~30–50% of WCAG — the mechanical failures only; text over a photo still needs an eye"*).
- For browser-observable changes (layout, copy, components), verify against the running app and **show proof** — screenshot the affected area, watch the console. Don't ask the user to eyeball it; demonstrate it.
- Flag which checks are *advisory* vs *hard-gated*, and call out any deliberate non-perfect score so a later agent doesn't "fix" an intentional setting.
```

---

### MODULE: git_flow

Read the full canonical content from `references/git_flow.md`.

---

### MODULE: adversarial_agent_protocol

**Full profile only** (or when the user explicitly asks for it). Skip on Lean projects — a
three-agent review per decision is friction a small site doesn't need.

Read the full canonical content from `references/adversarial_agent_protocol.md`.

---

### MODULE: documentation

Lead with the **sources of truth** — the short list of docs an agent reads before touching
what they govern — then the conventions for keeping them current. The `build_log.md` and
DECISION-doc apparatus is **Full-profile only**: on a Lean project, keep the sources-of-truth
list and `CHANGELOG.md`, and drop the rest.

```markdown
## Documentation & Design — sources of truth

The canonical docs for this project. Read the relevant one before changing what it governs,
and keep it current in the same PR that changes the underlying reality.

- **`README.md`** — public-facing overview: purpose, prerequisites, local setup, how to run
  tests, and a pointer to this guide. Update it in the same PR when setup steps change.
- **`CHANGELOG.md`** — [Keep a Changelog](https://keepachangelog.com/) format. Add
  user-facing changes under `## [Unreleased]` as you go; the release process promotes that
  block to a versioned, dated section. Never edit it retroactively.
- **`PRODUCT.md`** *(if present)* — who the project serves, brand/personality, design
  principles, anti-references. Read before changing copy or UX.
- **`DESIGN.md`** *(if present)* — the shipped design system: tokens, type, spacing, named
  rules. Keep in sync when the visual system changes.
- **`docs/architecture.md`** *(Full profile)* — living description of system topology and
  data flow; update it when a PR meaningfully changes either. A rough ASCII/Mermaid diagram helps.

> Add or drop rows to match the project. The value is that an agent finds, in one place,
> which document is authoritative for each kind of change.
```

A fresh `CHANGELOG.md` starts like:

```markdown
## [Unreleased]

## [{{version}}] — {{YYYY-MM-DD}}
### Added
### Changed
### Fixed
### Removed
```

#### Full-profile additions (skip these on a Lean project)

```markdown
### build_log.md

`build_log.md` lives at the repo root. It is append-only. Every session that makes
meaningful changes adds an entry:

```
## {{YYYY-MM-DD}} — {{short description}}

### Done
- <bullet per logical change>

### Decisions
- <any DECISION docs created or referenced>

### Next
- <what's left or blocked>
```

### DECISION Docs

Before implementing any of the following, a DECISION doc is required:
- New API endpoints
- Database schema changes
- Claude prompt changes
- Auth or payment flows
- Async job designs

DECISION docs live in `docs/decisions/` and follow this template:

```markdown
# DECISION: {{title}}

**Date:** {{YYYY-MM-DD}}
**Status:** Proposed | Accepted | Rejected | Superseded

## Context
What problem are we solving? Why now?

## Options Considered
1. **Option A** — pros / cons
2. **Option B** — pros / cons

## Decision
What we're doing and why.

## Consequences
What changes, what gets harder, what gets easier.
```
```

---

### MODULE: project_specific_notes

The non-obvious things that bite an agent who only read the code top to bottom — the
landmines, the single source of truth for each tricky behavior, the "looks wrong but is
intentional" details. Keep each note concrete and point it at the file that owns the behavior.

```markdown
## Project-specific notes

- **<Gotcha or invariant>** — <what's surprising, where it lives, why it's that way.>
- **<The one true path for X>** — <e.g. "the phone call is the only conversion — keep a
  tap-to-call within reach from every fold; nothing competes with it.">
- **<Data / asset quirk>** — <e.g. source masters live in a gitignored dir; only derivatives ship.>
- **<Time / locale / environment assumption>** — <e.g. business hours run on the office's
  timezone, derived in one module, not the visitor's.>
```

> If a note here is really a decision with alternatives considered, promote it to a DECISION
> doc (Full profile) and link it from this list instead of duplicating the reasoning.

---

## Step 4: Write the File

Output the assembled file as `{{instructions_filename}}` at the repo root (or current
working directory if the user hasn't specified). Use `create_file` targeting
`./{{instructions_filename}}`.

After writing, tell the user:
- The file path
- Which modules were included (and any that were skipped and why)
- Suggested next step: `git add {{instructions_filename}} && git commit -m "chore: add {{instructions_filename}}"`

---

## Step 5: Offer Companion Files

After delivering the `{{instructions_filename}}`, offer to scaffold the doc files it
references if they don't already exist. Offer only what the chosen profile actually uses:

- `README.md` — stub if one doesn't exist *(any profile)*
- `CHANGELOG.md` — with an `[Unreleased]` section *(any profile)*
- `build_log.md` — with a dated initial entry *(Full profile)*
- `docs/decisions/` — empty directory with a `.gitkeep` *(Full profile)*
- `docs/architecture.md` — stub with project name and placeholder sections *(Full profile)*

Ask: "Want me to scaffold the companion docs too? I can create them all in one shot."

### If you wrote AGENTS.md and the user also runs Claude Code

`AGENTS.md` is enough on its own — Claude Code reads it. Only if the user specifically
wants a Claude-named entry point on top of it, offer (don't add by default — a second copy
is a second thing to keep in sync):

- a **one-line `CLAUDE.md`** that points at it (`See [AGENTS.md](./AGENTS.md).`), or
- a **`CLAUDE.md` symlink** to `AGENTS.md`, where the toolchain and `.gitignore` allow it.

Some repos deliberately keep **no** committed `CLAUDE.md` — e.g. a `.gitignore` rule that
ignores `CLAUDE.md` in every directory so per-directory mem notes never leak into a build
output. Respect a rule like that: if `CLAUDE.md` is gitignored, don't add one — keep
`AGENTS.md` as the single committed source of truth.

---

## Reference Files

- `references/git_flow.md` — Full Git Flow + commit granularity conventions (MODULE: git_flow)
- `references/adversarial_agent_protocol.md` — Full AAP spec (MODULE: adversarial_agent_protocol)
