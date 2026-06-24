import type { CollectionRuleRow } from './collection.types'

export function mapCollectionRule(name: string, enabled: boolean): CollectionRuleRow {
  return { name, enabled }
}
