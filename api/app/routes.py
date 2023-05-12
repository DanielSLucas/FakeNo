from app.server import server
from flask import request, jsonify, send_from_directory, Response

from app.services.fakeNewsAnalysis import FakeNewsAnalysisService


@server.route("/", methods=["GET"])
def healthyCheck():
  return jsonify({
    "message": "API is working"
  })


@server.route('/files/<folder>/<filename>')
def getAsset(folder, filename):
  return send_from_directory(f"../public/{folder}", filename)


@server.route("/fakenews/analyse", methods=['POST'])
def analyseNewsArticle():
  body = request.json

  url = body['url']

  fake_news_analysis_serice = FakeNewsAnalysisService(url)

  return Response(fake_news_analysis_serice.execute(), mimetype="application/json")
