import wget

from absl import app
from absl import flags
import os
import shutil  

from zipfile import ZipFile
import pandas as pd
from sklearn.model_selection import train_test_split
from shutil import rmtree
import glob


DATA_DIR = "data"
IMAGE_DIR = "image"
ANNO_DIR = "annotation"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
TRAIN_IMAGE_DIR = os.path.join(TRAIN_DIR, IMAGE_DIR)
TRAIN_ANNO_DIR = os.path.join(TRAIN_DIR, ANNO_DIR)
VAL_DIR = os.path.join(DATA_DIR, "val")
VAL_ANNO_DIR = os.path.join(VAL_DIR, ANNO_DIR)
VAL_IMAGE_DIR = os.path.join(VAL_DIR, IMAGE_DIR)

def get_list(DIR_PATH):
  data_list = []
  for root, _, filenames in os.walk(DIR_PATH):
    data_list += [os.path.join(root, f) for f in filenames if f[-3:] == "jpg" ]
  return data_list

def move_files(data_list, TARGET_PATH):

  for filename in data_list:
    source_path = filename
    target_path = os.path.join(TARGET_PATH, filename.split("/")[-1]) 
    shutil.move(source_path, target_path)
def main(args):

  train_image_list = get_list(TRAIN_IMAGE_DIR) 
  train_anno_list = get_list(TRAIN_ANNO_DIR) 
  val_image_list = get_list(VAL_IMAGE_DIR) 
  val_anno_list = get_list(VAL_ANNO_DIR) 

  move_files(train_image_list, TRAIN_IMAGE_DIR)
  move_files(train_anno_list, TRAIN_ANNO_DIR)
  move_files(val_image_list, VAL_IMAGE_DIR)
  move_files(val_anno_list, VAL_ANNO_DIR)


if __name__ == '__main__':
  app.run(main)

