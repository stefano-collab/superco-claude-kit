#!/usr/bin/env python3
"""docx_fidelity - read, compare and RENDER .docx formatting so it can be matched, not guessed.

Built 3 September 2026 after a day in which twelve throwaway scripts each re-invented a docx
reader and each missed a class of formatting: two-tone headings (first-match colour), rules under
headings (w:pBdr never read), table fills (w:shd never read), images (checked the zip, not the
body), strikethrough (one of two variants). Stef, on the eighth occurrence: "don't say it's fixed
unless it actually is." This is the tool that lets me prove it instead.

    python docx_fidelity.py extract   <docx>                 run-level dump: every run, border, fill, drawing
    python docx_fidelity.py classdiff <exemplar> <candidate> element-CLASS comparison; exit 1 on any mismatch
    python docx_fidelity.py render    <docx> <out_prefix>    docx -> PDF (LibreOffice) -> PNG per page
    python docx_fidelity.py sidebyside <exemplar> <candidate> <out.png>
                                                             one image, exemplar left / candidate right, per page

The rule this enforces: nothing goes to Stef until `classdiff` exits 0 AND the `sidebyside` image
has been looked at. A green XML check is necessary, never sufficient - the founders photo went
missing while "images: 2" was reported, because the PNGs were in word/media/ and the <w:drawing>
that references them was not in the body.
"""
from __future__ import annotations

import io
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

T = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.S)          # <w:t> ONLY - never <w:tc>, <w:tbl>, <w:tr>
PARA = re.compile(r"<w:p\b(?![A-Za-z]).*?</w:p>", re.S)          # <w:p> ONLY - never <w:pPr>
ROW = re.compile(r"<w:tr\b(?![A-Za-z]).*?</w:tr>", re.S)         # <w:tr> ONLY - never <w:trPr>
RUN = re.compile(r"<w:r\b(?![A-Za-z]).*?</w:r>", re.S)           # <w:r>  ONLY - never <w:rPr>
BLOCK = re.compile(r"<w:tbl>.*?</w:tbl>|<w:p\b(?![A-Za-z]).*?</w:p>", re.S)
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
NBSP = "\u00a0"


def body_xml(path: str) -> str:
    return zipfile.ZipFile(path).read("word/document.xml").decode("utf8")


def text(x: str) -> str:
    return re.sub(rf"[{NBSP}\s]+", " ", "".join(T.findall(x))).strip()


def attr(x: str, pat: str, default: str = "-") -> str:
    m = re.search(pat, x)
    return m.group(1) if m else default


def run_sig(r: str) -> tuple:
    """(size_pt, colour, bold, italic, strike, font) for one run."""
    sz = attr(r, r'<w:sz w:val="(\d+)"', "0")
    return (int(sz) // 2,
            attr(r, r'<w:color w:val="([0-9a-fA-F]{6})"').lower(),
            bool(re.search(r'<w:b w:val="1"/>|<w:b/>', r)),
            bool(re.search(r'<w:i w:val="1"/>|<w:i/>', r)),
            bool(re.search(r'<w:strike w:val="1"/>|<w:strike/>', r)),
            attr(r, r'w:ascii="([^"]+)"'))


def para_sig(p: str) -> dict:
    runs = [r for r in RUN.findall(p) if T.search(r)]
    bdr = re.search(r"<w:pBdr>(.*?)</w:pBdr>", p, re.S)
    edges = tuple(re.findall(r"<w:(top|bottom|left|right)\b", bdr.group(1))) if bdr else ()
    return {"text": text(p), "runs": tuple(run_sig(r) for r in runs), "border": edges,
            "bullet": "<w:numPr>" in p, "drawing": "<w:drawing>" in p}


def table_sig(t: str) -> dict:
    rows = ROW.findall(t)
    fills = []
    for r in rows[:2]:
        fills.append(attr(r, r'<w:shd[^>]*w:fill="([0-9a-fA-F]{6})"').lower())
    return {"rows": len(rows), "hdr_fill": fills[0] if fills else "-",
            "body_fill": fills[1] if len(fills) > 1 else "-",
            "body_font": attr(rows[1], r'w:ascii="([^"]+)"') if len(rows) > 1 else "-",
            "first": text(rows[0])[:40] if rows else "", "drawing": "<w:drawing>" in t}


def blocks(path: str):
    for m in BLOCK.finditer(body_xml(path)):
        x = m.group(0)
        yield ("TABLE", table_sig(x)) if x.startswith("<w:tbl>") else ("P", para_sig(x))


# ----------------------------------------------------------------------------- extract
def cmd_extract(path: str) -> None:
    doc = body_xml(path)
    print(f"{path}\n  drawings in body: {len(re.findall(r'<w:drawing>', doc))}   "
          f"blips: {re.findall(r'r:embed=\"([^\"]+)\"', doc)}\n")
    for kind, s in blocks(path):
        if kind == "TABLE":
            print(f"TABLE rows={s['rows']} hdr=#{s['hdr_fill']} body=#{s['body_fill']} font={s['body_font']}"
                  f"{'  [DRAWING]' if s['drawing'] else ''}  {s['first']!r}")
            continue
        if not s["text"] and not s["drawing"]:
            continue
        flag = ("  BORDER" + str(s["border"]) if s["border"] else "") + ("  [DRAWING]" if s["drawing"] else "") + ("  bullet" if s["bullet"] else "")
        print(f"P{flag}")
        for sig in s["runs"]:
            sz, col, b, i, st, f = sig
            print(f"    run {sz:>3}pt #{col} {'B' if b else ' '}{'I' if i else ' '}{'S' if st else ' '} {f[:10]:10s}")
        print(f"      {s['text'][:90]!r}")


# ----------------------------------------------------------------------------- classdiff
def classes(path: str) -> dict:
    """Group every block by CLASS so two documents with different content can still be compared."""
    out = {"title": set(), "sect": set(), "sub": set(), "body": set(), "note": set(),
           "table": set(), "cta": set(), "struck": set(), "drawings": 0}
    doc = body_xml(path)
    out["drawings"] = len(re.findall(r"<w:drawing>", doc))
    for kind, s in blocks(path):
        if kind == "TABLE":
            if s["rows"] > 1:
                out["table"].add((s["hdr_fill"], s["body_fill"], s["body_font"]))
            continue
        t, runs = s["text"], s["runs"]
        if not runs:
            continue
        for sig in runs:
            if sig[4]:
                out["struck"].add(t[:30])
        key = (len(runs), tuple((r[0], r[1], r[2]) for r in runs), s["border"])
        if re.match(r"^0\d\s", t):
            out["sect"].add(key)
        elif t.startswith("*Not everyone"):
            out["note"].add(key)
        elif runs[0][0] == 12 and runs[0][1] == "089bd9" and len(runs) == 1:
            out["sub"].add(key)
        elif runs[0][0] >= 20:
            out["title"].add(key)
        elif runs[0][1] == "1155cc":
            out["cta"].add(key)
        elif runs[0][0] in (0, 11):
            out["body"].add(key)
    return out


def cmd_classdiff(exemplar: str, candidate: str) -> int:
    A, B = classes(exemplar), classes(candidate)
    bad = 0
    print(f"{'class':10s} {'result':8s} exemplar -> candidate")
    for k in ("title", "sect", "sub", "note", "table", "cta"):
        a, b = A[k], B[k]
        # subset, plus: a class the exemplar HAS and the candidate lost is a defect, but a class
        # NEITHER document uses is a match - an empty-vs-empty DIFFERS is a gate crying wolf.
        ok = b <= a and (bool(b) or not a)
        bad += not ok
        print(f"  {k:8s} {'MATCH' if ok else 'DIFFERS':8s} {sorted(a)} -> {sorted(b)}")
    ok = A["drawings"] == B["drawings"]
    bad += not ok
    print(f"  {'drawings':8s} {'MATCH' if ok else 'DIFFERS':8s} {A['drawings']} -> {B['drawings']}   (in BODY, not in word/media/)")
    print(f"  {'struck':8s} {'info':8s} exemplar={sorted(A['struck'])}  candidate={sorted(B['struck'])}")
    print("\nVERDICT:", "PASS" if bad == 0 else f"FAIL ({bad} class(es) differ)")
    return 0 if bad == 0 else 1


# ----------------------------------------------------------------------------- render
def to_pdf(docx: str, outdir: Path) -> Path:
    prof = Path.home() / "_lo_conv_profile"
    subprocess.run([SOFFICE, f"-env:UserInstallation=file:///{prof.as_posix()}", "--headless",
                    "--convert-to", "pdf", "--outdir", str(outdir), docx],
                   check=True, capture_output=True, timeout=180)
    return outdir / (Path(docx).stem + ".pdf")


def cmd_render(docx: str, prefix: str, dpi: int = 110) -> list[Path]:
    import fitz  # PyMuPDF
    with tempfile.TemporaryDirectory() as td:
        pdf = to_pdf(docx, Path(td))
        doc = fitz.open(pdf)
        outs = []
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            out = Path(f"{prefix}_p{i+1}.png")
            pix.save(out)
            outs.append(out)
        doc.close()
    print(f"rendered {len(outs)} page(s) -> {prefix}_p*.png")
    return outs


def cmd_sidebyside(exemplar: str, candidate: str, out: str, dpi: int = 110) -> None:
    """Render both, paste exemplar LEFT and candidate RIGHT per page, stack pages vertically.

    Uses a persistent scratch dir rather than TemporaryDirectory: on Windows the PDF stays
    locked by the renderer until the interpreter exits, and the auto-cleanup raised
    PermissionError BEFORE the sheet was saved."""
    import fitz
    from PIL import Image, ImageDraw
    work = Path(out).parent / "_docx_fidelity_work"
    for sub in ("a", "b"):
        (work / sub).mkdir(parents=True, exist_ok=True)
    pa = to_pdf(exemplar, work / "a"); pb = to_pdf(candidate, work / "b")
    pages = []
    with fitz.open(pa) as a, fitz.open(pb) as b:
        n = max(len(a), len(b))
        for i in range(n):
            ims = []
            for d in (a, b):
                if i < len(d):
                    ims.append(Image.open(io.BytesIO(d[i].get_pixmap(dpi=dpi).tobytes("png"))))
                else:
                    ims.append(Image.new("RGB", ims[0].size if ims else (800, 1000), "white"))
            w = ims[0].width + ims[1].width + 30
            h = max(ims[0].height, ims[1].height) + 40
            canvas = Image.new("RGB", (w, h), "white")
            canvas.paste(ims[0], (0, 40)); canvas.paste(ims[1], (ims[0].width + 30, 40))
            dr = ImageDraw.Draw(canvas)
            dr.text((10, 10), f"EXEMPLAR (Stef)  p{i+1}", fill="black")
            dr.text((ims[0].width + 40, 10), f"CANDIDATE (Claude)  p{i+1}", fill="black")
            dr.line([(ims[0].width + 15, 0), (ims[0].width + 15, h)], fill="red", width=3)
            pages.append(canvas)
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
    cmd = a[0]
    if cmd == "extract":
        cmd_extract(a[1])
    elif cmd == "classdiff":
        sys.exit(cmd_classdiff(a[1], a[2]))
    elif cmd == "render":
        cmd_render(a[1], a[2])
    elif cmd == "sidebyside":
        cmd_sidebyside(a[1], a[2], a[3])
    else:
        print(__doc__); sys.exit(2)
