const API_BASE_URL = "http://localhost:5000";

export async function getAnalysis() {
  return fetch(`${API_BASE_URL}/fakenews/analyse`,{
    method: "POST",
    headers: {
      "Access-Control-Allow-Origin": "*/*",
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      url: window.location.href,      
    }),
  })  
}

export async function getAsset(assetName) {
  return fetch(`${API_BASE_URL}/files/assets/${assetName}`).then(res => res.text());
}
