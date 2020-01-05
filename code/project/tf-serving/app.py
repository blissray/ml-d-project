# load Flask
import flask
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import request

from datetime import datetime
import os

import tempfile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tempfile

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

CHECKPOINT_DIR = "checkpoints"
model_list = sorted([os.path.join(CHECKPOINT_DIR, filename)
                     for filename in os.listdir(CHECKPOINT_DIR)])

new_model = keras.models.load_model(model_list[-1])

# define a predict function as an endpoint
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            filename = os.path.join(
                    app.config['UPLOAD_FOLDER'], "%s.%s" % (
                        now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
                        file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            data = {"success": False}
            return flask.jsonify(data)

    # data = {"success": False}
    # # get the request parameters
    # params = flask.request.json
    # if (params == None):
    #     params = flask.request.args
    # # if parameters are found, echo the msg parameter 
    # if (params != None):
    #     data["response"] = params.get("msg")
    #     data["success"] = True
    # # return a response in json format 


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# start the flask app, allow remote connections
app.run(host='0.0.0.0', port="8000")
