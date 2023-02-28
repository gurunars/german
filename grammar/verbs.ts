import { ensure, keys, removeSuffix } from './utils.ts'
import { IRREGULAR_VERBS } from './irregulaVerbs.ts'
import { VerbPresentForms, VerbPronounCases } from './types.ts'

const PRESENT_ENDINGS_MAP = {
  'en': {
    singular: {
      first: 'e',
      second: 'st',
      third: 't',
    },
    plural: {
      first: 'en',
      second: 't',
      third: 'en',
    },
  },
  'eln': {
    singular: {
      first: 'le',
      second: 'elst',
      third: 'elt',
    },
    plural: {
      first: 'eln',
      second: 'elt',
      third: 'eln',
    },
  },
  'ern': {
    singular: {
      first: 'ere',
      second: 'erst',
      third: 'ert',
    },
    plural: {
      first: 'ern',
      second: 'ert',
      third: 'ern',
    },
  },
}

const addEndings = (base: string, endings: VerbPronounCases): VerbPronounCases => ({
  first: base + endings.first,
  second: base + endings.second,
  third: base + endings.third,
})

const getSingularIrregularEndingsOverrides = (infinitive: string): Omit<VerbPronounCases, 'first'> | undefined =>
  IRREGULAR_VERBS[infinitive]

export const getVerbPresentEndings = (
  infinitive: string,
): VerbPresentForms => {
  const infinitiveEnding = ensure(
    keys(PRESENT_ENDINGS_MAP).find((it) => infinitive.endsWith(it)),
  ) as keyof typeof PRESENT_ENDINGS_MAP
  const base = removeSuffix(infinitive, infinitiveEnding)
  const presentEndings = PRESENT_ENDINGS_MAP[infinitiveEnding]
  return {
    singluar: {
      ...addEndings(base, presentEndings.singular),
      ...getSingularIrregularEndingsOverrides(infinitive),
    },
    plural: addEndings(base, presentEndings.plural),
  }
}
