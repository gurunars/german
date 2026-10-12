# German

A German course for the [flashcards](https://github.com/gurunars/flashcards) app: one deck per
lesson, each lesson building on the ones before it.

To follow the course, give the app the folder: `https://github.com/gurunars/german/tree/master/lessons`,
or import one lesson at a time as you get to it.

## How a lesson is made

Each card is an English sentence with the part being learnt in **bold**, the German sentence, and
a short English note on the grammar. `make json` (podman, nothing installed on the host) builds
`lessons/*.json` and `lessons/index.json` from:

- `lessons/lessons.tsv` — the course in order: number, folder, title;
- `lessons/grammar.tsv` — every grammar point, the lesson that teaches it, and its label;
- `lessons/NN-x/words.tsv` — the words a lesson introduces: lemma, part of speech, English, and
  for words without a Wiktionary table (pronouns, articles, particles…) their forms;
- `lessons/NN-x/cards.tsv` — its cards: grammar point, lemma and slot (or `-`), English, German, note.

The build refuses a card that
- practises a grammar point from a later lesson;
- uses a German word not introduced in this lesson or an earlier one — a later lesson may add
  forms of a word, so `den` only appears once the accusative is taught;
- names a lemma and a slot whose bold German is not the form [Wiktionary](https://kaikki.org)
  gives — so no gender, ending or conjugation is written from memory;

and a lesson whose new word no card uses. Forms of a word already introduced are not gated one
by one (*gewesen* passes once *sein* is taught): the grammar point and review keep those in step.
To add words, list them in the lesson's `words.tsv`, run `make forms` to fetch their tables into
`sentences/forms.json`, then write the cards.

## Archive

The earlier decks — topic word lists and the **Before B1** sentence deck — live in
`archive/words/`. `archive/words/*.csv` (one `English , German` pair per line) and
`sentences/*.tsv` are their sources; `make json` still rebuilds them, with priorities from each
word's rank in `archive/words/frequency_de.txt`.

Inflection tables: [Wiktionary](https://en.wiktionary.org) via [kaikki.org](https://kaikki.org),
licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Frequency data: [FrequencyWords](https://github.com/hermitdave/FrequencyWords) by Hermit
Dave (OpenSubtitles 2018, German, top 50,000 forms), licensed
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Lessons

- [Lesson 1 · Being and naming: sein, pronouns, der/die/das](lessons/01-sein.json) — 36 cards
- [Lesson 2 · Having things: haben, ein/eine, the accusative](lessons/02-haben.json) — 33 cards
- [Lesson 3 · Doing things: regular verbs in the present, the verb second](lessons/03-verbs.json) — 40 cards
- [Lesson 4 · Saying no: nicht and kein](lessons/04-negation.json) — 37 cards
- [Lesson 5 · Asking: W-questions and yes/no questions](lessons/05-questions.json) — 38 cards
- [Lesson 6 · Counting: numbers 0–20, prices and age](lessons/06-numbers.json) — 32 cards
- [Lesson 7 · Verbs that change their vowel: fahren, essen, lesen, sehen…](lessons/07-stem-change.json) — 37 cards
- [Lesson 8 · Family: mein, dein, sein, ihr, unser, euer, Ihr](lessons/08-possessives.json) — 36 cards
- [Lesson 9 · More than one: the plural of nouns](lessons/09-plural.json) — 38 cards
- [Lesson 10 · Telling the time: the clock, the days, um and am](lessons/10-clock.json) — 36 cards
- [Lesson 11 · Dates: the months, im, numbers to 100, der dritte Mai](lessons/11-dates.json) — 35 cards
- [Lesson 12 · For me, without you: accusative prepositions and pronouns](lessons/12-acc-prep.json) — 38 cards

## Decks

- [Before B1](archive/words/before_b1.json) — 337 cards
- [Adjectives](archive/words/adjectives.json) — 22 cards
- [Animals](archive/words/animals.json) — 68 cards
- [Antonyms](archive/words/antonyms.json) — 46 cards
- [Clothes](archive/words/clothes.json) — 58 cards
- [Colors](archive/words/colors.json) — 11 cards
- [Core](archive/words/core.json) — 754 cards
- [Crime and money](archive/words/crime_and_money.json) — 23 cards
- [Critical](archive/words/critical.json) — 99 cards
- [Directions](archive/words/directions.json) — 8 cards
- [Entertainment](archive/words/entertainment.json) — 8 cards
- [Family](archive/words/family.json) — 25 cards
- [Food](archive/words/food.json) — 81 cards
- [Fruits and vegetables](archive/words/fruits_and_vegetables.json) — 64 cards
- [House and furniture](archive/words/house_and_furniture.json) — 82 cards
- [Materials and tools](archive/words/materials_and_tools.json) — 47 cards
- [Misc](archive/words/misc.json) — 43 cards
- [Nature](archive/words/nature.json) — 83 cards
- [Office supplies](archive/words/office_supplies.json) — 53 cards
- [Parts of the body](archive/words/parts_of_the_body.json) — 72 cards
- [Phrases](archive/words/phrases.json) — 71 cards
- [Places](archive/words/places.json) — 64 cards
- [Professions](archive/words/professions.json) — 71 cards
- [Sports](archive/words/sports.json) — 25 cards
- [Time](archive/words/time.json) — 95 cards
- [Time prepositions](archive/words/time_prepositions.json) — 12 cards
- [Transport](archive/words/transport.json) — 11 cards
- [Traveling](archive/words/traveling.json) — 33 cards
- [Verbs](archive/words/verbs.json) — 247 cards
- [Weather](archive/words/weather.json) — 14 cards
