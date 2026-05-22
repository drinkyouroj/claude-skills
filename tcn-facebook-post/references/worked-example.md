# Worked Example — tcn-facebook-post

Two complete invocations end-to-end, showing inputs, dispatch, and final output. Used as a sanity check during skill development and as a reference for future tuning.

## Example 1: Tuesday Awareness day

### Inputs

- `purpose`: `Awareness`
- `source_material`:
  - Live news: "Treasury Department released FY2024 final figures; interest payments on federal debt = $881B, defense outlays = $880B"
  - FRESH list: "Treasury FY2024 final figures, interest-vs-defense crossover, services inflation Q1 data"
- `spent_list`: "Hormuz crossings 191/3000; April CPI energy +3.8% MoM; rate tool doesn't reach supply shocks"
- `date`: 2026-05-19

### Skill process

1. **Voice context loaded:** workspace/core/anti-ai-writing-style.md present, in working context.
2. **Lookup:** `purpose: Awareness` → shape: Caption (≤30 words), image_source: AI-generated, cta_rule: No link, voice_notes: drop closed em dashes, one warmth-marker max, no edge.
3. **Angle derivation:** Awareness day, audience is the general FB reader. Specific anchor from live news: interest payments now exceed defense budget, both >$880B. Plain-language interesting on its own; nothing in spent_list overlaps.
4. **Draft 3 options:**

### Output

```markdown
**Purpose:** Awareness
**Shape:** Caption
**Posting time:** 09:00 ET

### Option A — Safe
Interest payments on the federal debt are now bigger than the entire defense budget. Both crossed $880 billion last year. Most coverage isn't touching this.

**Image:** AI prompt: "Split-frame photograph, left half shows a stack of physical Treasury bond certificates on a desk, right half shows the Pentagon building exterior from below at golden hour. Equal weight to both halves. Documentary photography style, no logos, no text."

### Option B — Safe
The U.S. is now spending more on interest payments for the debt than on the entire military. First time in modern history. Honestly worth paying attention to.

**Image:** AI prompt: "Close-up overhead shot of a calculator displaying $881,000,000,000 on its screen, sitting on top of a folded American flag. Documentary photography, natural light, no other objects in frame."

### Option C — Safe
Quick reality check: the federal government now spends more paying interest on the debt than it does on defense. $881B vs $880B last year.

**Image:** AI prompt: "Two simple stacked piles of cash visible in a clean overhead photograph. Left pile labeled with a small handwritten card reading 'INTEREST', right pile labeled 'DEFENSE'. Both piles roughly equal in size. Natural daylight, white background."

**Recommendation:** Default to Option A (cleanest framing, strongest specific anchor). Option B if a slightly warmer "honestly" tone fits the week's mood. Option C if the previous day's posts have been heavier; this one lands lighter.
```

---

## Example 2: Friday Flagship CTA day

### Inputs

- `purpose`: `Flagship CTA`
- `source_material`:
  - X standalone copy (from Step 5 output): "Services inflation didn't slow in Q1. Goods deflation is masking that. The Fed's 2% target is being missed in the part of the economy that actually drives household budgets. (BLS Q1 release)"
  - Flagship article URL: `https://thecivicnode.substack.com/p/services-inflation-q1-2026`
  - Flagship article tagline (from article frontmatter): "Why the headline inflation number is hiding the real story for most households"
- `spent_list`: "Headline CPI 2.3% YoY April; goods deflation -0.4%; Fed dot plot December 2025; services inflation glossed earlier this week (Tue Note)"
- `flagship_url`: `https://thecivicnode.substack.com/p/services-inflation-q1-2026`
- `date`: 2026-05-22

### Skill process

1. **Voice context loaded.**
2. **Lookup:** `purpose: Flagship CTA` → shape: Paragraph (50-80 words), image_source: Substack hero (today's piece), cta_rule: Hard link at end, voice_notes: slight authority, plain-English tagline, no "predictably/naturally/of course."
3. **Angle derivation:** Funnel day. Restate the X claim in FB-Explainer voice — drop "Fed's 2% target is being missed" (too technical) and "BLS Q1 release" (citation is fine on X, redundant on FB). Plain-English: the headline number is misleading; the part most household budgets actually feel (services) isn't slowing.
4. **Draft 3 options:**

### Output

```markdown
**Purpose:** Flagship CTA
**Shape:** Paragraph
**Posting time:** 11:30 ET (after article publishes)

### Option A — Safe
The inflation number everyone's talking about is actually the smaller story. The bigger one is buried in the same release: services inflation, which covers rent, healthcare, and childcare, isn't slowing at all, and that's where most of your monthly budget actually lives. Today's piece walks through what that means for the next six months of household costs and what the Fed can realistically do about it.

Full piece: https://thecivicnode.substack.com/p/services-inflation-q1-2026

**Image:** Use Substack hero from https://thecivicnode.substack.com/p/services-inflation-q1-2026

### Option B — Safe
Here's the thing about this week's inflation report: the part that's slowing is goods (TVs, cars, appliances dropping in price). The part that's NOT slowing is services (rent, healthcare, childcare, car insurance) — and that's the part you feel every single month at home. Friday's piece pulls that apart and looks at why one keeps falling while the other one doesn't budge.

Full piece: https://thecivicnode.substack.com/p/services-inflation-q1-2026

**Image:** Use Substack hero from https://thecivicnode.substack.com/p/services-inflation-q1-2026

### Option C — Safe
The April inflation number looked like good news on the surface. Underneath it, the part of inflation most households actually feel is still running well above the Fed's target — services like rent, healthcare, childcare, and insurance show no sign of slowing. Worth understanding the gap before the next rate decision comes around in mid-June.

Full piece: https://thecivicnode.substack.com/p/services-inflation-q1-2026

**Image:** Use Substack hero from https://thecivicnode.substack.com/p/services-inflation-q1-2026

**Recommendation:** Default to Option A (cleanest narrative arc — "what you think it is vs. what it actually is"). Option B if the previous week's posts already covered the goods/services split; this one reinforces. Option C if the Fed meeting context matters more this week than the household-budget angle.
```

## Self-checks against the quality bar

For Example 1 (Tuesday Awareness):
- ✅ All 3 options ≤30 words (A: 25, B: 27, C: 24)
- ✅ No closed em dashes (caption length)
- ✅ Specific anchors (interest payments $881B, defense $880B)
- ✅ One warmth-marker in B ("honestly"); zero in A and C
- ✅ No banned vocab, no vague placeholder verbs
- ✅ All image guidance concrete (AI prompts with specific scene)
- ✅ All Safe (no news triggers required)
- ✅ No link (matches Awareness CTA rule)

For Example 2 (Friday Flagship CTA):
- ✅ All 3 options within 50-80 words (A: 66, B: 62, C: 55)
- ✅ Em dash usage: zero in A, one in B ("services ... — and that's the part"), one in C (introducing the services-list elaboration) — all within paragraph allowance (max 1 per post)
- ✅ Specific anchors (services inflation, six months, rent/healthcare/childcare/insurance, mid-June rate decision)
- ✅ Hard link on its own line at end
- ✅ No banned vocab, no vague placeholder verbs, no "of course/naturally/predictably"
- ✅ Substack hero image source specified
- ✅ All Safe (article is live by posting time)
