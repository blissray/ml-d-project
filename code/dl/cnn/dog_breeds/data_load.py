import os
import tensorflow as tf
DATA_DIR = "dataset"
TRAIN_DIR = "train"
TEST_DIR = "test"
LABEL_FILE = "labels.csv"

def _load_files():
    train_files = os.listdir(os.path.join(DATA_DIR, TRAIN_DIR))
    train_files = [os.path.abspath(
        os.path.join(DATA_DIR , TRAIN_DIR , filename) ) for filename in train_files]

    test_files = os.listdir(os.path.join(DATA_DIR, TEST_DIR))
    test_files = [os.path.abspath(
        os.path.join(DATA_DIR , TRAIN_DIR , filename) )  for filename in test_files]

    label_file = "labels.csv"
    return train_files, test_files, label_file

def _load_csv(filename):
    import csv 
    breed_names = []
    file_names = []
    label_dict = {}
    with open(filename, "r") as csv_file:
       csvreader = csv.reader(csv_file, delimiter = ",") 
       for row in csvreader:
          breed_names.append(row[1])
          file_names.append(row[0])
    from sklearn.preprocessing import LabelEncoder
    label_encoder = LabelEncoder()
    label_encoder.fit(breed_names)

    integer_encoded = label_encoder.transform(breed_names)

    for a,b in zip(file_names, integer_encoded):
        label_dict[a] = b
    return label_dict


def _preprocess_image(image):   
    image = tf.image.decode_jpeg(image, channels=3)   
    image = tf.image.resize(image, [255, 255])
    image /= 255.0  # normalize to [0,1] range    
    return image

def _load_and_preprocess_image(path):   
    image = tf.io.read_file(path)
    image = _preprocess_image(image)
    return image


def load_and_preprocess_from_path_label(path, label):   
    return _load_and_preprocess_image(path), label  

def get_dataset():
    train_files, test_files, label_file = _load_files()
    result = _load_csv(label_file)


    all_image_paths = []
    all_image_labels = []
    for filename in train_files:
        filename_only = filename.split("/")[-1].split(".")[0]
        all_image_paths.append(filename)
        all_image_labels.append(result[filename_only])
        
    ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))
    image_label_ds = ds.map(load_and_preprocess_from_path_label)
    image_label_ds  = image_label_ds.shuffle(1024)
    image_label_ds = image_label_ds.batch(32)
    image_label_ds = image_label_ds.prefetch(buffer_size=512)
    return image_label_ds


