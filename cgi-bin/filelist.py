#!/usr/bin/python3

print("Content-Type: application/json\n")

import sys
from PIL import Image
import os
import json
import re

imagestorage = os.environ['PHOTO_PATH']
imageuriprefix = os.environ['year'] + '/' + os.environ['album'] + '/'
imageroot = imagestorage + '/' + imageuriprefix

photoes = list()
videos = list()

imagematch = re.compile(r".*\.(jpg|png|jpeg|JPG)$")

for child in sorted(os.listdir(imageroot)):
    file = imageroot + child
    if not os.path.isfile(file):
        continue

    if imagematch.match(child) is not None:
        w = 0
        h = 0
        try:
            im = Image.open(file)
            orig_width, orig_height = im.size

            size = int(os.environ.get('size', 2048))

            if orig_width > orig_height:
                h = int(orig_height * size / orig_width)
                w = size
            else:
                w = int(orig_width * size / orig_height)
                h = int(size)
        except:
            continue

        photoes.append({'filename': imageuriprefix + child, 'height': h, 'width': w})
    elif child.lower().endswith(".mp4"):
        import cv2
        cap = cv2.VideoCapture(file)

        _, img = cap.read()
        orig_width = img.shape[1]
        orig_height = img.shape[0]

        videos.append({'filename': imageuriprefix + child, 'height': orig_height, 'width': orig_width})


print(json.dumps({"photos": photoes, "videos": videos}))


