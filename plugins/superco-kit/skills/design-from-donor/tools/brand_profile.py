"""Turn a raw page extraction into a reusable brand profile.

`page_fidelity.py` returns hundreds of measured rows, which is the right shape for rebuilding
that one page and the wrong shape for making anything else. A profile answers the questions a
new artefact actually asks: what is the body colour, what is the accent, what is the display
face and how is it set, what does a button look like here.

Everything is derived by frequency from real measurements. Nothing is invented, and where the
evidence is thin the field says so rather than guessing, because a confident wrong palette is
worse than an admitted gap.

Run:  python brand_profile.py spec.json --out profile.json
      python brand_profile.py spec.json --md          # readable, to paste into a brief
"""
from __future__ import annotations

import argparse
import colorsys
import json
import re
import sys
from collections import Counter
from pathlib import Path


def rgb(c: str):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", c or "")
    return tuple(int(m.group(i)) for i in (1, 2, 3)) if m else None


def sat(c: str) -> float:
    v = rgb(c)
    if not v:
        return 0.0
    r, g, b = (x / 255 for x in v)
    return colorsys.rgb_to_hls(r, g, b)[2]


def light(c: str) -> float:
    v = rgb(c)
    if not v:
        return 0.0
    r, g, b = (x / 255 for x in v)
    return colorsys.rgb_to_hls(r, g, b)[1]


# Page furniture is not the brand. A cookie banner, a country selector and a consent modal all
# carry their own styling, and on 8 Sep 2026 a profile built without this filter reported a
# brand's button as square with a 2px coral border. That was the Accept All button. The real
# buttons on the same page were pale pink and fully rounded at 33px, and the extraction had
# them all along. Everything downstream inherited the wrong shape.
FURNITURE = re.compile(
    r"cookie|consent|privacy|gdpr|accept all|reject all|see policies|manage preferences"
    r"|select country|choose your country|change region|newsletter pop|sign up and save"
    r"|skip to (main )?content|enable accessibility|accessibility menu", re.I)


def is_furniture(s: str) -> bool:
    return bool(FURNITURE.search(s or ""))


def build(spec: dict) -> dict:
    text = [t for t in spec.get("text", []) if not is_furniture(t.get("text"))]
    boxes = [b for b in spec.get("boxes", []) if not is_furniture(b.get("label"))]
    dropped = (len(spec.get("text", [])) - len(text),
               len(spec.get("boxes", [])) - len(boxes))
    if not text:
        return {"error": "no text runs in the extraction, so no profile can be built"}

    ink = Counter(t["colour"] for t in text)
    fonts = Counter(t["font"] for t in text if t.get("font"))
    sizes = Counter(t["size"] for t in text)

    body_colour, body_n = ink.most_common(1)[0]
    # An accent is a saturated colour that is NOT the body colour. Ordered by use, because the
    # one used 26 times is the accent and the one used twice is a detail.
    accents = [(c, n) for c, n in ink.most_common() if c != body_colour and sat(c) > 0.25]
    quiet = [(c, n) for c, n in ink.most_common()
             if c != body_colour and sat(c) <= 0.25 and light(c) < 0.75]

    display = max((t for t in text), key=lambda t: t["size"])
    body_size = Counter(t["size"] for t in text if 12 <= t["size"] <= 20).most_common(1)
    body_size = body_size[0][0] if body_size else None

    # letter spacing is usually a function of size: tight display, near zero body
    tracking = {}
    for t in text:
        ls = t.get("ls") or "0px"
        m = re.match(r"^(-?[\d.]+)px$", ls)
        if m:
            tracking.setdefault(t["size"], []).append(float(m.group(1)))
    tracking = {s: round(sum(v) / len(v), 2) for s, v in sorted(tracking.items()) if v}

    fills = Counter(b["bg"] for b in boxes if b.get("bg"))
    # A button is a small filled box with a short label. A band is a full width filled box.
    buttons, bands, cards = [], [], []
    page_w = (spec.get("page") or {}).get("width", 1280)
    for b in boxes:
        if not b.get("bg"):
            continue
        if b["w"] >= page_w * 0.9:
            bands.append(b)
        elif b["h"] <= 70 and b.get("label") and len(b["label"]) < 30:
            buttons.append(b)
        elif b["w"] > 150 and b["h"] > 90:
            cards.append(b)

    def clean(b):
        r = b.get("radius") or "0px"
        if "e+" in r:
            r = "999px"
        shape = ""
        m = re.match(r"^([\d.]+)px", r)
        if m and b["h"]:
            shape = "pill" if float(m.group(1)) >= b["h"] * 0.45 else (
                "square" if float(m.group(1)) < 3 else "rounded")
        return {"fill": b["bg"], "radius": r, "shape": shape, "w": b["w"], "h": b["h"],
                "border": b.get("border") or "", "shadow": b.get("shadow") or "",
                "label": b.get("label") or ""}

    return {
        "type": {
            "faces": [{"family": f, "runs": n} for f, n in fonts.most_common(4)],
            "display": {"size": display["size"], "weight": display["weight"],
                        "colour": display["colour"], "ls": display.get("ls"),
                        "example": display["text"][:60]},
            "body_size": body_size,
            "scale": [s for s, _ in sizes.most_common(8)],
            "tracking_by_size": tracking,
            "weights_used": sorted({str(t["weight"]) for t in text}),
        },
        "colour": {
            "body": {"value": body_colour, "runs": body_n},
            "accents": [{"value": c, "runs": n} for c, n in accents[:4]],
            "quiet": [{"value": c, "runs": n} for c, n in quiet[:3]],
            "fills": [{"value": c, "boxes": n} for c, n in fills.most_common(5)],
            "page_bg": (spec.get("page") or {}).get("bg", ""),
        },
        "components": {
            "buttons": [clean(b) for b in buttons[:4]],
            "bands": [clean(b) for b in bands[:3]],
            "cards": [clean(b) for b in cards[:3]],
        },
        "evidence": {"text_runs": len(text), "boxes": len(boxes),
                     "media": len(spec.get("media", [])),
                     "furniture_dropped": {"text": dropped[0], "boxes": dropped[1]}},
    }


def as_md(p: dict) -> str:
    if "error" in p:
        return "Could not build a profile: " + p["error"]
    t, c, k = p["type"], p["colour"], p["components"]
    L = ["# Brand profile", "",
         "Derived from %d measured text runs and %d boxes on the live page. Every value below "
         "was read off the rendered page, not described." % (p["evidence"]["text_runs"], p["evidence"]["boxes"]),
         "", "## Type", ""]
    for f in t["faces"]:
        L.append("- %s, on %d runs" % (f["family"], f["runs"]))
    d = t["display"]
    L += ["", "Display is %dpx weight %s in %s, tracking %s. Example: %r"
          % (d["size"], d["weight"], d["colour"], d.get("ls") or "0px", d["example"]),
          "Body is %spx." % t["body_size"],
          "Weights in use: %s. Do not introduce another one." % ", ".join(t["weights_used"]),
          "Scale: %s" % ", ".join(str(s) + "px" for s in t["scale"]),
          "", "Tracking by size, apply these exactly:",
          "  " + ", ".join("%dpx -> %s" % (s, v) for s, v in list(t["tracking_by_size"].items())[:10]),
          "", "## Colour", "",
          "- Body text %s, used on %d runs. This is the default ink, not black."
          % (c["body"]["value"], c["body"]["runs"])]
    for a in c["accents"]:
        L.append("- Accent %s, used %d times. Use it that sparingly." % (a["value"], a["runs"]))
    for q in c["quiet"]:
        L.append("- Secondary %s, %d times" % (q["value"], q["runs"]))
    for f in c["fills"]:
        L.append("- Fill %s, on %d boxes" % (f["value"], f["boxes"]))
    L += ["", "## Components", ""]
    for name, items in (("Button", k["buttons"]), ("Band", k["bands"]), ("Card", k["cards"])):
        for b in items:
            L.append("- %s: %s fill, %s, radius %s, %dx%d%s%s"
                     % (name, b["fill"], b.get("shape") or "shape unknown", b["radius"], b["w"], b["h"],
                        ", border " + b["border"] if b["border"] else "",
                        ", shadow" if b["shadow"] else ""))
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", default="")
    ap.add_argument("--md", action="store_true")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    p = build(spec)
    if a.md:
        text = as_md(p)
        if a.out:
            Path(a.out).write_text(text, encoding="utf-8")
            print("wrote " + a.out)
        else:
            print(text)
    else:
        out = a.out or "profile.json"
        Path(out).write_text(json.dumps(p, indent=1, ensure_ascii=False), encoding="utf-8")
        print("wrote " + out)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
