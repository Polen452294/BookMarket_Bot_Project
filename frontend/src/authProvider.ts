import type { AuthProvider } from "react-admin";

const KEY = "admin_token";

export const authProvider: AuthProvider = {
  login: async (params) => {
    // React Admin по умолчанию передаёт username/password.
    // Мы используем "password" как token.
    const token = (params.password || "").trim();
    if (!token) throw new Error("Token required");
    localStorage.setItem(KEY, token);
  },
  logout: async () => {
    localStorage.removeItem(KEY);
  },
  checkAuth: async () => {
    const t = localStorage.getItem(KEY);
    if (!t) throw new Error("Not authenticated");
  },
  checkError: async () => {},
  getPermissions: async () => [],
  getIdentity: async () => ({ id: "admin", fullName: "Admin" }),
};

export const getToken = () => localStorage.getItem(KEY) || "";
