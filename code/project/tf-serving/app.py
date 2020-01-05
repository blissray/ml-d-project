# load Flask 
import flask
app = flask.Flask(__name__)

import tempfile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tempfile


CHECKPOINT_DIR = "checkpoints"
model_list = sorted([os.path.join(CHECKPOINT_DIR, filename)
    for filename in os.listdir(CHECKPOINT_DIR)])


new_model = keras.models.load_model(model_list[-1])
print(new_model.summary())


# define a predict function as an endpoint 
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success": False}
    # get the request parameters
    params = flask.request.json
    if (params == None):
        params = flask.request.args
    # if parameters are found, echo the msg parameter 
    if (params != None):
        data["response"] = params.get("msg")
        data["success"] = True
    # return a response in json format 
    return flask.jsonify(data)

# start the flask app, allow remote connections
app.run(host='0.0.0.0', port="8000")