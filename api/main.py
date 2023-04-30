from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from services.analyse import analyse

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

  result = analyse(url)

  return jsonify(result)


if __name__ == "__main__":
  app.run()