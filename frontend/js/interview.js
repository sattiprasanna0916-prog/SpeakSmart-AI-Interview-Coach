import { apiRequest } from "./api.js";
import { API_BASE } from "./config.js";
import {
  addMessage,
  renderResult,
  toggleResult
} from "./ui.js";

import {
  getAudioBlob,
  clearAudioBlob
} from "./recording.js";

import { $ } from "./utils.js";

let currentQuestion = "";

export async function startInterview() {

  const level =
    $("level").value;

  const role =
    $("role").value;

  const category =
    $("category").value;

  const data = await apiRequest(
    "/question/generate",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        level,
        role,
        category
      })
    }
  );

  currentQuestion =
    data.question;

  $("chatBox").innerHTML = "";

  addMessage(
    "ai",
    currentQuestion
  );

  toggleResult(false);
}

export async function submitAudio() {

  const blob = getAudioBlob();

  if (!blob) {
    alert("Record audio first");
    return;
  }

  const form = new FormData();

  form.append("audio", blob, "recording.webm");
  form.append("question", currentQuestion);
  form.append("level", $("level").value);

  const token = localStorage.getItem("token");

  const response = await fetch(
    `${API_BASE}/attempts/submit`,
    {
      method: "POST",
      headers: {
        ...(token && {
          Authorization: `Bearer ${token}`
        })
      },
      body: form
    }
  );

  const data = await response.json();

  renderResult(data);
  toggleResult(true);

  clearAudioBlob();
}