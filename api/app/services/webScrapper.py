from app.services.baseService import BaseService
from app.models import Article
import newspaper

class WebScrapperService(BaseService):
  url = None
  article = None

  def __init__(self, url) -> None:
    super().__init__("WEB_SCRAPER")
    self.url = url

  def execute(self):
    self.get_article()
    self.result = self.article.__dict__
    return self.article

  def get_article(self):
    try:
      article = newspaper.Article(self.url, language='pt')
    
      article.download()
      article.parse()
      article.nlp()
      
      self.article = Article(
        title=article.title,
        authors=article.authors,
        publish_date=str(article.publish_date),
        content=article.summary,
        source=self.url
      ) 
    except:
      self.article = Article(
        title="Falha ao buscar informações no site",
        source=self.url
      )
