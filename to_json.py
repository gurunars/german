#!/usr/bin/env python3
"""Generate words/*.json flashcard decks from words/*.csv.

The CSVs stay the source of truth: one pair per line, English and German split on
the first comma. A trailing "* N" on either side is the card's priority (a bare "*"
means 2); it is taken out of the text. Each deck becomes

    {"name": "...", "description": "English → German",
     "frontLanguage": "en", "backLanguage": "de",
     "cards": [{"front": ..., "back": ..., "priority": 2}]}

Card text is Markdown, so characters Markdown would read as formatting are escaped.
words/index.json lists every deck with a link relative to itself, so the app can import
the whole folder from GitHub, GitHub Pages or anywhere else, and the "Decks" section of
README.md is rewritten to match.

Stdlib only; `make json` runs it in a container.
"""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORDS = os.path.join(ROOT, "words")
README = os.path.join(ROOT, "README.md")
# German word forms by frequency in subtitles: FrequencyWords (Hermit Dave), OpenSubtitles
# 2018, CC BY-SA 4.0 — https://github.com/hermitdave/FrequencyWords
FREQUENCY = os.path.join(WORDS, "frequency_de.txt")

# "bag * 2", "reparieren* 3", "once a day *"
PRIORITY_MARK = re.compile(r"\s*\*\s*(\d+(?:\.\d+)?)?\s*$")
MARKDOWN_SPECIAL = re.compile(r"([\\`*_\[\]])")

# Ranking reads the German side: hints in brackets go, alternatives split on these.
HINT = re.compile(r"\([^)]*\)")
ALTERNATIVES = re.compile(r"\s+/\s+|\s*~\s*|\s*<\s*|,")
WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+")
# Words that only frame a vocabulary item; the item is as common as the rest of it.
FRAME = {"der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "sich", "pl"}

# The deck to finish before a B1 course: the most frequent cards across all decks.
B1_FILE = "before_b1.json"
B1_NAME = "Before B1"
B1_SIZE = 1500


def load_ranks():
    """Word form → its rank in the frequency list (1 is the most frequent)."""
    ranks = {}
    with open(FREQUENCY, encoding="utf-8") as fil:
        for rank, line in enumerate(fil, start=1):
            form = line.split(" ", 1)[0]
            ranks.setdefault(form, rank)
    return ranks


def rank_of(german, ranks):
    """
    The card's frequency rank, or None when its words are not in the list. A word group
    is as rare as its rarest word (you need all of them); a card with alternatives is as
    common as its most common one.
    """
    best = None
    for alternative in ALTERNATIVES.split(HINT.sub(" ", german)):
        every = [w.lower() for w in WORD.findall(alternative)]
        # "der / die / das" is itself the word to learn, not a frame around one.
        words = [w for w in every if w not in FRAME] or every
        word_ranks = [ranks.get(w) for w in words]
        if not words or None in word_ranks:
            continue
        rarest = max(word_ranks)
        best = rarest if best is None else min(best, rarest)
    return best


def priority_of(rank, mark):
    """
    4 for the ten most frequent words, 3 for the top 100, 2 for the top 1,000, 1 at rank
    10,000 and 0.5 for words not in the list; the user's own "* N" mark multiplies it.
    """
    base = 0.5 if rank is None else min(4.0, max(0.5, 5 - math.log10(rank)))
    return round(base * (mark or 1.0), 2)


def split_priority(side):
    """The side without its priority mark, and the priority it gave (None when unmarked)."""
    match = PRIORITY_MARK.search(side)
    if not match:
        return side, None
    return side[: match.start()].strip(), float(match.group(1)) if match.group(1) else 2.0


def markdown(text):
    """Plain text as Markdown that shows exactly that text."""
    return MARKDOWN_SPECIAL.sub(r"\\\1", text)


def parse(path, ranks):
    cards, seen, problems = [], set(), []
    with open(path, encoding="utf-8") as fil:
        for number, line in enumerate(fil, start=1):
            line = line.strip()
            if not line:
                continue
            if "," not in line:
                problems.append("%d: no comma" % number)
                continue
            front, back = (side.strip() for side in line.split(",", 1))
            front, front_priority = split_priority(front)
            back, back_priority = split_priority(back)
            if not front or not back:
                problems.append("%d: blank side" % number)
                continue
            if (front, back) in seen:
                problems.append("%d: duplicate of an earlier line" % number)
                continue
            seen.add((front, back))
            mark = max((p for p in (front_priority, back_priority) if p is not None), default=None)
            rank = rank_of(back, ranks)
            card = {"front": markdown(front), "back": markdown(back), "priority": priority_of(rank, mark)}
            if rank is not None:
                card["rank"] = rank
            cards.append(card)
    return cards, problems


def deck_name(filename):
    return filename[: -len(".csv")].replace("_", " ").capitalize()


def write_readme(index):
    """Replace README.md's "## Decks" section, which runs to the end of the file."""
    with open(README, encoding="utf-8") as fil:
        text = fil.read()
    head = text.split("\n## Decks\n", 1)[0].rstrip("\n")
    lines = ["- [%s](words/%s) — %d cards" % (deck["name"], deck["url"], deck["cards"]) for deck in index]
    with open(README, "w", encoding="utf-8") as fil:
        fil.write(head + "\n\n## Decks\n\n" + "\n".join(lines) + "\n")


def deck(name, cards):
    return {
        "name": name,
        "description": "English → German",
        "frontLanguage": "en",
        "backLanguage": "de",
        "cards": cards,
    }


def write_json(filename, data):
    with open(os.path.join(WORDS, filename), "w", encoding="utf-8") as fil:
        json.dump(data, fil, ensure_ascii=False, indent=2)
        fil.write("\n")


def before_b1(all_cards):
    """
    The B1_SIZE most frequent cards across every deck, most frequent first. A card found in
    several decks is taken once, with its highest priority. Only identical pairs count as
    the same card: "die Bank" for "bank" and for "bench" are two things to learn.
    """
    unique = {}
    for card in all_cards:
        if "rank" not in card:
            continue
        key = (card["front"].lower(), card["back"].lower())
        if key not in unique or card["priority"] > unique[key]["priority"]:
            unique[key] = card
    return sorted(unique.values(), key=lambda c: (c["rank"], c["back"].lower()))[:B1_SIZE]


def main():
    ranks = load_ranks()
    index, failed, all_cards = [], False, []
    for filename in sorted(os.listdir(WORDS)):
        if not filename.endswith(".csv"):
            continue
        cards, problems = parse(os.path.join(WORDS, filename), ranks)
        for problem in problems:
            print("%s:%s (skipped)" % (filename, problem), file=sys.stderr)
        if not cards:
            print("%s: no cards" % filename, file=sys.stderr)
            failed = True
            continue
        name = deck_name(filename)
        target = filename[: -len(".csv")] + ".json"
        write_json(target, deck(name, cards))
        index.append({"name": name, "url": target, "cards": len(cards)})
        all_cards += cards
    b1 = before_b1(all_cards)
    write_json(B1_FILE, deck(B1_NAME, b1))
    index.insert(0, {"name": B1_NAME, "url": B1_FILE, "cards": len(b1)})
    write_json("index.json", {"name": "German words", "decks": index})
    write_readme(index)
    print("Wrote %d decks" % len(index))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
