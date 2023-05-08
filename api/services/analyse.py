from services.webScrapper import get_article, to_gpt, to_fakeNo
from services import fakeNewsDetector
from services.gpt import get_google_query, mount_user_prompt, get_gpt_analysis
from services.googleUtils import google_search
from services.utils import get_host_from_url
import json

def analyse(url):
  article = get_article(url)
  yield json.dumps({"title": "ARTICLE", "result": article})

  google_query = get_google_query(to_gpt(article))
  yield json.dumps({"title": "GOOGLE_QUERY", "result": google_query})

  google_search_results = google_search(google_query, 3, get_host_from_url(url))
  google_search_results_articles = [to_gpt(get_article(result_url)) for result_url in google_search_results]

  labeled_google_results = [f"# Resultado {i+1}:\n{article}" for i, article in enumerate(google_search_results_articles)]
  google_results_str = "\n\n".join(labeled_google_results)
  yield json.dumps({"title": "GOOGLE_SEARCH_RESULTS", "result": google_search_results_articles})

  isFake = fakeNewsDetector.isFake(to_fakeNo(article))
  fakeNo_prediction = "Fake" if isFake else "Real"
  yield json.dumps({"title": "FAKENO_AI_PREDICTION", "result": fakeNo_prediction})

  user_prompt = mount_user_prompt(to_gpt(article), fakeNo_prediction, google_results_str)
  gpt_analysis = get_gpt_analysis(user_prompt)
  yield json.dumps({"title": "GPT_ANALYSIS", "result": gpt_analysis})
