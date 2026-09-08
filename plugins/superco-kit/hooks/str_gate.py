"""Block a write to a prose file that adds a known AI tell.

The `slop-text-removal` skill describes the standard. A skill is a prompt though, and a prompt
gets ignored: on 8 September 2026 that skill was installed, its description matched the task
exactly, and 2 documents still went out with em dashes in them. So the mechanical half runs
here instead, where forgetting is not possible.

What it does NOT do: judge whether the writing is any good. That needs reading, and it lives in
the skill. This catches only what a regular expression can catch with certainty, which is the
formatting rules and a handful of phrasings that are always a tell.

Scope, deliberately narrow so it never becomes noise:
  - Markdown and text files only. Code is never touched.
  - Only the text THIS write adds, so an old file does not fail forever on somebody else's line.
  - Archives, logs and any folder of collected samples are exempt.
  - `<!-- str:skip reason -->` in the added text skips that write, and the reason is logged.

It fails open. If anything in here breaks, the write goes through and the error is logged
rather than blocking someone's work over a bug in a gate.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

PROSE_EXT = {".md", ".markdown", ".txt"}
SKIP_MARK = re.compile(r"<!--\s*str:skip\s*(.*?)\s*-->")
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

# Paths that are not the writer's own prose. A corpus of somebody else's writing must not be
# corrected, and neither must a log or an archive.
EXEMPT = [
    (r"/node_modules/|/\.git/|/__pycache__/", "not prose"),
    (r"/(state|logs?)/|\.log$|\.jsonl$", "not prose"),
    (r"/archive/|/voice-samples/|/samples/|/corpus/", "collected samples kept as they were"),
]


def _log(row):
    """Best effort, and never a reason to fail a write."""
    try:
        d = Path(os.environ.get("CLAUDE_PLUGIN_DATA") or (HERE.parent / ".gate-log"))
        d.mkdir(parents=True, exist_ok=True)
        with (d / "str-gate.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(dict(row, ts=time.strftime("%Y-%m-%dT%H:%M:%S"))) + "\n")
    except Exception:                               # noqa: BLE001
        pass


def _added_text(tool, ti, path):
    """What this write ADDS. An Edit is its replacement text. A Write of an existing tracked
    file is only the lines that are not already in it, so nobody inherits an old tell."""
    if tool == "Edit":
        return ti.get("new_string") or ""
    content = ti.get("content") or ""
    root = os.environ.get("CLAUDE_PROJECT_DIR")
    if not root:
        return content
    try:
        rel = Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
        r = subprocess.run(["git", "show", "HEAD:" + rel], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", cwd=root, timeout=15,
                           creationflags=CREATE_NO_WINDOW)
    except Exception:                               # noqa: BLE001
        return content
    if r.returncode != 0:
        return content                              # new file, so all of it is added
    old = set(r.stdout.splitlines())
    return "\n".join(l for l in content.splitlines() if l not in old)


def main() -> int:
    try:
        # Read the bytes and decode as UTF-8 explicitly. sys.stdin.read() uses the Windows
        # console codepage, which turns an em dash into a replacement character before any
        # regex sees it, so the gate silently passed the one tell it exists to catch.
        # Verified 8 Sep 2026: a real UTF-8 em dash payload did not block until this changed.
        raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
        p = json.loads(raw) if raw else {}
    except Exception:                               # noqa: BLE001
        return 0

    tool = p.get("tool_name") or ""
    ti = p.get("tool_input") if isinstance(p.get("tool_input"), dict) else {}
    path = str(ti.get("file_path") or "")
    if tool not in ("Write", "Edit") or not path:
        return 0

    norm = path.replace("\\", "/")
    if Path(norm).suffix.lower() not in PROSE_EXT:
        return 0                                    # not prose, and no log: that would be every write

    for rx, why in EXEMPT:
        if re.search(rx, norm, re.I):
            _log({"file": norm, "kind": "exempt", "why": why})
            return 0

    try:
        from style_tells import scan
        text = _added_text(tool, ti, path)
        # The marker counts only in what this write adds, and not inside backticks, so a file
        # explaining the marker's own syntax cannot exempt itself forever.
        m = SKIP_MARK.search(re.sub(r"`[^`\n]*`", "", text))
        if m:
            _log({"file": norm, "kind": "str:skip", "why": m.group(1) or "(no reason given)"})
            return 0
        hits = scan(text)
    except Exception as exc:                        # noqa: BLE001
        _log({"file": norm, "kind": "gate error, write allowed",
              "why": "%s: %s" % (type(exc).__name__, exc)})
        return 0

    _log({"file": norm, "kind": "checked", "tool": tool, "hits": len(hits), "chars": len(text)})
    if not hits:
        return 0

    lines = ["Writing standard: %d thing(s) to fix in what this write added to %s."
             % (len(hits), Path(norm).name),
             "Fix the text, then write it again. The `slop-text-removal` skill explains each one.",
             "If the text is a quotation or a deliberate example, add `<!-- str:skip reason -->`."]
    for ln, msg in hits[:25]:
        lines.append("  line %d: %s" % (ln, msg))
    sys.stdout.write(json.dumps({"decision": "block", "reason": "\n".join(lines)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
