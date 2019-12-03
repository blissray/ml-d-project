from absl import app
from absl import flags

import os
import shutil  
import glob
import random
import wget

from zipfile import ZipFile
import xml.etree.ElementTree as ET

import pandas as pd
from sklearn.model_selection import train_test_split
from shutil import rmtree

import tarfile



DATA_DIR = "data"
TRAIN_DIR = "train"
VAL_DIR = "val"
MASK_DIR = "mask"

FLAGS = flags.FLAGS
flags.DEFINE_boolean("reset", False,
                     "Whether to remove all downloaded dataset")
flags.DEFINE_float("test_ratio", 0.2,
                     "Whether to remove all downloaded dataset")

def main(args):
    IMAGE_PATH = os.path.join(DATA_DIR, TRAIN_DIR) 
    MASK_PATH = os.path.join(DATA_DIR, MASK_DIR) 
    image_list = sorted([filename for filename in os.listdir(IMAGE_PATH)])
    mask_list = sorted([filename for filename in os.listdir(MASK_PATH)])
    
#     filename = None
#     for idx, files in enumerate((zip(image_list,mask_list))):
#         if files[0] != files[1]:
#             filename = files[0]
#             break
#     print(filename)
    train_img, val_img, tain_mask, val_mask = train_test_split(
        image_list, mask_list, test_size=0.2)
    
    VAL_DIR = "val"
    val_path = os.path.join(DATA_DIR, VAL_DIR)

    if os.path.exists(val_path) is not True:
        os.mkdir(val_path)
        os.mkdir(os.path.join(val_path,"images"))
        os.mkdir(os.path.join(val_path,"mask"))
        os.mkdir(os.path.join(IMAGE_PATH,"images"))
        os.mkdir(os.path.join(IMAGE_PATH,"mask"))
        

    for filename in val_img:
        source_path = os.path.join(IMAGE_PATH, filename)
        target_path = os.path.join(DATA_DIR, VAL_DIR, "images", filename) 
        shutil.move(source_path, target_path)
    for filename in val_mask:
        source_path = os.path.join(MASK_PATH, filename)
        target_path = os.path.join(DATA_DIR, VAL_DIR, "mask", filename) 
        shutil.move(source_path, target_path)

    for filename in train_img:
        source_path = os.path.join(IMAGE_PATH, filename)
        target_path = os.path.join(DATA_DIR, TRAIN_DIR, "images", filename) 
        shutil.move(source_path, target_path)
    for filename in tain_mask:
        source_path = os.path.join(MASK_PATH, filename)
        target_path = os.path.join(DATA_DIR, TRAIN_DIR, "mask", filename) 
        shutil.move(source_path, target_path)
        
#   for filename, label in zip(x_train_files, y_train_labels):
#     source_path = os.path.join(DATA_DIR, TRAIN_DIR, filename)
#     target_path = os.path.join(DATA_DIR, TRAIN_DIR, label, filename) 
#     shutil.move(source_path, target_path)


if __name__ == '__main__':
  app.run(main)

