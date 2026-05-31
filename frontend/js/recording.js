import { $ } from "./utils.js";

let mediaRecorder;
let audioBlob;

let timerInterval;
let seconds = 0;

function updateTimer() {

  seconds++;

  const mins =
    String(
      Math.floor(seconds / 60)
    ).padStart(2, "0");

  const secs =
    String(
      seconds % 60
    ).padStart(2, "0");

  $("timer").innerText =
    `${mins}:${secs}`;
}

export async function startRecording() {

  const stream =
    await navigator.mediaDevices
      .getUserMedia({ audio: true });

  mediaRecorder =
    new MediaRecorder(stream);

  let chunks = [];

  mediaRecorder.ondataavailable = e => {
    chunks.push(e.data);
  };

  mediaRecorder.onstop = () => {

    audioBlob = new Blob(
      chunks,
      { type: "audio/webm" }
    );

    $("status").innerText =
      "Recording ready";

    clearInterval(timerInterval);
  };

  mediaRecorder.start();

  seconds = 0;

  $("timer").innerText = "00:00";

  timerInterval = setInterval(
    updateTimer,
    1000
  );

  $("status").innerText =
    "Recording...";

  // mic glow
  $("micIndicator").classList.add(
    "recording"
  );
}

export function stopRecording() {

  if (mediaRecorder) {

    mediaRecorder.stop();

    $("micIndicator")
      .classList.remove(
        "recording"
      );
  }
}

export function getAudioBlob() {
  return audioBlob;
}

export function clearAudioBlob() {
  audioBlob = null;
}