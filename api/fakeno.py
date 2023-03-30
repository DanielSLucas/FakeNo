from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd 
import newspaper
import pickle
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')

model = pickle.load(open("lrModel", "rb"))
vectorizer = pickle.load(open("vectorizer", "rb"))
porter_stemmer = PorterStemmer()

app = Flask(__name__)

CORS(app)

@app.route("/", methods=["GET"])
def healthyCheck():
  return jsonify({
    "message": "API is working"
  })

@app.route('/assets/<filename>')
def getAsset(filename):
  return send_from_directory('assets', filename)

@app.route("/fakenews/analyse", methods=['POST'])
def analyseNewsArticle():
  body = request.json

  url = body['url']
  summarize = body['summarize']

  article = getNewsArticle(url, summarize)
  serializedArticle = serializeArticle(article)

  isReal = bool(model.predict(serializedArticle)[0])

  return jsonify({ "isReal": isReal })

def getNewsArticle(url, summarize): 
  article = newspaper.Article(url, language='pt')
  
  article.download()
  article.parse()

  if(summarize):
    article.nlp()
    return article.summary

  return article.title +' '+' '.join(article.authors)+' '+article.text

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


if __name__ == "__main__":
  app.run()