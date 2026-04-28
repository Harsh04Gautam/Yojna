import { Stack } from "expo-router";
import React from "react";

export default function AuthLayout() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="signin" options={{ title: "Sign In" }}></Stack.Screen>
      <Stack.Screen name="signup" options={{ title: "Sign Up" }}></Stack.Screen>
    </Stack>
  );
}
