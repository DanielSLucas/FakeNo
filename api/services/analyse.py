from services.webScrapper import get_article, to_gpt, to_fakeNo
from services import fakeNewsDetector
from services.gpt import get_google_query, mount_user_prompt, get_gpt_analysis
from services.googleUtils import google_search


def analyse(url):
  article = get_article(url)

  google_query = get_google_query(to_gpt(article))

  google_search_results = google_search(google_query, 3, url)
  google_search_results_articles = [to_gpt(get_article(result_url)) for result_url in google_search_results]

  labeled_google_results = [f"# Resultado {i+1}:\n{article}" for i, article in enumerate(google_search_results_articles)]
  google_results_str = "\n\n".join(labeled_google_results)

  isFake = fakeNewsDetector.isFake(to_fakeNo(article))
  fakeNo_prediction = "Fake" if isFake else "Real"

  user_prompt = mount_user_prompt(article, fakeNo_prediction, google_results_str)
  gpt_analysis = get_gpt_analysis(user_prompt)

  return {
    "isFake": isFake,
    "analysis": gpt_analysis,
    "analysis_steps": [
      {"title": "Buscar conteúdo da url", "result": article},
      {"title": "Criar texto para buscar no google", "result": google_query},
      {"title": "Resultado da busca no google", "result": google_search_results_articles},
      {"title": "Predição da FakeNo-AI", "result": fakeNo_prediction},
      {"title": "Formatar prompt do usuário", "result": user_prompt},
      {"title": "Análise do gpt", "result": gpt_analysis},
    ]
  }