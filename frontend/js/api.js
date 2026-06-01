
import { API_BASE }
from "./config.js";

export async function apiRequest(

  endpoint,

  options = {}

){

  const token =
    localStorage.getItem("token");

  const response = await fetch(

    `${API_BASE}${endpoint}`,

    {

      headers:{

        "Content-Type":
          "application/json",

        ...(token && {
          Authorization:
            `Bearer ${token}`
        }),

        ...(options.headers || {})
      },

      ...options
    }
  );

  const data =
    await response.json();

  if(!response.ok){

    throw new Error(
      data.detail ||
      "API request failed"
    );
  }

  return data;
}
