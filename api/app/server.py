from flask import Flask
from flask_cors import CORS

server = Flask(__name__)
CORS(server)
