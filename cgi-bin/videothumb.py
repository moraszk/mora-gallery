#!/usr/bin/python3
import sys

sys.stdout.buffer.write("Content-Type: image/jpeg\r\n\r\n".encode('ascii'))

import cv2
import os

path = os.environ['VIDEO_PATH'] + '/' + os.environ['video']

cap = cv2.VideoCapture(path)

_, img = cap.read()
orig_width = img.shape[1]
orig_height = img.shape[0]
height = int(os.environ.get('size', 400))
width = orig_width * height / orig_height
frame = cv2.resize(img, (int(width), int(height)), interpolation = cv2.INTER_AREA)

sys.stdout.buffer.write(cv2.imencode("." + os.environ.get('format', 'jpg'), frame)[1].tobytes())


