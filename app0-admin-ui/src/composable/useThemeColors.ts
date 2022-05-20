import { computed, reactive } from 'vue'
import { createSharedComposable, useCssVar } from '@vueuse/core'
import { HSLToHex } from '/@src/utils/color-converter'

export const useThemeColors = createSharedComposable(() => {
  const primary = useCssVar('--primary', document.documentElement)
  const success = useCssVar('--success', document.documentElement)
  const info = useCssVar('--info', document.documentElement)
  const warning = useCssVar('--warning', document.documentElement)
  const danger = useCssVar('--danger', document.documentElement)
  const purple = useCssVar('--purple', document.documentElement)
  const blue = useCssVar('--blue', document.documentElement)
  const green = useCssVar('--green', document.documentElement)
  const yellow = useCssVar('--yellow', document.documentElement)
  const orange = useCssVar('--orange', document.documentElement)

  const themeColors = reactive({
    primary: computed(() => HSLToHex(primary.value)),
    // primaryMedium: '#b4e4ce',
    primaryMedium: '#5c97c8',
    // primaryLight: '#f7fcfa',
    primaryLight: '#b9d8f1',
    // secondary: '#ff227d',
    secondary: '#41b883',
    // accent: '#797bf2',
    accent: '#1769ad',
    accentMedium: '#d4b3ff',
    accentLight: '#b8ccff',
    success: computed(() => HSLToHex(success.value)),
    info: computed(() => HSLToHex(info.value)),
    warning: computed(() => HSLToHex(warning.value)),
    danger: computed(() => HSLToHex(danger.value)),
    purple: computed(() => HSLToHex(purple.value)),
    blue: computed(() => HSLToHex(blue.value)),
    green: computed(() => HSLToHex(green.value)),
    yellow: computed(() => HSLToHex(yellow.value)),
    orange: computed(() => HSLToHex(orange.value)),
    // lightText: '#a2a5b9',
    lightText: '#7b7f9e',
    fadeGrey: '#ededed',
  } as const)

  return themeColors
})
