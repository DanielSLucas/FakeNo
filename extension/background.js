async function isFakeNews() {
  if (document.querySelector("meta[property='og:type']")?.content !== "article") return;  

  const API_BASE_URL = "http://localhost:5000"
  const currentURL = window.location.href;
  
  const response = await fetch(`${API_BASE_URL}/fakenews/analyse`,{
    method: "POST",
    headers: {
      "Access-Control-Allow-Origin": "*/*",
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      url: currentURL,
      summarize: false,
    }),
  }).then(response => response.json())

  const isFake = !response.isReal;
  
  const assetName = isFake ? 'alert-circle.svg' : 'check-circle.svg';
  const asset = await fetch(`${API_BASE_URL}/assets/${assetName}`).then(res => res.text());
  
  const articleTitle = document.querySelector("article h1") 
    || document.querySelector("main h1") 
    || document.querySelector("h1");

  const spanElement = document.createElement("span");
  spanElement.innerHTML = asset;

  articleTitle.prepend(spanElement);  

  return;
}

chrome.tabs.onUpdated.addListener( (tabId, changeInfo, tab) => {
  if (changeInfo.status == 'complete' && tab.active) {
    chrome.scripting.executeScript({
      target: { tabId, },
      function: isFakeNews,
    });
  }
});