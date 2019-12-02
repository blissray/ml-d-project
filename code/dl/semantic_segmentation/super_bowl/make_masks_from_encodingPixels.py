import os
import cv2
from PIL import Image
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image

MASK_DIR = os.path.join("data", "mask")
def rle_to_pixels(str_rle):
    str_rle = " ".join(str_rle)
    pixels = []
    result = [int(value) for value in str_rle.split(" ")]
    result_list = np.array(result).reshape(-1,2).tolist()
    for start, end in result_list:
        pixels.extend(list(range(start-1, start+end-1)))
    return pixels

def rle_to_maks(filepath, encoding_pixels):
    img = cv2.imread(filepath)
    width, height, _ = img.shape
    mask = np.zeros((width,height)).flatten()
    mask[encoding_pixels] = 254
    return np.stack( 
        (mask.reshape(width,height),) * 3, axis=-1) 

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

    csv_path = "./data/stage1_train_labels.csv"
    df = pd.read_csv(csv_path)
    new_df = df.groupby(['ImageId'])['EncodedPixels'].apply(list).reset_index()
    new_df["list_pixels"] = new_df.EncodedPixels.map(rle_to_pixels)
    list_pixel_dict = new_df[["ImageId", "list_pixels"]].set_index("ImageId").to_dict()

    for imageId in new_df.ImageId.tolist():
        result = rle_to_maks(imgpath[imageId], 
            list_pixel_dict["list_pixels"][imageId])
        save_png(result, imageId)


if __name__ == "__main__":
    main()
