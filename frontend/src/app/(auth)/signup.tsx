import { View, Text, Button, ActivityIndicator, TextInput } from "react-native";
import React, { useState } from "react";
import { Link, router } from "expo-router";
import { useAuth } from "@/context/AuthContext";

export default function SignUpScreen() {
  const { signUp } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSignUp() {
    try {
      setError("");
      setIsSubmitting(true);

      await signUp(email, password);

      router.replace("/home");
    } catch (err) {
      setError("Unable to create account. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <View>
      <Text>Sign Up</Text>

      <TextInput
        placeholder="Email"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />

      <TextInput
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      {error ? <Text>{error}</Text> : null}

      {isSubmitting ? (
        <ActivityIndicator />
      ) : (
        <Button title="Create Account" onPress={handleSignUp} />
      )}

      <View>
        <Text>Already have an account? </Text>
        <Link href="/signin">Sign in</Link>
      </View>
    </View>
  );
}
