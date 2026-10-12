"""
The grammatical forms sentence cards drill, and how to find them in Wiktionary.

Shared by forms.py, which extracts them from kaikki.org's Wiktionary data, and
to_json.py, which checks every sentence against them. A slot names one form of a word:
its tags must all be on the Wiktionary form, and the form must carry no tag from
EXCLUDED that the slot does not ask for.
"""

# Variants nobody should learn first, and moods/degrees a slot must ask for explicitly.
EXCLUDED = {
    "subjunctive", "comparative", "superlative", "negative", "rare", "nonstandard",
    "archaic", "obsolete", "dated", "error-unknown-tag", "formal", "colloquial",
    # würde + infinitive is tagged future and subjunctive-ii: kept out of the one-word Konjunktiv II.
    "future",
}

_PERSONS = {
    "ich": {"first-person", "singular"}, "du": {"second-person", "singular"}, "er": {"third-person", "singular"},
    "wir": {"first-person", "plural"}, "ihr": {"second-person", "plural"},
}


def _persons(prefix, tags, label):
    """One slot per person: prefix.ich … prefix.ihr (wir also serves sie and Sie)."""
    return {"%s.%s" % (prefix, person): (tags | number, "%s, %s" % (label, person))
            for person, number in _PERSONS.items()}

# slot → (tags, label shown on the card)
SLOTS = {
    "verb": {
        "pres.ich": ({"present", "indicative", "first-person", "singular"}, "present, ich"),
        "pres.du": ({"present", "indicative", "second-person", "singular"}, "present, du"),
        "pres.er": ({"present", "indicative", "third-person", "singular"}, "present, er/sie/es"),
        "pres.wir": ({"present", "indicative", "first-person", "plural"}, "present, wir"),
        "pres.ihr": ({"present", "indicative", "second-person", "plural"}, "present, ihr"),
        "pret.er": ({"preterite", "indicative", "third-person", "singular"}, "simple past (Präteritum), er/sie/es"),
        "perf.er": ({"perfect", "indicative", "third-person", "singular"}, "perfect, er/sie/es"),
        "imp.du": ({"imperative", "second-person", "singular"}, "imperative, du"),
        "imp.ihr": ({"imperative", "second-person", "plural"}, "imperative, ihr"),
        # Konjunktiv II in one word: möchte, hätte, wäre, könnte.
        **_persons("konj2", {"subjunctive", "subjunctive-ii"}, "Konjunktiv II"),
    },
    "noun": {
        "nom.sg": ({"nominative", "singular"}, "nominative singular"),
        "acc.sg": ({"accusative", "singular"}, "accusative singular"),
        "dat.sg": ({"dative", "singular"}, "dative singular"),
        "gen.sg": ({"genitive", "singular"}, "genitive singular"),
        "nom.pl": ({"nominative", "plural"}, "nominative plural"),
        "acc.pl": ({"accusative", "plural"}, "accusative plural"),
        "dat.pl": ({"dative", "plural"}, "dative plural"),
    },
    "adj": {
        "weak.nom.m": ({"weak", "definite", "includes-article", "nominative", "masculine", "singular"},
                       "after der, masculine nominative"),
        "mixed.acc.m": ({"mixed", "indefinite", "includes-article", "accusative", "masculine", "singular"},
                        "after ein, masculine accusative"),
        "mixed.nom.n": ({"mixed", "indefinite", "includes-article", "nominative", "neuter", "singular"},
                        "after ein, neuter nominative"),
        "strong.dat.f": ({"strong", "without-article", "dative", "feminine", "singular"},
                         "no article, feminine dative"),
        "comparative": ({"comparative"}, "comparative"),
        "superlative": ({"superlative"}, "superlative"),
    },
}

# Articles a noun form may carry in its sentence: definite, or an ein-word (ein, kein, …).
_DEF = {"m": "der den dem des", "f": "die die der der", "n": "das das dem des"}
_CASES = ["nom", "acc", "dat", "gen"]
_PLURAL_DEF = {"nom": "die", "acc": "die", "dat": "den", "gen": "der"}
# The ein-words — ein, kein and the possessives — all take ein's endings: ein Hund, kein Hund,
# mein Hund; einen Hund, keinen Hund, meinen Hund. The plural ones take the endings ein would have
# if it had a plural. Ihr (formal your) is ihr with a capital, and sentences are compared lower-case.
EIN_WORDS = ["ein", "kein", "mein", "dein", "sein", "ihr", "unser", "euer"]
EIN_ENDINGS = {"m": ["", "en", "em", "es"], "f": ["e", "e", "er", "er"], "n": ["", "", "em", "es"],
               "pl": ["e", "e", "en", "er"]}


def ein_word(word, ending):
    """The ein-word [word] with [ending]: kein + en → keinen; euer drops its e before an ending: eure."""
    if word == "euer" and ending:
        return "eur" + ending
    return word + ending


def articles(gender, slot):
    """The articles that may stand before a noun in [slot]; '' means none."""
    case, number = slot.split(".")
    index = _CASES.index(case)
    if number == "pl":
        return {"", _PLURAL_DEF[case]} | {ein_word(w, EIN_ENDINGS["pl"][index]) for w in EIN_WORDS if w != "ein"}
    return {_DEF[gender].split()[index]} | {ein_word(w, EIN_ENDINGS[gender][index]) for w in EIN_WORDS}


def matches(tags, wanted):
    tags = set(tags)
    return wanted <= tags and not (tags & EXCLUDED) - wanted


GENDER_WORD = {"m": "der", "f": "die", "n": "das", "pl": "die"}
