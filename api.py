from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from algoritmo import cross_point

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-population', methods=['GET'])
def generate():
    resultados = cross_point.algoritmo_genetico_json([-10, 10], pop_size=4, generaciones=10, bits=5)
    data = {
        "code": 200,
        "data": resultados
    }
    return jsonify(data)


app.run('0.0.0.0', port=8000, debug=True)