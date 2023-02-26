export const removeSuffix = (value: string, suffix: string): string =>
  value.endsWith(suffix) ? value.substring(0, value.length - suffix.length) : value
