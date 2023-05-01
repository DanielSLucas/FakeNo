async function main() {
  const head = document.querySelector('head');

  const jsScript = document.createElement('script');
  jsScript.src = "http://localhost:5000/files/js/index.js";
  jsScript.type = "module";
  jsScript.crossOrigin = "anonymous";  

  head.append(jsScript)
}

chrome.tabs.onUpdated.addListener( (tabId, changeInfo, tab) => {
  if (changeInfo.status == 'complete' && tab.active) {
    chrome.scripting.executeScript({
      target: { tabId, },
      function: main,
    });
  }
});