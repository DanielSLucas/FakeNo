import { getAsset } from './api.js';

export async function addAnalyseButton() {
  const asset = await getAsset("search.svg");
  
  const articleTitle = getArticleTitle();

  const button = document.createElement("button");
  button.id = "fkn-btn-analyse";
  button.type = "button";
  button.innerHTML = asset;

  articleTitle.prepend(button);
}

export function getArticleTitle() {
  const articleTitle = document.querySelector("article h1") 
    || document.querySelector("main h1") 
    || document.querySelector("h1");
  
  return articleTitle
}

export async function toogleAnalyseButtonLoading() {
  const button = getAnalyseButton();

  const isLoading  = button.className.includes("loading");

  if (isLoading) {
    const asset  = await getAsset("search.svg");

    button.innerHTML = asset;
    button.className = "";
  } else {
    button.className += "loading";

    button.innerHTML = `
      <div class="fkn-loading-ring">
        <div></div><div></div><div></div><div></div>
      </div>
    `;
  }
}

export function getAnalyseButton() {
  return document.getElementById("fkn-btn-analyse")
}

export function disableAnalyseButton() {
  const analyseButton = getAnalyseButton();

  analyseButton.onclick = () => {};
  analyseButton.disabled = true;
}

export function addAnalysisCard(isFake, analysis) {
  const status = isFake ? "danger" : "success";

  const card = `
    <div id="fkn-analysis-card"  class="fkn-card fkn-border-${status} fkn-expand-contract fkn-contract">
      <div class="fkn-card-header fkn-bg-${status}">
        <strong>${isFake ? "Fake" : "Real"}</strong>
      </div>
      <div class="fkn-card-body">
        <p class="fkn-card-text" style="text-align: justify; font-weight: 450;">
          ${analysis}
        </p>
      </div>
    </div>
  `;
  
  const articleTitle = getArticleTitle();
  const articleHeader = articleTitle.parentElement;

  articleHeader.innerHTML += card;
}

export function expandAnalysisCard() {
  const cardEl = document.getElementById("fkn-analysis-card");

  const fullHeight = cardEl.getBoundingClientRect().height

  const styleEl = document.createElement("style");
  styleEl.innerHTML = `
    .fkn-card-collapsed { height: 0px; visibility: hidden; position: absolute; }
    .fkn-card-expanded { height: ${fullHeight}px; visibility: visible; position: inherit;}
  `
  document.querySelector("head").append(styleEl)

  cardEl.className += " fkn-card-collapsed";  
  setTimeout(() => {
    cardEl.className = cardEl.className.replace("fkn-card-collapsed", "fkn-card-expanded")
  }, 1000)
}