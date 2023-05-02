import { 
  addAnalyseButton, 
  getAnalyseButton, 
  addAnalysisCard,
  toogleAnalyseButtonLoading,
  expandAnalysisCard,
  disableAnalyseButton
} from './view.js';
import { getAnalysis } from './api.js';

await addAnalyseButton();

const analyseButton = getAnalyseButton();

analyseButton.onclick = async () => {
  await toogleAnalyseButtonLoading();
  
  const { isFake, analysis } = await getAnalysis();
  
  await toogleAnalyseButtonLoading();
  
  addAnalysisCard(isFake, analysis);
  expandAnalysisCard();

  disableAnalyseButton();
};

