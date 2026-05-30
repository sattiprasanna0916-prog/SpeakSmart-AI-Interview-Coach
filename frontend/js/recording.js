import { $ } from "./utils.js";

let mediaRecorder;
let audioBlob;

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
  };

  mediaRecorder.start();

  $("status").innerText =
    "Recording...";
}

export function stopRecording() {

  if (mediaRecorder) {
    mediaRecorder.stop();
  }
}

export function getAudioBlob() {
  return audioBlob;
}

export function clearAudioBlob() {
  audioBlob = null;
}