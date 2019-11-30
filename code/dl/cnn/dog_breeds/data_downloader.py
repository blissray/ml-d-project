import wget

from absl import app
from absl import flags
import os
import shutil  

from zipfile import ZipFile
import pandas as pd
from sklearn.model_selection import train_test_split
from shutil import rmtree


KAGGLE_DATA_URL = "https://storage.googleapis.com/teamlab-data/dog-breed-identification.zip"
STANFORD_DATA_URL = "https://storage.googleapis.com/teamlab-data/stanford-dogs-dataset.zip"
DATA_DIR = "data"
FLAGS = flags.FLAGS
flags.DEFINE_boolean("stanford_dataset", False,
                     "Whether to use Stanford dataset.")
flags.DEFINE_boolean("reset", False,
                     "Whether to remove all downloaded dataset")
flags.DEFINE_float("test_ratio", 0.2,
                     "Whether to remove all downloaded dataset")

# Required flag.
#flags.mark_flag_as_required("name")

def _data_downlad(dataset_name):
  if dataset_name == "KAGGLE":
    download_path = os.path.join(DATA_DIR, "dog-breed-identification.zip")
    wget.download(KAGGLE_DATA_URL, download_path)
  if dataset_name == "STANFORD":
    download_path = os.path.join(DATA_DIR, "stanford-dogs-dataset.zip")
    wget.download(STANFORD_DATA_URL, download_path)

def _write_current_download_configuration():
  import json 

  conf = dict()
  if FLAGS.stanford_dataset:
    conf["dataset"] = "STANFORD"
  else:
    conf["dataset"] = "KAGGLE_ONLY"
  
  conf["test_ratio"] = FLAGS.test_ratio

  with open('download_conf.json', 'w') as outfile:
    json.dump(conf, outfile)
  
def main(args):
  _write_current_download_configuration()

  if FLAGS.reset == True:
    print("Now, deleting current all downloaded dataset")
    rmtree(DATA_DIR)
    print("Done")

  if os.path.exists(DATA_DIR) is not True:
    os.mkdir(DATA_DIR)
    print("Make 'data' directory ")
  
  # Kaggle Dataset Download
  kaggle_data_path = os.path.join(DATA_DIR, "dog-breed-identification.zip") 
  if os.path.exists(kaggle_data_path) is not True:
    print("kaggle dog breed dataset download")
    _data_downlad("KAGGLE")
  print("\nKaggle dog breed dataset download is done")
  


  with ZipFile(kaggle_data_path, 'r') as zipObj:
     zipObj.extractall(DATA_DIR)

  train_file_path = os.path.join(DATA_DIR, "train.zip")
  with ZipFile(train_file_path, 'r') as zipObj:
     zipObj.extractall(DATA_DIR)

  test_file_path = os.path.join(DATA_DIR, "test.zip")
  with ZipFile(test_file_path, 'r') as zipObj:
     zipObj.extractall(DATA_DIR)
  
  label_csv_file_path = os.path.join(DATA_DIR, "labels.csv")
  label_df = pd.read_csv(label_csv_file_path)
  x = label_df.id + ".jpg"
  y = label_df.breed
  
  print ("Train / Validation Split: Split ratio - {0}".format(
      FLAGS.test_ratio))
  x_train_files, x_val_files, y_train_labels, y_val_labels = train_test_split(
    x, y, test_size = FLAGS.test_ratio, stratify = y)
  
  VAL_DIR = "val"
  TRAIN_DIR = "train"
  val_path = os.path.join(DATA_DIR, VAL_DIR)
  train_path = os.path.join(DATA_DIR, TRAIN_DIR)

  if os.path.exists(val_path) is not True:
    os.mkdir(val_path)
    label_list = set(y_val_labels.tolist())
    for label_name in label_list:
      os.mkdir(os.path.join(val_path, label_name))
      os.mkdir(os.path.join(train_path, label_name))

  for filename, label in zip(x_val_files, y_val_labels):
    source_path = os.path.join(DATA_DIR, TRAIN_DIR, filename)
    target_path = os.path.join(DATA_DIR, VAL_DIR, label, filename) 
    shutil.move(source_path, target_path)

  for filename, label in zip(x_train_files, y_train_labels):
    source_path = os.path.join(DATA_DIR, TRAIN_DIR, filename)
    target_path = os.path.join(DATA_DIR, TRAIN_DIR, label, filename) 
    shutil.move(source_path, target_path)

  # Stanford Dataset Download
  if FLAGS.stanford_dataset == True:
    stanford_data_path = os.path.join(DATA_DIR, "stanford-dogs-dataset.zip") 
    if os.path.exists(stanford_data_path) is not True:
      print("Stanford dataset download")
      _data_downlad("STANFORD")
    print("\nStanford dog breed dataset download is done")
    
    stanford_dataset_path = os.path.join(DATA_DIR, "stanford-dogs-dataset.zip")
    with ZipFile(stanford_dataset_path, 'r') as zipObj:
      zipObj.extractall(DATA_DIR)
    stanford_image_path = os.path.join(DATA_DIR, "images", "Images")
    for breed_name in os.listdir(stanford_image_path):
      label = breed_name[10:].lower()
      breed_path = os.path.join(stanford_image_path, breed_name)
      for filename in os.listdir(breed_path):
        source_path = os.path.join(breed_path, filename)
        target_path = os.path.join(DATA_DIR, TRAIN_DIR, label, filename) 
        shutil.move(source_path, target_path)
    shutil.rmtree(os.path.join(DATA_DIR, "images"))

    file_count = sum([len(files) for r, d, files in os.walk(train_path)])
    print("Number of train files : {0}".format(file_count))

    file_count = sum([len(files) for r, d, files in os.walk(val_path)])
    print("Number of validation files : {0}".format(file_count))

if __name__ == '__main__':
  app.run(main)

