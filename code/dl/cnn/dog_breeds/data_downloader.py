import wget

from absl import app
from absl import flags
import os
import shutil  

from zipfile import ZipFile
import pandas as pd
from sklearn.model_selection import train_test_split


KAGGLE_DATA_URL = "https://storage.googleapis.com/teamlab-data/dog-breed-identification.zip"
STANFORD_DATA_URL = "https://storage.googleapis.com/teamlab-data/stanford-dogs-dataset.zip"
DATA_DIR = "data"
#FLAGS = flags.FLAGS
#flags.DEFINE_string("name", None, "Your name.")
#flags.DEFINE_boolean("stanford_dataset", False,
                     #}"Whether to use Stanford dataset.")

# Required flag.
#flags.mark_flag_as_required("name")

def kaggle_data_downlad():
  download_path = os.path.join(DATA_DIR, "dog-breed-identification.zip")
  wget.download(KAGGLE_DATA_URL, download_path)

def stanford_data_downlad():
  download_path = os.path.join(DATA_DIR, "stanford-dogs-dataset.zip")
  wget.download(STANFORD_DATA_URL, download_path)

def main(args):
  if os.path.exists(DATA_DIR) is not True:
    os.mkdir(DATA_DIR)
  
  # Kaggle Dataset Download
  kaggle_data_path = os.path.join(DATA_DIR, "dog-breed-identification.zip") 
  if os.path.exists(kaggle_data_path) is not True:
    print("kaggle dog breed dataset download")
    kaggle_data_downlad()
  print("Kaggle dog breed dataset download is done")
  


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
  
  x_train_files, x_val_files, y_train_labels, y_val_labels = train_test_split(
    x, y, test_size = 0.2, stratify = y)
  
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
  stanford_data_path = os.path.join(DATA_DIR, "stanford-dogs-dataset.zip") 
  if os.path.exists(stanford_data_path) is not True:
    print("Stanford dataset download")
    stanford_data_downlad()
  print("Stanford dog breed dataset download is done")
  
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

if __name__ == '__main__':
  app.run(main)

  #wget.download(url, 'cat4.jpg')