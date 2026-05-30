import { STORAGE_KEYS } from "./config.js";

export function logout() {
  localStorage.clear();
  window.location.href = "index.html";
}

export function getToken() {
  return localStorage.getItem(
    STORAGE_KEYS.TOKEN
  );
}

export function getUserId() {
  return localStorage.getItem(
    STORAGE_KEYS.USER_ID
  );
}

export function saveAuth(data) {
  localStorage.setItem(
    STORAGE_KEYS.TOKEN,
    data.access_token
  );

  localStorage.setItem(
    STORAGE_KEYS.USER_ID,
    data.user.user_id
  );

  localStorage.setItem(
    STORAGE_KEYS.USER_EMAIL,
    data.user.email
  );
}