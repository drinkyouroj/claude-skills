# tcn-reddit-campaign — Design Spec

**Date:** 2026-06-05
**Status:** Approved (brainstorm complete) — ready for implementation plan
**Skill source-of-truth (to be built):** `/Users/justin/CascadeProjects/claude-skills/tcn-reddit-campaign/`
**Persistent state (data):** `~/Documents/substack-research/Substack Research/workspace/reddit-campaign/`

---

## 1. One-liner

A standing-aware Reddit promotion manager for The Civic Node. Given a published TCN article, it discovers topic-relevant subreddits, vets them against their rules **and** the user's account standing, and produces per-subreddit paste-ready posts — while persisting a dossier library and a posting ledger so the user never re-researches a sub, never breaks a cooldown, and always knows the next move.

It is a **research-and-draft tool, never a submit button.**

---

## 2. Goals / Non-goals

### Goals
- Turn a single published Substack URL into a vetted, per-subreddit posting plan with paste-ready drafts.
- Model the user's Reddit **standing** so the skill never marches a low-karma account into an auto-removal or a shadowban.
- Persist a growing **dossier library** (per-sub rules + history) and a **ledger** (what posted where/when) that survive across articles and sessions.
- Adapt framing per subreddit's self-promo policy, always with honest authorship.
- Surface **karma-building moves** for subs the account can't yet post to — karma-building is a first-class output, not an afterthought.

### Non-goals (v1)
- No autonomous posting, commenting, voting, or DMing. Ever.
- No multi-account management or ban-evasion tooling.
- No analytics dashboards beyond the lightweight ledger.
- Not an orchestrator step yet — built standalone, but with a clean enough interface to be called post-publish later (see §13).
- Does not write the article, the Substack Note, or other-platform social copy (those are existing TCN skills).

---

## 3. Hard constraints (safety guardrails)

These are load-bearing and must be stated in `SKILL.md` as non-negotiable:

1. **Read-only on the account.** Claude-for-Chrome is a *sensor*, never an *actuator*. The skill never submits posts/comments, never votes, never DMs. It needs no write access to the account.
2. **Honest authorship only.** Never pose as a third party; never fabricate that the user "found" their own piece. First-person, truthful attribution.
3. **Respect rules.** Honor each subreddit's rules and Reddit's sitewide rules: no vote manipulation, no ban evasion, no spamming, no posting where self-promo is forbidden outright.
4. **Human-in-the-loop on every submission.** All output is paste-ready; the user submits manually, then optionally pastes the resulting URL back to update state.

---

## 4. Resolved brainstorm decisions

| Decision | Choice | Consequence |
|---|---|---|
| Core loop | **Campaign manager** | Persistent state (dossiers + ledger) is the spine, not the prose |
| Account reality | **Aged but low-karma** | Skill must be standing-aware; karma-warming is a first-class output |
| Automation posture | **Read-auto, post-manual** | Chrome reads only; output is paste-ready bundles |
| Discovery model | **Topic-driven each time** | Stateless per-article discovery; stateful vetting + history (dossier cache) |
| Posting posture | **Per-sub adaptive framing** | Self-promo policy is a routing key into draft archetypes; honest authorship always |
| Article input | **Published URL + reads workspace** | Reads `workspace/drafts/<slug>/10-final.md`; runs post-publish |
| Browsing sensor | **Hybrid** | Discovery = knowledge + web search (no browser); Chrome = ground-truth rules + logged-in karma only |
| Name | **`tcn-reddit-campaign`** | "-campaign" because it does more than draft |

---

## 5. Architecture / Components

### 5.1 Article intake
- **Input:** published Substack URL + slug. If slug omitted, attempt to derive from URL; else ask.
- Reads `workspace/drafts/<slug>/10-final.md` for title + body; extracts topic, key claims, and the "hook" findings used to seed discovery and drafts.
- **Fallback:** if `10-final.md` is missing, ask the user to paste the article text/excerpt. (Mirrors the ecosystem's "skip-not-halt" fallback ethos.)

### 5.2 Discovery engine *(no browser)*
- Inputs: article topic + Marcus persona (`audience-profiles`) + Claude's subreddit-landscape knowledge + web search (`site:reddit.com <topic>` style queries).
- Output: ~10–15 candidate subreddits, each with a one-line rationale ("why Marcus is here / why this article fits").
- Dedupes candidates against the cached dossier library so known subs are reused, not re-discovered.

### 5.3 Dossier library *(persistent state)*
- One markdown file per subreddit: `dossiers/r-<sub>.md`.
- Schema (see §8.1): rules summary, self-promo policy class, karma/age gates, flair requirements, link policy (link-post vs text+comment), best-time-to-post notes, last-refreshed date, per-sub posting history.
- **Freshness policy:** if `last-refreshed` is older than the freshness window (default 30 days), re-verify via Chrome before trusting cached rules.

### 5.4 Vetting + eligibility engine *(Chrome for ground truth)*
- For each finalist: pull the **live rules page** via Chrome; classify self-promo policy; read karma/age gates and flair requirements.
- Pull the user's **current karma/standing** once per session via the logged-in profile page.
- Produce an eligibility verdict per sub — **Ready / Locked (build karma) / Risky / No-go (self-promo banned)** — cross-referenced against the cooldown ledger (a recently-posted sub is flagged on-cooldown).
- The verdict logic is a user-authored decision function (see §11) — it encodes the user's personal shadowban-risk posture.
- **Verdict → action routing:**
  - **Ready** → framing selector + drafting engine (full paste-ready bundle).
  - **Locked** → karma-warming planner (no promo draft yet).
  - **Risky** → draft *only* the most conservative archetype (value-first text, link-in-comment), prefixed with an explicit caution naming the risk; the user decides whether to use it. Never auto-promoted to Ready.
  - **No-go** → no draft; listed with the reason it was excluded.

### 5.5 Framing selector
- Maps a Ready sub's self-promo policy → draft archetype:
  - **strict no-promo** → value-first text post, link in a first comment
  - **promo-friendly** → transparent author ("I wrote this piece on X")
  - **discussion-heavy** → question-led discussion prompt, link in a comment
  - **self-promo thread exists** → thread-targeted post into that thread
- Shows the *why* (which rule signal selected which archetype) for user approval.
- The policy→archetype map is the second user-authored piece (see §12).

### 5.6 Drafting engine
- Per Ready sub, emits a **paste-ready bundle**:
  - target sub · post type (link vs text) · title · body · flair to select · the exact rule the post satisfies · link placement (body vs first comment — the comment is drafted too) · suggested post time.
- Voice = Reddit-native register (§9). Runs an AI-tell pass against `workspace/core/anti-ai-writing-style.md` (runtime load; fallback = skip voice pass, continue with structure).

### 5.7 Karma-warming planner
- For **Locked** subs (gated by karma the account lacks), output an "earn standing here" plan:
  - 2–3 genuine comment opportunities (real, current threads pulled via Chrome), or
  - a native, non-promotional text-post idea that builds karma without promoting.
- This is the mechanism that converts Locked → Ready over time.

### 5.8 Ledger
- Append-only log: `ledger.md`. Records what was posted, to which sub, when, with which framing, and the live URL (pasted back by the user after submitting).
- Optional outcome fields (upvotes / removed? / comment count) the user can fill later. **Kept in v1 as optional** — populated only if the user pastes results; never blocks a session.
- Drives cooldown enforcement and Mode 2's "what's next."

---

## 6. Modes (mirrors `tcn-content-plan`)

- **Mode 1 — Plan a piece** *(default):* URL in → discovery → vet → drafts + warming plan + ledger stub. The main flow.
- **Mode 2 — Campaign status / what's next:** no article; reads ledger + dossiers → cooldown clock, which Locked subs are near unlocking, karma progress, this week's recommended moves.
- **Mode 3 — Build standing in a sub:** target one specific sub → deep warming plan (genuine participation ideas) to move Locked → Ready.

Mode is inferred from invocation (URL present → Mode 1; "status/what's next" → Mode 2; named target sub → Mode 3) and confirmed when ambiguous.

---

## 7. Data flow (Mode 1)

```
published URL + slug
   │
   ▼
[Article intake] ── reads 10-final.md ──► topic + hook findings
   │
   ▼
[Discovery engine] (knowledge + web search) ──► ~10–15 candidates
   │  └─ dedupe vs dossier library
   ▼
[Vetting + eligibility] (Chrome: live rules + your karma)
   │  └─ write/refresh dossiers
   ▼
verdict per sub: Ready / Locked / Risky / No-go  (+ cooldown check)
   │
   ├──► Ready ──► [Framing selector] ──► [Drafting engine] ──► paste-ready bundles
   ├──► Risky ─► [Drafting engine] ──► conservative draft + caution (user decides)
   ├──► Locked ─► [Karma-warming planner] ──► warming moves
   └──► No-go ─► listed with exclusion reason (no draft)
   │
   ▼
[Ledger] stub written; user submits manually; pastes URL back to finalize
```

---

## 8. Data model

### 8.1 Dossier — `dossiers/r-<sub>.md`
```
---
sub: r/<name>
last_refreshed: YYYY-MM-DD
self_promo_policy: strict | promo-friendly | discussion-heavy | promo-thread | banned | unknown
karma_gate: <number or unknown>
karma_gate_type: comment | post | combined | unknown
age_gate_days: <number or unknown>
flair_required: no | "<comma-list of flairs>"   # 'no' = none; a quoted list = required, pick one
link_policy: link-post | text+comment | either | text-only
best_time_notes: <freeform>
---

## Rules summary
- <bulleted live rules relevant to self-promo, links, flair, formatting>

## My history here
| date | article | framing | url | outcome |
|------|---------|---------|-----|---------|
```

### 8.2 Ledger — `ledger.md`
```
| date | sub | article slug | framing | url | cooldown_until | outcome |
|------|-----|--------------|---------|-----|----------------|---------|
```

### 8.3 Targets — `targets.md` (optional)
Standing subs actively being warmed (Mode 3 output). One row per sub: `| sub | current karma | gate to clear | last warming action | last updated |`.

---

## 9. Voice register

New file `references/reddit-voice.md`:
- First-person, casual, community-native, **zero brand-speak**.
- Tone-matched to the host subreddit (a r/privacy post ≠ a r/CryptoCurrency post).
- No essay cadence / no heavy em-dash rhythm / no "publication" register.
- Anchored to the canonical AI-tell rules in `workspace/core/anti-ai-writing-style.md` (runtime load; fallback = skip voice pass).
- Explicitly distinct from the TCN brand voice used by `tcn-post` / `tcn-facebook-post` — on Reddit the user shows up as a *person*, not a publication. Brand voice is exactly what gets flagged as marketing.

---

## 10. File structure (skill, in claude-skills repo)

```
tcn-reddit-campaign/
├── SKILL.md
├── CLAUDE.md                     (cross-skill refs, per the ecosystem convention)
└── references/
    ├── reddit-voice.md           (Reddit-native register)
    ├── self-promo-playbook.md    (9:1 culture, policy→framing map, link-in-comment tactics)
    ├── dossier-template.md       (per-sub dossier schema, §8.1)
    └── eligibility-rules.md      (Ready/Locked/Risky/No-go logic + cooldown defaults)
```

---

## 11. User-authored logic #1 — eligibility decision

At implementation time, the user writes the **eligibility decision function** (~5–10 lines of pseudocode/rules in `references/eligibility-rules.md`). It maps `(sub gates, user karma/age, self-promo policy, cooldown state)` → `Ready | Locked | Risky | No-go`. This encodes the user's personal risk posture toward shadowbans and is too opinionated for a generic default. The spec provides the signature and inputs; the user supplies the thresholds and tie-breaks.

## 12. User-authored logic #2 — self-promo → framing map

The user writes the **policy→archetype map** (~5–10 lines in `references/self-promo-playbook.md`): which framing archetype to apply for which rule signal, and how aggressive to be at the margins. This is editorial judgment, not a default.

---

## 13. Cross-skill integration

- **Standalone v1** with a clean interface so it can later be invoked as a post-publish step from `tcn-content-plan` / `tcn-article-builder`.
- Reads the same workspace and the same `anti-ai-writing-style.md` voice file as the rest of the ecosystem.
- Uses `audience-profiles` (Marcus) as the discovery persona source.
- Per the ecosystem convention, document the relationship **in both files** (this skill references its callers; future orchestrators reference this skill).

---

## 14. Defaults (tunable)

- **Cooldown:** no repeat post to the same sub within **14 days**; no more than **3–4 subs/day** for one article (bursts read as spam).
- **Dossier freshness:** re-verify rules if `last_refreshed` older than **30 days**.
- **Discovery breadth:** **10–15** candidates per article → narrowed to the eligible few.

---

## 15. Error handling / fallbacks

- **Missing `10-final.md`:** ask user to paste article text; continue.
- **Chrome unavailable / not logged in:** degrade to Approach-C behavior for that session — ask user to paste the rules page and report karma; never guess gates silently.
- **Rules page ambiguous:** classify as **Risky**, surface the ambiguity, never auto-upgrade to Ready.
- **Missing voice file:** skip the AI-tell pass, keep structural output (ecosystem "skip-not-halt" convention).
- **Sub not found / private / banned:** mark **No-go** with reason; do not draft.

---

## 16. Acceptance criteria

1. Given a real published URL + slug, Mode 1 produces: a candidate list with rationales, per-sub eligibility verdicts, paste-ready bundles for Ready subs, and warming plans for Locked subs.
2. No output ever instructs or performs a submission; every draft is clearly paste-ready and attributed honestly.
3. A second run for a different article reuses cached dossiers (no re-research) and honors cooldowns from the ledger.
4. Mode 2 with no article reports cooldown state and next moves from persisted state alone.
5. A sub that bans self-promo is classified **No-go** and never drafted for.
6. Drafts carry: target sub, post type, title, body, flair, the satisfied rule, link placement (+ comment if applicable), suggested time.
7. The two user-authored logic blocks (§11, §12) are present as editable reference files, not hard-coded.

---

## 17. Ethics & safety posture

The skill's value depends on *not* getting the user banned, so its incentives align with good Reddit citizenship: value-first contribution, honest disclosure, rule compliance, and rate discipline. It explicitly refuses vote manipulation, sockpuppeting, ban evasion, and posting into communities that forbid self-promotion. These are encoded as hard constraints (§3), not soft suggestions.
