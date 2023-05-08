import { addAnalysisCard, disableAnalyseButton, toogleAnalyseButtonLoading, setTooltipContent } from "./view.js";
import { getAnalysis } from "./api.js";

export function isArticlePage() {
  return document.querySelector("meta[property='og:type']")?.content === "article";
}

const analysisSteps = {
  ARTICLE: "Processat conteúdo da página",
  GOOGLE_QUERY: "Gerar query de busca",
  GOOGLE_SEARCH_RESULTS: "Buscar no google",
  FAKENO_AI_PREDICTION: "Classificar com a FakeNo-AI",
  GPT_ANALYSIS: "Gerar análise com o GPT"
}

export async function handleAnalyseButtonClick() {
  const startTime = Date.now();
  await toogleAnalyseButtonLoading();
  
  const response = await getAnalysis();
  
  const reader = response.body.getReader() 
  const decoder = new TextDecoder();

  let analysis = "";

  reader.read().then(function process({ done, value }) {
    if (done) return;
  
    const step = JSON.parse(decoder.decode(value))

    setTooltipContent(
      `✅ ${analysisSteps[step.title]}... +${Date.now() - startTime}ms`
    )

    if(step.title === "GPT_ANALYSIS") {
      analysis = step.result
    }
  
    return reader.read().then(process)
  }).finally(async () => {
    await toogleAnalyseButtonLoading();
  
    addAnalysisCard(analysis);
  
    disableAnalyseButton(); 
  })
}