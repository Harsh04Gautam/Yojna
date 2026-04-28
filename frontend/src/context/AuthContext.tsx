import { login, signup } from "@/services/auth";
import { deleteToken, getToken, saveToken } from "@/storage/secureStorage";
import React, {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";

type User = {
  id: string;
  email: string;
};

type AuthContextType = {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadSession() {
      try {
        const storedToken = await getToken();
        if (storedToken) {
          setToken(storedToken);
          setUser({
            id: "1",
            email: "saved-user@example.com",
          });
        }
      } catch (error) {
        console.log("Failed to load auth session:", error);
      } finally {
        setIsLoading(false);
      }
    }

    loadSession();
  }, []);

  async function signIn(email: string, password: string) {
    const response = await login(email, password);
    await saveToken(response.token);
    setToken(response.token);
    setUser(response.user);
  }

  async function signUp(email: string, password: string) {
    const response = await signup(email, password);
    saveToken(response.token);
    setUser(response.user);
  }

  async function signOut() {
    await deleteToken();
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{ user, token, isLoading, signIn, signUp, signOut }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
