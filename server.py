import flask
from flask import current_app, request, jsonify

from algorithms.kmean.kmean import KMeanClusterer
from utils.preprocessor import Preprocessor

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>ML API</h1>
<p>This is the api for ML library.</p>'''

@app.route('/kmean', methods=['POST'])
def kmean():
    
    numpy_data = Preprocessor.get_2d_data(request)
    KMeanClusterer(numpy_data)
    return "Ler Lew"

app.run(debug=True, port=5000)