# Maintaining this kit

For whoever pushes to it. The team never needs this file.

## Bump the version on every push, or nothing reaches anybody

This is the one rule, and it's counter-intuitive enough to have been proven the hard way.

`plugins/superco-kit/.claude-plugin/plugin.json` carries a `version`. An installed machine
caches the plugin under that version number. If you push a changed skill without changing the
version, the cache stays valid and every installed machine keeps running the old file. The
push succeeds, GitHub shows the new content, and not one person receives it.

Measured on 8 September 2026: a skill edit was pushed at 0.2.0 with no bump. `plugin
marketplace update` reported success and the installed copy on disk was still the old file. A
live test run against that install still showed the old behaviour. Bumping to 0.2.1 and
running `plugin update` produced a new cache directory containing the change, and the same
test then passed.

So the sequence for any change is:

1. Edit the skill.
2. Bump `version` in `plugins/superco-kit/.claude-plugin/plugin.json`.
3. Commit and push.

Their machines pick it up in the background, or immediately with `/plugin marketplace update
superco` then `/plugin update superco-kit`, then a restart.

## Before you push

```bash
python ../tools/scrub_gate.py .     # refuses to publish anything private
claude plugin validate .            # manifests and every skill
```

The scrub gate is the thing standing between a private client name and a public repo. It
carries 9 rules and it's checked against a deliberately planted bad fixture, so it's known to
fire rather than assumed to. Never publish past a failing run: fix the file.

## What is deliberately not in here

The design standard and the emulation skill, held back for a rewrite. The receipt collector,
which is wired to one person's mailbox and spreadsheet and can't be installed by anyone else.

## Adding a skill

Drop a folder under `plugins/superco-kit/skills/<name>/` with a `SKILL.md` carrying `name` and
`description` frontmatter. Validate, bump, push. It appears for everyone with no action on
their side.

Write the description for the person who'll never read this repo. It's the only thing Claude
sees when deciding whether the skill is relevant, and it's what the reader sees in the list.
