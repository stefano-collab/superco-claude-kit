#!/usr/bin/env python3
"""html_fidelity - the web half of the format-fidelity loop (see .claude/skills/format-fidelity).

A rendered page has no runs either; it has ELEMENTS with COMPUTED styles, and the computed style
is the truth - never the stylesheet, which says what the author asked for rather than what the
browser did after the cascade, the fallbacks and the media queries. So this opens the page in a
real Chromium (Playwright) and reads getComputedStyle on every element that owns visible text.

    python html_fidelity.py extract   <url-or-file>                  one line per text element: tag, font, size, weight, colour, bg, border, spacing
    python html_fidelity.py classdiff <exemplar> <candidate>          exit 1 if candidate uses a (tag-role, font, size, weight, colour) class the exemplar never does
    python html_fidelity.py sidebyside <exemplar> <candidate> <out.png>   full-page screenshots, exemplar left / candidate right

Accepts http(s) URLs or local .html paths. Widths are fixed at 1280px so two captures compare
like for like - a responsive page at two widths is two different designs.

For a client's PALETTE and TYPE TOKENS use the brand-kit skill, which already walks a site and
writes tokens.css. This tool answers a narrower question: does the thing I built render in the
same classes as the thing I was told to copy?
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8", errors="replace")

WIDTH = 1280
JS = r"""
() => {
  const out = [];
  const skip = new Set(['SCRIPT','STYLE','NOSCRIPT','TEMPLATE','SVG','PATH']);
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  let el;
  while ((el = walker.nextNode())) {
    if (skip.has(el.tagName)) continue;
    const own = Array.from(el.childNodes).filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
    if (!own) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    out.push({
      tag: el.tagName.toLowerCase(),
      text: own.slice(0, 80),
      font: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(),
      size: Math.round(parseFloat(cs.fontSize)),
      weight: cs.fontWeight,
      color: cs.color,
      bg: cs.backgroundColor,
      lh: Math.round(parseFloat(cs.lineHeight)) || 0,
      ls: cs.letterSpacing,
      tt: cs.textTransform,
      bb: cs.borderBottomWidth !== '0px' ? cs.borderBottomWidth + ' ' + cs.borderBottomColor : '',
      mt: Math.round(parseFloat(cs.marginTop)), mb: Math.round(parseFloat(cs.marginBottom)),
      y: Math.round(r.top + window.scrollY), x: Math.round(r.left), w: Math.round(r.width),
    });
  }
  return out;
}
"""


def _target(s: str) -> str:
    return s if s.startswith(("http://", "https://")) else Path(s).resolve().as_uri()


def capture(target: str, shot: str | None = None) -> list[dict]:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": WIDTH, "height": 900})
        pg.goto(_target(target), wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(500)
        rows = pg.evaluate(JS)
        if shot:
            pg.screenshot(path=shot, full_page=True)
        b.close()
    return rows


def rgb_hex(c: str) -> str:
    if not c.startswith("rgb"):
        return c
    parts = [float(x) for x in c[c.index("(") + 1:c.index(")")].split(",")]
    if len(parts) == 4 and parts[3] == 0:
        return "transparent"
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in parts[:3])


def sig(r: dict) -> tuple:
    return (r["tag"], r["font"], r["size"], r["weight"], rgb_hex(r["color"]))


def cmd_extract(target: str) -> None:
    rows = capture(target)
    print(f"{target}  {len(rows)} text elements at {WIDTH}px\n")
    for r in rows:
        extra = " ".join(x for x in (
            f"bg={rgb_hex(r['bg'])}" if rgb_hex(r["bg"]) != "transparent" else "",
            f"border-b={r['bb']}" if r["bb"] else "",
            f"tt={r['tt']}" if r["tt"] != "none" else "",
            f"ls={r['ls']}" if r["ls"] != "normal" else "") if x)
        print(f"  {r['tag']:6s} {r['font'][:14]:14s} {r['size']:>3}px w{r['weight']:<4} {rgb_hex(r['color']):8s} lh{r['lh']:<3} m{r['mt']}/{r['mb']:<3} y={r['y']:<5} {extra:30s} {r['text'][:50]!r}")


def cmd_classdiff(exemplar: str, candidate: str) -> int:
    A = {sig(r) for r in capture(exemplar)}
    B = {sig(r) for r in capture(candidate)}
    extra = B - A
    print(f"classes  exemplar={len(A)} candidate={len(B)}")
    for k in sorted(A):
        print(f"   exemplar {k}")
    if extra:
        print("  DIFFERS - candidate uses classes the exemplar never does:")
        for k in sorted(extra):
            print(f"   !! {k}")
    else:
        print("  MATCH  - every candidate class exists in the exemplar")
    print("\nVERDICT:", "PASS" if not extra else f"FAIL ({len(extra)} extra class(es))")
    return 0 if not extra else 1


def cmd_sidebyside(exemplar: str, candidate: str, out: str) -> None:
    from PIL import Image, ImageDraw
    work = Path(out).parent / "_html_fidelity_work"
    work.mkdir(parents=True, exist_ok=True)
    a, b = work / "a.png", work / "b.png"
    capture(exemplar, str(a)); capture(candidate, str(b))
    ia, ib = Image.open(a), Image.open(b)
    W = ia.width + ib.width + 30; H = max(ia.height, ib.height) + 40
    c = Image.new("RGB", (W, H), "white")
    c.paste(ia, (0, 40)); c.paste(ib, (ia.width + 30, 40))
    d = ImageDraw.Draw(c)
    d.text((10, 10), "EXEMPLAR", fill="black"); d.text((ia.width + 40, 10), "CANDIDATE", fill="black")
    d.line([(ia.width + 15, 0), (ia.width + 15, H)], fill="red", width=3)
    c.save(out)
    print(f"side-by-side -> {out}  ({ia.width}x{ia.height} | {ib.width}x{ib.height})")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(2)
    if a[0] == "extract":
        cmd_extract(a[1])
    elif a[0] == "classdiff":
        sys.exit(cmd_classdiff(a[1], a[2]))
    elif a[0] == "sidebyside":
        cmd_sidebyside(a[1], a[2], a[3])
    else:
        print(__doc__); sys.exit(2)
