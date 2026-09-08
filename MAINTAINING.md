# Maintaining this kit

For whoever pushes to it. Nobody installing the kit needs this file.

## Bump the version on every push, or nothing reaches anybody

`plugins/superco-kit/.claude-plugin/plugin.json` carries a `version`, and an installed machine
caches the plugin under that number. Push a changed skill without changing the version and the
cache is still treated as valid, so the push works and GitHub shows the new content while every
installed machine carries on serving the old file.

This was measured on 8 September 2026. A skill edit was pushed at 0.2.0 with no bump, and
`plugin marketplace update` reported success while the installed copy on disk was still the
old file. A live test run against that install still produced the old behaviour. Bumping to
0.2.1 and running `plugin update` created a new cache directory with the change in it, and the
same test then passed.

Edit the skill, then run this:

```bash
python tools/release.py "what changed"
```

That bumps the patch version, commits and pushes. Add `--minor` for a bigger change.

There's also a pre-push hook that refuses a push touching anything under `plugins/` when the
version hasn't moved. It lives in `.git/hooks/`, which git doesn't clone, so install it once
per machine:

```bash
printf '#!/bin/sh\npython tools/release.py --check || exit 1\n' > .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

Both were tested on 8 September 2026 by editing a skill without bumping. `--check` exited 1
and named the file, and the real `git push` was refused. A push that touched only tooling went
through untouched.

Their machines pick it up in the background. If someone wants it immediately they can run
`/plugin marketplace update superco` and then `/plugin update superco-kit`, then restart.

## Before you push

```bash
python ../tools/scrub_gate.py .     # refuses to publish anything private
claude plugin validate .            # manifests and every skill
```

The scrub gate is what keeps a private client name out of a public repo. It carries 9 rules, and there's a fixture in
`tests/fixtures/knownbad/` to prove it fires. The fixture has 4 things planted in it:

- a client name
- an absolute Windows path
- a fake API key
- an em dash

Run the gate against that fixture and it should exit 1 and name all 4. If a run over the repo fails, fix the file it names, and don't publish
past it.

## What is deliberately not in here

The design standard and the emulation skill are held back for a rewrite. The receipt collector
is wired into one person's mailbox and spreadsheet, so nobody else can install it.

## Adding a skill

Drop a folder under `plugins/superco-kit/skills/<name>/` with a `SKILL.md` carrying `name` and
`description` frontmatter. Then validate it, bump the version and push. It appears for
everyone with no action on their side.

Spend time on the description. Claude reads it to decide whether the skill is relevant to what
someone just asked, and it's also the line the reader sees in their skill list.
