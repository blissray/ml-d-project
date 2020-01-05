from model import ResNet50ForDogBreed
from model import VGG16ForDogBreed

from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import callbacks


import os
from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("model_name", "VGG16",
                     "Choose the model name - VGG16 or ResNet50")
flags.DEFINE_float("learning_rate", 0.01,
                     "Input a learning rate for your optimizer")
flags.DEFINE_string("optimizer", "adam",
                     "Choose the optimizer - SGD, RMSProp, ADAM")

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
    learning_rate = FLAGS.learning_rate
    if FLAGS.optimizer.lower() == "sgd":
        optimizer = optimizers.SGD(
            learning_rate)
    if FLAGS.optimizer.lower() == "rmsprop":
        optimizer = optimizers.RMSProp(
            learning_rate)
    if FLAGS.optimizer.lower() == "adam":    
        beta_1 = 0.9
        beta_2 = 0.99
        epsilon = 0.0000001
        optimizer = optimizers.Adam(
            learning_rate, beta_1, beta_2, epsilon)
    return optimizer

def _number_of_files(dir_path):
    file_counter = 0
    for dir_name in os.listdir(dir_path):
        file_counter += len(list(os.listdir(os.path.join(dir_path, dir_name))))
    return file_counter

def main(args):
    if FLAGS.model_name == "VGG16":
        model = VGG16ForDogBreed(input_shape=(224,224,3))
    if FLAGS.model_name == "ResNet50":
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


    CHECKPOINT_DIR = "checkpoints"
    if os.path.exists(CHECKPOINT_DIR) is not True:
        os.mkdir(CHECKPOINT_DIR)

    import json
    with open('download_conf.json') as json_file:
        download_conf = json.load(json_file)
    
    model_info = "{0}/model-{1}_optimizer-{2}_dataset-{3}".format(
        CHECKPOINT_DIR, FLAGS.model_name, FLAGS.optimizer, 
        download_conf["dataset"]
    )
    csv_logger = callbacks.CSVLogger(
        '{0}_{1}_training.log'.format(FLAGS.model_name, download_conf["dataset"]))
    checkpointer = callbacks.ModelCheckpoint(
        filepath= model_info+'_{epoch:03d}_{val_accuracy:.2f}_{val_loss:.2f}.hdf5',
        monitor='val_loss', 
        verbose=1, save_best_only=True)
    
    callbacks_list = [csv_logger, checkpointer]

    MODEL_REPOSITORY_DIR = "models"
    if os.path.exists(MODEL_REPOSITORY_DIR) is not True:
        os.mkdir(MODEL_REPOSITORY_DIR)
    json_config = model.to_json()
    model_path = "{0}/model-{1}.json".format(
        MODEL_REPOSITORY_DIR, FLAGS.model_name
    )
    with open(model_path, 'w') as json_file:
        json_file.write(json_config)

    model.fit_generator(
        train_generator,
        steps_per_epoch=STEP_SIZE_TRAIN,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=STEP_SIZE_VALID,
        callbacks=callbacks_list)

if __name__ == '__main__':
    app.run(main)

