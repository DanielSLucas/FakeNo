class Article:
  title = None
  authors = None
  publish_date = None
  content = None
  source = None
  
  def __init__(self, title: str = "", authors: list = [], publish_date: str = "", content: str = "", source: str = "") -> None:
    self.title = title
    self.authors = ' '.join(authors)
    self.publish_date = publish_date
    self.content = content
    self.source = source
  
  def to_gpt(self):
    title = "Título: " + self.title
    authors = "Autor(es): " + self.authors
    publish_date = "Date de publicação: " + self.publish_date
    content = "Resumo: " + self.content
    source = "Fonte: " + self.source

    return "\n".join([title, authors, publish_date, content, source])

  def to_fakeNo(self):
    title = self.title
    authors = self.authors
    content = "Resumo: " + self.content

    return f"{title} {authors} {content}"

  def __str__(self) -> str:
    return self.to_gpt()
