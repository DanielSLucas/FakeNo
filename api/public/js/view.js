import { getAsset } from './api.js';

const ANALYSE_BUTTON_ID = "fkn-btn-analyse";
const ARTICLE_HEADER_ID = "fkn-article-header";
const ANALYSIS_CARD_ID = "fkn-analysis-card";

// HEADER FUNCTIONS

export async function modifyArticleHeader() {
  const oldTitleText = getArticleTitle().textContent

  const newArticleHeader = createArticleHeader();
  const newTitle = createH1Title(oldTitleText)
  const button = await createAnalyzeButton();

  newTitle.prepend(button)
  newArticleHeader.append(newTitle)

  replateCurrentTitle(newArticleHeader)
}

function getArticleTitle() {
  const articleTitle = document.querySelector("article h1") 
    || document.querySelector("main h1") 
    || document.querySelector("h1");
  
  return articleTitle
}

function createArticleHeader(){
  const articleHeader = document.createElement("div");
  articleHeader.id = ARTICLE_HEADER_ID;

  return articleHeader;
}

function createH1Title(title) {
  const h1 = document.createElement("h1");
  h1.innerText = title

  return h1;
}

function replateCurrentTitle(content) {
  const articleTitle = getArticleTitle();  

  articleTitle.replaceWith(content)
}

// ANALYSE BUTTON FUNCTIONS

async function createAnalyzeButton() {
  const asset = await getAsset("search.svg");

  const button = document.createElement("button");
  button.id = ANALYSE_BUTTON_ID;
  button.type = "button";
  button.innerHTML = asset;

  return button;
}

export async function toogleAnalyseButtonLoading() {
  const button = getAnalyseButton();  

  if (isLoading(button)) {
    await resetAnalyseButton()
  } else {
    setLoading(button)
  }
}

export function getAnalyseButton() {
  return document.getElementById(ANALYSE_BUTTON_ID)
}

async function resetAnalyseButton() {
  const newButton  = await createAnalyzeButton();
  getAnalyseButton().replaceWith(newButton)
}

function isLoading(element) {
  return element.className.includes("loading");
}

function setLoading(element) {
  element.className += "loading";

  element.innerHTML = `
    <div class="fkn-loading-ring">
      <div></div><div></div><div></div><div></div>
    </div>
  `;
}

export function disableAnalyseButton() {
  const analyseButton = getAnalyseButton();

  analyseButton.onclick = () => {};
  analyseButton.disabled = true;
}


export function addAnalysisCard(isFake, analysis) {
  const card = createAnalysisCardHTML(isFake, analysis)
    
  getArticleHeader().innerHTML += card;  
}

function createAnalysisCardHTML(isFake, analysis) {
  const status = isFake ? "danger" : "success";

  const card = `
    <div id="${ANALYSIS_CARD_ID}"  class="fkn-card fkn-border-${status} fkn-expand-contract fkn-contract">
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

  return card;
}

export function getArticleHeader() {
  return document.getElementById(ARTICLE_HEADER_ID);
}

// TODO refatorar essa função (ela faz coisas dms!!)
export function expandAnalysisCard() {
  const cardEl = document.getElementById(ANALYSIS_CARD_ID);

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