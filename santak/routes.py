from flask import request, Response, jsonify
from santak import app
from PIL import Image
import numpy as np
from santak.matching import match

@app.route("/")
def index():
    return "test index page"

@app.route("/img_debug", methods=["POST"])
def img_debug():
    img = Image.open(request.files['image'].stream)

    return jsonify({'msg': 'success', 'size': [img.width, img.height]})

@app.route("/match", methods=["POST"])
def match_img():

    img = np.array(Image.open(request.files['image'].stream))

    n_matches = request.args.get("num", default=5, type=int)

    matches = match(img, n_matches=n_matches)

    return jsonify({'msg': 'success', 'matches': matches})


