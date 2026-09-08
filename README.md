# Superco Claude kit

The skills from the AI session on 7 September, packaged so you can install them in about
2 minutes and get updates without doing anything.

Start with `/setup`. It interviews you and builds your own working setup from your answers.
Everything else in here is optional.

---

## Before you start

You need Claude Code. If you already have the Claude desktop app, you already have it: it's
the third tab along the top, next to Chat and Cowork. Same app, same login, nothing to
install.

If you don't have the desktop app, download it from claude.ai and sign in with your Superco
account.

You don't need a terminal, a GitHub account or git. The 2 commands below get typed into the
Claude Code chat box, the same way you'd type a message.

One thing to do first: make an empty folder somewhere sensible for your work, called
whatever you like. Claude Code works inside a folder, and it'll ask you to pick one the
first time you open the Code tab. Point it at the folder you just made. Everything `/setup`
builds will go in there.

---

## Install

Open the Code tab, with your folder open, and type this:

```
/plugin marketplace add https://github.com/stefano-collab/superco-claude-kit.git
```

Use the full address, not the short `owner/repo` form. The short form connects over SSH,
which needs keys set up, and the full one doesn't.

Then this:

```
/plugin install superco-kit@superco
```

Restart Claude Code when it asks. That's it.

To check it worked, type `/plugin list` and you should see `superco-kit`.

**If the first command fails**, it's almost always one of 2 things. Either the Code tab
hasn't been opened in this project folder yet, in which case open a folder first and try
again, or your Claude account settings block outside plugins, in which case message me and
I'll sort it with whoever administers the account.

---

## Then run this

```
/setup
```

It asks you about 15 questions: what your week actually looks like, how your work is
organised, which tools you use, what you'd never let it touch. Then it builds you a folder
structure, the `CLAUDE.md` it reads at the start of every session, a place for your API keys
and one skill for whatever you said you repeat most.

It won't write anything until you've answered. That's deliberate. A setup copied from
someone else's is worth very little, because what makes one work is that it matches how
that person works.

Give it 10 minutes and real answers. If you type "just do whatever", it will ask again.

---

## What's in the kit

Everything here works the moment it's installed, apart from the 2 marked otherwise.

| Skill | What it does | Reach for it when |
|---|---|---|
| `setup` | Interviews you, then builds your setup from your answers | First session. Start here |
| `grill-me` | Makes Claude interrogate you before it builds, so you answer questions instead of writing a brief | Writing the brief is the part you dread |
| `call-context` | A call transcript in, a structured brief out: attendees, pain points in their words, next steps with owners | You run client calls and the notes go stale |
| `slop-text-removal` | The writing standard. 34 tells that make text read as machine-written, and the fix for each | A first draft comes back sounding like nobody |
| `design-system` | The design standard. The direction gate, the diversification rule, the anti-AI tells, 21 hard rules and both render gates | Anything that gets looked at rather than read |
| `skill-creator` | Writes skill files properly. Record yourself doing the task once, hand it the recording | You have a second thing worth automating |
| `format-fidelity` | Copies the exact formatting of a document or a web page and proves it matches before you send it. Needs LibreOffice and 2 Python packages | Rebuilding something in a client's template |
| `build-loop` | For a big build. Writes the scoring rubric before the work exists, then something that didn't do the building checks it. Uses subagents | Being wrong would stay invisible for weeks |

### On the writing and design standards

Read them, then change them. They're mine, and they carry my opinions and my clients'
constraints. The parts worth keeping are the method and the tells. The parts worth replacing
are anything that assumes my work rather than yours.

The writing standard has one instruction that matters more than the rest of it: it's a
checklist you read a draft against, never a "make this sound human" rewrite. A bulk rewrite
flattens whoever the copy is meant to sound like. That was measured rather than asserted, and
the numbers are in the file.

---

## Updates

I push a change to this repo. Claude Code refreshes marketplaces in the background, and the
update applies the next time you restart. You don't reinstall and I don't send anything
round.

To pull an update immediately rather than waiting:

```
/plugin marketplace update superco
```

If a skill starts behaving differently from how it's described here, that's why. Tell me and
I'll fix it at the source, which fixes it for everybody.

---

## What isn't here

The receipt collector from the session. It reads a Gmail inbox, converts currencies and writes
into a specific spreadsheet, so it's wired to my accounts and my sheet rather than being
something you can install. The logic transfers, the wiring doesn't. Message me on Slack and
we'll build yours in an hour.

---

## One thing worth knowing before you start

The first time you build anything with this, it takes about 3 times longer than doing the
job by hand. Every run after that is faster. Most people who give up on this give up during
the first one, before they've seen the second.

---

## Help

Slack me. If a skill did something odd, paste what you asked and what it did, because that's
usually enough to fix the skill rather than just your session.
