import { 
  setupBootstrap, 
  addAnalyseButton, 
  getAnalyseButton, 
  addAnalysisCard,
  toogleAnalyseButtonLoading
} from './view.js';
import { getAnalysis } from './api.js';

setupBootstrap();
await addAnalyseButton();

const analyseButton = getAnalyseButton();

analyseButton.onclick = async () => {
  toogleAnalyseButtonLoading()
  const { isFake, analysis } = await getAnalysis();
  
  toogleAnalyseButtonLoading()
  addAnalysisCard(isFake, analysis)
};
