from os import getenv
from googleapiclient.discovery import build

from app.services.baseService import BaseService
from app.utils import execute_in_parallel, get_article

google_api_key = getenv("GOOGLE_API_KEY")
google_custom_search_engine_id = getenv("CUSTOM_SEARCH_ENGINE_ID")

class GoogleSearchService(BaseService):
  query = None
  url_host_to_exclude = None
  num_results = None
  search_results = None

  def __init__(self, query, url_host_to_exclude, num_results = 3) -> None:
    super().__init__("GOOGLE_SEARCH")
    self.query = query
    self.url_host_to_exclude = url_host_to_exclude
    self.num_results = num_results
  
  def execute(self):
    self.google_search()
    self.get_urls()
    self.get_articles()

    self.result = [rst.__dict__ for rst in self.search_results]

    return self.search_results
  
  def google_search(self):
    service = build("customsearch", "v1", developerKey=google_api_key)

    result = (
      service.cse()
      .list(
        q=self.query, 
        cx=google_custom_search_engine_id,
        num=self.num_results,
        siteSearch=self.url_host_to_exclude,
        siteSearchFilter="e"
      )
      .execute()
    )

    self.search_results = result

  def get_urls(self):
    search_results = self.search_results.get("items", [])
    self.search_results = [
      search_result["link"] for search_result in search_results
    ]
  
  def get_articles(self):
    self.search_results = execute_in_parallel(
      input_list=self.search_results,
      function=get_article
    )

class GoogleSearchResultsFormatterService(BaseService):
  search_result_articles = None

  def __init__(self, search_result_articles) -> None:
    super().__init__("GOOGLE_SEARCH_RESULTS_FORMATTER")
    self.search_result_articles = search_result_articles

  def execute(self):
    self.parse_to_gpt()
    self.label_results()
    self.join_labeled_results()
    
    self.result = self.search_result_articles
    return self.search_result_articles
  
  def parse_to_gpt(self):
    self.search_result_articles = [art.to_gpt() for art in self.search_result_articles]

  def label_results(self):
    self.search_result_articles = [
      f"# Resultado {i+1}:\n{article}" for i, article in enumerate(self.search_result_articles)
    ]
  
  def join_labeled_results(self):
    self.search_result_articles = "\n\n".join(self.search_result_articles)

    