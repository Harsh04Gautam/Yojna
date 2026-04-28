import { View, Text, Button } from "react-native";
import React from "react";
import { useAuth } from "@/context/AuthContext";
import { router } from "expo-router";

export default function HomeScreen() {
  const { user, signOut } = useAuth();

  async function handleSignOut() {
    await signOut();
    router.replace("/(auth)/signin");
  }
  return (
    <View>
      <Text>Home</Text>
      <Text>You are Signed In</Text>
      {user ? <Text>Email: {user.email}</Text> : null}
      <Button title="Sign Out" onPress={handleSignOut} />
    </View>
  );
}
