import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
# from tensorflow.keras.applications import VGG16




def model(input_shape = (255,255, 3), number_of_labels = 121):

    base_model = tf.keras.applications.ResNet50(
        weights='imagenet', include_top=False, input_shape=input_shape)

    for layer in base_model.layers:
        layer.trainable = False

    model = Sequential()
    model.add(base_model )
    model.add(
      layers.Flatten())
    model.add(layers.Dense(512, activation="sigmoid"))
    model.add(layers.Dense(number_of_labels, activation="softmax"))

    return model




    
