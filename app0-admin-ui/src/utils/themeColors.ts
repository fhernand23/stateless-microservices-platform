import { HSLToHex } from './color-converter'

const style = getComputedStyle(document.documentElement)

export const themeColors = {
  primary: HSLToHex(style.getPropertyValue('--primary')),
  // primaryMedium: '#b4e4ce',
  primaryMedium: '#5c97c8',
  // primaryLight: '#f7fcfa',
  primaryLight: '#b9d8f1',
  // secondary: '#ff227d',
  secondary: '#41b883',
  accent: '#1769ad',
  // accent: '#797bf2',
  accentMedium: '#d4b3ff',
  accentLight: '#b8ccff',
  success: HSLToHex(style.getPropertyValue('--success')),
  info: HSLToHex(style.getPropertyValue('--info')),
  warning: HSLToHex(style.getPropertyValue('--warning')),
  danger: HSLToHex(style.getPropertyValue('--danger')),
  purple: HSLToHex(style.getPropertyValue('--purple')),
  blue: HSLToHex(style.getPropertyValue('--blue')),
  green: HSLToHex(style.getPropertyValue('--green')),
  yellow: HSLToHex(style.getPropertyValue('--yellow')),
  orange: HSLToHex(style.getPropertyValue('--orange')),
  // lightText: '#a2a5b9',
  lightText: '#7b7f9e',
  fadeGrey: '#ededed',
}
