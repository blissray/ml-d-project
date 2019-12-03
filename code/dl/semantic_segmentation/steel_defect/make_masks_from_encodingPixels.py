import os
import cv2
from PIL import Image
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image

MASK_DIR = os.path.join("data", "mask")
def rle_to_pixels(str_rle):
    pixels = []
    if str_rle is not np.nan:
        result = [int(value) for value in str_rle.split(" ")]
        result_list = np.array(result).reshape(-1,2).tolist()
        for start, end in result_list:
            pixels.extend(list(range(start-1, start+end-1)))
    return pixels

def rle_to_mask(filepath, df):
    img = cv2.imread(filepath)
    height, width, channel = img.shape
    print(width, height)
    mask = np.zeros((width,height), dtype=np.int16).flatten()
    for index, rows in df.iterrows(): 
        mask[rows["list_pixels"]] = rows["class"]
    return np.stack( (mask.reshape(width,height).T,) * 3, axis=-1) 

def save_png(np_array, filename):
    im = Image.fromarray(np_array.astype(np.uint8))
    # plt.imshow(np_array)
    im.save(os.path.join(
        MASK_DIR, filename+".png"
    ))

def main():
    if os.path.exists(MASK_DIR) is not True:
        os.makedirs(MASK_DIR)
    TRAIN_PATH = "./data/train/"
    imgnames = [filename for filename in os.listdir(TRAIN_PATH)]
    imgpath = {img_name : os.path.join(TRAIN_PATH, img_name, "images", img_name+".png") for img_name in imgnames}

    csv_path = "./data/train.csv"
    df = pd.read_csv(csv_path)
    csv_path = "./data/train.csv"
#     df = df.dropna().reset_index(drop=True)
    
    file_df = df["ImageId_ClassId"].str.split("_", expand=True).rename(columns={0:"ImageId", 1:"class"})
    new_df = pd.merge(file_df, df, right_index=True, left_index=True)[["ImageId", "class", "EncodedPixels"]]
    new_df["list_pixels"] = new_df.EncodedPixels.map(rle_to_pixels)

    filepath_dict = {filename : os.path.join(TRAIN_PATH,filename) for filename in imgnames}
    for imageId in new_df.ImageId.tolist():
        result = rle_to_mask(
            filepath_dict[imageId], 
            new_df[new_df["ImageId"] == imageId])
        save_png(result, imageId.split(".")[0])


if __name__ == "__main__":
    main()
