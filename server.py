from flask import Flask, jsonify
import emobot

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world'

@app.route('/<text>')
def process(text):
    return jsonify(emobot.eval_emotion('text', text))

if __name__ == '__main__':
    app.run(debug=True)
