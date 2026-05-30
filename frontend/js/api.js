import { API_BASE } from "./config.js";
import { getToken } from "./auth.js";

export function getAuthHeaders() {
  const token = getToken();

  return {
    Authorization: `Bearer ${token}`
  };
}

export async function apiRequest(
  endpoint,
  options = {}
) {
  const response = await fetch(
    `${API_BASE}${endpoint}`,
    options
  );

  if (!response.ok) {
    const error = await response.json();

    throw new Error(
      error.detail || "Request failed"
    );
  }

  return response.json();
}