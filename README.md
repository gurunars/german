# German

Word lists for the [flashcards](https://github.com/gurunars/flashcards) app.

`words/*.csv` are the source — one `English , German` pair per line, split on the first
comma. `make json` (podman, nothing installed on the host) turns them into decks the app
imports by URL: `words/*.json`, with `frontLanguage: en` and `backLanguage: de`, listed
in [`words/index.json`](words/index.json). Commit the CSVs and the JSON together.

Every card is annotated with its **frequency rank**: the place of its German word in
`words/frequency_de.txt` (a word group counts as its rarest word; alternatives as their
most common one). The card's **priority** follows from it — 4 for the ten most frequent
words, 3 for the top 100, 2 for the top 1,000, 1 at rank 10,000, 0.5 when not ranked — and
a trailing `* N` on either side of a CSV line multiplies it (a bare `*` means 2).

**Before B1** is the 1,500 most frequent cards across all decks — the vocabulary to have
before starting a B1 course. `words/core.csv` holds the high-frequency words the topic
decks did not cover.

To import every deck at once, give the app the folder:
`https://github.com/gurunars/german/tree/master/words`.

`grammar/` holds grammar notes.

Frequency data: [FrequencyWords](https://github.com/hermitdave/FrequencyWords) by Hermit
Dave (OpenSubtitles 2018, German, top 50,000 forms), licensed
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Decks

- [Before B1](words/before_b1.json) — 1500 cards
- [Adjectives](words/adjectives.json) — 22 cards
- [Animals](words/animals.json) — 68 cards
- [Antonyms](words/antonyms.json) — 46 cards
- [Clothes](words/clothes.json) — 58 cards
- [Colors](words/colors.json) — 11 cards
- [Core](words/core.json) — 754 cards
- [Crime and money](words/crime_and_money.json) — 23 cards
- [Critical](words/critical.json) — 99 cards
- [Directions](words/directions.json) — 8 cards
- [Entertainment](words/entertainment.json) — 8 cards
- [Family](words/family.json) — 25 cards
- [Food](words/food.json) — 81 cards
- [Fruits and vegetables](words/fruits_and_vegetables.json) — 64 cards
- [House and furniture](words/house_and_furniture.json) — 82 cards
- [Materials and tools](words/materials_and_tools.json) — 47 cards
- [Misc](words/misc.json) — 43 cards
- [Nature](words/nature.json) — 83 cards
- [Office supplies](words/office_supplies.json) — 53 cards
- [Parts of the body](words/parts_of_the_body.json) — 72 cards
- [Phrases](words/phrases.json) — 71 cards
- [Places](words/places.json) — 64 cards
- [Professions](words/professions.json) — 71 cards
- [Sports](words/sports.json) — 25 cards
- [Time](words/time.json) — 95 cards
- [Time prepositions](words/time_prepositions.json) — 12 cards
- [Transport](words/transport.json) — 11 cards
- [Traveling](words/traveling.json) — 33 cards
- [Verbs](words/verbs.json) — 247 cards
- [Weather](words/weather.json) — 14 cards
