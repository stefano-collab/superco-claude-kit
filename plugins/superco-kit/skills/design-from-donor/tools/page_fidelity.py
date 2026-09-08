"""Extract everything needed to rebuild a page region, not just its text styles.

`html_fidelity.py` reads text and reads it well, but it has 3 limits that cap how close a
reproduction can get, all found on 8 Sep 2026 rebuilding the listkit.io hero:

1. It skips any element that has children, so a headline containing an inner coloured span
   loses every word around that span. On a heading-heavy page most of the display type
   silently disappears.
2. It captures no boxes. Buttons, pills, cards and section bands are what a page LOOKS like,
   and none of their fills, radii, borders or shadows were recorded.
3. It captures no images or logos, not even their position and size, so a rebuild has no idea
   something belongs there.

This reads all 3. Text comes from an element's OWN text nodes, so a parent and its inner span
are both recorded with their own colours.

Run:  python page_fidelity.py <url> [--height 1500] [--width 1280] [--out spec.json]
      python page_fidelity.py <url> --shot before.png     # capture early, before overlays
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

READ = r"""(maxY) => {
  const px = v => Math.round(parseFloat(v) || 0);
  const vis = el => {
    const c = getComputedStyle(el);
    return c.display !== 'none' && c.visibility !== 'hidden' && parseFloat(c.opacity) > 0.05;
  };
  const text = [], boxes = [], media = [];

  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    const y = Math.round(r.top + window.scrollY);
    if (y > maxY || r.width === 0 || r.height === 0 || !vis(el)) continue;
    const c = getComputedStyle(el);

    // 1. This element's OWN text, ignoring text that belongs to its children. This is the
    //    fix for the leaf-only rule: a headline and its inner span both get recorded.
    let own = '';
    for (const n of el.childNodes) if (n.nodeType === 3) own += n.nodeValue;
    own = own.replace(/\s+/g, ' ').trim();
    if (own) {
      text.push({y, x: Math.round(r.left), w: Math.round(r.width), tag: el.tagName.toLowerCase(),
        text: own.slice(0, 140),
        font: c.fontFamily.split(',')[0].replace(/["']/g, ''),
        size: px(c.fontSize), weight: c.fontWeight, colour: c.color,
        ls: c.letterSpacing === 'normal' ? '0px' : c.letterSpacing,
        lh: c.lineHeight, tt: c.textTransform, align: c.textAlign,
        decoration: c.textDecorationLine === 'none' ? '' : c.textDecorationLine});
    }

    // 2. Anything that reads as a box: it has a fill, a border, a radius or a shadow.
    const bg = c.backgroundColor, img = c.backgroundImage;
    const hasFill = bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent';
    const hasImg = img && img !== 'none';
    const hasBorder = px(c.borderTopWidth) || px(c.borderBottomWidth) || px(c.borderLeftWidth);
    const hasShadow = c.boxShadow && c.boxShadow !== 'none';
    const hasRadius = px(c.borderRadius) > 0;
    if ((hasFill || hasImg || hasBorder || hasShadow) && r.width > 8 && r.height > 4) {
      boxes.push({y, x: Math.round(r.left), w: Math.round(r.width), h: Math.round(r.height),
        tag: el.tagName.toLowerCase(),
        bg: hasFill ? bg : '', bgImage: hasImg ? img.slice(0, 220) : '',
        radius: hasRadius ? c.borderRadius : '',
        border: hasBorder ? (c.borderTopWidth + ' ' + c.borderTopStyle + ' ' + c.borderTopColor) : '',
        shadow: hasShadow ? c.boxShadow.slice(0, 160) : '',
        label: (el.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 40)});
    }

    // 3. Images, logos and icons. Position and size at minimum, and the markup for a small
    //    inline svg so a logo can be reproduced rather than guessed at.
    const tag = el.tagName.toLowerCase();
    if (tag === 'img' || tag === 'svg' || tag === 'picture' || tag === 'video') {
      const rec = {y, x: Math.round(r.left), w: Math.round(r.width), h: Math.round(r.height), tag};
      if (tag === 'img') { rec.src = (el.currentSrc || el.src || '').slice(0, 200); rec.alt = el.alt || ''; }
      if (tag === 'svg' && el.outerHTML.length < 4000) rec.svg = el.outerHTML;
      media.push(rec);
    }
  }

  // 4. Motion. Static computed styles say nothing about what the page DOES, so a rebuild
  //    lands still and lifeless next to a site that lifts, fades and slides. Hover styles
  //    live in the stylesheets rather than in any element, so read the rules directly.
  const hover = [], motion = [];
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (e) { continue; }   // cross origin, skip quietly
    if (!rules) continue;
    for (const rule of rules) {
      const sel = rule.selectorText || '';
      if (sel && /:hover|:focus-visible/.test(sel) && rule.style && rule.style.length) {
        const decls = [];
        for (const prop of rule.style) decls.push(prop + ': ' + rule.style.getPropertyValue(prop));
        if (decls.length) hover.push({selector: sel.slice(0, 120), css: decls.join('; ').slice(0, 300)});
      }
      if (rule.type === CSSRule.KEYFRAMES_RULE && motion.length < 12) {
        motion.push({name: rule.name, css: rule.cssText.slice(0, 400)});
      }
    }
  }

  // transitions and transforms that are already sitting on elements
  const transitions = [];
  for (const el of document.querySelectorAll('a, button, [role=button], .btn, .card')) {
    const c = getComputedStyle(el);
    if (c.transition && c.transition !== 'all 0s ease 0s' && transitions.length < 14) {
      transitions.push({tag: el.tagName.toLowerCase(),
                        label: (el.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 30),
                        transition: c.transition.slice(0, 160),
                        cursor: c.cursor});
    }
  }

  const body = getComputedStyle(document.body);
  return {page: {width: window.innerWidth, bg: body.backgroundColor,
                 font: body.fontFamily.split(',')[0].replace(/["']/g, '')},
          text, boxes, media,
          hover: hover.slice(0, 30), keyframes: motion, transitions};
}"""


WATCH = ("backgroundColor", "color", "borderColor", "boxShadow", "transform",
         "opacity", "textDecorationLine", "borderRadius", "filter", "scale")


def measure_hover(pg, max_y: int, limit: int = 10) -> list[dict]:
    """Hover each interactive element and record what actually changed.

    Reading `:hover` out of the stylesheets was tried first and it fails on site builders.
    Measured 8 Sep 2026 on a Framer site: every hover rule came back as an internal CSS
    variable, the keyframes belonged to Calendly and Framer, and every transition read `all`.
    None of it described the design.

    Hovering and diffing the computed style works whatever the CSS is written in, and it
    returns the value that actually lands rather than the variable that points at it.
    """
    out = []
    try:
        handles = pg.query_selector_all("a, button, [role=button]")
    except Exception:                               # noqa: BLE001
        return out
    for h in handles:
        if len(out) >= limit:
            break
        try:
            box = h.bounding_box()
            if not box or box["y"] > max_y or box["width"] < 24 or box["height"] < 16:
                continue
            before = h.evaluate("el => { const c = getComputedStyle(el); const o = {};"
                                "for (const k of %s) o[k] = c[k]; return o; }" % list(WATCH))
            h.hover(timeout=1200)
            pg.wait_for_timeout(320)                # let a transition finish
            after = h.evaluate("el => { const c = getComputedStyle(el); const o = {};"
                               "for (const k of %s) o[k] = c[k]; return o; }" % list(WATCH))
            changed = {k: [before[k], after[k]] for k in before if before[k] != after[k]}
            if changed:
                out.append({"label": (h.inner_text() or "").strip()[:34],
                            "tag": h.evaluate("el => el.tagName.toLowerCase()"),
                            "transition": h.evaluate("el => getComputedStyle(el).transition")[:120],
                            "changes": changed})
        except Exception:                           # noqa: BLE001
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--height", type=int, default=1500)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--out", default="spec.json")
    ap.add_argument("--shot", default="")
    ap.add_argument("--settle", type=int, default=1400,
                    help="ms to wait. Short on purpose: chat widgets and cookie bars mount late "
                         "and are not part of the design.")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": a.width, "height": 900}, device_scale_factor=2)
        pg.goto(a.url, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(a.settle)
        if a.shot:
            pg.screenshot(path=a.shot, clip={"x": 0, "y": 0, "width": a.width, "height": a.height})
        spec = pg.evaluate(READ, a.height)
        spec["hover_measured"] = measure_hover(pg, a.height)
        b.close()

    Path(a.out).write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")
    print("%s  %dpx x %dpx" % (a.url, a.width, a.height))
    print("  text runs %d, boxes %d, media %d, hover rules %d, keyframes %d, transitions %d"
          % (len(spec["text"]), len(spec["boxes"]), len(spec["media"]),
             len(spec.get("hover", [])), len(spec.get("keyframes", [])),
             len(spec.get("transitions", []))))
    print("  -> %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
