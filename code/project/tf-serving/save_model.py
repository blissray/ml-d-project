import tempfile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tempfile

import os

def _number_of_files(dir_path):
    file_counter = 0
    for dir_name in os.listdir(dir_path):
        file_counter += len(list(os.listdir(os.path.join(dir_path, dir_name))))
    return file_counter

def _make_generator(train, dataset_path, 
                    target_size = (224,224), batch_size=512):
    if train:
        datagen = ImageDataGenerator(
                    shear_range=0.2,
                    zoom_range=0.2,
                    horizontal_flip=True)
    else:
        datagen = ImageDataGenerator()
    generator = datagen.flow_from_directory(
            dataset_path,
            target_size=target_size, class_mode='sparse', batch_size=32, shuffle=True)
    return generator 


CHECKPOINT_DIR = "checkpoints"
model_list = sorted([os.path.join(CHECKPOINT_DIR, filename)
    for filename in os.listdir(CHECKPOINT_DIR)])


new_model = keras.models.load_model(model_list[-1])
print(new_model.summary())

DATA_DIR = "data"
VAL = "val"
val_path = os.path.join(DATA_DIR, VAL)

batch_size =512

number_of_val_files = _number_of_files(val_path)
STEP_SIZE_VALID= number_of_val_files // batch_size

eval_generator = _make_generator(train=False, dataset_path=val_path, batch_size=batch_size)


loss, acc = new_model.evaluate_generator(
    eval_generator, verbose=2)
print("복원된 모델의 정확도: {:5.2f}%".format(100*acc))

MODEL_DIR = tempfile.gettempdir()

version = 1
export_path = os.path.join(MODEL_DIR, str(version))
print('export_path = {}\n'.format(export_path))
if os.path.isdir(export_path):
  print('\nAlready saved a model, cleaning up\n')
  os.rmdir(export_path)

tf.saved_model.save(
    keras.backend.get_session(),
    export_path,
    inputs={'input_image': new_model.input},
    outputs={t.name:t for t in new_model.outputs})

print('\nSaved model:')
print(os.listdir(export_path))