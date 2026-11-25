"""One Line, No Deadline Met -- make.fun entry program.

Writes a single-line joke giving an excuse for a missed deadline to
/output/entry.txt (or $ENTRY_OUTPUT when set).

Pure Python stdlib, fully deterministic: no randomness, no clock, no
network. Three genuinely different candidate one-liners are scored
against the judge's brief, in the brief's own priority order, and the
strongest one is written out.

Judge criteria, most important first:
  1. really an excuse for a missed deadline
  2. funny -- a real joke with a turn or a surprise
  3. works as one line, punch landing at the end
  4. sounds like something a person would actually say when cornered
  5. fresh angle, not a stock retread
"""

import os

# --- Three candidate one-liners, three different angles -------------------
# A: reframe the miss as generosity (the deadline got a head start).
# B: comparison joke (the deadline as an abandoned gym membership).
# C: breakup metaphor (the deadline moved on to someone punctual).
CANDIDATES = {
    "A_head_start": (
        "I didn't miss the deadline, I just gave it a head start "
        "so it could finish without me."
    ),
    "B_gym_membership": (
        "I treated the deadline like my gym membership: full of "
        "plans in January, ghosted by February."
    ),
    "C_breakup": (
        "The deadline and I broke up \u2014 it moved on, I stayed, "
        "and now it's seeing someone who actually submits on time."
    ),
}

# Scores 0-5 per criterion, in the judge's priority order:
# (excuse, funny, one_line, sounds_human, fresh)
SCORES = {
    # A is a joke excuse, but the "I didn't miss it" denial softens
    # criterion 1; the head-start turn is clean and the punch lands
    # at the end, though the angle is a familiar reframe.
    "A_head_start": (4, 4, 5, 4, 3),
    # B is a solid comparison and sounds very human; the January /
    # February punch is the funniest beat of the three, but the
    # excuse itself is indirect and the January-gym setup is a
    # familiar trope, so it stays behind on criteria 1 and 5.
    "B_gym_membership": (4, 5, 4, 4, 4),
    # C names the missed deadline outright, the breakup turn is a
    # real surprise, it reads aloud as one sentence with the punch
    # ("seeing someone who actually submits on time") at the end,
    # it sounds exactly like something a cornered person would say,
    # and the breakup angle is fresh for deadline excuses.
    "C_breakup": (5, 4, 4, 5, 4),
}

CRITERIA = ("excuse", "funny", "one_line", "sounds_human", "fresh")


def pick_winner():
    """Pick the strongest candidate.

    Highest total wins; ties break on the judge's priority order,
    comparing criterion by criterion from most to least important.
    """
    ranked = sorted(
        CANDIDATES,
        key=lambda name: (sum(SCORES[name]), SCORES[name]),
        reverse=True,
    )
    return ranked[0]


def gate_ok(text):
    """Mirror the sealed gate: 1-200 chars, UTF-8, not only whitespace,
    exactly one line."""
    if not (1 <= len(text) <= 200):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    text.encode("utf-8")
    return True


def main():
    winner = pick_winner()
    entry = CANDIDATES[winner]
    assert gate_ok(entry), "winning entry failed the gate"
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(entry)
    print("winner: %s (%d chars)" % (winner, len(entry)))
    print(entry)


if __name__ == "__main__":
    main()
