import { useAuth } from "@/context/AuthContext";
import { Link, Redirect } from "expo-router";
import { ActivityIndicator, Text, View } from "react-native";

export default function Index() {
  const { user, isLoading } = useAuth();
  if (isLoading) {
    return (
      <View>
        <ActivityIndicator />
      </View>
    );
  }

  if (user) {
    return (
      <View className="flex-1 items-center justify-center bg-white">
        <Text className="text-xl font-bold text-blue-700 font-plusjakartasans">
          Welcome to Nativewind!
        </Text>
      </View>
    );
  }

  return (
    <Link href={"/(auth)/signin"} className="mt-4 p-4 bg-slate-400">
      Go to Sign In
    </Link>
  );
}
