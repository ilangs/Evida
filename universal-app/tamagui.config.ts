import { createTamagui, createTokens } from 'tamagui'

// 1. 토큰 수동 정의 (의존성 0%화)
const tokens = createTokens({
  color: {
    brandPrimary: '#10B981', // Emerald Green
    brandSecondary: '#3B82F6', // Electric Blue
    bgDeep: '#0A192F', // Deep Navy
    white: '#FFFFFF',
    gray1: '#111827',
    gray2: '#1F2937',
    gray3: '#374151',
  },
  space: {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
    6: 24,
    8: 32,
    10: 40,
    true: 16,
  },
  size: {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
    6: 24,
    8: 32,
    10: 40,
    true: 16,
  },
  radius: {
    0: 0,
    2: 4,
    4: 8,
    5: 12,
    6: 16,
    8: 24,
    10: 32,
  },
  zIndex: {
    0: 0,
    1: 100,
  }
})

// 2. 테마 정의
const themes = {
  dark: {
    background: tokens.color.bgDeep,
    color: tokens.color.white,
    primary: tokens.color.brandPrimary,
  },
  light: {
    background: tokens.color.white,
    color: tokens.color.bgDeep,
    primary: tokens.color.brandPrimary,
  }
}

// 3. 메인 설정
export const config = createTamagui({
  defaultTheme: 'dark',
  shouldAddPrefersColorScheme: true,
  themeClassNameOnRoot: false,
  shorthands: {
    bg: 'backgroundColor',
    p: 'padding',
    m: 'margin',
    f: 'flex',
    w: 'width',
    h: 'height',
  },
  fonts: {}, 
  themes,
  tokens,
  media: {
    xs: { maxWidth: 660 },
    sm: { maxWidth: 800 },
    md: { maxWidth: 1020 },
    lg: { maxWidth: 1280 },
  },
})

export type AppConfig = typeof config

declare module 'tamagui' {
  interface TamaguiCustomConfig extends AppConfig {}
}

export default config
