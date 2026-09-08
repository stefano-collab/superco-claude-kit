"""Rebuild a page region and iterate until the measurements agree.

A single build gets close and then stops, because nothing tells it what it got wrong. This
extracts the target, builds, measures the build against the target with the SAME extractor,
hands back the specific deltas, and goes again.

Stops on one of 3 things, and says which:
  converged   no defects left
  plateau     the defect count moved by less than 2 between rounds, so another round is
              spending money to move a number rather than the work
  exhausted   hit the round cap with defects remaining, which are then listed

Comparing target and build with the same extractor is the point. A different reader would be
measuring its own quirks as well as the difference.

Run:
  python fidelity_loop.py https://example.com --out ./work --rounds 3
  python fidelity_loop.py --report ./work        # re-print the last verdict, builds nothing
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
JUNK = ("cookie", "consent", "allow all", "deny", "show details", "usercentrics", "cookiebot",
        "book your 1:1", "cold email experts", "send us an imessage", "only a few slots left")


DEFAULT_BRIEF = """Recreate the first %dpx of %s as a single self-contained HTML file called repro.html, at 1280px wide.

This is a fidelity exercise. A side by side against the original should be hard to tell apart.

`spec.json` holds real measurements taken from the live page. All 3 parts matter:
- `text`: every text run with its own colour, size, weight, letter spacing, line height and position. Where a value is here, use it EXACTLY. Do not round it and do not improve it.
- `boxes`: every filled, bordered, rounded or shadowed box with its position, size, fill, radius, border and shadow. These are the bars, buttons, pills and bands.
- `media`: images and SVGs with position and size. Where an entry carries `svg` markup, INLINE IT VERBATIM rather than drawing your own.

`reference.png` is a screenshot of the same region. Use it for what numbers cannot express: reading order, how pieces sit together, and the shape of any logo.

Rules:
- Load the typeface from Google Fonts if it is available there. Nothing else external.
- Use ONLY the colours, sizes and weights that appear in spec.json. Never substitute a nearby value, and never add a bold the original does not use.
- A radius of 3.35544e+07px means fully rounded. Use 999px.
- Where an image cannot be reproduced, leave a neutral block of the right size rather than inventing artwork.
- Normal hyphens, no em dashes.
- Write only repro.html.
"""


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()[:60]


def px(v) -> float:
    """A css length as a number. 'normal' letter spacing is 0, and a unitless line height
    cannot be compared to a px one, so those come back as 0 and are skipped."""
    if v in (None, "", "normal", "none"):
        return 0.0
    m = re.match(r"^(-?[\d.]+)px$", str(v).strip())
    return round(float(m.group(1)), 1) if m else 0.0


def junk(s: str) -> bool:
    return any(j in norm(s) for j in JUNK)


def extract(url_or_file: str, out: Path, height: int, shot: str = "") -> dict:
    cmd = [sys.executable, str(HERE / "page_fidelity.py"), url_or_file,
           "--height", str(height), "--out", str(out)]
    if shot:
        cmd += ["--shot", shot]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", creationflags=NO_WINDOW)
    if r.returncode != 0:
        raise SystemExit("extract failed:\n" + (r.stderr or r.stdout))
    d = json.loads(out.read_text(encoding="utf-8"))
    d["text"] = [t for t in d["text"] if not junk(t["text"])]
    d["boxes"] = [b for b in d["boxes"] if not junk(b.get("label")) and b["h"] < 2000]
    out.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
    return d


def compare(target: dict, built: dict) -> tuple[int, list[str]]:
    """(defect count, human readable deltas). Each delta names the fix, not just the fault."""
    faults: list[str] = []
    tby = {norm(t["text"]): t for t in target["text"]}
    bby = {norm(t["text"]): t for t in built["text"]}

    for k, t in tby.items():
        b = bby.get(k)
        if not b:
            faults.append("MISSING TEXT: %r should be at y=%d x=%d, %dpx w%s %s"
                          % (t["text"][:60], t["y"], t["x"], t["size"], t["weight"], t["colour"]))
            continue
        # Font first. A wrong typeface is the largest defect available and the comparator did
        # not check it at all until 8 Sep 2026, when a run reported converged with the type
        # visibly tighter than the original.
        if norm(b.get("font")) != norm(t.get("font")):
            faults.append("FONT: %r is set in %s, should be %s"
                          % (t["text"][:40], b.get("font"), t.get("font")))
        if px(b.get("ls")) != px(t.get("ls")):
            faults.append("LETTER SPACING: %r is %s, should be exactly %s"
                          % (t["text"][:40], b.get("ls") or "0px", t.get("ls") or "0px"))
        if abs(px(b.get("lh")) - px(t.get("lh"))) > 1:
            faults.append("LINE HEIGHT: %r is %s, should be %s"
                          % (t["text"][:40], b.get("lh"), t.get("lh")))
        if b["size"] != t["size"]:
            faults.append("SIZE: %r is %dpx, should be %dpx" % (t["text"][:40], b["size"], t["size"]))
        if str(b["weight"]) != str(t["weight"]):
            faults.append("WEIGHT: %r is %s, should be %s" % (t["text"][:40], b["weight"], t["weight"]))
        if b["colour"] != t["colour"]:
            faults.append("COLOUR: %r is %s, should be %s" % (t["text"][:40], b["colour"], t["colour"]))
        # Found by looking at a converged run on 8 Sep 2026: the reproduction underlined the
        # announcement bar and the original does not. 0 measured defects, an obvious defect on
        # screen. The extractor had the value all along and nothing compared it.
        if (b.get("decoration") or "") != (t.get("decoration") or ""):
            faults.append("DECORATION: %r is %r, should be %r"
                          % (t["text"][:40], b.get("decoration") or "none",
                             t.get("decoration") or "none"))
        if (b.get("tt") or "") != (t.get("tt") or ""):
            faults.append("TEXT-TRANSFORM: %r is %r, should be %r"
                          % (t["text"][:40], b.get("tt") or "none", t.get("tt") or "none"))
        # Rendered width, which is the only thing that shows a font CUT mismatch. Measured on
        # 8 Sep 2026: every letter-spacing value matched exactly and the type still rendered
        # 9% tighter, because Google Fonts' DM Sans is not the build the site self-hosts.
        # A green style check and a wrong looking page are perfectly compatible.
        tw, bw = t.get("w") or 0, b.get("w") or 0
        if tw > 40 and abs(bw - tw) / tw > 0.05 and abs(bw - tw) > 10:
            faults.append("RENDERED WIDTH: %r measures %dpx and should measure %dpx, %+d%%. "
                          "The letter spacing value may already match, so this is the font cut "
                          "or the weight rendering differently. Adjust letter-spacing on this "
                          "element until the width matches, or source the exact font file."
                          % (t["text"][:40], bw, tw, round((bw - tw) / tw * 100)))
        dy, dx = abs(b["y"] - t["y"]), abs(b["x"] - t["x"])
        if dy > 14 or dx > 24:
            faults.append("POSITION: %r sits at y=%d x=%d, should be y=%d x=%d"
                          % (t["text"][:40], b["y"], b["x"], t["y"], t["x"]))

    # a size, weight or colour the target never uses is an invention, and those are what make
    # a reproduction look approximately right rather than right
    for key, label in (("size", "SIZE"), ("weight", "WEIGHT"), ("colour", "COLOUR")):
        tv = {str(r[key]) for r in target["text"]}
        for v, n in Counter(str(r[key]) for r in built["text"]).items():
            if v not in tv:
                faults.append("%s NOT IN THE ORIGINAL: %s used %d time(s). Replace it with the "
                              "nearest value the original actually uses: %s"
                              % (label, v, n, ", ".join(sorted(tv)[:8])))

    tfills = Counter(b["bg"] for b in target["boxes"] if b.get("bg"))
    bfills = Counter(b["bg"] for b in built["boxes"] if b.get("bg"))
    for fill, n in tfills.items():
        if fill not in bfills:
            box = next(b for b in target["boxes"] if b.get("bg") == fill)
            faults.append("MISSING BOX: a %s fill, %dx%d at y=%d x=%d, radius %s, on %r"
                          % (fill, box["w"], box["h"], box["y"], box["x"],
                             box.get("radius") or "0", (box.get("label") or "")[:30]))
    return len(faults), faults


def build(work: Path, deltas: list[str] | None) -> None:
    if deltas is None:
        prompt = ("Read brief.txt, spec.json and reference.png in this folder, then do exactly "
                  "what the brief says.")
    else:
        (work / "deltas.txt").write_text("\n".join(deltas), encoding="utf-8")
        prompt = ("repro.html already exists in this folder and is close. deltas.txt lists every "
                  "measured difference between it and the original, taken from the live page. "
                  "Fix every one of them in repro.html and change nothing else. Do not restyle "
                  "anything the deltas do not mention. Re-read spec.json for exact values.")
    r = subprocess.run(["claude", "-p", "--permission-mode", "acceptEdits",
                        "--allowedTools", "Read,Write,Edit,Glob,Grep"],
                       cwd=str(work), input=prompt, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", creationflags=NO_WINDOW)
    (work / "build.log").write_text((r.stdout or "") + (r.stderr or ""), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?")
    ap.add_argument("--out", default="./fidelity-work")
    ap.add_argument("--height", type=int, default=1500)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--report", default="")
    a = ap.parse_args()

    work = Path(a.report or a.out).resolve()
    if a.report:
        print((work / "verdict.txt").read_text(encoding="utf-8"))
        return 0
    if not a.url:
        raise SystemExit("a url is required unless you pass --report")

    work.mkdir(parents=True, exist_ok=True)
    target = extract(a.url, work / "spec.json", a.height, str(work / "reference.png"))
    if not (work / "brief.txt").exists():
        (work / "brief.txt").write_text(DEFAULT_BRIEF % (a.height, a.url), encoding="utf-8")
    print("target: %d text runs, %d boxes, %d media"
          % (len(target["text"]), len(target["boxes"]), len(target["media"])))

    history, deltas, verdict = [], None, "exhausted"
    for rnd in range(1, a.rounds + 1):
        build(work, deltas)
        if not (work / "repro.html").exists():
            raise SystemExit("round %d produced no repro.html, see build.log" % rnd)
        built = extract((work / "repro.html").as_uri(), work / "built.json", a.height,
                        str(work / "repro.png"))
        n, deltas = compare(target, built)
        history.append(n)
        print("round %d: %d defect(s)" % (rnd, n))
        for d in deltas[:6]:
            print("    " + d[:150])
        if n == 0:
            verdict = "converged"
            break
        if len(history) >= 2 and abs(history[-2] - history[-1]) < 2:
            verdict = "plateau"
            break

    lines = ["fidelity loop: %s" % verdict,
             "target: %s" % a.url,
             "defects by round: %s" % " -> ".join(str(h) for h in history)]
    if deltas and verdict != "converged":
        lines += ["", "%d remaining:" % len(deltas)] + ["  " + d for d in deltas]
    (work / "verdict.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[:3]))
    print("verdict written to %s" % (work / "verdict.txt"))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
