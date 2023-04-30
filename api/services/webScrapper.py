import newspaper

def get_article(url):
  try:
    article = newspaper.Article(url, language='pt')
  
    article.download()
    article.parse()
    article.nlp()
    
    return make_article(
      title=article.title,
      authors=article.authors,
      publish_date=str(article.publish_date),
      content=article.summary,
      source=url
    ) 
  except:
    return make_article(
      title="Falha ao buscar informações no site",
      source=url
    )

def make_article(title: str = "", authors: list = [], publish_date: str = "", content: str = "", source: str = ""):
  return {
    "title": title,
    "authors": ' '.join(authors),
    "publish_date": publish_date,
    "content": content,
    "source": source
  }

def to_gpt(article):
  title = "Título: " + article.get("title", "")
  authors = "Autor(es): " + article.get("authors", "")
  publish_date = "Date de publicação: " + article.get("publish_date", "")
  content = "Resumo: " + article.get("content", "")
  source = "Fonte: " + article.get("source", "")

  return "\n".join([title, authors, publish_date, content, source])

def to_fakeNo(article):
  title = article.get("title", "")
  authors = article.get("authors", "")
  content = "Resumo: " + article.get("content", "")

  return f"{title} {authors} {content}"