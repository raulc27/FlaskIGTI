from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "API funcionando...", 200

app.run(port=5000, debug=True)