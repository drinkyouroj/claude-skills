# tcn-reddit-campaign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `tcn-reddit-campaign` skill — a standing-aware Reddit promotion manager that turns a published TCN article into a vetted, per-subreddit posting plan with paste-ready drafts, backed by a persistent dossier + ledger.

**Architecture:** A single mode-based skill (3 modes) in `/Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/`, composed of a `SKILL.md` spine plus four reference files (voice register, self-promo playbook, dossier schema, eligibility rules). Persistent campaign *data* lives in the substack workspace at `workspace/reddit-campaign/` (dossiers + ledger), consistent with the ecosystem's logic/data split. The skill is read-only on the user's Reddit account: Claude-for-Chrome is a sensor for live rules + karma, never a submit button.

**Tech Stack:** Markdown skill files (no executable code). Runtime tools the skill invokes: Claude-for-Chrome (`mcp__Claude_in_Chrome__*`) for ground-truth reads, WebSearch for discovery, and the workspace filesystem for state. No build system, no package manager, no unit-test framework — verification is content/consistency checks plus a final end-to-end smoke test, matching this repo's "smoke-test verified" commit convention.

**Note on "tests":** This skill is a prose/prompt artifact, not code. Each task's verification step is a concrete content check (frontmatter validity, `grep` for required elements, read-through against named criteria) with an expected result — adapted from TDD's "define the check, then satisfy it" discipline. The final task is a true end-to-end smoke test against the spec's acceptance criteria.

**Spec:** `docs/superpowers/specs/2026-06-05-tcn-reddit-campaign-design.md`

**A note on the two "user-authored logic" blocks (spec §11, §12):** Per the user's "act independently" preference, these ship as **complete working defaults** that don't block execution, each clearly flagged as the designated tuning point for the user's risk posture / editorial judgment. The user tunes the constants later; the skill is fully functional out of the box. This satisfies spec acceptance criterion 7 (logic lives in editable reference files, not hard-coded).

---

## File Structure

| File | Responsibility |
|---|---|
| `tcn-reddit-campaign/SKILL.md` | Spine: frontmatter/triggering, hard constraints, 3 modes + routing, Mode-1 workflow, output contract, state bootstrap, sensor policy, ownership/related-skills, reference index |
| `tcn-reddit-campaign/references/dossier-template.md` | Per-subreddit dossier schema (the data model) |
| `tcn-reddit-campaign/references/eligibility-rules.md` | **User-tunable logic #1:** Ready/Locked/Risky/No-go decision + cooldown/freshness defaults + verdict→action routing |
| `tcn-reddit-campaign/references/self-promo-playbook.md` | **User-tunable logic #2:** self-promo-policy→framing-archetype map; 9:1 culture; link-in-comment tactics; honest-authorship rules |
| `tcn-reddit-campaign/references/reddit-voice.md` | Reddit-native voice register, anchored to `anti-ai-writing-style.md` |
| `tcn-reddit-campaign/CLAUDE.md` | Minimal stub (claude-mem manages session history here); cross-skill relationships live in SKILL.md, not here |
| *(runtime, not created at build)* `…/workspace/reddit-campaign/{dossiers/,ledger.md,targets.md}` | Persistent campaign state, lazily created by the skill on first run |

Build order is dependency-first: the data schema and the two logic files (which `SKILL.md` references) come before the spine; the smoke test comes last.

---

## Task 1: Dossier template (data schema)

**Files:**
- Create: `tcn-reddit-campaign/references/dossier-template.md`

- [ ] **Step 1: Create the skill + references directories**

```bash
mkdir -p "/Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/references"
```

- [ ] **Step 2: Write the dossier template file**

Create `tcn-reddit-campaign/references/dossier-template.md` with exactly this content:

````markdown
# Dossier Template — one file per subreddit

A dossier is the cached, ground-truthed record for a single subreddit. The skill writes one
per sub at `…/workspace/reddit-campaign/dossiers/r-<sub>.md` and reuses it across articles.
Refresh a dossier (re-read the live rules via Chrome) when `last_refreshed` is older than the
freshness window in `eligibility-rules.md` (default 30 days).

## Schema

```
---
sub: r/<name>
last_refreshed: YYYY-MM-DD
self_promo_policy: strict | promo-friendly | discussion-heavy | promo-thread | banned | unknown
karma_gate: <number or unknown>          # karma minimum to post (note type below)
karma_gate_type: comment | post | combined | unknown
age_gate_days: <number or unknown>       # account-age minimum to post
flair_required: yes | no | <which flairs exist>
link_policy: link-post | text+comment | either
best_time_notes: <freeform — when this sub is active, mod-removal patterns, etc.>
---

## Rules summary
- <bulleted, live rules that bear on self-promo, links, flair, formatting, AI content>

## My history here
| date | article slug | framing | url | outcome |
|------|--------------|---------|-----|---------|
```

## Field notes
- `self_promo_policy` is the routing key into `self-promo-playbook.md`. When unsure, record `unknown`
  (the eligibility logic treats `unknown` conservatively).
- `karma_gate` + `karma_gate_type`: many subs gate on *comment* karma specifically. Record the type so
  the eligibility check compares against the right number.
- `outcome` in the history table is optional and filled in later (upvotes / removed? / comment count);
  it is never required to complete a session.
````

- [ ] **Step 3: Verify the schema is complete**

Run:
```bash
F="/Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/references/dossier-template.md"
grep -cE "self_promo_policy|karma_gate|age_gate_days|flair_required|link_policy|last_refreshed" "$F"
```
Expected: `6` (one match per required field name).

- [ ] **Step 4: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-reddit-campaign/references/dossier-template.md
git commit -m "feat(tcn-reddit-campaign): add per-subreddit dossier schema

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: Eligibility rules (user-tunable logic #1)

**Files:**
- Create: `tcn-reddit-campaign/references/eligibility-rules.md`

- [ ] **Step 1: Write the eligibility rules file**

Create `tcn-reddit-campaign/references/eligibility-rules.md` with exactly this content:

````markdown
# Eligibility Rules — verdict logic + campaign defaults

> **▶ TUNE ME.** This file encodes the user's personal shadowban-risk posture. The constants and the
> decision order below are sensible defaults; the user adjusts them. Be more conservative by raising
> `KARMA_SAFETY_MARGIN` / `MIN_COMFORT_KARMA`; more aggressive by lowering them.

## Inputs
- From the dossier: `self_promo_policy`, `karma_gate`, `karma_gate_type`, `age_gate_days`, `flair_required`.
- From the logged-in Chrome profile read (once per session): `comment_karma`, `post_karma`,
  `account_age_days`.
- From the ledger: `last_posted_to_sub_days_ago` (or `never`), `posts_today`.

Define `relevant_karma` = the karma matching the sub's `karma_gate_type`
(`comment`→comment_karma, `post`→post_karma, `combined`→comment+post, `unknown`→the *smaller* of the two,
i.e. read it conservatively).

## Defaults (tunable constants)
```
COOLDOWN_DAYS       = 14     # min days before re-posting to the same sub
MAX_SUBS_PER_DAY    = 4      # max subs to post one article to in a day (bursts read as spam)
FRESHNESS_DAYS      = 30     # re-verify a dossier's rules if older than this
KARMA_SAFETY_MARGIN = 1.5    # want 1.5x the gate before "Ready" — avoids borderline auto-removal
MIN_COMFORT_KARMA   = 50     # below this total karma, link-posts in unknown-gate strict subs are Risky
```

## Decision (first match wins → verdict)
```
1.  self_promo_policy == banned                                   → No-go      ("self-promo prohibited")
2.  posts_today >= MAX_SUBS_PER_DAY                               → Risky      ("daily burst cap reached — defer to tomorrow")
3.  last_posted_to_sub_days_ago < COOLDOWN_DAYS                   → No-go      ("on cooldown, N days left")
4.  age_gate_days known AND account_age_days < age_gate_days      → Locked     ("account too young: need X days")
5.  karma_gate known AND relevant_karma < karma_gate             → Locked     ("need X karma, have Y")
6.  karma_gate known AND relevant_karma < karma_gate*MARGIN      → Risky      ("just over the gate — borderline")
7.  karma_gate unknown AND total_karma < MIN_COMFORT_KARMA
       AND self_promo_policy in {strict, unknown}                → Risky      ("unknown gate, thin karma, strict sub")
8.  flair_required AND no fitting flair identified                → Risky      ("flair required — confirm a fitting flair exists")
9.  otherwise                                                     → Ready
```

## Verdict → action routing
- **Ready**  → framing selector + drafting engine (full paste-ready bundle).
- **Risky**  → draft *only* the most conservative archetype (value-first text, link-in-comment),
              prefixed with an explicit caution naming the risk; the user decides whether to use it.
              Never auto-promote Risky → Ready.
- **Locked** → karma-warming planner (no promo draft yet).
- **No-go**  → list with the exclusion reason; no draft.

## Cooldown / cadence enforcement
- Before drafting, read the ledger: compute `posts_today` (rows dated today) and
  `last_posted_to_sub_days_ago` per candidate. Apply rules 2–3 above.
- After the user confirms a submission and pastes the URL, append a ledger row with
  `cooldown_until = post_date + COOLDOWN_DAYS`.
````

- [ ] **Step 2: Verify all four verdicts and the defaults are present**

Run:
```bash
F="/Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/references/eligibility-rules.md"
for tok in "No-go" "Risky" "Locked" "Ready" "COOLDOWN_DAYS" "MAX_SUBS_PER_DAY" "FRESHNESS_DAYS" "Verdict → action"; do
  grep -q "$tok" "$F" && echo "OK  $tok" || echo "MISSING  $tok"
done
```
Expected: eight `OK` lines, zero `MISSING`.

- [ ] **Step 3: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-reddit-campaign/references/eligibility-rules.md
git commit -m "feat(tcn-reddit-campaign): add eligibility verdict logic + cadence defaults

Tunable working defaults for Ready/Locked/Risky/No-go decisions; flagged
as the user's risk-posture tuning point.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: Self-promo playbook (user-tunable logic #2)

**Files:**
- Create: `tcn-reddit-campaign/references/self-promo-playbook.md`

- [ ] **Step 1: Write the self-promo playbook file**

Create `tcn-reddit-campaign/references/self-promo-playbook.md` with exactly this content:

````markdown
# Self-Promo Playbook — framing map + Reddit culture rules

## Hard rules (non-negotiable — repeated from SKILL.md)
- **Honest authorship only.** First-person, truthful attribution. Never pose as a third party who
  "found" the piece. Never astroturf.
- **No manipulation.** No vote brigading, no sockpuppets, no ban evasion, no posting where a sub
  bans self-promotion outright.
- **Member first.** Reddit's norm is roughly the 9:1 / 10% rule — your own links should be a small
  fraction of your activity in a community. A link from an account with no history in the sub reads
  as spam and is often auto-removed.

## Framing archetypes
- **transparent-author** — open "I wrote a piece on X" framing, link as the post itself.
- **thread-targeted** — post into the sub's recurring self-promo / share thread, transparently.
- **question-led** — lead with the article's sharpest finding as a genuine discussion prompt; put the
  link in your own first comment, framed as "I went deeper on this here."
- **value-first** — a self-contained, genuinely useful text post that stands alone even if nobody
  clicks; link in a first comment as a footnote, not the headline.

## ▶ TUNE ME — policy → archetype map
> This map encodes how aggressive the user is willing to be per rule signal. These are working
> defaults; the user adjusts the right-hand column.

```
self_promo_policy   →  archetype          link placement
-----------------------------------------------------------------
promo-friendly      →  transparent-author  link as post
promo-thread        →  thread-targeted     link in the self-promo thread
discussion-heavy    →  question-led        link in first comment
strict              →  value-first         link in first comment
unknown             →  value-first         link in first comment   (treat as strict until confirmed)
banned              →  (no draft)          —                       (No-go; see eligibility-rules.md)
```

## Link-in-comment tactic (why it exists)
Many subs auto-filter link-posts from low-history accounts but allow text posts. Leading with a text
post that delivers value, then dropping the Substack link in your own first comment, both respects the
community and survives spam filters. For `question-led` and `value-first`, always draft that first
comment as part of the bundle.

## What the skill must show the user
For each Ready/Risky sub, state which archetype was selected **and the rule signal that selected it**
(e.g. "strict no-self-promo rule → value-first, link-in-comment"). The user approves before posting.
````

- [ ] **Step 2: Verify every policy value maps to an archetype and the hard rules are present**

Run:
```bash
F="/Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/references/self-promo-playbook.md"
for tok in "promo-friendly" "promo-thread" "discussion-heavy" "strict" "unknown" "banned" \
           "transparent-author" "thread-targeted" "question-led" "value-first" \
           "Honest authorship" "No manipulation"; do
  grep -q "$tok" "$F" && echo "OK  $tok" || echo "MISSING  $tok"
done
```
Expected: twelve `OK` lines, zero `MISSING`.

- [ ] **Step 3: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-reddit-campaign/references/self-promo-playbook.md
git commit -m "feat(tcn-reddit-campaign): add self-promo framing map + culture rules

Policy->archetype map (tunable), honest-authorship hard rules, 9:1 culture,
link-in-comment tactic.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: Reddit voice register

**Files:**
- Create: `tcn-reddit-campaign/references/reddit-voice.md`

- [ ] **Step 1: Write the voice register file**

Create `tcn-reddit-campaign/references/reddit-voice.md` with exactly this content:

````markdown
# Reddit Voice Register

The voice for every Reddit post and comment this skill drafts. **Deliberately not the TCN brand voice**
used by `tcn-post` / `tcn-facebook-post`. On Reddit the user shows up as Justin-the-person, a member of
the community who happens to write a newsletter — not as a publication. Brand voice is exactly what
gets flagged as marketing and downvoted.

## Anchor (load at runtime)
Load `~/Documents/substack-research/Substack Research/workspace/core/anti-ai-writing-style.md` and run
its AI-tell removal pass over every draft. **Fallback:** if the file is missing, skip the AI-tell pass
and continue with structurally-correct output (ecosystem "skip-not-halt" convention) — note the skip.

## Rules
1. **First person, casual.** Write like a comment, not a column. Contractions, plain syntax, no throat-clearing.
2. **Tone-match the host sub.** Mirror the community's register: technical in r/ethereum, plain-spoken in
   r/politics, dry and privacy-literate in r/privacy. Read the dossier's `best_time_notes` and top-thread
   tone before drafting.
3. **Zero brand-speak.** No "The Civic Node," no taglines, no "dispatch" jargon, no slogan closers.
4. **No hype, no clickbait.** Ban "this changes everything," "you won't believe," "must-read," and the
   essay-style em-dash cadence. Reddit punishes marketing rhythm.
5. **Substance first, link second.** Open with the thing the community actually values (a finding, a
   question, a useful summary). The link is a footnote, never the pitch.
6. **Match length to the sub.** Most subs reward concise. Don't paste an essay where a tight comment wins.
7. **Honest, low-key disclosure.** Acceptable patterns: "Full disclosure, I wrote this." /
   "I write a newsletter on this stuff and went deeper here:" — never hidden, never salesy.

## Quick anti-pattern check (reject a draft if it does any of these)
- Reads like a press release or a LinkedIn post.
- Leads with the link or the brand.
- Uses the TCN tagline / "dispatch" framing / signature sign-off.
- Could not stand as a useful contribution if the link were removed.
````

- [ ] **Step 2: Verify the anchor, fallback, and brand-distinction are present**

Run:
```bash
F="/Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/references/reddit-voice.md"
for tok in "anti-ai-writing-style.md" "skip-not-halt" "not the TCN brand voice" "Zero brand-speak" "disclosure"; do
  grep -qi "$tok" "$F" && echo "OK  $tok" || echo "MISSING  $tok"
done
```
Expected: five `OK` lines, zero `MISSING`.

- [ ] **Step 3: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-reddit-campaign/references/reddit-voice.md
git commit -m "feat(tcn-reddit-campaign): add Reddit-native voice register

First-person community voice anchored to anti-ai-writing-style.md; explicitly
distinct from TCN brand voice.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: SKILL.md spine + CLAUDE.md stub

**Files:**
- Create: `tcn-reddit-campaign/SKILL.md`
- Create: `tcn-reddit-campaign/CLAUDE.md`

- [ ] **Step 1: Write SKILL.md**

Create `tcn-reddit-campaign/SKILL.md` with exactly this content:

````markdown
---
name: tcn-reddit-campaign
description: >
  Standing-aware Reddit promotion manager for The Civic Node (TCN). Use this skill whenever the user
  wants to find subreddits for a Substack article, check subreddit rules, draft Reddit posts to
  promote a piece, or manage their Reddit promotion over time — including phrases like "plan Reddit
  for this piece", "where should I post this on Reddit", "find subreddits for my article", "promote
  this on Reddit", "draft a Reddit post for X", "reddit campaign", "what's my Reddit status", "what
  should I post on Reddit next", "which subreddits can I post to", or "help me build karma in r/X".
  The skill discovers topic-relevant subreddits, vets them against their rules AND the user's account
  standing, and produces per-subreddit paste-ready posts with the framing each sub's self-promo rules
  allow. It NEVER submits anything: it is read-only on the account and hands the user paste-ready
  drafts to post manually. Does NOT write the article (that's tcn-draft / tcn-article-builder), and
  does NOT write X/LinkedIn/Facebook social copy (that's tcn-post / tcn-facebook-post).
---

# tcn-reddit-campaign

A campaign manager for promoting TCN articles on Reddit without getting shadowbanned. It turns a
published Substack URL into a vetted, per-subreddit posting plan with paste-ready drafts, and it
remembers — caching subreddit dossiers and logging what was posted where, so it never re-researches a
sub, never breaks a cooldown, and always knows the next move.

## Hard constraints (never violate)
1. **Read-only on the account.** Claude-for-Chrome is a *sensor*, never a submit button. Never post,
   comment, vote, or DM. Output is always paste-ready for the user to submit.
2. **Honest authorship only.** First-person, truthful attribution. Never pose as a third party; never
   astroturf.
3. **Respect the rules.** Honor each sub's rules and Reddit sitewide rules. No vote manipulation, no
   ban evasion, no posting where self-promo is banned outright.
4. **Human-in-the-loop on every submission.** The user submits; then optionally pastes the URL back so
   the ledger updates.

## Modes
| User intent | Mode |
|---|---|
| Gives a published article URL / "plan Reddit for this piece" | **Mode 1 — Plan a piece** |
| "what's my Reddit status" / "what should I post next" (no article) | **Mode 2 — Campaign status** |
| "help me build standing in r/X" (a named sub) | **Mode 3 — Build standing** |

Identify the mode from the request; if ambiguous, ask.

## Browsing sensor policy (hybrid)
- **Discovery uses no browser:** Claude's subreddit knowledge + `audience-profiles` (Marcus persona) +
  WebSearch (`site:reddit.com <topic>`).
- **Chrome is the ground-truth sensor only for:** the live rules page of finalist subs, and the user's
  logged-in karma/account-age (read once per session). Use `mcp__Claude_in_Chrome__*`.
- If Chrome is unavailable/not logged in: degrade gracefully — ask the user to paste the rules page and
  report their karma. Never guess gates silently.

## State bootstrap
Campaign state lives at `~/Documents/substack-research/Substack Research/workspace/reddit-campaign/`.
On first run, if it does not exist, create:
- `reddit-campaign/dossiers/` (empty dir)
- `reddit-campaign/ledger.md` with this header:
  `| date | sub | article slug | framing | url | cooldown_until | outcome |`
  `|------|-----|--------------|---------|-----|----------------|---------|`
- `reddit-campaign/targets.md` (created lazily by Mode 3).

## Mode 1 — Plan a piece (the main flow)
1. **Intake.** Take the published Substack URL + slug. Read `workspace/drafts/<slug>/10-final.md` for
   title + body; extract the topic and the 2–3 sharpest "hook" findings. If `10-final.md` is missing,
   ask the user to paste the article text.
2. **Discovery (no browser).** Generate ~10–15 candidate subreddits (knowledge + Marcus persona +
   WebSearch), each with a one-line "why Marcus is here / why this article fits" rationale. Dedupe
   against existing dossiers in `reddit-campaign/dossiers/`.
3. **Vet (Chrome).** For each finalist without a fresh dossier (or one older than `FRESHNESS_DAYS`),
   read the live rules page and write/refresh `dossiers/r-<sub>.md` per `references/dossier-template.md`.
   Read the user's karma/account-age once.
4. **Eligibility.** Apply `references/eligibility-rules.md` → verdict per sub
   (Ready / Risky / Locked / No-go), cross-checked against the ledger for cooldown/burst caps.
5. **Frame + draft.** For Ready (and conservatively, Risky) subs, select the archetype via
   `references/self-promo-playbook.md`, then draft in the `references/reddit-voice.md` register. Run the
   AI-tell pass (anchor file). Emit one **paste-ready bundle** per sub (see Output contract).
6. **Warming.** For Locked subs, produce a short karma-warming plan: 2–3 genuine comment opportunities
   (real current threads, via Chrome) or one native non-promo text-post idea that earns the standing to
   unlock the sub.
7. **Ledger stub.** Present the plan. When the user confirms a submission and pastes its URL, append a
   ledger row with `cooldown_until = post_date + COOLDOWN_DAYS`.

## Output contract — the paste-ready bundle
Every Ready/Risky draft ships with all of:
- **target sub** · **post type** (link / text) · **title** · **body** · **flair to select** ·
  **the exact rule it satisfies** · **link placement** (body or first comment — the comment is drafted
  too if applicable) · **suggested post time**.
Risky bundles are prefixed with an explicit caution naming the risk. No-go subs are listed with the
exclusion reason and no draft.

## Mode 2 — Campaign status / what's next
No article. Read `ledger.md` + dossiers → report: subs currently on cooldown (and when they clear),
Locked subs closest to unlocking, the user's karma progress, and a recommended set of this week's moves
(which warming comments to leave, which subs are now Ready). No drafting unless asked.

## Mode 3 — Build standing in a sub
Given a named sub, read/refresh its dossier, then produce a deeper warming plan (genuine participation
ideas grounded in current threads) to move it Locked → Ready. Record progress in `targets.md`.

## Fallbacks
- Missing `10-final.md` → ask for pasted text; continue.
- Chrome unavailable → ask user to paste rules + karma; continue.
- Ambiguous rules → classify **Risky**, surface the ambiguity, never auto-upgrade to Ready.
- Missing voice anchor file → skip AI-tell pass, keep structural output; note the skip.
- Sub private/banned/not found → **No-go** with reason; no draft.

## What this skill owns
- Subreddit discovery, rule vetting, standing/eligibility judgment, per-sub framing, Reddit-native
  drafting, karma-warming plans, and the persistent dossier + ledger.

## What this skill does NOT own
- Writing the article (`tcn-draft`, `tcn-article-builder`).
- X / LinkedIn / Facebook social copy (`tcn-post`, `tcn-facebook-post`).
- Submitting anything to Reddit (the user does this manually — by hard constraint).

## Related skills
- `audience-profiles` — the Marcus persona that seeds discovery.
- `workspace/core/anti-ai-writing-style.md` — the canonical voice anchor (shared across the ecosystem).
- Future: callable as a post-publish step from `tcn-content-plan` / `tcn-article-builder`. Standalone today.

## References
- `references/dossier-template.md` — per-sub dossier schema.
- `references/eligibility-rules.md` — verdict logic + cadence defaults (user-tunable).
- `references/self-promo-playbook.md` — policy→framing map + culture rules (user-tunable).
- `references/reddit-voice.md` — the Reddit-native voice register.
````

- [ ] **Step 2: Write the CLAUDE.md stub**

Create `tcn-reddit-campaign/CLAUDE.md` with exactly this content:

````markdown
# tcn-reddit-campaign — Session History

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->

<claude-mem-context>
</claude-mem-context>
````

- [ ] **Step 3: Verify SKILL.md frontmatter, constraints, modes, and output contract**

Run:
```bash
F="/Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/SKILL.md"
# frontmatter present
head -1 "$F" | grep -qx -- "---" && echo "OK frontmatter open" || echo "MISSING frontmatter"
grep -q "^name: tcn-reddit-campaign$" "$F" && echo "OK name" || echo "MISSING name"
# the four hard constraints, three modes, never-submit invariant, the 7 bundle fields
for tok in "Read-only on the account" "Honest authorship only" "Human-in-the-loop" \
           "Mode 1 — Plan a piece" "Mode 2 — Campaign status" "Mode 3 — Build standing" \
           "paste-ready bundle" "the exact rule it satisfies" "link placement" "suggested post time" \
           "NEVER submits" "10-final.md" "eligibility-rules.md" "self-promo-playbook.md" "reddit-voice.md"; do
  grep -q "$tok" "$F" && echo "OK  $tok" || echo "MISSING  $tok"
done
```
Expected: every line prints `OK …`, zero `MISSING`.

- [ ] **Step 4: Commit**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git add tcn-reddit-campaign/SKILL.md tcn-reddit-campaign/CLAUDE.md
git commit -m "feat(tcn-reddit-campaign): add SKILL.md spine + CLAUDE.md stub

Triggering frontmatter, hard constraints, 3 modes, hybrid sensor policy,
Mode-1 workflow, paste-ready output contract, state bootstrap, references.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: End-to-end smoke test (acceptance criteria)

This task runs the skill against a real fixture and checks it against spec §16. No new files except a
throwaway dry-run note (not committed). The smoke test is performed by reasoning through the skill as
written — it does not submit anything to Reddit.

**Fixture:** slug `you-own-the-hotspot-nova-labs-owns-what-it-earns` (the one draft dir with a
`10-final.md`). A representative Substack URL for the dry run:
`https://drinkyouroj.substack.com/p/you-own-the-hotspot` (exact URL not load-bearing for the dry run).

- [ ] **Step 1: Confirm the fixture article exists**

Run:
```bash
ls -1 "/Users/justin/Documents/substack-research/Substack Research/workspace/drafts/you-own-the-hotspot-nova-labs-owns-what-it-earns/10-final.md"
```
Expected: the path prints (file exists).

- [ ] **Step 2: Dry-run Mode 1 (reason through, do not submit, do not browse if Chrome absent)**

Load `tcn-reddit-campaign/SKILL.md` and its references. Using the fixture article's topic
(community-owned wireless / DePIN / Helium-style networks), produce — in chat, as a dry run — :
- a candidate list (~10–15) with per-sub rationales,
- for 2–3 plausible subs (e.g. r/helium, r/CryptoCurrency, r/privacy), a worked eligibility verdict
  using `eligibility-rules.md` against an assumed thin-karma profile,
- one full paste-ready bundle for a Ready sub, and
- one warming plan for a Locked sub.

Verify against spec §16 acceptance criteria. Check each:
```
[ ] 1. Output includes candidates+rationales, verdicts, Ready bundles, Locked warming plan
[ ] 2. No step instructs or performs a submission; drafts are paste-ready + honestly attributed
[ ] 5. A self-promo-banned sub is classified No-go and not drafted for
[ ] 6. The bundle carries all 7 fields (sub, type, title, body, flair, rule, link placement, time)
[ ] 7. Eligibility + framing came from the reference files, not hard-coded prose
```
Expected: all five boxes checkable from the dry-run output. If any fails, fix the relevant reference
or SKILL.md section and re-run this step.

- [ ] **Step 3: Dry-run Mode 2 with empty state**

Confirm the state bootstrap logic: with no `reddit-campaign/` dir, the skill would create the ledger
header and report "no history yet — here's how to start." Verify against criteria:
```
[ ] 3. (simulated) a second article run would reuse a cached dossier + honor cooldown from the ledger
[ ] 4. Mode 2 reports cooldown state + next moves from persisted state alone
```
Expected: both reason out correctly from the SKILL.md Mode-2 + state-bootstrap sections.

- [ ] **Step 4: Verify the never-submit invariant end-to-end**

Run:
```bash
grep -rn -iE "submit|post the|click post|hit submit" \
  /Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/ \
  | grep -viE "never|paste-ready|read-only|sensor|manually|user submits|human-in-the-loop|does NOT own|exclusion" || echo "CLEAN: no stray submission instructions"
```
Expected: `CLEAN: no stray submission instructions` (every mention of submitting is guarded by a
negation / manual-by-user qualifier). If any unguarded line appears, fix it.

- [ ] **Step 5: Commit the smoke-test verification**

```bash
cd /Users/justin/CascadeProjects/claude-skills
git commit --allow-empty -m "chore(tcn-reddit-campaign): smoke-test verified against spec acceptance criteria

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review (completed during planning)

**Spec coverage** — every spec section maps to a task:
- §3 hard constraints → Task 5 SKILL.md (+ echoed in Tasks 2–3 reference files); verified Task 6 Step 4.
- §5.1–5.8 components → Task 5 Mode-1 workflow steps 1–7; data model → Task 1; eligibility → Task 2; framing → Task 3; voice → Task 4.
- §6 modes → Task 5 mode table + Mode 1/2/3 sections.
- §7 data flow incl. Risky/No-go routing → Task 2 (verdict→action) + Task 5.
- §8 data model → Task 1 (dossier), Task 5 (ledger header), Task 5 Mode 3 (targets).
- §9 voice → Task 4. §10 file structure → Tasks 1–5. §11/§12 user-tunable logic → Tasks 2/3 (shipped as defaults + TUNE ME flags). §13 integration → Task 5 "Related skills". §14 defaults → Task 2. §15 fallbacks → Task 5 Fallbacks. §16 acceptance → Task 6. §17 ethics → Tasks 2,3,5 hard-rule blocks.

**Placeholder scan** — no TBD/TODO/"handle appropriately"; every file's full content is inlined; the "TUNE ME" blocks are complete working defaults, not placeholders.

**Type/name consistency** — verdict names (Ready/Risky/Locked/No-go), archetype names (transparent-author/thread-targeted/question-led/value-first), policy values (strict/promo-friendly/discussion-heavy/promo-thread/banned/unknown), constant names (COOLDOWN_DAYS/MAX_SUBS_PER_DAY/FRESHNESS_DAYS/KARMA_SAFETY_MARGIN/MIN_COMFORT_KARMA), and file paths are identical across Tasks 1–6 and match the spec.
