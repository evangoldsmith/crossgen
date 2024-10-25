from flask import Flask
import datetime

from engine.generator import Board

x = datetime.datetime.now()
app = Flask(__name__)

@app.route("/")
def index():
    return "CrossGen API is running!"

@app.route("/generate")
def generate():
    crossword = Board(difficulty=0, useLLM=True)
    crossword.generate()

    return crossword.get_json()

