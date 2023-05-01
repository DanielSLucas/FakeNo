import { getAsset } from './api.js';

export function setupBootstrap() {
  const head = document.querySelector('head');
  const body = document.querySelector('body');

  const cssLink = document.createElement('link');
  cssLink.href = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css";
  cssLink.rel = "stylesheet";
  cssLink.integrity = "sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ";
  cssLink.crossOrigin = "anonymous";

  const jsScript = document.createElement('script');
  jsScript.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js";
  jsScript.integrity = "sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe";
  jsScript.crossOrigin = "anonymous";

  head.append(cssLink);
  body.append(jsScript);
}

export async function addAnalyseButton() {
  const asset = await getAsset("search.svg");
  
  const articleTitle = document.querySelector("article h1") 
    || document.querySelector("main h1") 
    || document.querySelector("h1");

  const button = document.createElement("button");
  button.id = "btn-analyse"
  button.className = "btn";
  button.style.background = "#39444E";
  button.innerHTML = asset;

  articleTitle.prepend(button);
}

export function toogleAnalyseButtonLoading() {
  const button = getAnalyseButton();

  const isLoading  = button.className.includes("loading");

  if (isLoading) {
    getAsset("search.svg").then(asset => {
      button.innerHTML = asset
      button.className = "btn"
    });
  } else {
    button.className += " disabled loading"

    button.innerHTML = `
      <div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Carregando...</span>
      </div>
    `
  }
}

export function getAnalyseButton() {
  return document.getElementById("btn-analyse")
}


export function addAnalysisCard(isFake, analysis) {
  const status = isFake ? "danger" : "success";

  const card = `
    <div class="card border-${status} bg-light mb-3">
      <div class="card-header bg-${status}" style="display: flex; align-items: center; gap: 0.5rem;">
        <strong style="font-size: 1.5rem;">${isFake ? "Fake" : "Real"}</strong>
      </div>
      <div class="card-body">
        <p class="card-text" style="text-align: justify; font-weight: 450;">
          ${analysis}
        </p>
      </div>
    </div>
  `;
  
  const articleHeader = document.querySelector("article header");

  articleHeader.innerHTML += card;
}

