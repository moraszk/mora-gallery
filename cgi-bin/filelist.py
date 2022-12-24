#!/usr/bin/python3

print("Content-Type: application/json\n")

import sys
import cv2
import os
import json

imagestorage = os.environ['PHOTO_PATH']
imageuriprefix = os.environ['year'] + '/' + os.environ['album'] + '/'
imageroot = imagestorage + '/' + imageuriprefix

photoes = list()

for child in os.listdir(imageroot):
    file = imageroot + child
    if not os.path.isfile(file):
        continue

    w = 0
    h = 0
    try:
        img = cv2.imread(file)

        orig_width = img.shape[1]
        orig_height = img.shape[0]

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

print(json.dumps(photoes))

