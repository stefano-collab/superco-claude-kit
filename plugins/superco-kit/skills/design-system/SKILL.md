---
name: design-system
description: The design gate. The AI tells and what to do instead, the hard rules, brand and licence, plus both render gates. Read it before shipping any page, calculator, report or branded document. Direction comes from the design-from-donor skill, so this file checks work rather than starting it.
---

# Design system, the gate

This says what a visual deliverable must not do, and how it gets checked. It doesn't say where
the design comes from.

## Direction comes from a donor

Use the `design-from-donor` skill. It extracts a real page, reads its measured values and
builds from those, and it refuses to start without a donor.

That split came out of a measured test. The same brief was built twice, once following a full
design standard and once with no guidance at all. Both were rejected on sight. The standard did
prevent faults, catching 3 em dashes the unguided version shipped, and it still produced
nothing anyone wanted to look at. A list of prohibitions carries no taste. The same brief built
from an extracted real page was accepted immediately.

So the rules stayed here and the direction moved to the donor.

## What to do with this file

Read it before you ship, not before you start. The tells below are the ones that make a page
read as machine-made, and the hard rules are the ones that get noticed when they're broken.

One more gate worth running on anything built from a donor: check that no colour, weight or
typeface appears in your build that the donor doesn't use. An invented accent is the fastest
way to make something look adjacent to a brand rather than part of it.

And look at the rendered page. Measured twice: a build reported 0 defects while underlining a
bar the original didn't, and another reported 0 defects while missing every photograph on the
page. A checker scores type, colour and geometry. It can't score whether a page looks like
anything.

# Part 3 - The tells, and the do-instead

**Colour**
- Tell: pure `#000`/`#fff`; flat grey text (`#666`); the default saturated indigo/violet
  (`#6366F1` is the "an AI made this" accent); rainbow or purple-to-pink hero gradients.
- Do: near-black text (`#0A0A0B`/`#141414`), off-white ground with a faint warm or cool tint
  (not pure white, and *not* the overused warm-cream `#F4F1EA`). Build a real 8-10 step ramp
  per hue in HSL/OKLCH. **Tint greys toward the brand hue** ("greys don't have to be grey").
  One disciplined accent used on <10% of the surface. Gradients only low-contrast and
  same-family.

**Typography**
- Tell: Inter/Roboto/Space Grotesk at one weight; headings only ~1.3x body; centred everything;
  default line-height.
- Do: **strong contrast** - display heading >=3x body size, tight tracking on large text
  (`letter-spacing:-.02em` to `-.03em`), a real weight jump (700/800 head vs 400 body), and at
  least one characterful, non-default face. Body `line-height:1.5-1.6`, headings `1.05-1.15`,
  measure <=65ch. Left-align long text; centre only short hero lines.

**Layout**
- Tell: one narrow centred column; perfect symmetry; identical 3-card grids; the exact default
  order (hero -> 3 features -> testimonial -> CTA); edge-to-edge sameness.
- Do: **intentional asymmetry** - off-centre hero, a 60/40 split, one element that breaks the
  grid. Vary section rhythm. A generous max-width (~1080-1200px) with some content sitting
  deliberately narrow. You don't have to fill the screen.

**Structural devices must mean something.** Numbering, eyebrows, dividers and labels encode
something true about the content or they are decoration. `01 / 02 / 03` is legitimate when the
content genuinely is a sequence - a real process, a walked-through report - and a tell when it
is three unordered features wearing numbers.

**One channel, one meaning.** Do not encode a measured value and an uncertainty bound in the
same visual channel. The the report build split chart drew real counts as solid bars and "none found,
ceiling is N" as dashed bars of the same kind, on the same axis. Fourteen dashed against eight
solid, scattered down the rows with no visible rule, and the reader's reaction was the correct
one: *"some have dotted lines some dont. why?"* The uncertainty had swallowed the finding. Two
fixes, and it needs both: **sort so the two states form blocks** with a labelled divider rather
than alternating, and **move the bound off the chart** into the click-through beside the
evidence. A chart shows what was measured; a caveat that applies to a subset of rows belongs
where that subset is explained.

**Every stacked section carries its own exhibit.** Covered under the report build above, and it is
the failure that costs the most rework. Read the assembled page top to bottom before shipping:
five sections drawing the same two-panel chart is one exhibit with five captions, and it reads
as filler.

**Spacing**
- Tell: uniform ~16px gaps; cramped; ambiguous spacing (equal space above/below a heading so it
  doesn't group with its text).
- Do: a **fixed scale only** (4/8-based: 4,8,12,16,24,32,48,64,96,128). Start with too much
  whitespace, then subtract. Group related items tighter, separate unrelated blocks wider -
  proximity is the cheapest hierarchy. Section padding >=96px vertical reads premium; 32px
  reads bootstrap-template.

**Components**
- Tell: glassmorphism cards; uniform `border-radius:8px` on everything; a border on every box;
  symmetric `0 4px 6px rgba(0,0,0,.1)` shadows; emoji pill badges.
- Do: **fewer borders** - separate with background contrast, space, or a layered shadow (a tight
  ambient + a soft cast, single light source; the two-page build's `_shared.css` is the worked example). A
  deliberate radius language (crisp 2-4px throughout, or one confident large radius - not
  random). No emoji furniture.

**Motion**
- Tell: everything fades/slides in on scroll with the same 500ms+ AOS animation; bouncy springs
  on serious content; hover = colour change only.
- Do: motion **<300ms, `ease-out`, `transform`+`opacity` only**, `prefers-reduced-motion`
  honoured, and animate as *few* things as possible. High-frequency actions get little motion.
  Reserve one signature moment for expressiveness.

**An animated numeral must never read its target value out of the DOM.** A count-up or scramble
that does `const final = el.textContent` on entry will, on a second pass over an element still
animating, capture the *garbled* string as the value to settle on - and it sticks. The
the report build report displayed "27,543 stores" and "9.22x" where the truth was 22,363 and 2.49x; a
probe hammering one node six times settled the old code on 60,654 against a true 22,363. Capture
the value once into `dataset.*`, allow one timer per node, and restore the true value on an
unconditional timer. Same discipline for any deferred render - give each a generation number so
a superseded one drops instead of overwriting whatever took the stage. Full write-up: memory
`animation-must-not-own-the-value`.

**Fake chrome and fabricated data** (the two most damaging tells, because they cost credibility
as well as looking generic)
- Tell: a mocked-up browser window with three traffic-light dots, a fake address bar, a fake app
  sidebar, or a re-drawn dashboard used as decoration. Instantly recognisable as AI filler and
  the single most-copied "product page" cliche.
- Tell: invented metric cards - "98% accuracy", "3.2x faster", "10,000+ shipments" - numbers with
  no source, dropped in because the layout had a gap.
- Do: show the real thing. Our assets ARE the product, so a live preview of the actual tool beats
  a drawing of one (the calculator build's hero preview is the pattern). If a figure appears anywhere on the page
  it must be traceable to a source; a number we cannot source does not go on the page, no matter
  how good the layout looks with it. This is a client-credibility rule, not a taste rule.

**Nav and footer**
- Tell: the default AI nav (wordmark left, three or four inline links, one filled button hard
  right) and the default AI footer (four columns of links, a social row, a tiny copyright line).
  Both are fingerprints.
- Do: on a single-purpose page most of that chrome should not exist at all. A wordmark and one
  action is usually the whole nav - SuperCo's `.head` is a centred logo and nothing else. A
  footer that is one line of attribution beats four invented columns.

**Imagery / texture**
- Tell: no imagery, or generic stock / pastel-blob "corporate Memphis" AI illustrations; flat
  single-colour backgrounds.
- Do: real texture - subtle noise/grain (2-4% opacity), a faint dot/line grid used *sparingly and
  intentionally* (the report build's 14px dot paper), a soft radial glow behind the hero (the two-page build's
  fixed ellipse), or real product/data visuals. One crafted detail beats a flat template. A faint
  grid hero background is itself an AI tell if it's the only idea - texture with intent, not as
  filler.

## What actually separates studio work from clean-but-generic

- **Art direction / a point of view.** Commit to a mood before touching CSS. Every choice serves
  it.
- **A signature motif.** One repeated custom detail that's recognisably this page - SuperCo's
  stepped loading checklist, the report build's crop marks, the calculator build's gold arrow. It's what you'd
  recognise on a second page by the same hand.
- **Type contrast + a characterful face.** The fastest premium signal.
- **Intentional asymmetry and restraint.** Confidence to leave space empty and break symmetry
  once. Two type sizes and one accent doing 90% of the work reads more expensive than more.
- **Micro-detail.** `tabular-nums` on figures, aligned units, optical (not mathematical)
  centering, crafted focus/hover/active/disabled states, consistent shadow light source. The
  invisible details are what the eye reads as "someone cared."
- **Spend the boldness in one place.** Let the signature element be the one memorable thing and
  keep everything around it quiet. Before shipping, remove one accessory.

# Part 4 - The hard rules (follow every time)

1. No pure black or white. Near-black text, tinted off-white ground. Tint every grey toward the
   brand hue.
2. One accent, disciplined. Never the default indigo. Build a ramp; use the accent on <10% of
   the surface.
3. Spacing from a fixed scale only (4/8-based). No arbitrary px. Section padding >=96px.
4. Type contrast mandatory: display >=3x body, tight tracking on large text, a clear weight
   jump, one non-Inter face, body measure <=65ch.
5. Fewer borders. Separate with space, contrast, or a layered shadow (single light source).
6. Break symmetry once. Off-centre hero or a 60/40 split; never a stack of identical centred
   sections in default order.
7. Motion budget: <=300ms, `ease-out`, `transform`/`opacity` only, `prefers-reduced-motion`
   honoured, few elements.
8. High-frequency output updates instantly with minimal motion; reserve expressive motion for
   one signature moment.
9. One intentional texture layer (subtle noise, a faint grid, or a soft hero glow). Never a flat
   single-colour page - but never texture as filler either.
10. Ship a signature motif - one repeated custom detail that makes it recognisably not a
    template.
11. `font-variant-numeric:tabular-nums` on all figures; align currency/units; craft the
    interaction states.
12. Whitespace first, then subtract. Group by proximity so hierarchy comes from spacing before
    size or colour.
13. **Every interactive element is at least 44x44px to a finger.** Not how big it *looks* - how
    big its box is. This is the rule that has actually bitten, twice.
14. Name the tone, the source build and the diversification axes out loud before writing CSS;
    stamp them into the `<style>` block and append them to `knowledge-base/design-log.json`. On
    a white-labelled or client-owned deliverable, use the client-confidential stamp form with no
    "your own brand".
15. Differ from the previous build on at least two of the three axes (paper band, display style,
    accent hue).
16. No fake browser chrome, no re-drawn app UI, no invented metrics. Every figure on the page
    traces to a source.
17. Run the slop test against the rendered screenshot before handing anything over, and report
    the score honestly. Part 6 below.
18. **An animated numeral never re-reads its target from the DOM**, and every deferred render
    claims a generation number. Assert the rendered values equal the source data *after* abuse -
    burst clicks, ten re-renders in half a second - not only after a clean load.
19. **Read the assembled page top to bottom before shipping.** Sections designed as switchable
    lenses render as the same exhibit five times when stacked.
20. **When the donor is a live site, extract its computed styles including pseudo-elements.**
    Never build from a description of a screenshot.
21. **Nothing on a report is hand-typed.** Every figure is computed by the generator and the
    build asserts its own consistency.

## Touch targets: the slider trap (read before styling any input)

A hairline slider is the house look, and it produces a broken control if you style it naively:

```css
/* WRONG - ships a 2px touch target. Both the another calculator and the calculator build calculators shipped this. */
input[type=range]{-webkit-appearance:none;height:2px;background:var(--hairline)}
input[type=range]::-webkit-slider-thumb{width:17px;height:17px;/* drawn big, but... */}
```

The thumb is *drawn* 17px, but Chrome only dispatches pointer events inside the input's own
border box - 2px tall. On a phone a finger landing on that ribbon makes a native range input jump
straight to that x-position, and landing a few px off scrolls the page instead. This presents as
"the slider jumps on mobile" and is very hard to diagnose from the symptom - the calculator build burned several
rounds chasing it as a scroll-anchoring bug.

Fix: keep the visual track thin, but grow the input's box on touch devices only, so the desktop
rendering stays pixel-identical.

```css
@media (pointer:coarse){
  input[type=range]{height:44px;background:transparent;margin:0}
  input[type=range]::-webkit-slider-runnable-track{height:2px;background:var(--hairline);border-radius:2px}
  input[type=range]::-webkit-slider-thumb{margin-top:-7.5px}   /* (track - thumb) / 2, border-box */
  input[type=range]::-moz-range-track{height:2px;background:var(--hairline);border-radius:2px}
}
```

Scoping to `pointer:coarse` rather than a width breakpoint is deliberate: it targets touch input
itself, so a touch laptop is covered and a narrow desktop window is not needlessly relaid out.

## Calculator-specific craft

- **The output panel updates instantly.** A calculator is a high-frequency action, so the result
  recomputes with no fade, no count-up, no stagger. Reserve expressive motion for one signature
  moment elsewhere on the page.
- **Never animate the result value.** Rule 18 bites hardest here, because the result *is* the
  product.
- **`tabular-nums` on every figure.** Figures that shift width as they update look broken, and on
  a calculator they update constantly. the calculator build sets it once on `body`.
- **Show the model.** The transparent-model pattern (`interactive-lead-magnet/references/build-qa-deploy.md`)
  is the point of the asset: the prospect can see what the number is made of. A black-box result
  is worth less than a smaller number with its workings shown.
- **Fix the height of any block whose value changes**, so the layout does not jump between
  states.

# Part 5 - Brand, licence and fonts

Anchor to the client's real cues: the client's own brand file, or the brand file produced at
intake. Format spec and the contrast linter: your brand file format and
a contrast linter. When the client's own site branding is weak, Stef may
grant explicit creative licence to go beyond it - take the anti-AI/premium direction while keeping
the real accent and logo. Do not invent a brand the client doesn't have; do elevate a weak one
when told to.

**Where the client's brand FACTS come from: the client's brand kit.** Palette, type, both
logo lockups, radii and rhythm, measured off the client's live site by the `brand-kit` skill -
inline its `tokens.css` and reference the `--brand-*` names rather than sampling a screenshot by
eye. Two things to read before trusting it: `manifest.json` must show `logo.verified: true` (an
unverified lockup can be a customer's mark lifted from a "trusted by" wall), and the **Inferred
values** section of `brand-kit.md` lists everything that was NOT observed and therefore needs a
decision. **The kit supplies tokens, never layout** - layout and hierarchy stay with this file and
its four house donors, and a kit feeds a donor rather than replacing one.

**Brand fidelity outranks internal look-diversification.** A client-branded asset is not a free
choice, so a real documented brand can legitimately fail the diversification rule or a slop-test
font gate. State the override out loud in the build stamp comment with the reason - the two-page build's
`_shared.css` header is the model. Do not silently fail the gate and do not edit the threshold.

**Mine the client's own shipped assets, not just their website.** A marketing site is built by
whoever built the site; a shipped client deliverable is the house system as actually used, and it
is what the prospect will already have seen. Before extracting from a website, check
their existing deliverables and the intake folder for an existing branded asset. Unzip a docx
(`word/media/` for logos, `word/document.xml` for `w:color`, `w:fill`, `w:ascii` fonts, `w:sz`
sizes). Record what you found in the client's own brand file so the next build does not
re-derive it.

**Fonts and self-containment.** The page is usually a single hosted file, so linking Google Fonts
is fine (no CSP on a normal host). Always give a strong fallback stack. If the page is ever
previewed as a claude.ai Artifact the CSP blocks font CDNs - inline the face as a data URI there,
as SuperCo does with its `/*TOKEN*/` placeholders. Prefer characterful faces over the
Inter/Space-Grotesk defaults.

**A brand font's ligatures can silently rewrite legal copy.** "trademarks" rendered as "(tm)s" in
a SuperCo footer because Bianco Sans carries a `tm` ligature, and nothing in the source was wrong
so no text check could catch it. On any block whose wording has to be exact - disclaimers,
liability and trademark notices, legal entity names - set
`font-variant-ligatures:none;font-feature-settings:"liga" 0,"dlig" 0,"clig" 0,"calt" 0`, and read
the rendered block as an image before shipping.

# Part 6 - The gates

Nothing ships unrendered. Which gate applies depends on what the deliverable is.

## The slop test (HTML pages)

Two halves. Report the score honestly in the handover line: `Slop test: 26/29 - fails: 7, 21, 24`.
A score you did not actually run is worse than no score, because it launders a guess as a check.
If you did not run it, say so.

**Half 1 - static, 19 gates, scripted.** Run it on the **first** compile, not at the end: the
failures are all two-line CSS fixes and they are expensive to discover after the copy is settled.

```bash
python .claude/skills/interactive-lead-magnet/assets/slop_test.py <file.html>
```

Exits 1 on any CRITICAL failure. Covers: build stamp + axes, default AI indigo, pure black/white,
default fonts, type contrast, tabular-nums, reduced-motion, `transition-all`, motion over 300ms,
bounce easing, hover-scale, fake browser chrome, focus-visible, `z-index:9999`, radius uniformity,
em/en dashes, emoji, and the coarse-pointer slider trap. Gate spec:
`.claude/skills/interactive-lead-magnet/references/slop-test.md`.

Do not edit the thresholds to make a build pass. Fix the build.

**Half 2 - visual, 10 gates, judged from the screenshot.** Render with headless Chrome, then
answer each of these about the actual image. **Every answer must be "no".**

| # | Gate | Fails if |
|---|---|---|
| 20 | Default section order | Hero, then three identical cards, then testimonial, then CTA - the stock sequence |
| 21 | Perfect symmetry | Everything centred, nothing breaks the grid, no 60/40 split anywhere |
| 22 | Identical section rhythm | Every band the same height and padding, so the page reads as one texture |
| 23 | No signature motif | Nothing you would recognise on a second page by the same hand |
| 24 | Flat ground | No texture layer at all - no grain, no considered grid, no hero glow |
| 25 | Cramped vertical space | Section padding visibly under ~96px; content touching its container |
| 26 | Borders doing all the separating | A visible box around nearly every group instead of space or contrast |
| 27 | Weak type hierarchy | Display and body look close in size; nothing anchors the page |
| 28 | Decorative filler | Icon tiles, stock-ish illustration, pastel blobs, emoji badges |
| 29 | Invented figures | Any number on the page you cannot trace to a source |

Gate 29 is a business risk rather than a taste risk. Treat a failure there as CRITICAL regardless
of how the rest scores.

**Two conditional waivers, and only with the reason stated out loud.** Gate 24 is waived where a
deliberately austere or utilitarian tone means flatness IS the direction. Gate 21 is waived for a
single-column document or calculator where a centred measure is the correct reading experience -
not because the layout was easier that way. Nothing else is waivable.

**The point is the second pass.** First render almost never clears; the value is screenshotting
your own work, scoring it honestly and going back. A build that passed first time usually means
the test was run carelessly.

## Mobile QA (HTML pages)

Run `.claude/skills/interactive-lead-magnet/assets/mobile-qa.js` against the hero **and** the
mocked result view: `overflowPx` must be 0 and no control may be under 44px. `--window-size` does
NOT give you a phone viewport, and it does not merely differ - headless clamps the layout
viewport to a floor (504 CSS px when asked for 430 on this machine), so a narrow render
invents horizontal overflow that the real page does not have. Probe it before believing
any width finding: render a one-line page that prints `document.documentElement.clientWidth`
and read the number back. If the result view hides behind an API round-trip, build the mock
harness and render every result branch with `assets/render-qa.js` in the first ten minutes - a
naive screenshot QAs only the hero.

## The branded-document render gate (docx and PDF)

Mandatory before any branded PDF or docx reaches Stef - **ours or a client's**. Branded-doc layout
was the single biggest manual time-sink of mid-July 2026 (the SuperCo PDF fan-out alone ran ~890
messages), and nearly every correction was the same handful of machine-checkable faults caught by
Stef eyeballing a screenshot. Target: turn ~20 correction rounds into 1-2.

**Procedure.** Generate the doc. If it is a docx, render to PDF with LibreOffice (not OpenOffice -
headless fails), auto-detecting `soffice` and using an isolated profile so a running instance does
not block it (memory `docx-pdf-render-libreoffice`):

```bash
soffice --headless --convert-to pdf --outdir <outdir> "<file.docx>" \
  -env:UserInstallation=file:///<isolated-temp-profile>
```

Then **look at every page** - Read the rendered PDF, passing the full `pages` range, since the Read
tool renders PDF pages as images. Run the checklist. Fix and re-render on any fail. Only a clean
doc is handed over. If something is genuinely a judgement call rather than a clear fault, surface
it with the doc rather than guessing.

**Layout / spacing**
- [ ] No text overlap - no heading sitting on body text, no element over another.
- [ ] No content overflowing the page edge or print margin; nothing clipped.
- [ ] Gap between a callout / social-proof box and the CTA is within range - not a dead gap.
- [ ] No dead white space under or around a logo.
- [ ] Margins and alignment consistent page to page.

**Designed-PDF layout** (black covers, case-study pages, image blocks). Added 24 July 2026 after
the AGNODOS proposal: every one of these got through the gate above and was caught by Stef
instead. They are the difference between one correction round and four.
- [ ] Gap between a client logo and the next element is roughly one logo-height, not a void.
- [ ] Section spacing is the template's native gap. Spacing was NOT widened to fill a short page
      (white space at the foot is fine; stretched rows are not).
- [ ] Every screenshot is framed (rounded white plate + thin stroke), never a raw crop.
- [ ] Screenshots end on a natural terminator (CTA button, section end), never mid-sentence or
      mid-list, and carry no cookie bar, promo teaser or popup.
- [ ] A half-width column is not followed by full-width body text under it. One measure per
      column, held down the page.
- [ ] Page number does not collide with a footer strip. If the last page carries the footer, it
      carries no page number.
- [ ] Nothing left in from a removed section - no stale contents entry, orphan heading, or asset
      variable no page uses.

**Headings / hierarchy**
- [ ] Heading level matches what was requested - no H1 where H2/H3 was specified.
- [ ] Body text is NOT in a heading colour.

**Brand / cleanliness**
- [ ] Logo shape consistent and correct - rounded where the brand uses rounded, same treatment
      across pages.
- [ ] No orphan subtitle, no explainer paragraph, no "Style: GrowthFlare" scaffolding line, no
      stray eyebrow Stef didn't ask for.
- [ ] Palette and fonts are the brand's, not a default.
- [ ] No placeholder text, `<...>` tokens, or Lorem left in.
- [ ] Font table read off the PDF (`page.get_fonts()`), not just the pages. A missing font falls back silently, and a Google variable font installs at its DEFAULT instance, which for Hanken Grotesk and Manrope is the lightest weight - body copy renders ExtraLight and bold is faked off Regular. Instantiate static 400/700 faces with `fontTools.varLib.instancer`.
- [ ] A coloured page ground sampled as PIXELS in the margin, never eyeballed. Docx page fill needs `displayBackgroundShape` set and often does not survive PDF export.
- [ ] Any rasterised logo has a transparent ground. One baked on white is an invisible white rectangle the moment the page is not white.

**Ground truth to seed the check from:** your own brand's own specs are in
your own brand's design file. SuperCo's are the exemplars in the `superco-branded-pdf`
skill - the approved logo treatment and the gap ratios Stef gave verbatim. When a new approved
exemplar appears, add its spec here so the gate tightens.

## Failure modes already survived

Read this list before shipping anything report-shaped. Every one of these actually happened.

- The same chart rendered in every section.
- A count-up animation displaying a **wrong number** permanently, because it re-read its target
  from the DOM.
- A deferred slide render landing after presentation mode was exited.
- Slides overflowing the viewport by 190-440px each.
- Print clipping the fourth KPI and overflowing the page.
- The home view showing less than presentation mode did, because a row rendered on one path only.
- Separator rules spanning the column instead of the viewport.
- `noindex` living only in a file the host silently ignored.
- Licensee names cut mid-bracket by a naive `split(",")[0]`, shipping "Disney (plus MoD" to a live
  client page.
- A brand font's `tm` ligature rewriting a trademark notice.
- A 2px slider touch target on two separate builds.

# Cross-references

- your own brand's design file - the other design file. Anything your own brand-branded.
- this skill - the prose half of the same standard. Every visual
  deliverable is checked against it too.
- `knowledge-base/design-log.json` - the diversification log. Every visual build appends.
- your brand file format - the per-client brand file format and the contrast
  linter.
- `.claude/skills/interactive-lead-magnet/` - the calculator build pipeline: intake brief,
  standard blocks, mechanic and open loop, data and honesty, build/QA/deploy, the slop-test
  script.
- `docs/DECISIONS.md` - where design architecture decisions land.

**The vendored Anthropic design skills** (`frontend-design`, `canvas-design`,
`web-artifacts-builder`) were archived on 8 August 2026 to
`archive/2026-08-08-vendored-design-skills/`. They carried competing guidance and were
overwritten on update, taking hand-added house rules with them. If one is ever restored it is
craft-only and loses to this file on every point of conflict.
