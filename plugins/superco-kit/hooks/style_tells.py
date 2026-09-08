#!/usr/bin/env python3
"""The one home for the MECHANICAL half of the writing standard.

Every gate that uses it imports this module and there must never be a second copy of the list:
the lead-magnet gate (check_magnet_style.py), the reply-agent generator's own self-check, the
sales-letter QA and the STR eval. A tell added here starts being enforced everywhere on the next
run.

WHAT THIS IS NOT. It checks only what a machine can check with certainty. Negative parallelism,
the editorial tail, figurative verbs and the rest of the judgement tells are a READ against STR,
never a grep.

Precision is the number that matters here: a hit on text a person wrote is a false alarm, and a
gate that cries wolf gets switched off. Measured 7 Sep 2026 on the STR corpus, the first version
of this file sat at 71% precision, every false alarm from two rules: the expanded-verb rule
firing on a single "we are" in Stef's own text, and the tailing-negation rule firing on a list
of genuine negatives ("no storage fees, no receiving fees, no peak surcharges"). Both are now
conditional, which is why scan() looks at the passage as a whole and not only at the match.

    from style_tells import scan
    for line, msg in scan(text, skip=("unresolved placeholder",)):
        ...

Quoted spans ("...") and blockquote lines (> ...) are stripped before scanning. They are someone
else's words or an example of the fault, and STR itself is full of the second kind.
"""
import re

# tell 2 (contraction avoidance). A person contracts most of the time, not all of the time, so a
# passage is flagged on DENSITY: three or more expanded forms and at most one contraction.
EXPANDED = (r"\b(?:[Ii]t is|[Tt]here is|[Tt]hat is|[Hh]ere is|[Ii] am|[Ii] will|[Ww]e are|[Ww]e will|"
            r"[Ww]e would|[Yy]ou are|[Yy]ou will|[Yy]ou would|"
            r"[Tt]hey are|does not|do not|did not|cannot|will not|is not|are not|was not|"
            r"were not|have not|has not|had not|would not|could not|should not)\b"
            # "we have"/"you have" contract only before a past participle. "Do you have a
            # moment" does not, and the first version of this tell flagged it.
            r"|\b(?:[Ww]e have|[Yy]ou have|[Ii] have)(?=\s+(?:been|got|had|"
            r"seen|done|made|worked|tried|run|spent|\w+ed\b))")
# a contraction cannot carry sentence stress, so a match at the end of a clause is exempt
EXPANDED_EXEMPT_AFTER = re.compile(r"^\s*(?:[.,;:!?)]|$|-\s)")
CONTRACTED = re.compile(r"\b\w+n't\b|\b(?:it|that|there|here|what|who)'s\b|\b\w+'(?:re|ve|ll|d)\b",
                        re.I)

NUMBER_WORDS = (r"\b(?:three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
                r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|"
                r"seventy|eighty|ninety|hundred|thousand)\b")

TELLS = {
    "tilde approximator (tell 36)": r"~\d",
    "ISO currency code in prose (tell 37)": r"\b(?:EUR|USD|GBP|BRL|MXN) ?\d",
    # the fragment has to END the sentence to count: "One click, no spreadsheets." A negative
    # clause that carries on ("not a problem for the first month because...") is a clause.
    "tailing negation (tell 16)": r"[a-z]{3,}, (?:no [a-z]+|not (?:a|an|per) [a-z]+)(?: [a-z]+){0,2}[.!]",
    "en or em dash": r"[–—]",
    "AI vocabulary (tell 25)": r"\b(?:seamless|leverag\w*|unlock\w*|robust|delv\w*|"
                               r"streamlin\w*|elevat\w*|crucial|pivotal|comprehensive|foster\w*|"
                               r"landscape|journey|tapestry|runsheets?|run-sheets?)\b",
    "number word where a digit belongs (tell 3)": "(?i:" + NUMBER_WORDS + r")(?=\s+(?:of the\s+)?[a-z])",
    # "two" only before a countable plural ("two weeks", "the two calls"); "two of" and "two
    # months" in Stef's own text stayed as words, and precision on the corpus decides this rule
    "two before a plural where 2 belongs (tell 3)": r"(?i)\btwo (?:weeks|days|months|years|calls|emails|"
                                                    r"replies|tasks|campaigns|lists|files|steps|things|"
                                                    r"asks|versions|options|sets|rounds|hours|minutes)\b",
    # "It's not about X, it's about Y" and "not X, but Y" in one clause - the front half of
    # tell 13 that the tailing-negation rule cannot see
    "negative parallelism (tell 13)": r"(?i)\b(?:is not|isn't|not) (?:about |just |only )?[^,.;\n]{2,40}, "
                                      r"(?:it is|it's|but|rather) (?:about |just )?\w",
    # a colon-led flourish label before the content: "Two things from you:", "Three quick notes:"
    "colon-led flourish label (tell 9)": r"(?im)^(?:two|three|four|five|a few|some|quick|three quick) "
                                         r"(?:things|points|notes|updates|items|asks)[^\n:]{0,40}:\s*$",
    # performed casualness, the register a model reaches for when told to sound human. Every
    # phrase here came out of a blind test on 7 Sep 2026, where both arms read as AI.
    "performed casual (tell 41)": r"(?i)\b(?:happy either way|just wanted you across it|worth a look|"
                                  r"nothing urgent|no strings attached|no pressure|no catch|"
                                  r"just flagging|on a brighter note|straight to work|let's talk)\b",
    "Oxford comma": r"\b\w+, \w+(?: \w+){0,2}, (?:and|or) \b",
    "month-day date": r"\b(?:January|February|March|April|June|July|August|September|October|"
                      r"November|December) \d{1,2}\b(?!\d)",
    "Hi team greeting (tell 39)": r"^\s*(?:Hi|Hey|Hello) (?:team|there|all|everyone)\b",
    "dash-bracketed aside (tell 8)": r"\w - [^-\n]{3,80}? - \w",
    # a bold run that OPENS a line or a list item is a label in a taxonomy and is allowed; one
    # that follows other words on the line is the tell
    "bold inside body text (tell 6)": r"(?<=[A-Za-z0-9,;:)] )\*\*[^*\n]{2,80}\*\*",
    # the builder's own block markers are not placeholders - excluded by name, because the first
    # version of this gate flagged all 17 of them and no real defect
    "unresolved placeholder": r"\[(?!SPLIT\]|/SPLIT\]|STATS\]|/STATS\]|LOGOS\]|/LOGOS\]|"
                              r"TEAM\]|/TEAM\]|PAGEBREAK\])[A-Z][A-Z \-]{4,}\]",
}

_QUOTED = re.compile(r'"[^"]{2,600}"')
_BLOCKQUOTE = re.compile(r"^\s*>.*$", re.M)
_HEADING = re.compile(r"^\s*#{1,6} .*$", re.M)
_CODE = re.compile(r"`[^`\n]*`")
# a markdown table row is data, and STR says one tilde in a dense technical table is survivable;
# the replay of 20 real writes on 7 Sep 2026 found its only false block in a calibration table
_TABLE_ROW = re.compile(r"^\s*\|.*$", re.M)


def _mask(text):
    """Replace quoted spans, blockquotes, headings, table rows and inline code with spaces of
    the same length so line numbers and offsets survive."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    for rx in (_CODE, _QUOTED, _BLOCKQUOTE, _HEADING, _TABLE_ROW):
        text = rx.sub(blank, text)
    return text


def _is_list_of_negatives(text, pos):
    """'no storage fees, no receiving fees, no peak surcharges' is a list, not a tail."""
    window = text[max(0, pos - 160):pos + 80]
    return len(re.findall(r"\bno \w+", window, re.I)) >= 3


# the hard formatting rules apply everywhere, cold email and cold call scripts included; the
# style tells do not (Stef, 6 Sep 2026: the script skills carry their own voice)
FORMATTING_ONLY = ("en or em dash", "Oxford comma", "month-day date", "unresolved placeholder",
                   "ISO currency code in prose (tell 37)", "tilde approximator (tell 36)")


def scan(text, skip=(), formatting_only=False):
    """[(line_number, message)] for every mechanical tell in `text`. Empty means it passed.
    formatting_only=True runs the hard formatting rules alone, for scripts STR does not gate."""
    found = []
    if formatting_only:
        skip = tuple(skip) + ("expanded verb",) + tuple(k for k in TELLS if k not in FORMATTING_ONLY)
    masked = _mask(text)

    def line_of(pos):
        return masked[:pos].count("\n") + 1

    if "expanded verb" not in skip:
        expanded = [m for m in re.finditer(EXPANDED, masked)
                    if not EXPANDED_EXEMPT_AFTER.match(masked[m.end():m.end() + 3])]
        contracted = len(CONTRACTED.findall(masked))
        if len(expanded) >= 3 and contracted <= 1:
            for m in expanded:
                found.append((line_of(m.start()),
                              "expanded verb, %d in a passage with %d contractions (tell 2): %r"
                              % (len(expanded), contracted, m.group(0))))
    for label, rx in TELLS.items():
        if label in skip:
            continue
        flags = re.M if label.startswith("Hi team") else 0
        for m in re.finditer(rx, masked, flags):
            if label.startswith("tailing negation") and _is_list_of_negatives(masked, m.start()):
                continue
            found.append((line_of(m.start()), "%s: %r" % (label, m.group(0))))
    return sorted(found)
