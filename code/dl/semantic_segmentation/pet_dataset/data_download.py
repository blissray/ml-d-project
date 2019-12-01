from absl import app
from absl import flags

import os
import shutil  
import glob
import random
import wget
import tarfile

from zipfile import ZipFile
import xml.etree.ElementTree as ET

import pandas as pd
from sklearn.model_selection import train_test_split
from shutil import rmtree





PET_IMG_DATA_URL = "https://storage.googleapis.com/teamlab-data/images.tar.gz"
PET_ANNO_DATA_URL = "https://storage.googleapis.com/teamlab-data/annotations.tar.gz"

DATA_DIR = "data"
MODEL_DIR = "models"

FLAGS = flags.FLAGS
# Required flag.
#flags.mark_flag_as_required("name")

flags.DEFINE_boolean("reset", False,
                     "Whether to remove all downloaded dataset")
flags.DEFINE_float("test_ratio", 0.2,
                     "Whether to remove all downloaded dataset")

def _data_downlad(dataset_name):
  if dataset_name == "PET":
    download_path = os.path.join(DATA_DIR, "images.tar.gz")
    wget.download(PET_IMG_DATA_URL, download_path)

    download_path = os.path.join(DATA_DIR, "annotations.tar.gz")
    wget.download(PET_ANNO_DATA_URL, download_path)


def _xml_to_df(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main(args):

  if FLAGS.reset == True:
    print("Now, deleting current all downloaded dataset")
    rmtree(DATA_DIR)
    print("Done")

  if os.path.exists(DATA_DIR) is not True:
    os.mkdir(DATA_DIR)
    print("Make 'data' directory ")
  
  image_data_path = os.path.join(DATA_DIR, "images.tar.gz") 
  anno_data_path = os.path.join(DATA_DIR, "annotations.tar.gz") 

  if os.path.exists(image_data_path) is not True:
    print("Dataset is downloading")
    _data_downlad("PET")
  print("\nDataset download is done")
  
  tar = tarfile.open(image_data_path)
  tar.extractall(DATA_DIR)
  tar = tarfile.open(anno_data_path)
  tar.extractall(DATA_DIR)

  IMG_DIR = os.path.join(DATA_DIR, "images")
  ANNO_DIR =os.path.join(DATA_DIR, "annotations")


  filenames = [filename.split(".")[0] for filename in os.listdir(IMG_DIR)]
  random.shuffle(filenames) 
  print(len(filenames))
  train_files = filenames[:160]
  val_files = filenames[160:]
  
  # VAL_DIR = "val"
  # TRAIN_DIR = "train"
  # val_path = os.path.join(DATA_DIR, VAL_DIR)
  # train_path = os.path.join(DATA_DIR, TRAIN_DIR)

  # if os.path.exists(val_path) is not True:
  #   os.mkdir(val_path)
  #   os.mkdir(os.path.join(val_path, "images"))
  #   os.mkdir(os.path.join(val_path, "annotations"))

  # if os.path.exists(train_path) is not True:
  #   os.mkdir(train_path)
  #   os.mkdir(os.path.join(train_path, "images"))
  #   os.mkdir(os.path.join(train_path, "annotations"))

  # for filename in train_files:
  #   source_path = os.path.join(IMG_DIR, filename+".jpg")
  #   target_path = os.path.join(train_path, "images", filename+".jpg") 
  #   shutil.move(source_path, target_path)

  #   source_path = os.path.join(ANNO_DIR, filename+".xml")
  #   target_path = os.path.join(train_path, "annotations", filename+".xml") 
  #   shutil.move(source_path, target_path)

  # for filename in val_files:
  #   source_path = os.path.join(IMG_DIR, filename+".jpg")
  #   target_path = os.path.join(val_path, "images", filename+".jpg") 
  #   shutil.move(source_path, target_path)

  #   source_path = os.path.join(ANNO_DIR, filename+".xml")
  #   target_path = os.path.join(val_path, "annotations", filename+".xml") 
  #   shutil.move(source_path, target_path)
  # rmtree(IMG_DIR)
  # rmtree(ANNO_DIR)
  
  # train_anno_path = os.path.join(train_path, "annotations")
  # val_anno_path = os.path.join(val_path, "annotations")
  # train_anno_df = _xml_to_df(train_anno_path)
  # val_anno_df = _xml_to_df(val_anno_path)

  # train_anno_df.to_csv(
  #     os.path.join(DATA_DIR,'train_raccoon_labels.csv'), index=None)
  # val_anno_df.to_csv(
  #     os.path.join(DATA_DIR,'val_raccoon_labels.csv'), index=None)

  # print('Successfully converted xml to csv.')

  # if os.path.exists(MODEL_DIR) is not True:
  #   os.mkdir(MODEL_DIR)
  #   print("Make 'models' directory ")
  #   _data_downlad("MODEL")
  #   print("\nRaccoon YOLOv3 pretraind-model download is done")

if __name__ == '__main__':
  app.run(main)

