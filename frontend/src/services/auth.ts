type LoginResponse = {
  token: string;
  user: {
    id: string;
    email: string;
    name?: string;
  };
};

export async function login(
  email: string,
  password: string,
): Promise<LoginResponse> {
  await new Promise((resolve) => setTimeout(resolve, 800));

  if (!email || !password) {
    throw new Error("Email and Password are required");
  }

  return {
    token: "fake-token-123",
    user: {
      id: "1",
      email,
      name: "Harsh",
    },
  };
}

export async function signup(
  email: string,
  password: string,
): Promise<LoginResponse> {
  await new Promise((resolve) => setTimeout(resolve, 800));

  if (!email || !password) {
    throw new Error("Email and password are required");
  }

  return {
    token: "fake-token-123",
    user: {
      id: "1",
      email,
      name: "Harsh",
    },
  };
}
