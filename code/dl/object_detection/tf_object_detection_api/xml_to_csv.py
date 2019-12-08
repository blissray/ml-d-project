import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import json

def xml_to_csv(path):
    xml_list = []
    for dir_name, _, filenames in os.walk(path):
      for f in filenames:
        if f[-3:] == "xml":
          xml_file_path = os.path.join(dir_name, f)
          xml_file = open(xml_file_path, 'r') 
          tree = ET.ElementTree(ET.fromstring(xml_file.read()))
          root = tree.getroot()
          for member in root.findall('object'):
              value = (xml_file_path.split("/")[-1].split(".")[0],
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text.lower(),
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
              xml_list.append(value)
          xml_file.close()
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    TRAIN_PATH = os.path.join("data","train","annotation")
    VAL_PATH = os.path.join("data","val","annotation")

    for folder in [TRAIN_PATH, VAL_PATH]:
        xml_df = xml_to_csv(folder)
        xml_df.to_csv(os.path.join(folder, 'labels.csv'), index=None)
        print('Successfully converted xml to csv.')
    
    with open("label_map.json", "w") as outfile:
        result = {value : i for i, value in enumerate(sorted(xml_df["class"].unique().tolist()))}
            
        json.dump(result, outfile) 
    template = "item {{\n id : {} \n name: '{}'\n}}\n"

    with open("label_map.pbtxt", "w") as outfile:
        for key, value in result.items():
            outfile.write(
               template.format(
                   value, key) 
            )
        


main()