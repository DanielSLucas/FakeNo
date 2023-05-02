async function main() {
  const head = document.querySelector('head');

  const cssStyle = document.createElement('link');
  cssStyle.href = "http://localhost:5000/files/styles/styles.css";
  cssStyle.rel = "stylesheet";
  cssStyle.crossOrigin = "anonymous";

  const jsScript = document.createElement('script');
  jsScript.src = "http://localhost:5000/files/js/index.js";
  jsScript.type = "module";
  jsScript.crossOrigin = "anonymous";

  head.append(cssStyle, jsScript);
}

chrome.tabs.onUpdated.addListener( (tabId, changeInfo, tab) => {
  if (changeInfo.status == 'complete' && tab.active) {
    chrome.scripting.executeScript({
      target: { tabId, },
      function: main,
    });
  }
});