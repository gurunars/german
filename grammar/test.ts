import { removeSuffix } from './utils.ts'

type PronounType = {
  first: string
  second: string
  third: string
}

type VerbPresentForms = {
  singluar: PronounType
  plural: PronounType
}

const getDefaultVerbPresentForms = (
  infinitive: string,
) => {
  const base = removeSuffix(infinitive, 'en')
}
