---
name: design-from-donor
description: Build any visual deliverable by extracting a real page's design and working from its measured values. Use for lead magnets, calculators, landing pages, client reports, decks, branded documents and any HTML a client or prospect will see. Requires a donor page and refuses to start without one.
---

# Design from a donor

Every visual build starts by extracting a real page and reading its measured values. No path through this skill begins with a description of a look.

## The rule that makes this work

**No donor, no build. Ask for one and stop.**

Not a mood board, not "clean and modern", not an adjective. A URL. If nobody will name one,
say plainly that you can't start, and offer the library below.

This is a hard gate rather than a preference, and it came out of a measured test on
8 September 2026. The same brief was built twice, once following the house design standard in
full and once with no guidance at all. Both were rejected on sight. The standard prevented
faults, catching 3 em dashes the unguided version shipped, and still produced nothing anyone
wanted to look at, because a list of prohibitions carries no taste. The same brief built from
an extracted page was accepted immediately.

A rule list can tell you what to avoid. Only a real page can tell you what to do.

## Where the donor comes from, in order

1. **The client's own site.** Almost always right, and it's the only source that makes the
   deliverable genuinely theirs. Use it whenever their branding is good enough to carry the
   piece.
2. **A page the client names.** If they say "we want something like X", extract X.
3. **The library** in `donors/` beside this skill, when the client's own branding is too weak to
   build on. 6 profiles, each measured from a live page:

   | Donor | Register |
   |---|---|
   | `listkit` | bright SaaS, navy and one blue, fully rounded, negative tracking |
   | `outreachify` | quiet SaaS, almost no fills, one indigo moment, zero tracking |
   | `cloudflare` | editorial tech, near black on white, orange accent, medium weight display |
   | `withallo` | dark green bands, 300 weight body, a yellow pop |
   | `glaze` | DTC beauty, warm brown on pink, positive tracking, pill buttons |
   | `historic-newspapers` | editorial ecom, heavy condensed uppercase, high contrast |

4. **A fresh extraction** of any page whose design is right for the job.

Borrowing a donor's language for an unrelated client is deliberate house practice, decided
7 Sep 2026. Say which donor a build descends from in the build stamp, so the next build can
diverge from it rather than repeating it.

## The loop

### 1. Extract

```bash
python tools/page_fidelity.py <url> --height 1600 --out spec.json --shot reference.png
```

Reads text at run level, boxes with their fills and radii, media with inline SVG where it is
small enough to lift, and hover states measured by actually hovering.

### 2. Profile

```bash
python tools/brand_profile.py spec.json --md --out brand-profile.md
```

Turns hundreds of rows into what a new artefact asks: body ink, accents by how often they're
really used, faces, weights, the type scale, the tracking curve and the button, band and card
treatments with their shapes.

### 3. Look at the screenshot before you build

The profile reads the DOM, and on some brands the DOM isn't where the design lives. Measured
on a beauty brand: its hero is a video, its headline never appears in the DOM at all, and the
profile had taken its button shape from the cookie banner. The page built from that profile
was wrong in every way that mattered.

So read `reference.png` yourself and decide which of these the donor is:

- **Typography led.** The display type is real text. The profile carries most of the design
  and you can lean on it.
- **Image led.** The hero is a photograph or a video and the type sits inside it. The profile
  carries the palette and little else. The screenshot is your primary source, and you build
  generous image areas rather than filling the space with small drawings.

### 4. Build

Use the measured values exactly. Never substitute a nearby colour, never add a weight the
donor doesn't use, and apply the tracking curve at every size, because tracking is the
signature people read without being able to name it.

### 5. Gate it

```bash
python tools/fidelity_loop.py <url> --out ./work --rounds 3
```

For a reproduction, that runs the whole loop and stops on converged, plateau or exhausted. For
a new artefact in a donor's language, check by hand that no colour, weight or face appears
that the donor doesn't use.

Then the parts of the house standard that still apply: the tells, the hard rules, the render
gates. Those live in the `design-system` skill and this skill doesn't replace them.
It replaces the part that told you to pick from 4 house builds.

### 6. Render it and look

A green check and a wrong looking page are perfectly compatible. Measured twice on 8 September:
a reproduction reported 0 defects while underlining a bar the original did not, and another
reported 0 defects while missing every photograph on the page.

Screenshot the result and read it. The comparator scores type, colour and geometry. It can't
score whether a page looks like anything.

## What this cannot do

- **Exact font cuts.** A licensed face isn't on Google Fonts, and a substitute renders at a
  different width. One reproduction matched every letter-spacing value and still ran 9%
  tighter, because the cut differed. The loop reports this as a rendered width defect and
  plateaus on it honestly rather than pretending.
- **Photography.** Nothing here copies a client's images, deliberately. Build image areas of
  the right shape and leave them empty.
- **Section patterns.** The profile carries atoms rather than architecture, so a generator
  still invents its own section rhythm and grid. Watch for a card grid appearing in a brand
  that has no cards.
