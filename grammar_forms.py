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
}

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
    },
    "noun": {
        "nom.sg": ({"nominative", "singular"}, "nominative singular"),
        "acc.sg": ({"accusative", "singular"}, "accusative singular"),
        "dat.sg": ({"dative", "singular"}, "dative singular"),
        "gen.sg": ({"genitive", "singular"}, "genitive singular"),
        "nom.pl": ({"nominative", "plural"}, "nominative plural"),
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
# The ein-words all take ein's endings — ein Hund, kein Hund; einen Hund, keinen Hund — and the
# plural ones take the endings ein would have if it had a plural.
EIN_WORDS = ["ein", "kein"]
EIN_ENDINGS = {"m": ["", "en", "em", "es"], "f": ["e", "e", "er", "er"], "n": ["", "", "em", "es"],
               "pl": ["e", "e", "en", "er"]}


def ein_word(word, ending):
    """The ein-word [word] with [ending]: kein + en → keinen."""
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


GENDER_WORD = {"m": "der", "f": "die", "n": "das"}
