from os import getenv
from googleapiclient.discovery import build

google_api_key = getenv("GOOGLE_API_KEY")
google_custom_search_engine_id = getenv("CUSTOM_SEARCH_ENGINE_ID")

def google_search(query: str, num_results: int, url_to_exclude: str):
  service = build("customsearch", "v1", developerKey=google_api_key)

  result = (
    service.cse()
    .list(
      q=query, 
      cx=google_custom_search_engine_id,
      num=num_results,
      siteSearch=url_to_exclude,
      siteSearchFilter="e"
    )
    .execute()
  )

  search_results = result.get("items", [])

  search_results_urls = [search_result["link"] for search_result in search_results]

  return search_results_urls
