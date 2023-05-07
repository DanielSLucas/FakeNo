import { addAnalysisCard, disableAnalyseButton, toogleAnalyseButtonLoading } from "./view.js";
import { getAnalysis } from "./api.js";

export function isArticlePage() {
  return document.querySelector("meta[property='og:type']")?.content === "article";
}

export async function handleAnalyseButtonClick() {
  await toogleAnalyseButtonLoading();
  
  const { analysis } = await getAnalysis();
  
  await toogleAnalyseButtonLoading();
  
  addAnalysisCard(analysis);

  disableAnalyseButton(); 
}