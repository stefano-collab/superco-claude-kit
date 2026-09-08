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

## Phase 3: connect their tools

Their own tools are where the useful context lives, so wire them up now. These are official
plugins maintained by the vendors, so nobody has to hunt for an API key.

The marketplace that carries them isn't on a fresh machine, so add it first:

```
/plugin marketplace add anthropics/claude-plugins-official
```

Then install the ones that match their job:

| Job | Install |
|---|---|
| Delivery and project management | `atlassian`, `shopify-ai-toolkit`, `figma`, `slack` |
| Marketing and content | `slack`, `figma` |

```
/plugin install atlassian@claude-plugins-official
```

Say what each one does before you install it, in a line each. Atlassian reads and writes Jira
issues and Confluence pages. Slack searches messages and threads they already have access to.
The Shopify toolkit brings live documentation search and GraphQL validation, which is the fix
for a model that confidently gets Shopify wrong. Figma reads design files.

Install the whole row for their job unless they named a tool they don't touch. Somebody who
never opens Figma doesn't need it, so skip it and say out loud that you skipped it and why.
Silently installing less than the table says is the thing to avoid, because then nobody knows
what they have.

Then tell them 2 true things, because both matter:

- Installing a connector doesn't sign them in. The first time one gets used it asks them to
  authorise it, and they see exactly what it wants.
- Connectors only register after a restart, so they won't work in this session. Everything
  else this skill builds does.

## Phase 3b: what you can read right now

Connectors start working next session, so this session uses whatever they can point you at.
Ask for a folder path or a few pasted examples. That's the normal route, so treat it as
normal.

If something fails, say what failed and carry on. Never leave a half built repository behind,
and never write a file that pretends a read succeeded.

### The .env rule

Write a key name into `.env` only when something in this kit or one of their installed
connectors actually reads it. An empty `JIRA_API_TOKEN=` that nothing consumes is worse than
no line at all, because they fill it in and nothing happens.

Most of what this setup does needs no key. Where one is genuinely needed, ask them to paste it
into `.env` themselves, add `.env` to `.gitignore`, and never print a key back into the chat.

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

### 3. The .env file, only if it earns its place

Follow the .env rule in phase 3b. A key name goes in only when something actually reads it,
and for most people that means this file is empty or close to it, because the connectors
handle authentication themselves.

Create it with `.gitignore` alongside either way, so there's somewhere obvious for a key to
live later.

If they have no keys and wouldn't know where to find one, say so plainly and move on. The
connectors installed in phase 3 cover the tools they named, so a missing key blocks nothing.

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
