"""Bump the plugin version, commit and push, in one command.

An installed machine caches the plugin under its version number, so a push that changes a
skill without changing the version reaches nobody. The cache stays valid and every teammate
carries on running the old file, while GitHub shows the new one. That is the worst shape of
failure available here: it looks fine from the pushing end and is invisible from theirs.

So the bump is not left to memory. This does it, and the pre-push hook refuses a push that
skipped it.

Run:  python tools/release.py "commit message"
      python tools/release.py "message" --minor    # 0.4.1 -> 0.5.0
      python tools/release.py --check              # exit 1 if a bump is owed, changes nothing
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PLUGIN = REPO / "plugins" / "superco-kit" / ".claude-plugin" / "plugin.json"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# A change under any of these reaches the reader, so it needs a new version. A change to the
# README or this tooling does not, because nothing caches those.
SHIPPED = ("plugins/",)


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=str(REPO), capture_output=True, text=True,
                       creationflags=NO_WINDOW)
    if check and r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit(r.returncode)
    return r.stdout.strip()


def shipped_changed_since_push() -> list[str]:
    """Files under plugins/ that differ from what the remote already has."""
    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
    base = upstream if upstream else ""
    names = []
    if base:
        names += git("diff", "--name-only", base, "HEAD", check=False).splitlines()
    names += git("diff", "--name-only", "HEAD", check=False).splitlines()      # unstaged
    names += git("diff", "--name-only", "--cached", check=False).splitlines()  # staged
    # Untracked too. `git diff` cannot see a file git has never heard of, so a brand new skill
    # or hook was invisible here and would have shipped with no version bump, which is the one
    # failure this tool exists to prevent. Found 8 Sep 2026 when the hooks/ folder was added.
    names += git("ls-files", "--others", "--exclude-standard", check=False).splitlines()
    if not base:                                    # never pushed: everything counts
        names += git("ls-files", check=False).splitlines()
    return sorted({n for n in names if n and n.replace("\\", "/").startswith(SHIPPED)})


def version_changed_since_push() -> bool:
    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
    if not upstream:
        return True                                 # brand new repo, nothing cached anywhere
    rel = str(PLUGIN.relative_to(REPO)).replace("\\", "/")
    old = git("show", "%s:%s" % (upstream, rel), check=False)
    if not old:
        return True
    try:
        return json.loads(old).get("version") != read_version()
    except json.JSONDecodeError:
        return True


def read_version() -> str:
    return json.loads(PLUGIN.read_text(encoding="utf-8"))["version"]


def write_version(v: str) -> None:
    t = PLUGIN.read_text(encoding="utf-8")
    t2 = re.sub(r'("version"\s*:\s*")[^"]+(")', r"\g<1>%s\g<2>" % v, t, count=1)
    if t2 == t:
        raise SystemExit("could not rewrite the version field in %s" % PLUGIN)
    PLUGIN.write_text(t2, encoding="utf-8")


def bumped(v: str, minor: bool) -> str:
    parts = [int(x) for x in v.split(".")]
    while len(parts) < 3:
        parts.append(0)
    if minor:
        return "%d.%d.0" % (parts[0], parts[1] + 1)
    return "%d.%d.%d" % (parts[0], parts[1], parts[2] + 1)


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    minor = "--minor" in argv
    msg = next((a for a in argv if not a.startswith("--")), None)

    changed = shipped_changed_since_push()
    if not changed:
        print("nothing shipped changed, no bump needed")
        return 0
    if version_changed_since_push():
        print("version already bumped to %s for %d shipped file(s)" % (read_version(), len(changed)))
        return 0
    if check_only:
        sys.stderr.write(
            "A bump is owed. These reach the reader and the version has not changed:\n  "
            + "\n  ".join(changed)
            + "\n\nRun: python tools/release.py \"<message>\"\n")
        return 1

    if not msg:
        sys.stderr.write("a commit message is required\n")
        return 2
    new = bumped(read_version(), minor)
    write_version(new)
    print("version -> %s (%d shipped file(s) changed)" % (new, len(changed)))
    git("add", "-A")
    git("commit", "-m", "%s (v%s)" % (msg, new))
    git("push", "origin", "HEAD")
    print("pushed v%s" % new)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
