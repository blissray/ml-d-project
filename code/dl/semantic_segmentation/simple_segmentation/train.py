import cv2
import numpy as np
from model.augmentations import randomHueSaturationValue, randomShiftScaleRotate, randomHorizontalFlip
import model.unet as unet
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, TensorBoard
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import img_to_array

import os
import random

from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.optimizers import Adam
from model.losses import bce_dice_loss, dice_loss, weighted_bce_dice_loss, weighted_dice_loss, dice_coeff

SIZE = (256, 256)
BASE_SIZE = 256
def data_gen(img_folder, mask_folder, batch_size, is_train=False):
  c = 0
  n = os.listdir(img_folder) #List of training images
  random.shuffle(n)
  
  while (True):
    img = np.zeros((batch_size, BASE_SIZE, BASE_SIZE, 3)).astype('float')
    mask = np.zeros((batch_size, BASE_SIZE, BASE_SIZE, 1)).astype('float')

    for i in range(c, c+batch_size): #initially from 0 to 16, c = 0. 

      train_img = cv2.imread(img_folder+'/'+n[i])
      train_img = cv2.resize(train_img, (BASE_SIZE, BASE_SIZE))
      # Read an image from folder and resize
                                                         
      train_mask = cv2.imread(mask_folder+'/'+n[i], cv2.IMREAD_GRAYSCALE)
      train_mask = cv2.resize(train_mask, (BASE_SIZE, BASE_SIZE))
    #   train_mask = train_mask.reshape(BASE_SIZE, BASE_SIZE, 1) # Add extra dimension for parity with train_img size [512 * 512 * 3]
      if is_train:
        # train_img = randomHueSaturationValue(train_img,
        #                             hue_shift_limit=(-50, 50),
        #                             sat_shift_limit=(0, 0),
        #                             val_shift_limit=(-15, 15))
        train_img, train_mask = randomShiftScaleRotate(train_img, train_mask,
                                        shift_limit=(-0.0625, 0.0625),
                                        scale_limit=(-0.1, 0.1),
                                        rotate_limit=(-20, 20))
        train_img, train_mask = randomHorizontalFlip(train_img, train_mask)
        # fix_mask(mask)
      train_mask = np.expand_dims(train_mask, axis=2)

      img[i-c] = train_img #add to array - img[0], img[1], and so on.
      mask[i-c] = train_mask

    c+=batch_size
    if(c+batch_size>=len(os.listdir(img_folder))):
      c=0
      random.shuffle(n)
                  # print "randomizing again"
    yield img, mask



DATA_DIR = "data"
IMAGE_TEST_DIR = "images_prepped_test"
IMAGE_TRAIN_DIR = "images_prepped_train"
ANNO_TEST_DIR = "annotations_prepped_test"
ANNO_TRAIN_DIR = "annotations_prepped_train"


def fix_mask(mask):
    mask[mask < 100] = 0.0
    mask[mask >= 100] = 255.0

# # Processing function for the training data
# def train_process(data):
#     img, mask = data
#     img = img[:,:,:3]
#     mask = mask[:, :, :3]
#     mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#     # fix_mask(mask)
#     img = cv2.resize(img, SIZE)
#     mask = cv2.resize(mask, SIZE)
#     img = randomHueSaturationValue(img,
#                                    hue_shift_limit=(-50, 50),
#                                    sat_shift_limit=(0, 0),
#                                    val_shift_limit=(-15, 15))
#     img, mask = randomShiftScaleRotate(img, mask,
#                                        shift_limit=(-0.0625, 0.0625),
#                                        scale_limit=(-0.1, 0.1),
#                                        rotate_limit=(-20, 20))
#     img, mask = randomHorizontalFlip(img, mask)
#     # fix_mask(mask)
#     img = img/255.
#     mask = mask/255.
#     mask = np.expand_dims(mask, axis=2)
#     return (img, mask)


# # Processing function for the validation data, no data augmentation
# def validation_process(data):
#     img, mask = data
#     img = img[:,:,:3]
#     mask = mask[:, :, :3]
#     mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#     # fix_mask(mask)
#     img = cv2.resize(img, SIZE)
#     mask = cv2.resize(mask, SIZE)
#     fix_mask(mask)
#     img = img/255.
#     mask = mask/255.
#     mask = np.expand_dims(mask, axis=2)
#     return (img, mask)

def main():
    model = unet.get_unet_256(num_classes=11)

    # Save Model Info
    MODEL_REPOSITORY_DIR = "model_repo"
    if os.path.exists(MODEL_REPOSITORY_DIR) is not True:
        os.mkdir(MODEL_REPOSITORY_DIR)
    json_config = model.to_json()
    model_path = "{0}/unet_256_model.json".format(
        MODEL_REPOSITORY_DIR)
    with open(model_path, 'w') as json_file:
        json_file.write(json_config)

    callbacks = [EarlyStopping(monitor='val_loss',
                           patience=8,
                           verbose=1,
                           min_delta=1e-4),
             ReduceLROnPlateau(monitor='val_loss',
                               factor=0.1,
                               patience=4,
                               verbose=1,
                               epsilon=1e-4),
             ModelCheckpoint(monitor='val_loss',
                             filepath='weights/best_weights.hdf5',
                             save_best_only=True,
                             save_weights_only=True)]

    epochs=100

    IMAGE_TRAIN_PATH = os.path.join(DATA_DIR, IMAGE_TRAIN_DIR)
    ANNO_TRAIN_PATH = os.path.join(DATA_DIR, ANNO_TRAIN_DIR)
    IMAGE_TEST_PATH = os.path.join(DATA_DIR, IMAGE_TEST_DIR)
    ANNO_TEST_PATH = os.path.join(DATA_DIR, ANNO_TEST_DIR)


    # train_frame_path = '/path/to/training_frames'
    # train_mask_path = '/path/to/training_masks'

    # val_frame_path = '/path/to/validation_frames'
    # val_mask_path = '/path/to/validation_frames'

    # Train the model
    BATCH_SIZE = 4
    train_gen = data_gen(
        IMAGE_TRAIN_PATH,ANNO_TRAIN_PATH, 
        batch_size = BATCH_SIZE, is_train=True)
    val_gen = data_gen(
        IMAGE_TEST_PATH,ANNO_TEST_PATH, 
        batch_size = BATCH_SIZE, is_train=False)
    opt = Adam(lr=1E-5, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

    NO_OF_TRAINING_IMAGES = len(os.listdir(IMAGE_TRAIN_PATH))
    NO_OF_VAL_IMAGES = len(os.listdir(IMAGE_TEST_PATH))

    TRAIN_STEPS_PER_EPOCH = NO_OF_TRAINING_IMAGES // BATCH_SIZE
    VAL_STEPS_PER_EPOCH = NO_OF_VAL_IMAGES // BATCH_SIZE

    model.compile(optimizer=opt, 
                  loss=dice_loss, 
                  metrics=[dice_coeff])    
    model.fit_generator(generator=train_gen,
                    epochs=epochs,
                    steps_per_epoch = TRAIN_STEPS_PER_EPOCH,
                    callbacks=callbacks,
                    validation_data=val_gen,
                    validation_steps=VAL_STEPS_PER_EPOCH
    )


if __name__ == "__main__":
    main()
