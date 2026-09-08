---
name: setup
description: Interview someone about their job and build them a working Claude setup for it - the folder structure, the CLAUDE.md read every session, a knowledge base filled from their real material and a first skill. Use on a first session, or when someone says set me up, build my setup, get me started.
---

# Setup

Builds someone a working repository shaped around the job they actually do.

2 things make this worth running rather than copying a folder tree off the internet. It
asks before it builds, and it fills the knowledge base with their own material rather than
leaving empty files.

## How you write, from your first reply

- Normal hyphens rather than em dashes or en dashes, in any reply and any file.
- Digits for numbers. "5 minutes", "3 rules", never "five" or "three".
- Ordinary complete sentences, not clipped and not punchy.
- No bold in the middle of a sentence.

The `slop-text-removal` skill ships alongside this one and carries the rest.

## The rule

Ask the questions first, and write nothing at all until they have been answered. Not one
folder, not one file, not a draft for them to react to.

If someone says "just do whatever", tell them that a setup built without their answers is a
folder they will stop opening, and ask again. An unanswered question gets asked rather than
filled with a sensible default.

## Phase 1: which job

Ask this before anything else, because it decides the whole shape:

> Which is closest to your job? Delivery and project management, or marketing and content?
> If neither fits, describe what you do in a sentence.

Everything below forks on the answer. If they describe something else, build the closest
shape and say which one you used and why.

## Phase 2: interview

Small batches, reacting to what comes back. Cover these, without reading them out as a list.

**Both jobs**

1. What is the job in their own words, rather than the job title?
2. Where does a normal week actually go?
3. What do they do repeatedly that follows the same shape every time?
4. What would they most like to never do by hand again?
5. What must Claude never do? Push for specifics. "Never send anything to a client without
   me reading it" is a rule, and "be professional" is not.
6. Where do they want to be asked before it continues, and where should it just run?
7. Is anything on this list not really an AI problem? Saying "that's a filter in your email
   client" is worth more than a skill that half works.

**Delivery and project management**

8. What is the unit of the work? Projects, clients, builds, stores?
9. How many are live at once, and what is a real one called?
10. Which platform do they spend the most time in, and which version or API surface matters?
11. Where do project decisions currently live? Jira, a doc, a call recording, their head?
12. What makes a brief or a scope good enough that a developer doesn't come back with
    questions?

**Marketing and content**

8. What is the unit of the work? Brands, campaigns, events, clients?
9. How many are live at once, and what is a real one called?
10. Whose voice does the writing have to sound like, and where are the best examples of it?
11. Which part of writing do they want help with? Almost nobody wants a first draft, so ask
    rather than assuming.
12. What are they measured on?

## Phase 3: what you can reach

Ask what you're allowed to pull from, and offer both routes plainly:

> I can pull your own material in so this is useful immediately. If you have an API key for
> the tools you use, I can read from them directly. If you haven't got one, point me at a
> folder or paste a few examples and that works too.

Then, for whichever applies:

- **A key exists.** Ask them to put it in `.env` themselves rather than pasting it into the
  chat. Read it from there. Never print a key back, and never write one into any other file.
- **No key.** Ask for a folder path or a few pasted examples. This is the normal case, so
  treat it as normal rather than as a downgrade.

If a pull fails, say what failed and carry on with the other route. Never leave a half built
repository behind, and never write a file that pretends a pull succeeded.

## Phase 4: read it back

Summarise in under 20 lines what you heard: their job, their unit, their rules, what you can
reach and the first thing worth automating. Ask them to correct it, and wait.

People change an answer at this point more often than not, and a structure built on the
uncorrected version is wrong from its first day.

## Phase 5: build

Only now, and in this order.

### 1. The folder structure

Use their unit from question 8 and their real names from question 9. A tree containing
`client-a` and `client-b` is one they won't recognise as theirs.

Delivery and project management:

```
CLAUDE.md                        read first, every session
.env                             keys, never pasted into a chat
projects/<a real one>/
  profile.md                     everything Claude should know about this one
knowledge-base/
  <platform>.md                  what the docs say, pulled in phase 6
  how-we-scope.md                what good looks like here
  LEARNINGS.md                   what it got wrong once, so it stops
skills/
  <their answer to question 4>/
```

Marketing and content:

```
CLAUDE.md
.env
brands/<a real one>/
  profile.md
knowledge-base/
  voice.md                       their register, built from real examples
  LEARNINGS.md
skills/
  <their answer to question 4>/
```

There's no clients folder in the marketing shape. They work on their own company's
marketing, so a clients folder would sit empty and make the tree look like someone else's.

Build fewer folders than you think you need, and only ones they gave you a reason for.

### 2. CLAUDE.md

Write it from their answers to questions 1, 5 and 6. Every line traces to something they
said, and where the wording is theirs, quote it.

It gets read first in every session, so their rules apply without them repeating themselves.
Keep it short, because a long one gets skimmed by everybody including the model.

### 3. The .env file

List the keys for the tools they named, as names with empty values, and add it to
`.gitignore` in the same breath.

If they have no keys and wouldn't know where to find one, say so plainly and move on. Write
the file with the tool names and a comment saying where each key comes from, so it's ready
when they want it. Most of what this setup does needs none, so don't let it feel like a
prerequisite.

## Phase 6: fill the knowledge base

An empty knowledge base is the reason most of these get abandoned in week 2. Put real
material in it now, while they're watching.

**Delivery and project management.** Pull the current documentation for the platform they
named in question 10. Try `llms.txt` at the root of the docs site first, because it's a
single file written for this purpose and it saves crawling. Write
`knowledge-base/<platform>.md` with the version or date you pulled, the sections that matter
to their work and the links, rather than a copy of the whole thing.

Then get their real work in. Ask for recent call notes, tickets or scoping documents, by API
if they have a key and by folder or paste if not. Read them and write
`knowledge-base/how-we-scope.md` from what is actually in them, not from what a good scope
looks like in general.

**Marketing and content.** Collect 20 to 30 pieces of their own published writing, or the
writing they want to sound like. That's what `knowledge-base/voice.md` is built from: the
register, the sentence shapes, the words they use and the ones they never use. A voice file
written from adjectives is worthless, so it has to come from real passages.

For both, create `knowledge-base/LEARNINGS.md` with a single line explaining what it's for:
one insight per line, added whenever something goes wrong, read before the next run.

Say out loud what you pulled and how current it is. If the platform documentation is 3 months
old, that's a fact they need rather than a detail to hide.

### One skill

Build it for their answer to question 4, and only that one. A second skill built before the
first has been used is a guess.

## Phase 7: prove it runs

Don't hand over a folder you have never used.

Run the skill you just built, once, on something real of theirs, while they watch. Fix what
the run exposes. If it needs something they haven't given you, that's the most useful thing
this session can find, so say so and fix it now.

Then reread every file you wrote against the rules at the top of this skill. Measured across
test runs, a setup built for someone who asked for no em dashes had none, and one built for
someone who didn't think to ask had 25 across 6 files.

## Phase 8: hand over

Tell them 3 things and stop.

- Where their CLAUDE.md is, and that adding a line to it changes every future session.
- That saying "make this a standing rule" adds a line without them opening the file.
- That the first thing they build takes about 3 times longer than doing it by hand, and
  everything after that's faster. Someone who doesn't know that quits during the first one.

## What good looks like

Two people who run this end up with visibly different setups: different folder names, a
different first skill, different rules in CLAUDE.md and a knowledge base with their own
material in it.

If two runs produce near identical output, the interview was skipped and this skill failed,
whatever the files look like.
