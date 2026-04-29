import { Slot } from 'expo-router';
import { TamaguiProvider, Theme } from 'tamagui';
import { config } from '../tamagui.config';

export default function RootLayout() {
  if (!config) return null; // 설정 로드 대기

  return (
    <TamaguiProvider config={config} defaultTheme="dark">
      <Theme name="dark">
        <Slot />
      </Theme>
    </TamaguiProvider>
  );
}
