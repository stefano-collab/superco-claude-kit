---
name: setup
description: Interview the person, then build them their own Claude working setup - the folder structure, the CLAUDE.md it reads every session, the .env for their keys, and a first skill for whatever they repeat most. Use on a first session, or when someone says set me up, build my setup, get me started.
---

# Setup

Builds someone their own working setup, from an interview rather than a template.

The whole value is in the interview. A folder structure copied from someone else is worth
almost nothing, because the thing that makes it work is that it matches how that person
actually works. So the rule below is absolute.

## Before anything else, how you write

This applies from your very first reply, not just to the files at the end. It's first here
because when it sat further down the page it got ignored.

- Normal hyphens only. No em dashes, no en dashes, in any reply or any file. Use a comma, a
  full stop or brackets.
- Digits for numbers. "5 minutes", "3 rules", never "five" or "three".
- Ordinary complete sentences. Not clipped, not punchy.

The `slop-text-removal` skill ships alongside this one and has the rest. Read it before you
write the files in Phase 3.

## The rule

**Ask the questions first. Write nothing until they're answered.**

Not one folder, not one file, not a draft to react to. If the person gives short answers,
ask again. If they say "just do whatever", say that you need 5 minutes of answers or the
result will be generic, and ask again.

An unanswered question is never filled with a sensible default. It gets asked.

## Phase 1: interview

Ask in small batches, and react to what comes back. These are the areas to cover, not a
script to read out.

**What they do**

1. What's the job, in their words? Not the title, the actual work.
2. Walk through a normal week. Where does the time go?
3. What do they do repeatedly that follows the same shape every time?
4. What's the task they'd most like to never do by hand again?

**How their work is organised**

5. What's the unit of their work? Clients, brands, projects, campaigns, stores, cases?
   This decides the folder structure, so get a real answer rather than a guess.
6. Roughly how many of those are live at once, and what's a real one called?
7. Where does the information about each one currently live? Email, a doc, a spreadsheet,
   their head?

**What they already have**

8. Which tools do they use every day? Name them.
9. Which of those have an API key they could get hold of, or already have?
10. Have they built anything with AI already, even something small? What was it?
11. What have they tried that didn't work?

**Their standards**

12. What does good written work look like to them? Ask for a real example if they have one.
13. What must it never do? Get specifics. "Never write to a client without me reading it"
    is a rule. "Be professional" isn't.
14. Where do they want to be asked before it continues, and where should it just run?

**The honest one**

15. Is there anything on this list that doesn't actually need AI? Say so if you spot one.
    An answer of "that's a filter in your email client" is worth more than a skill that
    half works.

## Phase 2: read it back

Before building, summarise what you heard in under 20 lines: their work, their unit, their
rules, and the first thing worth automating. Ask them to correct it.

Wait for the correction. People change an answer here more often than not, and a structure
built on the uncorrected version is wrong from the first day.

## Phase 3: build

Only now. 4 things, in this order.

**1. The folder structure**, using their unit from question 5 and their real names from
question 6. A structure with `client-a` and `client-b` in it has already failed.

```
CLAUDE.md              read first, every session
.env                   every key in one place, never pasted into a chat
<their-unit>/          one folder per client, brand, project, whatever they said
  <a real one>/
    profile.md         everything Claude should know about this one
knowledge/             what they believe about their craft, and their standards
skills/                the jobs, written down once each
```

Fewer folders than you think. Only create one they gave you a reason for.

**2. CLAUDE.md**, written from their answers to questions 12, 13 and 14. Every line traces
to something they said. Quote them where the wording is theirs.

It's the file read first in every session, so their rules apply without them repeating
themselves. Keep it short. A long one gets skimmed by everybody, including the model.

**3. `.env`**, listing the keys for the tools they named in question 9, as names with empty
values. Add it to `.gitignore` in the same breath. Never put a real key in any other file,
and never print one back into the chat.

**4. One skill**, for their answer to question 4. Just the one. It's the proof that the
setup does something, and a second one built before the first has been used is a guess.

Write it, then run it on something real in front of them, then fix what the run exposed.

## Check your own output before Phase 4

Reread what you wrote, and what you said, against the rules at the top of this file.

Measured across test runs: the setup built for someone who explicitly asked for no em dashes
had none, and the setup built for someone who didn't ask had 25 across 6 files. Stating the
rule once at the top isn't reliably enough on its own, so check the files by eye before
handing them over.

## Phase 4: hand over

Tell them 3 things and stop.

- Where their CLAUDE.md is, and that adding a line to it changes every future session.
- That "make this a standing rule" is how they add a line without opening the file.
- That the first build of anything takes about 3 times longer than doing it by hand, and
  every run after that is faster. Someone who doesn't know that quits during the first one.

## What good looks like

Two people who run this should end up with visibly different setups. Different folder names,
different rules in CLAUDE.md, a different first skill.

If two runs produce near-identical output, the interview was skipped and this skill failed,
whatever the files look like.
