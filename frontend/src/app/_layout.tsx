import "@/global.css"
import { useFonts } from "expo-font"
import { SplashScreen } from "expo-router"
import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import React, { useEffect } from 'react';
import { useColorScheme } from 'react-native';

import { AnimatedSplashOverlay } from '@/components/animated-icon';
import AppTabs from '@/components/app-tabs';

export default function TabLayout() {
  const [fontsLoaded, error] = useFonts({
    "PlusJakartaSans-ExtraBold": require('@/assets/fonts/PlusJakartaSans-ExtraBold.ttf'),
    "PlusJakartaSans-Bold": require('@/assets/fonts/PlusJakartaSans-Bold.ttf'),
    "PlusJakartaSans-Regular": require('@/assets/fonts/PlusJakartaSans-Regular.ttf'),
    "PlusJakartaSans-Medium": require('@/assets/fonts/PlusJakartaSans-Medium.ttf'),
    "PlusJakartaSans-Light": require('@/assets/fonts/PlusJakartaSans-Light.ttf'),
  })

  useEffect(() => {
    if (error) throw error;
    if (fontsLoaded) SplashScreen.hideAsync()


  }, [fontsLoaded, error])

  const colorScheme = useColorScheme();

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <AnimatedSplashOverlay />
      <AppTabs />
    </ThemeProvider>
  );
}
