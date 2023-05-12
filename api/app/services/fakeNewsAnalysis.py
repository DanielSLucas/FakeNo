from app.services.baseService import BaseService
from app.services.webScrapper import WebScrapperService
from app.services.fakenoAI import FakeNoAIService
import app.services.gpt as gpt
from app.services.google import GoogleSearchService, GoogleSearchResultsFormatterService
from app.utils import get_host_from_url, mount_gpt_input

class FakeNewsAnalysisService(BaseService):
  url = None

  def __init__(self, url) -> None:
    super().__init__("FAKE_NEWS_ANALYSIS")
    self.url = url
  
  def execute(self):
    web_scrapper_service = WebScrapperService(self.url)
    article = web_scrapper_service.execute()
    yield web_scrapper_service.to_json()

    get_google_query_service = gpt.GetGoogleQueryService(article.to_gpt())
    google_query = get_google_query_service.execute()
    yield get_google_query_service.to_json()

    google_search_service = GoogleSearchService(google_query, get_host_from_url(self.url))
    google_search_results = google_search_service.execute()
    yield google_search_service.to_json()

    search_results_formatter_service = GoogleSearchResultsFormatterService(google_search_results)
    google_results_formatted = search_results_formatter_service.execute()
    yield search_results_formatter_service.to_json()

    fakeNo_ai_service = FakeNoAIService(article.to_fakeNo())
    fakeNo_prediction = fakeNo_ai_service.execute()
    yield fakeNo_ai_service.to_json()

    gpt_input = mount_gpt_input(article.to_gpt(), fakeNo_prediction, google_results_formatted)
    get_analysis_service = gpt.GetAnalysisService(gpt_input)
    gpt_analysis = get_analysis_service.execute()
    yield get_analysis_service.to_json()

    self.result = gpt_analysis
    
    return gpt_analysis
