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





DATA_URL = "https://storage.googleapis.com/teamlab-data/severstal-steel-defect-detection.zip"
FILENAME = "severstal-steel-defect-detection.zip"
DATA_DIR = "data"
MODEL_DIR = "models"

FLAGS = flags.FLAGS
flags.DEFINE_boolean("reset", False,
                     "Whether to remove all downloaded dataset")
flags.DEFINE_float("test_ratio", 0.2,
                     "Whether to remove all downloaded dataset")

def _data_downlad(dataset_name):
  download_path = os.path.join(DATA_DIR, FILENAME)
  wget.download(DATA_URL, download_path)

def main(args):
  if FLAGS.reset == True:
    print("Now, deleting current all downloaded dataset")
    rmtree(DATA_DIR)
    print("Done")
  if os.path.exists(DATA_DIR) is not True:
    os.mkdir(DATA_DIR)
    print("Make 'data' directory ")
  
  data_path = os.path.join(DATA_DIR, FILENAME) 
  if os.path.exists(data_path) is not True:
    print("Dataset downloading")
    _data_downlad("DATASET")
  print("\ndataset download is done")

  with ZipFile(data_path, 'r') as zipObj:
    zipObj.extractall(DATA_DIR)

  train_path = os.path.join(DATA_DIR, "train_images.zip")
  if os.path.exists(
    os.path.join(DATA_DIR, "train")) is not True:
    os.mkdir(os.path.join(DATA_DIR, "train"))
  with ZipFile(train_path, 'r') as zipObj:
    zipObj.extractall(
      os.path.join(DATA_DIR, "train"))
  
  test_path = os.path.join(DATA_DIR, "test_images.zip")
  if os.path.exists(
    os.path.join(DATA_DIR, "test")) is not True:
    os.mkdir(os.path.join(DATA_DIR, "test"))
  with ZipFile(test_path, 'r') as zipObj:
    zipObj.extractall(
      os.path.join(DATA_DIR, "test"))  


if __name__ == '__main__':
  app.run(main)

