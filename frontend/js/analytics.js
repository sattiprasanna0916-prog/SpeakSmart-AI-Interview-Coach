
import { apiRequest } from "./api.js";
import { $ } from "./utils.js";

export async function loadAnalytics(userId) {

  try {

    const response = await apiRequest(
      `/progress/user/${userId}`
    );

    console.log("Analytics:", response);

    const data = response.data;

    // LEVEL
    $("userLevel").innerText =
      data.current_level ||
      data.level ||
      "-";

    // SCORE
    $("avgScore").innerText =
      Math.round(
        data.avg_final ||
        data.average_score ||
        data.final_score ||
        0
      );

    // WEAK SKILL
    $("weakSkill").innerText =
      data.weakest_skill ||
      "Grammar";

    // STREAK
    $("streak").innerText =
      `${data.streak_days || 0} days`;

    // FLUENCY
    document.getElementById(
      "fluencyBar"
    ).style.width =
      `${(
        data.avg_fluency ||
        data.fluency ||
        0
      ) * 10}%`;

    // GRAMMAR
    document.getElementById(
      "grammarBar"
    ).style.width =
      `${(
        data.avg_grammar ||
        data.grammar ||
        0
      ) * 10}%`;

    // ACCURACY
    document.getElementById(
      "accuracyBar"
    ).style.width =
      `${(
        data.avg_accuracy ||
        data.accuracy ||
        0
      ) * 10}%`;

  } catch (err) {

    console.error(
      "Analytics load failed",
      err
    );
  }
}
