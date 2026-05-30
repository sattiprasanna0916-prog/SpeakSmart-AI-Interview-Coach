import { apiRequest } from "./api.js";

import { $ } from "./utils.js";

export async function loadAnalytics(
  userId
) {

  const data = await apiRequest(
    `/progress/user/${userId}`
  );

  const progress =
    data.data || {};

  $("userLevel").innerText =
    progress.current_level || "-";

  $("avgScore").innerText =
    progress.avg_final || 0;

  $("weakSkill").innerText =
    progress.weakest_skill || "-";

  $("streak").innerText =
    `${progress.streak_days || 0} days`;
}