import flask
from flask import current_app, request, jsonify, Response, stream_with_context

from algorithms.kmean.kmean import KMeanClusterer
from utils.preprocessor import Preprocessor
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
@app.route('/', methods=['GET'])
def home():
    return '''<h1>ML API</h1>
<p>This is the api for ML library.</p>'''

@app.route('/kmean', methods=['GET'])
def kmean():
    print("The request is: " + str(request.headers))
    numpy_data = Preprocessor.get_2d_data([[1,4],[2,5],[2,6],[3,5],[2,8]])
    kmean = KMeanClusterer(numpy_data)
    print(kmean)
    print(kmean.wcss())
    gen = kmean.stream()
    # # return gen
    # def generate ():
    #     import time
    #     import numpy as np
    #     for i in range(100):
    #         li = ['hello', 'how', 'are', 'you']
    #         yield li[int(np.random.randint(0,3))]
    # return Response(stream_with_context(generate()))
    return gen

app.run(debug=True, port=5000)