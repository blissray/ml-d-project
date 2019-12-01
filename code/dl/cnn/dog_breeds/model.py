from tensorflow.keras.applications.vgg16  import VGG16
from tensorflow.keras.applications.resnet50  import ResNet50

from tensorflow.keras import layers 
from tensorflow.keras.models import Model
import tensorflow as tf

def VGG16ForDogBreed(input_shape =(224, 224,3), num_classes=120):
    base_model = VGG16(input_shape=input_shape, 
                    include_top=False, weights="imagenet")
    for layer in base_model.layers:
        layer.trainable = False

    model = tf.keras.Sequential([
        base_model,
        layers.Flatten(),
        layers.Dense(512, activation=tf.keras.activations.linear),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dense(num_classes, activation=tf.nn.softmax)
    ])

    return model

def ResNet50ForDogBreed(input_shape =(224, 224,3), num_classes=120):
    base_model = ResNet50(input_shape=input_shape, 
                    include_top=False, weights="imagenet")
    for layer in base_model.layers:
        layer.trainable = False

    model = tf.keras.Sequential([
        base_model,
        layers.Flatten(),
        layers.Dense(512, activation=tf.keras.activations.linear),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dense(num_classes, activation=tf.nn.softmax)
    ])

    return model