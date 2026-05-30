export const $ = (id) => document.getElementById(id);

export function analyzeAnswerQuality(answer) {
  if (!answer) return "empty";

  const words = answer.split(" ").length;

  if (words < 8) return "short";
  if (words < 20) return "medium";

  return "good";
}

export function calculateSimilarity(answer, ideal) {
  if (!answer || !ideal) return 0;

  const answerWords = answer.toLowerCase().split(/\s+/);
  const idealWords = ideal.toLowerCase().split(/\s+/);

  const uniqueMatches = new Set(
    idealWords.filter(word =>
      answerWords.includes(word)
    )
  );

  return Math.round(
    (uniqueMatches.size / idealWords.length) * 100
  );
}