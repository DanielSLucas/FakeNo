import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd 
import pickle
import re

nltk.download('stopwords')
nltk.download('punkt')

fakeNo = pickle.load(open("lrModel", "rb"))
vectorizer = pickle.load(open("vectorizer", "rb"))

porter_stemmer = PorterStemmer()

def isFake(article): 
  fakeNo_input = to_fakeNo_input(article)

  isReal = bool(fakeNo.predict(fakeNo_input)[0])

  return not isReal


def to_fakeNo_input(article):
  sampleDf = pd.DataFrame({ "features": [article] })
  sampleDf["features"] = sampleDf["features"].apply(stemming_tokenizer)

  return vectorizer.transform(sampleDf["features"].values)  


def stemming_tokenizer(df):
  words = re.sub(r"[^A-Za-z0-9]", " ", df).lower().split()
  words = [porter_stemmer.stem(word) for word in words if not words in stopwords.words('portuguese')]
  words = ' '.join(words)

  return words