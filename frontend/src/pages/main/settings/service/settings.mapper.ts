import type { AppSetting, SettingRow } from './settings.types'

export function mapSettingRow(item: AppSetting): SettingRow {
  return {
    settingKey: item.setting_key,
    settingValue: item.setting_value,
  }
}
