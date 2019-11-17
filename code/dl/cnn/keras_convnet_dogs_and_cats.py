import os, shutil
import pandas as pd
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras import models
from tensorflow.keras import layers


def build_label(dataset):
  return [1 if "dog" in filename else 0 for filename in dataset ]


original_dataset_dir = './dataset/dogs_and_cats'
train_dir = os.path.join(original_dataset_dir, "train")
filenames = [filename for filename in os.listdir(train_dir)] 

from random import shuffle
shuffle(filenames)

train_set = filenames[:20000]
validation_set = filenames[20000:22500]
test_set = filenames[22500:]

train_label = build_label(train_set)
validation_label = build_label(validation_set)
test_label = build_label(test_set)

train_df = pd.DataFrame({"filename": train_set, "class": train_label})
validation_df = pd.DataFrame({"filename": validation_set, "class": validation_label})
test_df = pd.DataFrame({"filename": test_set, "class": test_label})

# 포인트 keras image 전처리 데이터 셋 확인하기

from tensorflow.keras.preprocessing.image import ImageDataGenerator
image_generator = ImageDataGenerator(
    rescale=1./255)
train_datagenerator = image_generator.flow_from_dataframe(
  train_df, train_dir, target_size=(150,150),batch_size=200, class_mode='binary')
validation_datagenerator = image_generator.flow_from_dataframe(
  validation_df, train_dir, target_size=(150,150),batch_size=50, class_mode='binary')
test_datagenerator = image_generator.flow_from_dataframe(
  test_df, train_dir, target_size=(150,150),batch_size=50, class_mode='binary')



model = models.Sequential()
model.add(
  layers.Conv2D(
      32,(3,3), activation='relu', input_shape=(150,150,3)))
model.add(
  layers.MaxPooling2D((2,2)))

model.add(
  layers.Conv2D(
      64,(3,3), activation='relu'))
model.add(
  layers.MaxPooling2D((2,2)))

model.add(
  layers.Conv2D(
      128,(3,3), activation='relu'))
model.add(
  layers.MaxPooling2D((2,2)))

model.add(
  layers.Flatten())
model.add(layers.Dense(512, activation="relu"))
model.add(layers.Dense(1, activation="sigmoid"))

model.compile(loss='binary_crossentropy',
             optimizer=optimizers.RMSprop(lr=1e-4),
             metrics=['acc'])

from tensorflow.keras.callbacks import ModelCheckpoint

filepath="weights.basic.best.h5"

checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

history = model.fit_generator(
    train_datagenerator, 
    steps_per_epoch=100,
    epochs=30,
    validation_data=validation_datagenerator,
    callbacks=callbacks_list,
    validation_steps=50)

# Save the weights
model.save_weights('base_model_weights_dogs_and_cats.h5')

# Save the model architecture
with open('base_model_dogs_and_cats.json', 'w') as f:
    f.write(model.to_json())

model.load_weights('weights.basic.best.h5')

score = model.evaluate_generator(
    test_datagenerator, workers=12)
print("Loss: ", score[0], "Accuracy: ", score[1])

