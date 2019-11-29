from model import ResNet50ForDogBreed
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

from absl import app
from absl import flags

def _make_generator(train, dataset_path, 
                    target_size = (224,224), batch_size=32):
    if train:
        datagen = ImageDataGenerator(
                    shear_range=0.2,
                    zoom_range=0.2,
                    horizontal_flip=True,
                    rescale=1. / 255)
    else:
        datagen = ImageDataGenerator(rescale=1. / 255)
    generator = datagen.flow_from_directory(
            dataset_path,
            target_size=target_size, class_mode='sparse', batch_size=32, shuffle=True)
    return generator 

def main(args):
    model = ResNet50ForDogBreed()

    loss_object = losses.SparseCategoricalCrossentropy()
    learning_rate = 0.5
    beta_1 = 0.9
    beta_2 = 0.99
    epsilon = 0.00001
    epochs = 100

    optimizer = optimizers.Adam(learning_rate, beta_1, beta_2, epsilon)

    model.compile(loss=loss_object,
              optimizer=optimizer,
              metrics=['accuracy'])
    DATA_DIR = "data"
    TRAIN = "train"
    VAL = "val"
    train_path = os.path.join(DATA_DIR, TRAIN) 
    val_path = os.path.join(DATA_DIR, VAL) 

    train_generator = _make_generator(train=True, dataset_path=train_path)
    val_generator = _make_generator(train=False, dataset_path=val_path)
   
    STEP_SIZE_TRAIN= 30802 // 32
    STEP_SIZE_VALID= 8058 // 32 


    model.fit_generator(
        train_generator,
        steps_per_epoch=STEP_SIZE_TRAIN,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=STEP_SIZE_VALID)
    model.save_weights('first_try.h5')  # always save your weights after training or during training

if __name__ == '__main__':
  app.run(main)




    # from tensorflow.keras.callbacks import EarlyStopping
    # early_stopping = EarlyStopping(patience=10, restore_best_weights=True, monitor="val_accuracy")


    #model.fit(dataset, epochs=epochs)

