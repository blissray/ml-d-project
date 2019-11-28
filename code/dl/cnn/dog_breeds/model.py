from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras import layers 
from tensorflow.keras.models import Model
import tensorflow as tf

class ResNet50ForDogBreed(Model):
    def __init__(self, input_shape =(224, 224,3), num_classes=120):
        # call the parent constructor
        super(ResNet50ForDogBreed, self).__init__()
        self.base_model = ResNet50(input_shape=input_shape, include_top=False, weights='imagenet')
        for layer in self.base_model.layers:
            layer.trainable = False

        self.flatten = tf.keras.layers.Flatten()
        self.dense_layer = tf.keras.layers.Dense(1024, activation=tf.nn.relu)
        self.dropout = tf.keras.layers.Dropout(0.5)
        self.last_layer = tf.keras.layers.Dense(num_classes, activation=tf.nn.softmax)

    def call(self, inputs, training=False):
        x = self.base_model(inputs)
        x = self.flatten(x)
        x = self.dense_layer(x)
        if training:
            x = self.dropout(x, training=training)
        return self.last_layer(x)


