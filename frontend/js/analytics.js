import { apiRequest } from "./api.js";
import { $ } from "./utils.js";

export async function loadAnalytics(userId) {

  try {

    const data = await apiRequest(
      `/progress/user/${userId}`
    );

    $("userLevel").innerText =
      data.current_level || "-";

    $("avgScore").innerText =
      data.avg_final || 0;

    $("weakSkill").innerText =
      data.weakest_skill || "-";

    $("streak").innerText =
      `${data.streak_days || 0} days`;

    // progress bars
    document.getElementById(
      "fluencyBar"
    ).style.width =
      `${(data.avg_fluency || 0) * 10}%`;

    document.getElementById(
      "grammarBar"
    ).style.width =
      `${(data.avg_grammar || 0) * 10}%`;

    document.getElementById(
      "accuracyBar"
    ).style.width =
      `${(data.avg_accuracy || 0) * 10}%`;

  } catch (err) {

    console.error(
      "Analytics load failed",
      err
    );
  }
}