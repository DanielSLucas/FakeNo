import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd 
import newspaper
import pickle
import re

nltk.download('stopwords')
nltk.download('punkt')

model = pickle.load(open("lrModel", "rb"))
vectorizer = pickle.load(open("vectorizer", "rb"))

porter_stemmer = PorterStemmer()

def isFake(url): 
  article = getNewsArticle(url, True)
  print(article)
  serializedArticle = serializeArticle(article)

  isReal = bool(model.predict(serializedArticle)[0])

  return not isReal


def getNewsArticle(url, summarize): 
  article = newspaper.Article(url, language='pt')
  
  article.download()
  article.parse()

  if(summarize):
    article.nlp()
    return f"{article.title} {' '.join(article.authors)} {article.summary}"
    
  return f"{article.title} {' '.join(article.authors)} {article.text}"


def serializeArticle(article):
  sampleDf = pd.DataFrame({ "features": [article] })
  sampleDf["features"] = sampleDf["features"].apply(stemming_tokenizer)

  serializedArticle = vectorizer.transform(sampleDf["features"].values)

  return serializedArticle


def stemming_tokenizer(df):
  words = re.sub(r"[^A-Za-z0-9]", " ", df).lower().split()
  words = [porter_stemmer.stem(word) for word in words if not words in stopwords.words('portuguese')]
  words = ' '.join(words)

  return words