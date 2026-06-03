# Note Format Spec — Pre-Save Validation Checklist

This is the **pre-save validation checklist** the `tcn-paid-note` skill runs at Steps 5 and 7, before it writes a note to `workspace/paid/`. It does not define the format — it **verifies** a drafted note against the format.

**The format authority is the DNA doc:** `workspace/paid/_template-thinking-behind-the-thinking-note.md`. That file OWNS the title formula (§4), the four furniture lines (§6), the body rules (§7), the closer-aphorism pattern (§8), the full frontmatter spec (§9), the word band, and the exemplar gallery (§10). When a rule and its rationale are in question, read the DNA doc. This file turns those rules into mechanical checks and does not re-derive them.

Structural model: this file is to the DNA doc what `.claude/skills/tcn-flagship-cover/references/output-frontmatter-spec.md` is to `workspace/core/_template-flagship-cover.md` — the enforcement layer, not the source of truth.

**Acceptance contract.** This checklist must catch a malformed note: a missing furniture line, a body em dash, an out-of-band word count, or an unconfirmed derived field. If a check fails, fix the note before writing — see the Pre-save gate below.

---

## 1. Frontmatter schema

Reproduce this block at the top of every note. Each field is annotated with how it is set:

- **`auto`** — derived mechanically; no writer input needed, but the derivation must be shown.
- **`confirm`** — derived, then confirmed with the writer before saving. Never silently assumed.
- **`set-at-save`** — computed at the final save step (Step 7), not estimated earlier.

```yaml
title: confirm            # from interview
subtitle: confirm
type: auto                # paid-note — constant for this series
status: auto              # draft — constant on creation
pillar: confirm           # inherit from flagship manifest (workspace/drafts/{slug}/manifest.md)
published: confirm        # flagship date + 5 days (Fri→Wed) default
created: set-at-save      # today
updated: set-at-save      # today
word_count: set-at-save   # accurate count after final draft
plan_ref: auto            # "" — usually empty unless a content-plan item maps to this note
series: auto              # The thinking behind the thinking — constant for this series
series_ref: auto          # "<Flagship Title> (published <date>)"
source_url: confirm        # https://drinkyouroj.substack.com/p/{slug}
```

(This matches DNA §9 and design-spec §8. Keep all three consistent — if the format changes, change the DNA doc first, then mirror here and in the spec.)

### Field checks

- [ ] **`title`** — present, quoted, and is a title-formula instance per DNA §4 (`I Had the Wrong ___` default, or a sanctioned exception `I Almost Wrote "___"` / `The Sentence I Cut`). **confirm** — came from the interview, not invented at save.
- [ ] **`subtitle`** — present, quoted, two parallel sentences, **joined by a period** (the em-dash join is deprecated/grandfathered for federal-state only; new notes use a period — see DNA §6 and furniture check 2b below). **confirm.**
- [ ] **`type`** — exactly `paid-note` (constant for this series). **auto.**
- [ ] **`status`** — exactly `draft` on creation (constant; the writer flips to `ready` later, outside this skill). **auto.**
- [ ] **`pillar`** — set, and read from the flagship manifest at `workspace/drafts/{slug}/manifest.md`, not guessed. **confirm.**
- [ ] **`published`** — set; default is flagship publish date **+ 5 days** (Fri → Wed). **confirm** the date with the writer.
- [ ] **`created`** — today's date, `YYYY-MM-DD`. **set-at-save.**
- [ ] **`updated`** — today's date, `YYYY-MM-DD` (re-stamped on edits). **set-at-save.**
- [ ] **`word_count`** — an **accurate count of the final draft**, computed at save. Not estimated, not left from an earlier draft. **set-at-save.** Should be in the same family as the §3b body count (the two differ by a few words depending on furniture inclusion — see §3b).
- [ ] **`plan_ref`** — empty string `""` unless a content-plan item maps to this note (usually empty). **auto.**
- [ ] **`series`** — exactly `The thinking behind the thinking` (constant for this series). **auto.**
- [ ] **`series_ref`** — composed as `<Flagship Title> (published <flagship date>)`. **auto** — confirm the derivation is correct against the flagship.
- [ ] **`source_url`** — set to `https://drinkyouroj.substack.com/p/{slug}`, derived from the flagship slug. **confirm.** Required going forward. (Grandfather clause: federal-state predates this field and carries an empty `Process note` link; a back-catalog lint must NOT flag it. New notes always populate it, and the `Process note —` furniture link resolves to this URL — see furniture check 3.)

> **Fail condition (unconfirmed derived field):** if `pillar`, `published`, `series_ref`, or `source_url` was filled by assumption rather than read-from-source-and-confirmed, the note is not saveable. Confirm, then save.

---

## 2. Furniture-line checklist

The four locked lines from DNA §6. They appear in this order, directly under the frontmatter, with the body in between. Fill the angle brackets; everything else is byte-for-byte from the DNA skeleton.

- [ ] **(a) Title repeat.** The `title:` string appears a second time as **plain text** (no `#` heading) directly under the frontmatter. It is **identical** to the YAML `title:` field — same string, byte-for-byte.
- [ ] **(b) Italic subtitle.** Directly under the title repeat: the subtitle, **italic** (`*...*`), identical to the YAML `subtitle:` field. Two parallel sentences — first names the wrong read, second names the correction/truer thread. **Joined by a period, NOT an em dash.** (The em-dash join is a deprecated, grandfathered case for federal-state; new notes fail this check if they use an em dash to join the two sentences.)
- [ ] **(c) Process-note line.** Present, verbatim shape: `*Process note — analytical backstage for [<Flagship Title>](<flagship url>).*` The flagship title is a live link to the `source_url`. **This line keeps its em dash — it is the ONE em dash permitted in the body region** (see §3a). The flagship title inside the link matches `series_ref`'s title. (Trailing period inside or outside the link is cosmetic — either is fine.)
- [ ] **(d) Horizontal rule + refrain.** A `---` line separates the body from the closing refrain, then the founding-tier refrain appears **verbatim and italic**:

  ```
  *Founding-tier subscribers get this in every issue: the analytical moves behind the piece, including the ones that didn't survive contact with the primary sources.*
  ```

  The refrain is byte-for-byte identical every issue. A paraphrase fails this check.

> **Fail condition (missing furniture line):** if any of (a)–(d) is absent, out of order, or altered (paraphrased refrain, dropped `---`, missing title repeat, subtitle joined with an em dash), the note is not saveable.

---

## 3. Body validation

The **body** is the region between the `*Process note —*` line and the closing refrain, exclusive of both boundary lines. All three body checks below (em-dash, word-count, link) operate on **one shared region idiom** so they cannot disagree:

```bash
sed -n '/^\*Process note/,/^Founding-tier/p' NOTE.md | sed '1d;$d'
```

This anchors the lower boundary on the `*Founding-tier*` refrain line (not on the first `---`), so a stray separator inside the body does not truncate the region. A body-internal `---` is **discouraged** — the notes don't use one, and the `---` is reserved as the furniture rule before the refrain (§2d) — but if one is present, the unified region still spans the full body.

### (a) Body em-dash scan — must return zero

Zero em dashes (`—`) in the body. The locked `*Process note —*` furniture line is the only em dash permitted in the body region, and it is a boundary line, not body — so the body proper has **none**. Use semicolons, periods, parentheses, or commas instead (DNA §7).

Run the scan in the Pre-save gate below. A nonzero count fails.

### (b) Word count — within the band

Band (DNA §7): **240 hard floor / 365–490 target / 490 ceiling.**

- **FAIL** if body word count is **under 240** or **over 490**. Not saveable.
- **FLAG as "below target"** (warn, do not block) if **240–364**. Allowed only when the move is genuinely tight; the default ambition is 365–490. The first installment anchors the floor.
- **PASS** if **365–490** (the mature-installment target band). For per-exemplar counts (clean-body vs. frontmatter), see the DNA doc's verification table — they live in one place there, not restated here.

The frontmatter `word_count` field (§1) and this body-region count should be in the **same family**, not identical: they differ by a few words depending on whether the title/subtitle furniture is included (the DNA notes the frontmatter `word_count` is the writer-set, furniture-inclusive figure). Use the body-region count for the band check.

### (c) Primary-source link count — 2 to 4

The body carries **2–4 inline `[anchor](url)` links** to primary sources the **flagship already cites** (the HIP markdown, the capacity-auction report, the analyst note, the court filing). Do not invent links; reuse the flagship's sourcing (DNA §7).

- **FAIL** if **under 2** or **over 4**.

> **Fail conditions (body):** body em-dash count > 0; body word count < 240 or > 490; primary-source link count < 2 or > 4. Any of these → not saveable.

---

## 4. Pre-save gate

**If any check above fails, fix the note before writing. Never save a note that fails the em-dash check or the furniture checks.** (Word-count "below target" 240–364 is a warn, not a block; everything else in §§1–3 is a block.)

### Body em-dash check (run after drafting, before save)

The task-canonical one-liner. Body = between the Process-note line and the refrain:

```bash
# DO NOT RUN — illustrative only; misfires on conformant notes (it matches the Process-note line's one allowed em dash). Use the boundary-stripped form below.
# Run after drafting, before save. Body = between the Process-note line and the refrain.
sed -n '/^\*Process note/,/^Founding-tier/p' DRAFT.md | grep -n '—' && echo "FAIL: em dash in body" || echo "PASS: no body em dash"
```

> **Boundary caveat — read before trusting the output.** The `sed` range above is **inclusive** of the matched `*Process note —*` line, which legitimately carries the one allowed em dash. So this exact command reports `FAIL` on a *conformant* note because it sees the furniture line's em dash, not a body em dash. To gate on the **body proper**, drop the two boundary lines first (`sed '1d;$d'`), which is the check the skill should actually run:
>
> ```bash
> # Body-proper em-dash gate (excludes the Process-note furniture line and the refrain boundary).
> sed -n '/^\*Process note/,/^Founding-tier/p' DRAFT.md | sed '1d;$d' | grep -n '—' \
>   && echo "FAIL: em dash in body" || echo "PASS: no body em dash"
> ```
>
> Verified against `workspace/paid/2026-06-10-thinking-behind-the-thinking-windfall-thread.md`: the boundary-stripped form returns **PASS** (conformant), and returns **FAIL** when an em dash is injected into a body sentence. Use the boundary-stripped form as the gate; treat a bare-command `FAIL` as "re-check whether the only match is the furniture line."

### Word-count and link gates (companions to the em-dash gate)

All three body gates share the same region idiom (`sed -n '/^\*Process note/,/^Founding-tier/p' DRAFT.md | sed '1d;$d'`) so they always agree on where the body starts and ends.

```bash
# Body word count — band: <240 FAIL, 240-364 FLAG below target, 365-490 PASS, >490 FAIL.
# Drop any separator/blank lines before counting so a stray --- never skews the count.
sed -n '/^\*Process note/,/^Founding-tier/p' DRAFT.md | sed '1d;$d' | grep -vE '^(---|[[:space:]]*)$' | wc -w

# Primary-source link count — must be 2-4.
sed -n '/^\*Process note/,/^Founding-tier/p' DRAFT.md | sed '1d;$d' | grep -o '](http[^)]*)' | wc -l
```

---

## 5. Glob note (carry-forward from the DNA doc)

When the skill **discovers existing notes** (to build the exemplar gallery, to dedup, to count installments), it must match the **dated note form** and exclude templates and cover prompts.

- **Match:** `workspace/paid/YYYY-MM-DD-thinking-behind-the-thinking-{slug}.md` (a leading ISO date).
- **EXCLUDE:** `_template-*` and `*-cover*.md` (covers, `*-cover-prompt.md`).

The broad pattern `workspace/paid/*-thinking-behind-the-thinking-*.md` **wrongly matches** the DNA doc (`_template-thinking-behind-the-thinking-note.md`), the cover template (`_template-thinking-behind-the-thinking-cover.md`), and any `*-cover-prompt.md` siblings. Enumerate notes by the dated form and filter the excludes — never hardcode the installment count (the series grows weekly).

```bash
# Correct note enumeration: dated form only, templates and covers excluded.
ls workspace/paid/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-thinking-behind-the-thinking-*.md \
  | grep -v -- '-cover'
```
