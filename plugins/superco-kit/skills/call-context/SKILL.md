---
name: call-context
description: Turn a call transcript into a structured brief - attendees, pain points in their own words, triggers, objections and next steps. Use when someone references a call, meeting or transcript, or wants a conversation turned into something actionable.
allowed-tools: Read, Write, Grep, WebSearch
---

# Call context

A transcript is not a brief. This turns one into the other, in the speaker's own language.

The brief you write follows the `slop-text-removal` skill that ships alongside this one. Use
normal hyphens rather than em dashes. Digits for numbers. No bold mid-sentence.

## Phase 1: get the transcript

Ask where it is coming from:

- A folder you already keep them in. Say where once and it will look there every time.
- Pasted text.
- A file path.

Whatever records your calls, read the text rather than calling its API. Note that some
recorders return only metadata and an AI summary on every tier, which is not a transcript
and will quietly give you a brief about a summary.

Read the whole thing before extracting anything.

## Phase 2: extract

- **Company:** name, size, industry
- **Attendees:** names, titles, role in the decision
- **Pain points:** their exact words, not a paraphrase
- **Current tools:** what they use now, what they tried before
- **Triggers:** why now, what changed, what the timeline is
- **Objections:** concerns raised, and whether each was answered or left open
- **Next steps:** what was agreed and who owes it
- **Quotable moments:** the lines that reveal what they actually think

## Phase 3: write the brief

```
## Call brief: [Company], [Date]

### Attendees
- [Name] ([Title]), [role in the decision]

### Pain points, their words
1. "[exact quote]" - [context]
2. "[exact quote]" - [context]

### Current stack
- [Tool]: [what they use it for]

### Triggers
- [Why they are looking now]

### Objections
- [Concern]: [how it was addressed, or left open]

### Next steps
- [ ] [Action] - [owner]

### Angles
- [Two or three follow-up angles that trace to a specific thing they said]
```

## Before you call it done

- [ ] Pain points use their language, not yours
- [ ] Every attendee has a title
- [ ] Next steps name an owner and are specific, never "follow up"
- [ ] Each angle traces to a quote above it

## A note on quoting people

The brief will be read by people who were not on the call. A quote taken out of its
context can make a colleague or a client sound worse than they were. Quote the problem,
never the person.
