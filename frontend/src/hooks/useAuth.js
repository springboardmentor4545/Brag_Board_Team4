import { useState } from "react";
import { apiClient } from "../api/client";
import { API_ENDPOINTS } from "../api/config";

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const register = async (email, password) => {
    setLoading(true);
    try {
      const response = await apiClient.post(API_ENDPOINTS.USERS.REGISTER, {
        email,
        password,
      });
      setUser(response);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await apiClient.post(API_ENDPOINTS.USERS.LOGIN, {
        username: email,
        password,
      });
      apiClient.setToken(response.access_token);
      setUser(response);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    apiClient.clearToken();
    setUser(null);
  };

  return { user, loading, error, register, login, logout };
}
