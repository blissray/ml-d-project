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


STANFORD_DATA_URL = "https://storage.googleapis.com/teamlab-data/stanford-dogs-dataset.zip"
DATA_DIR = "data"
FLAGS = flags.FLAGS
flags.DEFINE_boolean("reset", False,
                     "Whether to remove all downloaded dataset")
flags.DEFINE_float("test_ratio", 0.2,
                     "Whether to remove all downloaded dataset")

# Required flag.
#flags.mark_flag_as_required("name")

def _data_downlad(dataset_name):
  if dataset_name == "STANFORD":
    download_path = os.path.join(DATA_DIR, "stanford-dogs-dataset.zip")
    wget.download(STANFORD_DATA_URL, download_path)

def main(args):

  if FLAGS.reset == True:
    print("Now, deleting current all downloaded dataset")
    rmtree(DATA_DIR)
    print("Done")

  if os.path.exists(DATA_DIR) is not True:
    os.mkdir(DATA_DIR)
    os.mkdir(os.path.join(DATA_DIR, "train"))
    os.mkdir(os.path.join(DATA_DIR, "train", "image"))
    os.mkdir(os.path.join(DATA_DIR, "train", "annotation"))
    os.mkdir(os.path.join(DATA_DIR, "val"))
    os.mkdir(os.path.join(DATA_DIR, "val", "image"))
    os.mkdir(os.path.join(DATA_DIR, "val", "annotation"))
    print("Make 'data' directory ")
  
  stanford_data_path = os.path.join(DATA_DIR, "stanford-dogs-dataset.zip") 
  if os.path.exists(stanford_data_path) is not True:
    print("Stanford dataset download")
    _data_downlad("STANFORD")
  print("\nStanford dog breed dataset download is done")
  
  stanford_dataset_path = os.path.join(DATA_DIR, "stanford-dogs-dataset.zip")
  with ZipFile(stanford_dataset_path, 'r') as zipObj:
    zipObj.extractall(DATA_DIR)
  
  TRAIN_PATH = os.path.join(DATA_DIR, "train")
  TRAIN_IMG_PATH = os.path.join(DATA_DIR, "train", "image")
  TRAIN_ANNO_PATH = os.path.join(DATA_DIR, "train", "annotation")
  VAL_PATH = os.path.join(DATA_DIR, "val")
  VAL_IMG_PATH = os.path.join(DATA_DIR, "val", "image")
  VAL_ANNO_PATH = os.path.join(DATA_DIR, "val", "annotation")

  stanford_image_path = os.path.join(DATA_DIR, "images", "Images") 
  stanford_anno_path = os.path.join(DATA_DIR, "annotations", "Annotation") 

  original_dir_label_dict = {}
  for breed_name in os.listdir(stanford_image_path):
    label = breed_name[10:].lower()
    original_dir_label_dict[breed_name] = label

  for breed_name in original_dir_label_dict.values():
    os.mkdir(os.path.join(TRAIN_IMG_PATH, breed_name))
    os.mkdir(os.path.join(TRAIN_ANNO_PATH, breed_name))
    os.mkdir(os.path.join(VAL_IMG_PATH, breed_name))
    os.mkdir(os.path.join(VAL_ANNO_PATH, breed_name))

  image_list = []
  filename_list = []
  for root, _, filenames in os.walk(stanford_image_path):
    image_list += [os.path.join(root, f) for f in filenames if f[-3:] == "jpg" ]
    filename_list += [f.split(".")[0] for f in filenames if f[-3:] == "jpg"]
  image_list.sort()

  anno_list = [] 
  for root, _, filenames in os.walk(stanford_anno_path):
    anno_list += [os.path.join(root, f) for f in filenames if f in filename_list]
  anno_list.sort() 
  
  print ("Train / Validation Split: Split ratio - {0}".format(
      FLAGS.test_ratio))
  x_train_files, x_val_files, y_train_labels, y_val_labels = train_test_split(
    image_list, anno_list, test_size = FLAGS.test_ratio)
  

  for image_path, label_path in zip(x_val_files, y_val_labels):

    label = original_dir_label_dict[image_path.split("/")[-2]]
    filename = image_path.split("/")[-1] 
    source_path = image_path 
    target_path = os.path.join(VAL_IMG_PATH, label, filename) 
    shutil.move(source_path, target_path)

    filename = label_path.split("/")[-1]
    source_path = label_path 
    target_path = os.path.join(VAL_ANNO_PATH, label, filename+".xml") 
    shutil.move(source_path, target_path)

  for image_path, label_path in zip(x_train_files, y_train_labels):

    label = original_dir_label_dict[image_path.split("/")[-2]]
    filename = image_path.split("/")[-1] 
    source_path = image_path 
    target_path = os.path.join(TRAIN_IMG_PATH, label, filename) 
    shutil.move(source_path, target_path)

    filename = label_path.split("/")[-1]
    source_path = label_path 
    target_path = os.path.join(TRAIN_ANNO_PATH, label, filename+".xml") 
    shutil.move(source_path, target_path)

  shutil.rmtree(os.path.join(DATA_DIR, "images"))
  shutil.rmtree(os.path.join(DATA_DIR, "annotations"))


if __name__ == '__main__':
  app.run(main)

