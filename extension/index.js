const mainElement = document.querySelector("main");
const button = document.querySelector("button");


async function isFakeNews() {
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
  
  if (isFake) {
    const articleHeader = document.querySelector("h1").parentElement;

    articleHeader.style = "display: flex; align-items: center;"

    const imgElement = document.createElement("img");

    imgElement.src = `${API_BASE_URL}/assets/alert-circle.png`;
    imgElement.alt = `Alerta de fake news`
    imgElement.ariaLabel = "Possivelmente fake!"    

    articleHeader.append(imgElement);
  }

  return;
}

button.addEventListener("click", async () => {  
  const [tab] = await chrome.tabs.query(({
    active: true,
    currentWindow: true,
  }));

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: isFakeNews,
  });
});