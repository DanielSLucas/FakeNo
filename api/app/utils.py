from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from app.services.webScrapper import WebScrapperService

def get_host_from_url(url):
  parsed_url = urlparse(url)
  return parsed_url.netloc

def mount_gpt_input(text, ai_prediction, google_results):
  return '\n\n'.join([
    f"Texto: {text}",
    f"FakeNo-AI: {ai_prediction}",
    f"Google: {google_results}"
  ])

def execute_in_parallel(input_list, function):
  with ThreadPoolExecutor() as executor:
    results = executor.map(function, input_list)
  return list(results)

def get_article(url):
  return WebScrapperService(url).execute()

