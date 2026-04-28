import { View, Text, TextInput, ActivityIndicator, Button } from "react-native";
import React, { useState } from "react";
import { Link, router } from "expo-router";
import { useAuth } from "@/context/AuthContext";

export default function SignInScreen() {
  const { signIn } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSignIn() {
    try {
      setError("");
      setIsSubmitting(true);
      await signIn(email, password);

      router.replace("/home");
    } catch (err) {
      setError("Unable to sign in. Please check your email and password.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <View>
      <Text>SignIn</Text>
      <TextInput
        placeholder="email"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        placeholder="password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      {error ? <Text>{error}</Text> : null}
      {isSubmitting ? (
        <ActivityIndicator />
      ) : (
        <Button title="Sign In" onPress={handleSignIn} />
      )}
      <Link href={"/(auth)/signin"}>Create account</Link>
      <View>
        <Text>Don't have and account?</Text>
        <Link href={"/(auth)/signup"}>Sign up</Link>
      </View>
    </View>
  );
}
