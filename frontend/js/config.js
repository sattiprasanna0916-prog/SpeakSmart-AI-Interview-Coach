export const API_BASE =
  window.location.origin.includes("localhost")
    ? "http://127.0.0.1:8000"
    : "https://english-ai-tutor-1.onrender.com";

export const STORAGE_KEYS = {
  TOKEN: "token",
  USER_ID: "user_id",
  USER_EMAIL: "user_email"
};

export const MAX_QUESTIONS = 5;