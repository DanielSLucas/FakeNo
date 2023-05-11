import { addAnalysisCard, disableAnalyseButton, toogleAnalyseButtonLoading, setTooltipContent } from "./view.js";
import { getAnalysis } from "./api.js";

const analysisSteps = {
  ARTICLE: {
    description: "Processar conteúdo da página",
    executionTime: null
  },
  GOOGLE_QUERY: {
    description: "Gerar query de busca",
    executionTime: null
  },
  GOOGLE_SEARCH_RESULTS: {
    description: "Buscar no google",
    executionTime: null
  },
  FAKENO_AI_PREDICTION: {
    description: "Classificar com a FakeNo-AI",
    executionTime: null
  },
  GPT_ANALYSIS: {
    description: "Gerar análise com o GPT",
    executionTime: null
  },
}

export async function handleAnalyseButtonClick() {
  await toogleAnalyseButtonLoading();
  
  let stepTime = Date.now();
  const response = await getAnalysis();
  
  const reader = response.body.getReader() 
  const decoder = new TextDecoder();
  
  let analysis = "";

  reader.read().then(function process({ done, value }) {
    if (done) return;
  
    const step = JSON.parse(decoder.decode(value))

    analysisSteps[step.title].executionTime = Date.now() - stepTime;
    setTooltipContent(
      createStepsList(analysisSteps)
    )
    stepTime = Date.now();

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

function createStepsList(steps) {
  const stepKeys = Object.keys(steps)
  const fomattedSteps = stepKeys.map(stepKey => {
    const step = steps[stepKey];
    const icon = step.executionTime ? '✅' : '➖';
    const time = step.executionTime ? `+${step.executionTime}ms` : ''
    return `<li>${icon} ${step.description}... ${time}</li>`
  })
  
  return `
    <ul>
      ${fomattedSteps.join('\n')}
    </ul>
  `
}