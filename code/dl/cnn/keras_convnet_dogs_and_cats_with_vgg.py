import os, shutil
import pandas as pd
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.applications import VGG16


def build_label(dataset):
  return [1 if "dog" in filename else 0 for filename in dataset ]

conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(150,150,3))

original_dataset_dir = './dataset/dogs_and_cats'
train_dir = os.path.join(original_dataset_dir, "train")
filenames = [filename for filename in os.listdir(train_dir)] 

from random import shuffle
shuffle(filenames)

train_set = filenames[:20000]
validation_set = filenames[20000:]

train_label = build_label(train_set)
validation_label = build_label(validation_set)

train_df = pd.DataFrame({"filename": train_set, "class": train_label})
validation_df = pd.DataFrame({"filename": validation_set, "class": validation_label})

# 포인트 keras image 전처리 데이터 셋 확인하기
from tensorflow.keras.preprocessing.image import ImageDataGenerator
aug_generator = ImageDataGenerator(
    rescale=1./255, rotation_range=40, width_shift_range=0.2,
    height_shift_range=0.2, shear_range=0.2, zoom_range=0.2,
    horizontal_flip=True, fill_mode='nearest')
image_generator = ImageDataGenerator(
    rescale=1./255)
train_datagenerator = aug_generator.flow_from_dataframe(
  train_df, train_dir, target_size=(150,150),batch_size=20, class_mode='binary')
validation_datagenerator = image_generator.flow_from_dataframe(
  validation_df, train_dir, target_size=(150,150),batch_size=20, class_mode='binary')

conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(150,150,3))
conv_base.trainalbe= False 
model = models.Sequential()
model.add(conv_base)
model.add(
  layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(512, activation="relu"))
model.add(layers.Dense(1, activation="sigmoid"))
model.compile(loss='binary_crossentropy',
             optimizer=optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-5, decay=0.0, amsgrad=False),
             metrics=['acc'])


from tensorflow.keras.callbacks import ModelCheckpoint

filepath="weights.best.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

history = model.fit_generator(
    train_datagenerator, 
    steps_per_epoch=1000,
    epochs=100,
    validation_data=validation_datagenerator,
    callbacks=callbacks_list,
    validation_steps=250)

# Save the weights
model.save_weights('model_weights.h5')


with open('model_architecture.json', 'w') as f:
    f.write(model.to_json())


