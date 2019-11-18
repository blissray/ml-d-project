import os
from PIL import Image

for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        filepath = os.path.join(root,file)
        if filepath.upper().endswith("PNG"):
            try:
                picture = Image.open(filepath)
            except IOError as e:
                print(e)
                os.remove(filepath)
