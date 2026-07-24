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
let currentQuestionNumber = 0;
const TOTAL_QUESTIONS = 5;

// Start Interview / Generate Question
export async function startInterview() {

  // If interview already finished
  if (currentQuestionNumber >= TOTAL_QUESTIONS) {
    alert("🎉 Interview Completed!");
    return;
  }

  const level = $("level").value;
  const role = $("role").value;
  const category = $("category").value;

  const data = await apiRequest(
    "/question/generate",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        level,
        role,
        category
      })
    }
  );

  currentQuestion = data.question;

  // Clear chat only for first question
  if (currentQuestionNumber === 0) {
    $("chatBox").innerHTML = "";
  }

  currentQuestionNumber++;

  // Update progress
  $("progress").textContent = currentQuestionNumber;

  $("progressFill").style.width =
    `${(currentQuestionNumber / TOTAL_QUESTIONS) * 100}%`;

  addMessage(
    "ai",
    `Question ${currentQuestionNumber}: ${currentQuestion}`
  );

  toggleResult(false);
}

// Submit Audio
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

// Next Question
export async function nextQuestion() {

  if (currentQuestionNumber >= TOTAL_QUESTIONS) {

    alert("🎉 Interview Completed!");

    return;
  }

  await startInterview();
}

// Retry Current Question
export function retryAnswer() {

  toggleResult(false);

}