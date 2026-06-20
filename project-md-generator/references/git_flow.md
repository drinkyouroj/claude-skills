# Git Flow & Commit Conventions

## Branch Model

| Branch | Role |
|---|---|
| `main` | Production-ready releases only. Protected — no direct commits, PRs only. Tag every merge. |
| `develop` | Integration branch and default working branch. Features land here first. Protected. |
| `feature/*` | One branch per feature or fix, cut from `develop` and merged back via PR. |
| `release/*` | Cut from `develop` when ready to ship. Merged to `main` **and** back to `develop`. |
| `hotfix/*` | Cut from `main` for an urgent fix. Merged to both `main` and `develop`. |
| `preview` *(optional)* | Long-lived client-review / staging branch with its own deploy, sitting between `develop` and production. Add this for client work or anything that needs a stable review environment; drop the row if there's no staging step. |

### Rules

- `main` and `develop` are **protected**. No direct commits. PRs only.
- Branch names: `feature/short-description`, `fix/short-description`, `chore/short-description`.
- If you find yourself on `main`, switch to `develop` before making changes.
- Delete feature branches after merge; never delete a long-lived branch (`develop`, `preview`).
- Every merge to `main` gets a version tag: `v{{MAJOR}}.{{MINOR}}.{{PATCH}}`.

---

## Semantic Versioning

Follow [semver](https://semver.org/):

| Change type | Version bump |
|---|---|
| Breaking change / incompatible API | MAJOR |
| New feature, backward-compatible | MINOR |
| Bug fix, backward-compatible | PATCH |

Pre-release: `v1.2.0-alpha.1`, `v1.2.0-beta.1`, `v1.2.0-rc.1`

### Keep the version consistent everywhere

A release's version usually lives in more than one file, and the copies drift silently the
moment one is bumped by hand. List every place it appears for *this* project and keep them in
lockstep each release. A typical set:

> **The version lives in N places — keep them consistent every release:**
> 1. the package manifest (`package.json` / `pyproject.toml` / `Cargo.toml` …)
> 2. the lockfile, if it self-references the version
> 3. the `CHANGELOG.md` heading for the release
> 4. the annotated git tag `vX.Y.Z` (use `-a`; a lightweight tag is skipped by `--follow-tags`)
> 5. the GitHub Release, if you publish them
>
> Prefer one command that bumps as many as possible at once (`npm version`, `bump-my-version`,
> `hatch version` …) over hand-editing — hand-editing is where the drift starts.

---

## Commit Message Format

Follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body — wrap at 72 chars]

[optional footer — BREAKING CHANGE, closes #issue]
```

**Types:**

| Type | Use for |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `chore` | Maintenance, tooling, deps |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `refactor` | Code change with no behavior change |
| `perf` | Performance improvement |
| `ci` | CI/CD config changes |

**Examples:**

```
feat(api): add POST /manuscripts endpoint

fix(parser): handle empty chapter titles without crashing

chore(deps): upgrade fastapi to 0.115

docs(decisions): add DECISION doc for async job architecture

test(manuscripts): add coverage for empty input edge case
```

---

## Commit Granularity

**Commit per logical change — not per file, not per hour, not per task.**

A logical change is the smallest unit of work that leaves the codebase in a valid state.

### Correct granularity examples

- One commit to add a migration, a separate commit to add the model, a separate commit
  to add the repository layer.
- One commit for the DECISION doc, a separate commit for the prompt file it describes,
  a separate commit for the eval test.

### Anti-patterns

- ❌ Batching unrelated changes into one commit ("misc fixes")
- ❌ Splitting a single logical change across multiple commits to pad history
- ❌ "WIP" commits on shared branches
- ❌ Committing commented-out code

---

## Attribution & When to Commit

- **No attribution trailers.** Don't append `Co-Authored-By`, "Generated with …", or any
  tool-attribution footer to commits. A commit message is its subject, an optional body, and
  any Conventional-Commit footer (`BREAKING CHANGE:`, `closes #123`) — nothing more. Match
  existing history.
- **Commit and push only when the user asks.** Do the work and leave it for the user to land;
  don't commit or push on your own initiative unless they've said so for the session. Pushing
  is outward-facing and hard to walk back.

---

## Pull Requests

- PR title = Conventional Commit format: `feat(scope): description`
- PR description must include: what changed, why, and how to test it.
- Link any related DECISION doc.
- Merge feature branches into `develop` with `--no-ff` (no squash) so release history and
  tagged commits stay intact.
- Merge release and hotfix branches into `main` with `--no-ff` as well.
