import { AuthProvider } from "react-admin";

const API = "http://localhost:8000";

export const authProvider: AuthProvider = {
  login: async ({ username, password }) => {
    const res = await fetch(`${API}/admin/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) {
      throw new Error("Invalid credentials");
    }

    const data = await res.json();
    // backend должен вернуть { token: "..." }
    localStorage.setItem("admin_jwt", data.token);
  },

  logout: async () => {
    localStorage.removeItem("admin_jwt");
  },

  checkAuth: async () => {
    const token = localStorage.getItem("admin_jwt");
    if (!token) throw new Error("Not authenticated");
  },

  checkError: async (error: any) => {
    const status = error?.status || error?.statusCode;
    if (status === 401 || status === 403) {
      localStorage.removeItem("admin_jwt");
      throw new Error("Unauthorized");
    }
  },

  getIdentity: async () => {
    return { id: "admin", fullName: "Admin" };
  },

  getPermissions: async () => [],
};
