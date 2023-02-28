export const removeSuffix = (value: string, suffix: string): string =>
  value.endsWith(suffix) ? value.substring(0, value.length - suffix.length) : value

export const keys = <K extends string, T>(record: Record<K, T>) => Object.keys(record)

export const ensure = <T>(value?: T): T => {
  if (value === undefined) {
    throw 'Undefined'
  }
  return value
}
