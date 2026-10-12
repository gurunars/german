#!/usr/bin/env python3
"""Fetch the inflection tables of sentences/lemmas.tsv and lessons/*/words.tsv into sentences/forms.json.

Tables come from kaikki.org's machine-readable Wiktionary (CC BY-SA), one small file per
word, cached in .kaikki/ so a rerun only fetches new words. forms.json is committed, so
`make json` builds offline. Stdlib only; `make forms` runs it in a container.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

from grammar_forms import SLOTS, matches

ROOT = os.path.dirname(os.path.abspath(__file__))
LEMMAS = os.path.join(ROOT, "sentences", "lemmas.tsv")
LESSONS = os.path.join(ROOT, "lessons")
FORMS = os.path.join(ROOT, "sentences", "forms.json")
CACHE = os.path.join(ROOT, ".kaikki")
# Tags that mark a table's scaffolding rather than a form of the word.
NOT_A_FORM = {"table-tags", "inflection-template", "class", "romanization"}
# Words a multi-word form borrows from other lemmas — "der alte", "habe gesagt", "werde sagen",
# "zu sagen" — which a lesson has to teach on their own before a sentence may use them.
BORROWED = set("""
der die das den dem des ein eine einen einem einer eines zu sich
bin bist ist sind seid sein war warst waren wart gewesen sei seiest seien seiet wäre wärest wärst wären wäret wärt
habe hast hat haben habt hatte hattest hatten hattet gehabt hätte hättest hätten hättet
werde wirst wird werden werdet wurde wurdest wurden wurdet geworden worden würde würdest würden würdet
""".split())


def lemmas():
    """(lemma, pos, english) of every word with a table: the Before B1 list, then each lesson's
    new words. Lesson words of other parts of speech list their forms by hand."""
    sources = [LEMMAS]
    if os.path.isdir(LESSONS):
        sources += sorted(
            os.path.join(LESSONS, name, "words.tsv")
            for name in os.listdir(LESSONS)
            if os.path.isfile(os.path.join(LESSONS, name, "words.tsv"))
        )
    seen = set()
    for source in sources:
        with open(source, encoding="utf-8") as fil:
            for line in fil:
                if not line.strip() or line.startswith("#"):
                    continue
                lemma, pos, english = line.rstrip("\n").split("\t")[:3]
                if pos in SLOTS and lemma not in seen:
                    seen.add(lemma)
                    yield lemma, pos, english


def entries(lemma):
    path = os.path.join(CACHE, lemma + ".jsonl")
    if not os.path.exists(path):
        quoted = urllib.parse.quote(lemma)
        url = "https://kaikki.org/dictionary/German/meaning/%s/%s/%s.jsonl" % (
            urllib.parse.quote(lemma[0]), urllib.parse.quote(lemma[:2]), quoted)
        os.makedirs(CACHE, exist_ok=True)
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        with open(path, "wb") as fil:
            fil.write(data)
    with open(path, encoding="utf-8") as fil:
        return [json.loads(line) for line in fil if line.strip()]


def gender_of(entry):
    """m, f or n from the head line, e.g. "Hund m (strong, …)"."""
    for head in entry.get("head_templates", []):
        match = re.match(r"\S+ ([mfn])\b", head.get("expansion", ""))
        if match:
            return match.group(1)
    return None


def table(lemma, pos):
    """slot → accepted forms, from the first entry of [pos] that has an inflection table."""
    for entry in entries(lemma):
        if entry.get("lang_code") != "de" or entry.get("pos") != pos or not entry.get("forms"):
            continue
        slots = {}
        for slot, (wanted, _label) in SLOTS[pos].items():
            found = []
            for form in entry["forms"]:
                text = form.get("form", "")
                if matches(form.get("tags", []), wanted) and text not in found and text != "-":
                    found.append(text)
            if found:
                slots[slot] = found
        if slots:
            # Every word of every form, so a lesson can tell which lemma a sentence's word is.
            words = {lemma}
            for form in entry["forms"]:
                if set(form.get("tags", [])) & NOT_A_FORM:
                    continue
                parts = [w for w in form.get("form", "").split() if w.isalpha()]
                words.update(parts if len(parts) == 1 else (w for w in parts if w.lower() not in BORROWED))
            result = {"pos": pos, "slots": slots, "all": sorted(words)}
            if pos == "noun":
                result["gender"] = gender_of(entry)
            return result
    return None


def main():
    out, failed = {}, False
    for lemma, pos, english in lemmas():
        found = table(lemma, pos)
        if found is None or (pos == "noun" and not found.get("gender")):
            print("%s: no %s table" % (lemma, pos), file=sys.stderr)
            failed = True
            continue
        found["english"] = english
        missing = sorted(set(SLOTS[pos]) - set(found["slots"]))
        if missing:
            print("%s: no %s (those cards are skipped)" % (lemma, ", ".join(missing)), file=sys.stderr)
        out[lemma] = found
    with open(FORMS, "w", encoding="utf-8") as fil:
        json.dump(out, fil, ensure_ascii=False, indent=1, sort_keys=True)
        fil.write("\n")
    print("Wrote forms of %d words" % len(out))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
