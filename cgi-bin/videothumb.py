#!/usr/bin/python3
import sys
import os

header = "Content-Type: image/" + os.environ.get('format', 'jpeg') + "\r\n\r\n"
sys.stdout.buffer.write(header.encode('ascii'))

import cv2

path = os.environ['VIDEO_PATH'] + '/' + os.environ['video']

cap = cv2.VideoCapture(path)

_, img = cap.read()
orig_width = img.shape[1]
orig_height = img.shape[0]
height = int(os.environ.get('size', 400))
width = orig_width * height / orig_height
frame = cv2.resize(img, (int(width), int(height)), interpolation = cv2.INTER_AREA)

points = np.array([[25, 25], [25, 65], [65, 45]])
cv2.fillPoly(img, pts=[points], color=(255, 255, 255))

sys.stdout.buffer.write(cv2.imencode("." + os.environ.get('format', 'jpg'), frame)[1].tobytes())


