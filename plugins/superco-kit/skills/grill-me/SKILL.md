---
name: grill-me
description: Make Claude interrogate you before it builds anything, so you answer questions instead of writing a brief. Use before a new skill, a new integration, a campaign, a document, or any job with more than one decision in it. Triggers on "grill me", "before building", "interrogate me".
---

# Grill me

Reverses who does the work of specifying. Instead of writing a brief and watching it come
back wrong, you answer questions until the ambiguity is gone, and the thing gets built once.

Use it when writing the brief is the part you dread, or when you can tell you have not
thought it through yet and want something to find the holes.

## When

- A new skill, or a new connection to a tool
- A document whose shape you have not settled
- Anything with more than one decision in it
- Any time your first instinct is "I am not sure how to ask for this"

## The prompt

```
Before building, grill me.
Ask every question needed to avoid wrong assumptions.
Focus on:
- inputs
- outputs
- where I want to check it before it continues
- what failure looks like
- how we will know it is good
- what you must never do
- where this should be interactive and where you should just run
```

## How it should run

1. Questions come in tight batches, not one at a time and not forty at once. The one or two
   that most change the build come first.
2. Skip anything already answered in your project instructions or your own files. A question
   whose answer is written down is a wasted turn.
3. When the questions run out, it restates the spec back to you: inputs, outputs,
   checkpoints, failure modes, what good looks like, what it must never do.
4. Only then does it build. If a new assumption shows up halfway, it stops and grills again.

## If you are building a skill

List the reference material the skill will need before the grilling starts, and make those
files out of real examples rather than invented ones. Do the work up front and the skill
consumes it. What makes a skill better than a good prompt is the documented opinion inside
it, and an opinion has to come from somewhere real.

## What you get

A short spec you can read in a minute and approve, or correct. Approve it and the build
starts from something you have actually agreed to.

## Why this one is worth having

Most bad output is not a model failure. It is a briefing failure that nobody caught until
the work came back. Being asked six good questions costs two minutes and removes the round
trip where you explain what you meant.
