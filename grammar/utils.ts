export const removeSuffix = (value: string, suffix: string): string =>
  value.endsWith(suffix) ? value.substring(0, value.length - suffix.length) : value

export const keys = <Shape extends Record<string, unknown>>(record: Shape): (keyof Shape)[] =>
  Object.keys(record) as (keyof Shape)[]

export const ensure = <T>(value?: T): T => {
  if (value === undefined) {
    throw 'Undefined'
  }
  return value
}

export const findFirst = <T>(items: T[], predicate: (item: T) => boolean): T => ensure(items.find(predicate))
