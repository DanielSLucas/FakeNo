from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from services.analyse import analyse

app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def healthyCheck():
  return jsonify({
    "message": "API is working"
  })


@app.route('/files/<folder>/<filename>')
def getAsset(folder, filename):
  return send_from_directory(f"public/{folder}", filename)


@app.route("/fakenews/analyse", methods=['POST'])
def analyseNewsArticle():
  body = request.json

  url = body['url']  

  return Response(analyse(url), mimetype="application/json")

if __name__ == "__main__":
  app.run()