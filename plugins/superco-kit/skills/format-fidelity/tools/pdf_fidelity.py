#!/usr/bin/env python3
"""pdf_fidelity - the PDF half of the format-fidelity loop (see .claude/skills/format-fidelity).

A PDF has no runs; it has SPANS, and a span is the same thing: the smallest stretch of text that
shares one (font, size, colour, weight). Two-tone headings, 8pt notes and coloured CTAs all show
up here exactly as they do in a docx run dump - which is why this reads spans and never lines.

    python pdf_fidelity.py extract   <pdf>                   span-level dump per page + rules + fills + images
    python pdf_fidelity.py classdiff <exemplar> <candidate>  span-class comparison; exit 1 if candidate uses a
                                                             (size, colour, bold, font) class the exemplar never does
    python pdf_fidelity.py sidebyside <exemplar> <candidate> <out.png>

Rules and fills come from page.get_drawings(): a thin filled rect (h < 3pt) is a rule, a wide one
behind text is a table fill. Images are counted from page.get_images(full=True) - the ones actually
PLACED on the page, not the ones stored in the file.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding="utf8", errors="replace")


def spans(page):
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip():
                    yield s


def span_sig(s) -> tuple:
    bold = bool(s["flags"] & 16) or "bold" in s["font"].lower()
    italic = bool(s["flags"] & 2) or "italic" in s["font"].lower()
    return (round(s["size"]), f"{s['color']:06x}", bold, italic, s["font"].split("-")[0])


def shapes(page):
    rules, fills = [], []
    for d in page.get_drawings():
        r = d["rect"]
        if d.get("fill") is None:
            continue
        col = "%02x%02x%02x" % tuple(int(c * 255) for c in d["fill"][:3])
        if r.height < 3 and r.width > 40:
            rules.append((round(r.y0), round(r.width), col))
        elif r.height >= 3 and r.width > 40 and col != "ffffff":
            fills.append((round(r.y0), round(r.width), round(r.height), col))
    return rules, fills


def cmd_extract(pdf: str) -> None:
    with fitz.open(pdf) as d:
        print(f"{pdf}  pages={len(d)}")
        for i, page in enumerate(d):
            rules, fills = shapes(page)
            print(f"\n== page {i+1}  rules={len(rules)} fills={len(fills)} images={len(page.get_images(full=True))}")
            for y, w, c in rules:
                print(f"   RULE y={y} w={w} #{c}")
            for y, w, h, c in fills:
                print(f"   FILL y={y} {w}x{h} #{c}")
            for s in spans(page):
                sz, col, b, it, f = span_sig(s)
                print(f"    {sz:>3}pt #{col} {'B' if b else ' '}{'I' if it else ' '} {f[:12]:12s} y={round(s['bbox'][1]):>4} {s['text'][:70]!r}")


def classes(pdf: str) -> dict:
    """DISTINCT images, never the per-page sum: a document one page longer repeats the same logo
    on the extra page, and summing made the count track PAGE COUNT rather than image content."""
    out = {"span": set(), "rule_colours": set(), "fill_colours": set(), "images": 0}
    xrefs = set()
    with fitz.open(pdf) as d:
        for page in d:
            for s in spans(page):
                out["span"].add(span_sig(s))
            rules, fills = shapes(page)
            out["rule_colours"] |= {c for _, _, c in rules}
            out["fill_colours"] |= {c for *_, c in fills}
            xrefs |= {im[0] for im in page.get_images(full=True)}
    out["images"] = len(xrefs)
    return out


def cmd_classdiff(exemplar: str, candidate: str) -> int:
    A, B = classes(exemplar), classes(candidate)
    bad = 0
    extra = B["span"] - A["span"]
    print(f"span classes  exemplar={len(A['span'])} candidate={len(B['span'])}")
    for k in sorted(A["span"]):
        print(f"   exemplar {k}")
    if extra:
        bad += 1
        print("  DIFFERS - candidate uses classes the exemplar never does:")
        for k in sorted(extra):
            print(f"   !! {k}")
    else:
        print("  MATCH  - every candidate span class exists in the exemplar")
    for k in ("rule_colours", "fill_colours"):
        ok = B[k] <= A[k]
        bad += not ok
        print(f"{k:13s} {'MATCH' if ok else 'DIFFERS':8s} {sorted(A[k])} -> {sorted(B[k])}")
    ok = A["images"] == B["images"]
    bad += not ok
    print(f"{'images':13s} {'MATCH' if ok else 'DIFFERS':8s} {A['images']} -> {B['images']}   (placed on pages)")
    print("\nVERDICT:", "PASS" if bad == 0 else f"FAIL ({bad} class(es) differ)")
    return 0 if bad == 0 else 1


def cmd_sidebyside(exemplar: str, candidate: str, out: str, dpi: int = 110) -> None:
    from PIL import Image, ImageDraw
    pages = []
    with fitz.open(exemplar) as a, fitz.open(candidate) as b:
        for i in range(max(len(a), len(b))):
            ims = []
            for d in (a, b):
                if i < len(d):
                    ims.append(Image.open(io.BytesIO(d[i].get_pixmap(dpi=dpi).tobytes("png"))))
                else:
                    ims.append(Image.new("RGB", ims[0].size if ims else (800, 1000), "white"))
            w = ims[0].width + ims[1].width + 30
            h = max(ims[0].height, ims[1].height) + 40
            c = Image.new("RGB", (w, h), "white")
            c.paste(ims[0], (0, 40)); c.paste(ims[1], (ims[0].width + 30, 40))
            dr = ImageDraw.Draw(c)
            dr.text((10, 10), f"EXEMPLAR  p{i+1}", fill="black")
            dr.text((ims[0].width + 40, 10), f"CANDIDATE  p{i+1}", fill="black")
            dr.line([(ims[0].width + 15, 0), (ims[0].width + 15, h)], fill="red", width=3)
            pages.append(c)
    W = max(p.width for p in pages); H = sum(p.height for p in pages)
    sheet = Image.new("RGB", (W, H), "white")
    y = 0
    for p in pages:
        sheet.paste(p, (0, y)); y += p.height
    sheet.save(out)
    print(f"side-by-side ({len(pages)} page pair(s)) -> {out}")


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
