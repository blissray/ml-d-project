from model import ResNet50ForDogBreed
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

from absl import app
from absl import flags

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

def _make_optimizer():
    learning_rate = 0.01
    beta_1 = 0.9
    beta_2 = 0.99
    epsilon = 0.0000001
    optimizer = optimizers.Adam(learning_rate, beta_1, beta_2, epsilon)
    return optimizer

def _number_of_files(dir_path):
    file_counter = 0
    for dir_name in os.listdir(dir_path):
        file_counter += len(list(os.listdir(os.path.join(dir_path, dir_name))))
    return file_counter

def main(args):
    model = ResNet50ForDogBreed(input_shape=(224,224,3))
    optimizer = _make_optimizer()
    model.compile(loss="sparse_categorical_crossentropy",
              optimizer=optimizer,
              metrics=['accuracy'])
    DATA_DIR = "data"
    TRAIN = "train"
    VAL = "val"
    train_path = os.path.join(DATA_DIR, TRAIN) 
    val_path = os.path.join(DATA_DIR, VAL) 
    
    number_of_train_files = _number_of_files(train_path)
    number_of_val_files = _number_of_files(val_path)
    
    batch_size =512
    epochs = 500

    train_generator = _make_generator(train=True, dataset_path=train_path, target_size = (224,224), batch_size=batch_size)
    val_generator = _make_generator(train=False, dataset_path=val_path, batch_size=batch_size)

    STEP_SIZE_TRAIN= number_of_train_files // batch_size
    STEP_SIZE_VALID= number_of_val_files // batch_size


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

