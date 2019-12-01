from tensorflow.keras.applications.vgg16  import VGG16
from tensorflow.keras.applications.resnet50  import ResNet50

from tensorflow.keras import layers 
from tensorflow.keras.models import Model
import tensorflow as tf

class VGG16ForDogBreed(Model):
    def __init__(self, input_shape =(224, 224,3), num_classes=120):
        # call the parent constructor
        super(VGG16ForDogBreed, self).__init__()
        self.base_model = VGG16(input_shape=input_shape, include_top=False, weights="imagenet")
        for layer in self.base_model.layers:
            layer.trainable = False

        self.flatten = tf.keras.layers.Flatten()
        self.dense_layer = tf.keras.layers.Dense(512, activation=tf.keras.activations.linear)
        self.batch_layer = tf.keras.layers.BatchNormalization()
        self.relu_layer = tf.keras.layers.Activation('relu')
        
        self.last_layer = tf.keras.layers.Dense(num_classes, activation=tf.nn.softmax)

    def call(self, inputs, training=False):
        x = self.base_model(inputs)
        x = self.flatten(x)
        x = self.dense_layer(x)
        x = self.batch_layer(x)
        x = self.relu_layer(x)
        return self.last_layer(x)

    def get_config(self):
        config = {'name': self.__class__.__name__, 
            'base_model': self.base_model.get_config(),
            'flatten': self.flatten,
            'dense_layer': self.dense_layer,
            'batch_layer': self.batch_layer,
            'relu_layer': self.relu_layer,
            'last_layer': self.last_layer
        }
        
        return list(config.items())

class ResNet50ForDogBreed(Model):
    def __init__(self, input_shape =(224, 224,3), num_classes=120):
        # call the parent constructor
        super(ResNet50ForDogBreed, self).__init__()
        self.base_model = ResNet50(input_shape=input_shape, include_top=False, weights="imagenet")
        for layer in self.base_model.layers:
            layer.trainable = False

        self.flatten = tf.keras.layers.Flatten()
        self.dense_layer = tf.keras.layers.Dense(512, activation=tf.keras.activations.linear)
        self.batch_layer = tf.keras.layers.BatchNormalization()
        self.relu_layer = tf.keras.layers.Activation('relu')
        
        self.last_layer = tf.keras.layers.Dense(num_classes, activation=tf.nn.softmax)

    def call(self, inputs, training=False):
        x = self.base_model(inputs)
        x = self.flatten(x)
        x = self.dense_layer(x)
        x = self.batch_layer(x)
        x = self.relu_layer(x)
        return self.last_layer(x)

    def get_config(self):
        config = {'name': self.__class__.__name__, 
            'base_model': self.base_model.get_config(),
            'flatten': self.flatten,
            'dense_layer': self.dense_layer,
            'batch_layer': self.batch_layer,
            'relu_layer': self.relu_layer,
            'last_layer': self.last_layer
        }

        return list(config.items()))
