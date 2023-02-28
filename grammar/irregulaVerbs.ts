import { VerbPronounCases } from './types.ts'

export const IRREGULAR_VERBS: Record<string, Omit<VerbPronounCases, 'first'>> = {
  'essen': {
    second: 'isst',
    third: 'isst',
  },
}
