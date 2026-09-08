---
name: format-fidelity
description: Copy the exact formatting of an existing document, PDF or web page into a new one, and prove it matches before anyone sees it. Use for "make it look exactly like this", branded reports, proposals, landing pages or any second attempt after someone says the formatting is still wrong.
---

# Format fidelity

Built after 8 failed attempts to reproduce one document. Effort was never the problem.
Every attempt read the original at the wrong level, rebuilt it from a description of itself,
and declared victory off a green text check.

## Requirements

The tools ship next to this skill, in `tools/`. They need:

- **LibreOffice** on the path as `soffice`, for rendering
- **PyMuPDF** (`pip install pymupdf`) for the PDF reader
- **Playwright** (`pip install playwright` then `playwright install chromium`) for web pages

If you only need the web page reader, you only need Playwright.

## The idea in one line

Formatting lives in the smallest unit of the format, so read it there. Then lift the
original's own units into the new file rather than rebuilding them. Then prove the result
twice, once by class in the source and once by eye in the render.

The smallest unit, per format:

| Source | Unit | What carries the formatting | Tool |
|---|---|---|---|
| .docx, or a Google Doc exported as docx | the **run** | font, size, colour, bold, italic, strike, plus border rules, bullets, spacing, shading fills, drawings in the body, bullet glyphs and the font table | `tools/docx_fidelity.py` |
| PDF | the **span** | font name, size, colour, flags, render type (3 means invisible), drawings for rules and fills, placed images | `tools/pdf_fidelity.py` |
| web page or HTML | the element's **computed style** | font family, size, weight, colour, line height, letter spacing, text transform, background, border, margins. Never the stylesheet | `tools/html_fidelity.py`, fixed at 1280px |

A paragraph, a line or a CSS rule is the wrong level. A paragraph-level read of a two-tone
heading returns one colour. A stylesheet tells you what was asked for, not what the browser did.

## The loop

Every step is required. The gate is steps 5 and 6 together, and neither alone has ever
been enough.

### 1. Extract the original at run level

```bash
python tools/docx_fidelity.py extract "<original.docx>"
python tools/pdf_fidelity.py  extract "<original.pdf>"
python tools/html_fidelity.py extract "<url or file.html>"
```

Read the whole dump. Write down every attribute that varies *within* one visual element:
the heading whose number is blue and whose text is black, the title whose last word is a
different colour. Those are the ones a first-match reader flattens.

### 2. Classify the units into element classes

Group the dump into the classes the design actually has: title, section head, subhead, body,
note, table header, table body, call to action, image, footer. Record each class as its full
signature, meaning run count and per run the size, colour, weight and font, plus border
edges, bullet and fill. That record is the spec the build works from.

### 3. Build by lifting, never by reconstructing

- **Lift the original element whole** and replace only its text. The docx tool keeps the run
  count and swaps text run by run, so a two-tone heading stays two-tone.
- Never regenerate from a spec what can be copied. A rebuilt element is a guess about the
  original. A lifted one *is* the original.
- Carry the invisible parts with it: the bullet glyph definitions, the font table and the
  embedded font files for bold faces, the root namespaces when a drawing moves between files,
  and the keep-with-next flag on headings.
- **Edit the existing file in place where there's one.** A text diff can't see the bold,
  the bullets or the image someone added by hand, so regenerating over their file quietly
  destroys their edits.

### 4. Classdiff

```bash
python tools/docx_fidelity.py classdiff "<original>" "<candidate>"
```

Exit 1 on any mismatch. Subset, not equality: a shorter document legitimately uses fewer
classes, but a class the original never uses is always a defect. Compare drawings and images
by count in the body, never by files in the package.

### 5. Render both and actually look

```bash
python tools/docx_fidelity.py sidebyside "<original>" "<candidate>" out.png
```

Open the PNG and compare page by page. This is where an orphaned heading, a fake bold face
or a wrong bullet glyph shows up. A green classdiff with an unviewed render isn't done.

### 6. Run the render gate on the PDF

```bash
python tools/pdf_fidelity.py classdiff <original>.pdf <candidate>.pdf
```

The render is a second, independent reading and it sees what the source can't. On the
first real run it reported 283 invisible spans in one font on the candidate and none on the
original: the candidate had no bold face, so LibreOffice was synthesising bold on every
heading. The source check passed, because bold *was* requested. The eye passed, because fake
bold looks bold. Only the render's font table knew.

### 7. Ship the evidence, not a claim

Show the side-by-side image and the classdiff verdict lines. Never write "fixed" - show the
picture and let it say so.

## Traps that cost a day each

- **Regex over the document XML must not match tag prefixes.** A pattern for the text tag
  will also match the table-cell-borders tag; a pattern for the paragraph tag will match the
  paragraph-properties tag. The tools carry the bounded versions already, so do not
  re-derive them.
- **First-match extraction flattens multi-run elements.** Extract per run, always.
- **Two images in the zip proves nothing.** Count the drawings in the document body.
- **Every formatting flag has two spellings**, the bare tag and the tag with an explicit
  value, plus an explicit zero meaning off. Read all 3 states.
- **The XML declaration comes before the root**, so matching from position zero fails.
- **Block-by-block diffing can't compare two documents with different content.** Compare
  by class.
- **Capture web pages at a fixed width.** Two widths are two designs.
- **LibreOffice locks the PDF** until the interpreter exits, so use a persistent working
  directory rather than a temporary one, and kill stray `soffice` processes before a rerun
  or the conversion silently hands back the old file.

## The class gates cannot see a swap

Added after a 71-document batch passed every gate with a heading style applied to body text
and a bullet style applied to a single word. It was found by a person looking at a page.

Classdiff compares *sets* of classes. A heading class used on the wrong paragraph is still
the heading class, so the set matches and both gates pass. The defect is in the assignment,
and no set comparison can see it. Two rules follow:

1. **Capture the donor elements from the untouched original, before the first edit.** Reading
   a donor by index after other edits have run takes it from a document whose indices have
   already shifted, so the subhead donor and the bullet donor swap places.
2. **Add a shape assertion per class**, because it's cheap and it's the only thing that
   catches this. A subhead is short, so fail it over about 6 words. A bullet isn't a bare
   Title Case noun. A note is one sentence. Validate the assertions against a document you
   know is broken before you trust them.

And one document per shape isn't enough when the batch is large. The 5 rendered and read
were all 3-subhead documents, and the defect only occurred in the 4 that had a fourth.
Sample the structural variants, not just a few at random.
