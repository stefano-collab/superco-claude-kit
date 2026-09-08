---
name: slop-text-removal
description: The house standard for written output. What good reads like, the AI tells in measured order, and the hard formatting rules. Use before any prose deliverable goes to a client or a colleague - documents, emails, reports, landing pages and any prompt that emits prose.
---

# Slop text removal

The single source of truth for how written output reads. It's the default for everything
written that isn't a chat reply.

Read your own draft against it. It's a detection pass, never a "humanise this" rewrite. That
distinction matters more than anything else on this page: a bulk rewrite flattens whoever the
copy is meant to sound like, and quietly converts US spelling to British on its way past.

## What it applies to

Documents, proposals, reports, landing pages, internal notes, plans, emails and messages
including ones you'll paste somewhere else, and any prompt or template that generates prose.

For a prompt or a template, scan the copy it emits rather than the instructions. A prompt is
mostly orders addressed to the model, where a full verb form is correct. The emitted copy is
the fact list the model reuses verbatim, the answer templates and the link text. Scanning
everything flags 60 correct instructions and no real defect, and a gate that cries wolf gets
switched off.

## What it doesn't apply to

Anything with its own voice system: sales scripts, social posts and copy written to sound
like a specific person. Where you spot a tell in one of those, fix it in that thing's own
voice guide as well as here. Don't run this file over it.

## The order is fixed, and the tells are not first

Measured in two blind tests on 7 September 2026: copy written with this file as the system
prompt read as machine-written in 5 of 6 registers, and looping it through a judge until every
tell was gone made it worse. Removing slop pushes the model into a second machine register,
clipped and punchy ("Two weeks in: 4,200 sent"), because no list of faults ever says "don't
compress". Copy written from a description of how a real person writes, plus 30 of their own
passages and no tells at all, was approved first time in 4 of 5 registers.

So:

1. Write from the register and from real passages. Collect 30 pieces of writing by the
   person or the brand the copy should sound like. That is the prompt. Not this file.
2. Then read the draft against the tells below and fix what the read finds, by hand.
3. Then run a mechanical check for the formatting rules. It's the last gate, never the first.

If you have no corpus yet, start one. Every time you rewrite something the model produced,
save the before and the after. 30 samples is enough to change the output.

### The register

- Ordinary, complete sentences. Not clipped, not punchy, not compressed. A sentence has a subject and a verb and says one thing. "The campaign has been live for 2 weeks and we have sent 4,200 emails" rather than "Two weeks in: 4,200 sent".
- Plain connectors between sentences: "Also,", "However,", "This means that", "So", "but". They are used freely and are not a fault.
- Repeating a word is fine. If the subject is replies, the word "replies" appears in every sentence that is about replies. No synonyms for variety.
- Digits for every number. 6 rather than "six", 2 weeks rather than "two weeks".
- Contractions where a person would use them, not forced. "it's", "don't", "isn't", and also "we have" and "that is" when they come naturally.
- No tail on a sentence that comments on the sentence. The fact is stated and the sentence ends. No "which is a good sign", no "not just the label", no "and it shows".
- No colon followed by a list of fragments. No opener like "Quick update:" or "Three things:". Start with the first fact.
- No sales phrasing and no chattiness. Not "happy either way", not "worth a look", not "let me know and I'll action it", not "keen to get your view". Ask the question and stop: "Do you want us to re-approach him or leave it?"
- Asides go in brackets. Never a pair of dashes.
- Emails: greeting on its own line, then the facts, then the question, then a sign-off. Nothing else.
- Reports and documents: slightly formal, third person where the agency is the subject, still ordinary sentences. "A closer look at this month's replies found that the sequencer's labelling understates positive replies."
- Length: as long as the facts need, never shorter. Cutting words is not the goal; leaving nothing clever in is.
- No short verdict sentence after a fact. "This rule is false." and "The fix is X." are the model's punch; fold them into the sentence before with "which is wrong" or soften them: "It would be fixed by matching on the domain".
- Ordinary words over exact ones. "wrong" not "false", "fixed" not "prioritised", "the display name issue" not "the display-name fix". No hyphenated compounds built for the sentence.
- Quoted phrases in single quotes.
- "Don't" and "isn't" even in a document. "Do not" only where the sentence stresses it.

### Passages Stef approved or wrote, one per register

Client email:

"Hi Victoria, / The September campaign has been live for 2 weeks now. We have sent 4,200
emails, had 11 positive replies and booked 3 calls, of which 1 was a no-show. / Can you confirm
the 2 remaining booked calls are in your diary for next week? Also, do you want us to
re-approach the no-show or leave it? / Thanks, Stef"

Client report:

"A closer look at this month's replies found the sequencer's own labelling understates positive
replies. It marked 6 replies as positive; reading every reply by hand found 7. Two of the
strongest replies this month had been filed as not interested and would have gone unanswered
without checking manually. Next month, every reply will be read by hand. Also, any reply the
tool marks not interested will get a second look before it's ignored. This should raise the
genuine positive reply count and reduce the risk of a good reply being missed."

Lead magnet (US client voice):

"Here's a fixed weekly price for your route. You know the number before the week starts and it
doesn't move if a delivery runs long or a customer isn't home. / You get one driver on your
route, briefed on your product and your customers, with a backup driver briefed the same way so
a sick day doesn't turn into a missed delivery. / You get one number to call, and the same
person answers it each time."

Automation email:

"3 receipts didn't get logged in the finance inbox this week because the sender changed its
display name and the logger didn't recognise it. It would be fixed by matching on sender domain
as well as display name. / The renewal pack ran unattended for the first time this
week and completed without issue. / Let me know if you want the display name issue to be fixed
this week."

LEARNINGS entry:

"Insight: The enrichment tool excluded 2,391 accounts on the rule 'no MX record means no
mailbox', which is wrong. A 150-account probe on the excluded list recovered 6.3% verified
addresses. / How to apply: Don't use 'no MX record' as an exclusion filter in enrichment."

Landing page:

"We start with a 15-minute call to get the brief right. You tell us which page and what it
needs to do. / Within 5 days we send you a free redesign of that page, built on what you told
us. / Then you decide whether to keep it. There's no contract for the redesign."

## The tells

In order of how often they appeared in Stef's 29 rewrites, most frequent first. The examples
are quoted from the corpus, so each one is a thing that was actually written and actually
rejected.

1. **The editorial tail.** A closing clause or sentence that comments on the fact just stated:
   "The seven above is the honest count", "and it's not coming back", "and it's wrong", "not to
   look busy", "before a single email is sent", "That is a clear signal about where the next
   month's volume should sit", "on the strongest ABM reply of the window". Stef cut every one.
   The fact stands alone. If the reader needs the implication, state it as a plain next step
   ("That means next month's volume should focus on these campaigns"), never as a verdict on
   the sentence before.

2. **Contraction avoidance.** "did not", "do not", "is not the problem", "that is", "they are",
   "here is", "it is". No person types an email that way. Use "didn't", "don't", "isn't",
   "that's", "they're", "here's", "it's". Exception: keep the full form where the sentence
   lands on the verb ("it is, and that's the problem") and in contracts. Density is the tell.
   Stef's own text has "we are" and "that is" in it now and then; a passage where every verb
   is expanded and none is contracted is the signature.

3. **Number words.** "six positives", "ten genuine positive replies", "no calls", "a fifth of
   the list", "five of the seven sources", "about ten separate files", "the two emails". Stef
   rewrote every one as a digit: 6, 10, 0 calls, 1/5, 5/7, 10, the 2 emails. Write the digit.
   A person reading a number wants to see a number. "One" as a pronoun ("one of those") stays
   a word.

4. **Negation-contrast constructions.** "two different campaigns, not one", "capped by time,
   not by demand", "simple, not big and bold", "collisions, not shared owners", "no result, no
   performance fee, and we carry the setup cost", "Rather than tune it, we audited". The
   claim is stated by denying something nobody said. Write the positive claim alone, or put
   the contrast in brackets: "capped by time (not by demand)". A genuine list of negatives
   ("no storage fees, no receiving fees, no peak surcharges") is fine, because each item is a
   fact rather than a rhetorical foil.

5. **Figurative verbs and nouns for plain mechanics.** "per-account enrichment buys the same
   person up to six times", "inflates every yield number", "the seen-state had eaten them",
   "the gate is holding", "under the 3% worry line", "the cause upstream", "that is a signal
   the two campaigns". Stef replaced each with the literal word: "paying for the details of
   the same person up to 6 times", "the gate is performing fine", "danger mark", "that means".
   A metaphor for a mechanism hides the mechanism. Say what happens.

6. **Bold lead-in labels.** "**5. Bounce rate is fine and is not the problem.**", "**How to
   apply:**", "**Collapse to OWNER UNITS...**", "**15-minute call**". Stef stripped every bold
   run. Bold inside body text is a template shape, and bolded phrases mid-sentence read as
   shouting. Write the sentence. Where a label is needed, it's a heading or a plain "Pricing".

7. **Intensifiers and stance adverbs.** "exactly how we source", "Say it plainly and
   confidently", "real, qualified manufacturers", "the honest count", "You said it plainly",
   "It settles into a rhythm", "the flagship campaign", "Start human and natural". Each is a
   word about the writer's attitude rather than the subject. Cut it. "Here's how we source",
   "qualified manufacturers", "Start in a natural way".

8. **Dash-bracketed asides.** "everyone else - Australia, NZ, Europe, Asia, the Middle East -
   lost it", "The first build - thirty campaigns launched on 17 July - did not work", "writes
   window_items - everything published in the window, not only what no previous fetch has
   seen - and it landed". Stef put every aside in brackets or gave it its own sentence:
   "Everyone else (AU, NZ, Europe, Asia, Middle East) lost it". A pair of spaced hyphens
   around a clause is model punctuation.

9. **Colon-led flourish labels.** "THE big one on tariffs, and the strongest thing you can
   say:", "Pricing, and never quote one line of it alone:", "Two reasons: (1) ... (2) ...",
   "The call is not needed at this point:". A wind-up before the content. Use the plain label
   ("Tariffs (most key point)", "PRICING") or join with "so" and "because".

10. **Staccato repetition for emphasis.** "The approved prompt says 15. The cold email he had
    just read says 15." Short. Punchy. Twice. Stef joined them: "The approved prompt says 15
    and the cold email he had just read says that too." One short sentence is emphasis; a
    pattern of them is a tell.

11. **Vivid rephrasing of an ordinary thing.** "a diary commitment to a stranger" for a call
    pitch, "without you lifting a finger" for "without you needing to do anything", "no single
    read tells the next run" for "no single file tells the next run". The plain noun was
    available and the model reached past it. Reach back.

12. **Numbered reasons in prose.** "(1) this repo sends real invoices ...; (2) when I tried
    ...". Stef's version: "because a. this repo sends actual invoices ... and b. when I tried
    ...". Either lowercase letters in a sentence, or a real bulleted list. Parenthesised digits
    inside a paragraph belong to a paper, and a person doesn't write that way.

13. **Negative parallelism.** "It's not about speed, it's about reliability." One is a choice;
    3 on a page is a signature. Same family as tell 4. Rewrite as the positive claim alone.

14. **Rule of three.** "Faster, cheaper, simpler." "carriers, prices and data" when the reader
    needs one of them. Cut to the one that matters, or make it two so it stops scanning as a
    rhythm.

15. **Inanimate subjects with human verbs.** "The data tells a story", "the decision emerged",
    "the numbers speak for themselves". Name the actor.

16. **Tailing negations.** "One click, no spreadsheets." "The options come from the selected
    item, no guessing." A clipped negative fragment bolted on instead of written as a clause.
    Write the claim, drop the tail.

17. **Manufactured drama.** Fragments. For emphasis. The pattern, not the one instance.

18. **Vague attribution.** "Industry experts note", "many operators find", "studies show".
    Source it or cut it.

19. **Aphorism formulas.** "X is the Y of Z", "the currency of trust", "X becomes a trap". An
    ordinary claim reshaped into something quotable. The default failure of a section header.

20. **Signposting.** "In this section we'll look at", "Let's dive in", "It's worth noting
    that". Delete and start with the content.

21. **Generic positive conclusion.** A last line that congratulates the reader and says nothing.
    Cut it or replace it with the open loop.

22. **Copula avoidance.** "serves as", "represents", "stands as" where "is" was correct.

23. **Elegant variation.** Cycling synonyms for one thing ("drop", "delivery", "drop-off",
    "consignment") when the reader needs one consistent word. Pick the client's own term and
    repeat it.

24. **Hedging stacked on hedging.** "It may potentially help to some extent." One honest hedge
    is credibility and 3 is mush.

25. **Overused AI vocabulary.** "delve", "landscape", "tapestry", "pivotal", "robust",
    "seamless", "leverage", "crucial", "comprehensive", "foster", "elevate", "journey",
    "unlock", "streamline", "signal" (as a noun for "evidence"), "honest" (as praise for a
    number), and "runsheet" (banned outright by Stef, 5 Sep 2026). Swap for the plain word.

26. **Sales adjectives.** "vibrant", "stunning", "nestled", "cutting-edge", "world-class".
    Promotional gloss with no factual content. Cut it or replace it with the fact that earned it.

27. **Shallow gerund analysis.** "...highlighting the importance of visibility",
    "...underscoring the need for change". The clause restates the fact as a moral. Delete it.

28. **Chatbot residue.** "I hope this helps", "let me know if you need anything else", "feel
    free to reach out" surviving into a document or email. Cut.

29. **Heading restated in the first sentence.** "Carrier costs" followed by "Carrier costs are a
    major factor". Start with the content the heading promised.

30. **Answering objections nobody raised.** "This isn't about replacing your team" when nobody
    suggested it was. Names the fear and plants it.

31. **Rejecting fake alternatives.** "Some say X, but..." where nobody says X.

32. **Lazy extremes.** "every", "always", "never" doing imprecise work. Use the real quantity.

33. **Monotonous rhythm.** Every sentence the same length and shape. Read it aloud.

34. **Trade jargon used as if it were plain speech.** "The line stops", "the spot desk",
    "individual inboxes". Say the thing plainly to a stranger.

35. **Speculative gap-filling.** "While specific details are limited...", "likely began". When
    the model cannot find a source it writes a sentence about not finding one and invents
    filler. **This one is a factual risk before it's a style one.** Cut the sentence and record the gap honestly
    ([[stef-validate-claims]]).

36. **The tilde approximator.** "~$0.26", "~500 leads". Write "about" or commit to the figure.

37. **Currency codes where a symbol belongs.** "USD 30K", "GBP 5M" in prose. Write "$30K",
    "£5M". Exceptions: contracts, and a deliberate FX conversion naming both currencies.

38. **Hyphenated word-pair in predicate position.** "the report is high-quality". Hyphenate
    attributively ("a high-quality report") and drop it after the noun.

39. **"Hi team" greetings.** "Hi team", "Hi there", "Hey team", "Hello all". Use the person's
    name, otherwise a bare "Hi," and get straight into it.

40. **False ranges.** "From small couriers to national carriers" as filler that names no real
    boundary.

41. **Conversational rhetorical openers.** "Honestly?", "Look,", "Here's the thing". The
    theatrical pause before a routine point.

42. **Persuasive authority tropes.** "The real question is", "at its core", "what really
    matters". Pretending to cut through noise before restating an ordinary point.

_Tells 1 to 12 are the measured ones from the 7 September 2026 corpus. 13 onward are carried
from the earlier list (Wikipedia's Signs of AI writing via the Humanizer skill, `humanizer-cli`'s
catalogue, `blader/humanizer` and `hardikpandya/stop-slop`); the tools themselves stay
uninstalled, they are rewriters and they contradict the dash rule. A tell in the carried set
with zero corpus hits after the next 50 rows moves to an appendix._

## Hard formatting rules

These come from CLAUDE.md and are not negotiable.

- **Normal hyphens only.** No em dashes, no en dashes. Anywhere, ever.
- **No emojis** in deliverables.
- **British English** in internal docs and your own materials: fulfilment, optimise,
  colour, prioritise. **Exception:** anything written on a client's behalf uses their market
  voice. A US client's emails to US readers use US spelling and that owner's register.
- **Day-month dates.** "18 May", never "May 18".
- **No Oxford comma.** "carriers, prices and data", never "carriers, prices, and data". Added
  27 August 2026, after it ran through a whole build unnoticed.
- **Digits for numbers** in body text, per tell 3. "6 positives", "2 emails", "10 files".
- **No bold inside body text**, per tell 6. Bold is for headings and for a single defined term.
- **A list of facts is a bulleted list.** 4 facts in one paragraph become 4 bullets.
- Deliverables are written in a client-presentable first-person agency voice.

## How the judge reads a draft

The judgement half runs in a fresh context that never saw the draft being written: one
isolated `claude -p` process per passage, with no tools and no project instructions, and this
file as the whole system prompt. The brief it gets is adversarial by design. Assume the passage
is machine-written, list every tell with the exact phrase, then name the 3 sentences no person
would type even if no numbered tell fits, then give one verdict. "Does it flow" is the question
the author always answers yes to, so it's never asked.

The mechanical half is a regex module with one home, imported by every gate that uses it rather
than copied into each. It catches only what a machine can catch with certainty.

Measure the two halves separately: the regex on precision, because a false alarm gets a gate
switched off, and the judge on recall, because a miss is a tell that reached a reader.

<!-- judge:stop -->

## Measured results

| Run | Corpus | Regex precision | Regex recall | Judge precision | Judge recall | Span recall |
|---|---|---|---|---|---|---|
| before, 7 Sep 2026 | 43 rows, 10 registers | 71.4% | 51.7% | 93.8% | 51.7% | 57.6% |
| after, 7 Sep 2026 | same 43 rows (in-sample: the rewrite was drawn from them) | 100% | 51.7% | 92.6% | 86.2% | 60.6% |
| after Phase B regex additions, 7 Sep 2026 | 63 rows | 100% | 65.1% | (unchanged) | (unchanged) | (unchanged) |

Blind tests, same day, Stef judging: tells as system prompt 0 of 6 read human; tells plus fix
loop 0 of 6; his passages alone 0 of 6; register description plus his passages plus a hand read
against the tells 5 of 5 approved (1 after his own rewrite). Corpus at 63 rows.

Keep the row-by-row record wherever the corpus lives, and only change the standard when the
after beats the before.


## Annealed from script reviews

The sections below came out of cold email reviews. Scripts are no longer gated by STR, but each
lesson was written here as well as in the script skill, per the 6 September 2026 rule, because
the same fault shows up in reports, proposals and reply agents.

### The one deliberate contradiction

Humanizer treats curly quotes as an AI tell, because they betray paste-from-a-chat-window in plain
prose. Design canon treats straight quotes as cheap-looking in rendered type. Both are right in
their own place, so the rule is:

**Rendered page copy uses proper curly quotes and a real apostrophe. Anything that ships as plain
text or code uses straight quotes.**

Do not flip-flop on this.

### The contraction rule has one mechanical exception, and a blanket regex will break it

A contraction cannot carry sentence stress, so it cannot end a clause: "nobody can tell you where
it's" is not English, and neither is "that is what it's". Bulk-substituting "it is" to "it's"
produces exactly that, twice in one session on 27 August 2026 - the second time because the same
regex was re-run over already-corrected text. Contract by reading the sentence, or exclude a
match followed by a full stop, a question mark or the end of the line. Same class as
[[corrections-into-the-generator-not-its-output]]: a sweeping fix over prose re-breaks what a
careful pass already fixed.

### Write for the reader's English, not your own

**When copy goes to a market that reads English as a second language, plain English is a hard
constraint rather than a preference.** From a review on 27 August 2026, on a campaign where 36%
of the list was in Brazil and Mexico and the copy had been settled as English-only: *"NEEDS TO BE
SIMPLE ENGLISH THAT EVEN A NON NATIVE BRAZILIAN OR MEXICAN ENGLISH SPEAKER CAN UNDERSTAND"*.

The failure was not vocabulary. Every long word in that draft was ordinary. It was CONSTRUCTION:
"the answer usually sits in three or four people's sent items, so it has to be reassembled before
anyone can look at it" is a native-speaker sentence with a metaphor, a passive and a subordinate
clause. It measured grade 11 while the emails around it measured 4.

**Measure it, do not claim it.** Flesch-Kincaid grade per email, computed from the copy itself.
Target grade 8 or below for a second-language market; a UK broadsheet runs 12-14. Report the
median and the worst. Where a style skill's own structure forces a higher score - GrowthFlare
Framework A is a single 30-word conditional sentence and cannot get below about 12 - say so, and
let the trade-off be chosen deliberately rather than hidden.

**The related trap: invented specificity reads as detail and is really noise.** The same draft said
carriers get used out of habit "because they're the ones who answer quickly". Nothing in the client
material, the reviews or the research says that. The client's own words are that the team "calls
directly the historical partner" and does not trust the alternatives. A specific-sounding reason
with no source is worse than a general one, because it invites a reply nobody can back up.

### A statistic must connect to what THIS reader personally gains or loses

From a review on 28 August 2026, after 3 figures in a row were rejected:

> *"The reason we use that quote for AU transport - 71% of buyers won't buy furniture again after
> a bad experience - is because we're reaching out to a founder who has a vested interest in
> selling more furniture... If you reach out to an operations manager who probably just is doing
> the 9-to-5 and doesn't really care about revenue, he's not going to care about this figure."*

**The test is the READER'S stake, not the topic's relevance.** "Manufacturers spend around 10% of
revenue on transport" is true, sourced and on-topic, and it is worthless to a salaried operations
manager, because company revenue is not their problem. A founder owns revenue. An ops manager owns
their own workload, their line not stopping, and not being the person who found out last.

**And the standing rule that came with it: if no figure genuinely fits, do not use one.**

> *"If you think something just has no point and you can't think of any figure that would make
> sense, then obviously stop trying to make one. Stop allowing me to keep coming back to it."*

3 rejected figures in a row is the signal that the SLOT is wrong, not the figure. Write the
email without a statistic and say why.

**The other half of the same failure: I had condensed the email past comprehension.** The opening
line was a bare statistic and the next line began "Full visibility of every load" - no product
named, no bridge, no context. Concision is not the goal; a reader understanding it is. **Read the
finished email top to bottom as the recipient before publishing it.** A gate cannot catch
incoherence.
