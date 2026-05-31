import { $ } from "./utils.js";

export function addMessage(type, text) {
  const chatBox = $("chatBox");

  if (!chatBox) return;

  const msg = document.createElement("div");

  msg.className = `chat-msg ${type}`;

  msg.innerText = text;

  chatBox.appendChild(msg);

  chatBox.scrollTop =
    chatBox.scrollHeight;
}

export function toggleResult(show) {
  
  const section = $("resultSection");

  if (!section) return;

  section.style.display =
    show ? "block" : "none";
}

export function renderResult(data) {
  toggleResult(true);
  const scores = data.scores || {};

  $("fluency").innerText =
    scores.fluency ?? "-";

  $("grammar").innerText =
    scores.grammar ?? "-";

  $("accuracy").innerText =
    scores.accuracy ?? "-";

  $("final").innerText =
    scores.final_score ?? "-";

  $("improvedAnswer").innerText =
    data.improved_answer ||
    "No suggestion";

  const feedbackList = $("feedbackList");

  feedbackList.innerHTML = "";

  (data.feedback || "")
    .split("\n")
    .forEach(item => {

      if (!item.trim()) return;

      const li =
        document.createElement("li");

      li.innerText = item;

      feedbackList.appendChild(li);
    });
}