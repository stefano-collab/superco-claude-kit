---
name: build-loop
description: Run a substantial build through plan -> build -> render -> independent check -> iterate, with the rubric fixed before the work starts. Use when the cost of being wrong is high AND the error would stay invisible for a while - client copy and lead magnets, money code, and equally big INTERNAL builds like an observability workflow or an enrichment pipeline. Run it per phase on a multi-phase job. Not for mechanical edits or one-file fixes.
target_model: claude-opus-5
---

# Build loop

The Mitchell Keller harness pattern, adapted for this repo. **The one idea it is built on: the
model that made the work is too generous grading its own homework.** Self-evaluation scores 8/10,
declares itself done, and exits early - so the checker must be a different agent, in a fresh
context, that never saw the maker's reasoning.

Adopted 6 Aug 2026 at Stef's instruction. The upstream package (`LeadGrowGTM/loop-engineer`) was
assessed on 3 Aug and rejected as non-portable - it installs agents into the global `~/.claude/`,
patches the host `CLAUDE.md`, seeds root files, routes to skills we do not have, hard-fails on a
dirty tree (ours always is), and its ship stage needs a private LeadGrow CLI. Stef's call was to
take the harness anyway: *"apart from the leadgrow cli it sounds excellent"*. So this is the
pattern, re-implemented against our own gates, with the parts that cannot work here named below
rather than quietly dropped.

## Not this loop - the other one

**If the goal is a NUMBER rather than an artifact, use `benchmark-loop` instead.** Reply rate,
bounce rate, email find rate, classifier precision, cost per booked call: for those, "did the
thing get made" is the wrong question and this loop's completeness gate cannot express it. The
routing test in one line - **if you could tell it was done by looking at a file, use this loop;
if you could only tell by running a measurement, use benchmark-loop.**

Added 13 Aug 2026, from the two-loop split in the upstream this harness came from. Multi-phase
work often wants both in sequence (build it here, tune it there); never both on one goal.

## When to run it

**The test is NOT "is it client-facing".** That was the original wording and Stef corrected it on
6 Aug: *"why does build-loop only affect client facing stuff, can it not be for internal stuff like
building out an observability workflow at the same level of a saas which is a huge job?"* He is
right, and the evidence was the same day's session - every failure that hurt him was INTERNAL: a
Sunday Report whose sources had been dead for weeks, a reflection job that had silently stopped
reflecting, a monitor whose verdict could never clear. None had a client to catch them, which
makes them worse candidates for going unchecked, not better.

**The real test is: cost of being wrong x how long it would stay invisible.** Run the loop when
both are high.

**Run it for:**

- Client-facing work - cold email scripts, lead magnets, reports, campaign copy.
- **Substantial internal builds** - an observability workflow, an enrichment pipeline, a new
  automation with state, anything multi-file that will run unattended. These need it MORE, because
  nobody downstream will notice they are wrong.
- Money code - pricing, billing, anything that spends.

**Do not run it for:** a mechanical edit, a one-file fix, a skill tweak, or research. The loop
costs three subagents and a rubric. Spending that on a config change is theatre.

**For a build big enough to have phases** (the SaaS-scale case), run the loop PER PHASE rather
than once at the end. A rubric written for a ten-phase job is too abstract to score anything, and
a checker that first sees the work after phase ten cannot tell you which phase went wrong.

**Internal builds also want a watch on them** once they finish. The
loop proves the artefact was built right; a watch proves it keeps working once nobody is
watching. They are different questions and a big internal build needs both.

## The loop

### 1. Plan - BEFORE any building

```
Agent(subagent_type: "harness-planner", prompt: "<goal> + context paths + where to write")
```

It writes `BRIEF.md` and `RUBRIC.md` into the build's working folder. **Read the rubric and
sanity-check it against the client's `profile.md` yourself.** A wrong rubric confidently gates a
wrong build.

**Every acceptance criterion Stef stated in his own words gets its own dimension, and if he said
it twice, make it a gate.** A rubric that scores only what the build side thought to measure will
pass a build he rejects on sight. 8 Aug 2026, the run viewer: nine dimensions, PASS at 4.875/5
with both gates at 5, and his standing requirement, "i wanted it to look exactly like freckle",
was never a dimension. Dimension 5 scored conformance to `design-system.md`, which is the house
standard and not the donor. He scrapped the whole UI the same afternoon. Before accepting the
rubric, list his criteria from the brief and the chat, and check each one appears.

**Do not skip this step and write the rubric later.** That is the single failure the whole
pattern exists to prevent - a post-hoc rubric scores what you already made.

### 2. Build

You build it, in this session, following the governing skill to the letter. Not a subagent:
delegating the make loses Stef's oversight and the skill routing, and he is the approval gate
that upstream's "shipper" agent cannot replace.

Do not read `RUBRIC.md` again while building. Build to the skill and the brief.

### 3. Render

```
Agent(subagent_type: "harness-prover", prompt: "<artifact paths> + <what to render>")
```

It builds the docx, resolves the merge variables against real rows, runs the tests, counts the
list - and reports facts only. Skip this only when the artifact has no rendered form that differs
from its source, which is rare.
**Every command you hand the prover runs for real.** It has Bash and executes what you wrote,
verbatim. On the first run, 6 Aug 2026, a prover step omitted `--no-sync` and created a live Google
Sheet in Stef's Drive that then had to be trashed. Put the dry-run / no-sync / offline flag on every
command in the prover's instruction yourself - the prover will not add it for you.

**Build the prover's evidence list from the RUBRIC's dimensions, not from what you remember
changing.** The checker has no Bash, so anything the prover was not asked for is evidence nobody can
obtain afterwards. In that same run dimension 1 was capped at 4/5 only because the prover was asked
for the test file's diff and not the source file the rubric names.

### 4. Check

```
Agent(subagent_type: "fresh-eyes-checker",
      prompt: "<RUBRIC.md path> + <artifact paths> + <the prover's pasted output>")
```

**Pass it the rubric, the artifacts and the prover's evidence. Never pass it your own reasoning,
your draft notes, or your opinion of the work.** It returns a score per dimension with `file:line`
evidence, and one of PASS / ITERATE / PLATEAU.

### 5. Iterate or stop

- **PASS** - go to Stef's approval gate.
- **ITERATE** - fix EVERY defect the checker named, not only the dimensions that scored low, then
  run 3 and 4 again. Append each round to `CYCLE_LOG.md`. One contact bake-off, 24 Aug 2026:
  round 2 scored 4.0 and docked three dimensions on named defects; round 3 fixed the failing gate
  alone and left the other three, and the mean fell to 3.3. A defect left in place does not stay
  in the dimension that found it, and the round is spent.
- **PLATEAU** - the mean moved by less than +-0.1 between rounds. **Stop looping and take it to
  Stef with the log.** A plateau means the remaining gap needs a decision, not another attempt,
  and grinding past it burns tokens to move a number rather than the work.

Cap at **3 rounds** unless Stef says otherwise. If it has not passed by then, the brief or the
rubric is wrong, and that is a conversation.

**Never ask Stef whether to run the remaining stages.** Once the loop starts, the prover, the
fresh-eyes checker and each iterate round run automatically; the only gate is his ship approval
at the end. Asking mid-loop stalls the build and hands him a decision he already made when he
asked for build-loop. Stef, 19 August 2026, on being asked to authorise the fresh-eyes check.

### 6. Ship - which here means Stef

There is no shipper agent. Upstream's runs `/no-mistakes` and opens a PR through a CLI we do not
have, and our own rules forbid an unattended `git push` anyway. **The ship gate is Stef's
approval, unchanged**, and the loop's job is to arrive at it with the work already checked. Give
him the artifact, the PASS verdict and the cycle log together - and where the build is a campaign,
the pre-launch QA result alongside it, per `CLAUDE.md`.

## What it produces

In the build's working folder:

```
BRIEF.md      the problem, success criteria, out of scope, constraints, risks
RUBRIC.md     3-6 dimensions, each with a concrete 5 and 1, plus the PASS threshold
CYCLE_LOG.md  one entry per round: scores, evidence, verdict, what changed next
```

Keep them with the deliverable. `CYCLE_LOG.md` is what turns "I think it is good" into a record
of what was actually checked and what it scored.

## The three agents

| Agent | Does | Cannot |
|---|---|---|
| `harness-planner` | BRIEF + RUBRIC before the build | Run anything, build anything (no Bash, no Agent) |
| `harness-prover` | Renders the artifact, reports facts | Score, judge, or fix (its own rules) |
| `fresh-eyes-checker` | Scores against the rubric, PASS/ITERATE/PLATEAU | Run or regenerate the work (no Bash, no Agent) |

**The isolation is mechanical, not a promise.** Planner and checker have no Bash and no Agent
tool, so they physically cannot execute or delegate. That is the whole reason the checker's score
is worth anything.

## Deliberately not adopted

- **`harness-maker`** - we keep the make in the main session for oversight and skill routing.
- **`harness-shipper`** - needs `/no-mistakes` and a private CLI; Stef's approval is the gate.
- **Provider-aware model resolution** (bun scripts, claudex/codex proxies) - irrelevant here.
- **Global `~/.claude/agents/` install** - our agents live in the repo, versioned with it. This
  was the main reason the upstream installer was rejected.
- **`harness-inbounds-checker` and `harness-novelty-checker`** - built for a benchmarking climb
  loop we do not run. **The novelty checker is worth revisiting** the moment we keep a copy
  variant ledger: it rejects a variant that is a near-duplicate of one already measured, which is
  exactly the check the monthly copy refresh needs to avoid being fingerprinted.

## What two real runs of this loop actually cost, and where the value was (19 Aug 2026)

Two builds went through the full loop the same day - a transcript-outage watcher and a CloudTalk
reliability fix. Both PASSED or reached PASS-1, and the numbers are worth having before quoting
an ETA:

- **A phase is ~45-60 min of build plus ~15 min of harness.** Planner, prover and checker are
  ~90-210s each; what dominates is the round trips, not the agents.
- **Budget TWO prover passes on any build the user is still correcting.** The first prover pass
  here graded code that no longer existed - Stef corrected a core assumption mid-build - and the
  whole cycle had to be re-run. That is not waste to be avoided, it is the normal shape of a
  build where the user is the only source of what the data MEANS.
- **The checker earned its cost on the gate, not on the mean.** Both builds cleared the mean
  comfortably (4.17 and 4.67) while failing the gate on something real. A mean-only rule would
  have shipped both.

**The most valuable thing the loop did was refuse a build that "worked".** The transcript watcher
passed every test, ran green on the deployed job, and had a defect that made three leads vanish
from its own output - the exact failure it was built to prevent, one level down. Nothing in the
build side found it; a fresh context reading the rubric did, twice.

**And the prover is worth more than it looks.** It reported, unprompted, that the deployed run
being cited as verification predated the fix by seven minutes, and that the new module had no
tests of its own. Both were true, both were mine, and neither would have surfaced from the build
side - the maker knows what they meant to prove.

Corollary for the ITERATE rounds: fix the specific dimension and RE-READ the file before
re-submitting. One round here was spent on a verdict that scored a line I had already changed,
because the evidence I pasted was newer than the file the checker had read.
