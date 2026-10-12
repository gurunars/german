#!/usr/bin/env python3
"""Build lessons/*.json, one deck per lesson, and lessons/index.json from lessons/*/*.tsv.

The lessons are a sequence: each assumes the ones before it and nothing after it, and the
build enforces that rather than trusting it.

    lessons/lessons.tsv        number, folder, title — the order of the course
    lessons/grammar.tsv        tag, lesson, label — every grammar point and where it is taught
    lessons/NN-x/words.tsv     lemma, pos, English[, forms] — the words the lesson introduces
    lessons/NN-x/cards.tsv     tag, lemma, slot, English, German, note — its cards

A card fails the build when
- its grammar tag is unknown or belongs to a later lesson;
- a word of its German sentence is not a form of a word introduced in this lesson or an
  earlier one (nouns, verbs and adjectives take their forms from Wiktionary, via
  sentences/forms.json and `make forms`; other words list theirs by hand, and a later
  lesson may list more forms of the same word — `den` only once the accusative is taught);
- nothing is bold on either side, or, when it names a lemma and a slot, its bold German is
  not the form Wiktionary gives for that slot.
A lesson fails when one of its new words is in none of its cards.

Stdlib only; `make json` runs it in a container.
"""
import json
import os
import re
import sys

from grammar_forms import SLOTS
from to_json import BOLD, check_sentence

ROOT = os.path.dirname(os.path.abspath(__file__))
LESSONS = os.path.join(ROOT, "lessons")
FORMS = os.path.join(ROOT, "sentences", "forms.json")
README = os.path.join(ROOT, "README.md")
WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+")


def rows(path, width, problems, optional=0):
    """The tab-separated lines of [path], comments and blank lines skipped, with their numbers."""
    with open(path, encoding="utf-8") as fil:
        for number, line in enumerate(fil, start=1):
            if not line.strip() or line.startswith("#"):
                continue
            fields = [f.strip() for f in line.rstrip("\n").split("\t")]
            if not width - optional <= len(fields) <= width:
                problems.append("%s:%d: expected %d tab-separated fields, got %d"
                                % (os.path.relpath(path, ROOT), number, width, len(fields)))
                continue
            yield number, fields + [""] * (width - len(fields))


def words_of(german):
    return {w.lower() for w in WORD.findall(german.replace("**", ""))}


def build_lesson(number, folder, title, grammar, known, forms, problems):
    """The lesson's deck, growing [known] by its words; problems appended to [problems]."""
    base = os.path.join(LESSONS, folder)
    new = {}
    for line, (lemma, pos, english, listed) in rows(os.path.join(base, "words.tsv"), 4, problems, optional=1):
        where = "lessons/%s/words.tsv:%d" % (folder, line)
        if pos in SLOTS:
            entry = forms.get(lemma)
            if entry is None:
                problems.append("%s: no forms for %s — run `make forms`" % (where, lemma))
                continue
            surface = {w.lower() for w in entry["all"]}
        elif listed:
            surface = {w.strip().lower() for w in listed.split(",") if w.strip()}
        else:
            problems.append("%s: a %s lists its forms in the fourth column" % (where, pos))
            continue
        new[lemma] = surface
        for word in surface:
            known.setdefault(word, lemma)

    cards, used = [], set()
    for line, (tag, lemma, slot, english, german, note) in rows(os.path.join(base, "cards.tsv"), 6, problems):
        where = "lessons/%s/cards.tsv:%d" % (folder, line)
        taught = grammar.get(tag)
        if taught is None:
            problems.append("%s: unknown grammar tag %s" % (where, tag))
            continue
        if taught[0] > number:
            problems.append("%s: %s is taught in lesson %d" % (where, tag, taught[0]))
            continue
        if not BOLD.search(english) or not BOLD.search(german):
            problems.append("%s: nothing bold on one side" % where)
            continue
        unknown = sorted(w for w in words_of(german) if w not in known)
        if unknown:
            problems.append("%s: not taught yet: %s" % (where, ", ".join(unknown)))
            continue
        if lemma not in ("", "-"):
            entry = forms.get(lemma)
            problem = "no forms for %s" % lemma if entry is None else check_sentence(entry, slot, english, german)
            if problem:
                problems.append("%s: %s" % (where, problem))
                continue
        used |= {lemma_ for lemma_, surface in new.items() if words_of(german) & surface}
        cards.append({"front": english, "back": german, "note": "%s. %s" % (taught[1], note), "priority": 1})

    for lemma in sorted(set(new) - used):
        problems.append("lessons/%s/words.tsv: %s is introduced but no card uses it" % (folder, lemma))
    return {
        "name": "Lesson %d · %s" % (number, title),
        "description": "English → German",
        "frontLanguage": "en",
        "backLanguage": "de",
        "cards": cards,
    }


def write_readme(index):
    """Replace README.md's "## Lessons" section, which sits just before "## Decks"."""
    with open(README, encoding="utf-8") as fil:
        text = fil.read()
    head, decks = text.split("\n## Decks\n", 1)
    head = head.split("\n## Lessons\n", 1)[0].rstrip("\n")
    lines = ["- [%s](lessons/%s) — %d cards" % (deck["name"], deck["url"], deck["cards"]) for deck in index]
    with open(README, "w", encoding="utf-8") as fil:
        fil.write(head + "\n\n## Lessons\n\n" + "\n".join(lines) + "\n\n## Decks\n" + decks)


def main():
    problems = []
    with open(FORMS, encoding="utf-8") as fil:
        forms = json.load(fil)
    grammar = {}
    for _, (tag, lesson, label) in rows(os.path.join(LESSONS, "grammar.tsv"), 3, problems):
        grammar[tag] = (int(lesson), label)
    known, index = {}, []
    for _, (number, folder, title) in rows(os.path.join(LESSONS, "lessons.tsv"), 3, problems):
        deck = build_lesson(int(number), folder, title, grammar, known, forms, problems)
        target = folder + ".json"
        with open(os.path.join(LESSONS, target), "w", encoding="utf-8") as fil:
            json.dump(deck, fil, ensure_ascii=False, indent=2)
            fil.write("\n")
        index.append({"name": deck["name"], "url": target, "cards": len(deck["cards"])})
    with open(os.path.join(LESSONS, "index.json"), "w", encoding="utf-8") as fil:
        json.dump({"name": "German lessons", "decks": index}, fil, ensure_ascii=False, indent=2)
        fil.write("\n")
    write_readme(index)
    for problem in problems:
        print(problem, file=sys.stderr)
    print("Wrote %d lessons" % len(index))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
