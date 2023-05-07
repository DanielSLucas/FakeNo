from urllib.parse import urlparse

def get_host_from_url(url):
  parsed_url = urlparse(url)
  return parsed_url.netloc