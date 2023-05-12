import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd 
import pickle
import re

from app.services.baseService import BaseService

nltk.download('stopwords')
nltk.download('punkt')

class FakeNoAIService(BaseService):
  fakeNo = pickle.load(open("lrModel", "rb"))
  vectorizer = pickle.load(open("vectorizer", "rb"))
  porter_stemmer = PorterStemmer()
  news_article = None
  isFake = None

  def __init__(self, news_article) -> None:
    super().__init__("FAKENO_AI")
    self.news_article = news_article

  def execute(self):
    self.check_news_article()
    self.result = "Fake" if self.isFake else "Real"
    return self.result

  def check_news_article(self): 
    self.parse_news_article()

    self.isFake = not bool(self.fakeNo.predict(self.news_article)[0])    

  def parse_news_article(self):
    df = pd.DataFrame({ "features": [self.news_article] })
    df["features"] = df["features"].apply(self.stemming_tokenizer)

    self.news_article = self.vectorizer.transform(df["features"].values)  

  def stemming_tokenizer(self, text):
    words = re.sub(r"[^A-Za-z0-9]", " ", text).lower().split()
    words = [self.porter_stemmer.stem(word) for word in words if not words in stopwords.words('portuguese')]
    words = ' '.join(words)

    return words