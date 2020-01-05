#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for, request
import requests
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            filename = os.path.join(app.config['UPLOAD_FOLDER'], "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            file.save(filename)

            url = 'http://estella.gachon.ac.kr:8000/predict'
            files = {'file': open(filename, 'rb')}

            r = requests.post(url, files=files)
            data = json.loads(r.text)

            return jsonify(data)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True)
