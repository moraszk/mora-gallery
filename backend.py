#!/usr/bin/python3

from flask import Flask
from flask import make_response, Response
app = Flask(__name__)
import cv2
import numpy as np
from PIL import Image
import os
import json
import re
import io


root_path="/media/mora_photo/nyilvanos/"

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/yearlist')
def yearlist():
    years = []
    for entry in os.scandir(root_path):
        if entry.is_dir():
            year = int(entry.name)
            if year > 1950 and year < 2030:
                years.append(year)
    years.sort()
    return Response(
            json.dumps(years),
            mimetype='application/json')


imagematch = re.compile(r".*\.(jpg|png|jpeg|JPG)$")

@app.route('/filelist/<int:year>/<string:album>')
def filelist(year, album):
    photoes = list()
    videos = list()

    imageroot = root_path + '/' + str(year) + '/' + album + '/'
    prefix = str(year) + '/' + album + '/'

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

                size = 2048

                if orig_width > orig_height:
                    h = int(orig_height * size / orig_width)
                    w = size
                else:
                    w = int(orig_width * size / orig_height)
                    h = int(size)
            except:
                continue

            photoes.append({'filename': prefix + child, 'height': h, 'width': w})
        elif child.lower().endswith(".mp4"):
            import cv2
            cap = cv2.VideoCapture(file)

            _, img = cap.read()
            orig_width = img.shape[1]
            orig_height = img.shape[0]

            videos.append({'filename': prefix + child, 'height': orig_height, 'width': orig_width})


    return Response(
            json.dumps({"photos": photoes, "videos": videos}),
            mimetype='application/json')

logop = Image.open("/srv/mora-gallery/public/logo.png")
logosize = 250
logo = logop.resize((int(logop.size[0]/logop.size[1]*logosize),logosize))
del logop
del logosize

@app.route('/watermark/jpeg/<int:year>/<string:album>/<string:filename>')
def watermark(year,album,filename):
    path = root_path + '/' + str(year) + '/' + album + '/' + filename 

    if not os.path.isfile(path):
        return

    im = Image.open(path)

    orig_width, orig_height = im.size

    size = 2048

    h=0
    w=0

    if orig_width > orig_height:
        h = int(orig_height * size / orig_width)
        w = size
    else:
        w = int(orig_width * size / orig_height)
        h = int(size)

    im2 = im.resize((w,h))

    im2.paste(logo, (w-logo.size[0],h-logo.size[1]), logo)
    
    buf = io.BytesIO()
    
    im2.save(buf, format='JPEG')

    response = make_response(buf.getvalue())
    response.headers.set('Content-Type', 'image/jpeg')
    return response


@app.route('/thumbnail/jpeg/<int:year>/<string:album>/<string:filename>')
def imagethumb(year,album,filename):
    path = root_path + '/' + str(year) + '/' + album + '/' + filename 

    if not os.path.isfile(path):
        return

    im = Image.open(path)

    orig_width, orig_height = im.size

    size = 400

    h=0
    w=0

    if orig_width > orig_height:
        h = int(orig_height * size / orig_width)
        w = size
    else:
        w = int(orig_width * size / orig_height)
        h = int(size)

    im.resize((h,w))
    
    buf = io.BytesIO()
    
    im.save(buf, format='JPEG')

    response = make_response(buf.getvalue())
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/videothumbnail/jpeg/<int:year>/<string:album>/<string:filename>.mp4')
def videothumb(year,album,filename):
    path = root_path + '/' + str(year) + '/' + album + '/' + filename + '.mp4'

    cap = cv2.VideoCapture(path)
    _, img = cap.read()
    orig_width = img.shape[1]
    orig_height = img.shape[0]
    height = 400
    width = orig_width * height / orig_height
    frame = cv2.resize(img, (int(width), int(height)), interpolation = cv2.INTER_AREA)

    points = np.array([[50, 50], [50, 130], [130, 90]])
    cv2.fillPoly(frame, pts=[points], color=(255, 255, 255))

    response = make_response(cv2.imencode('.jpg', frame)[1].tobytes())
    response.headers.set('Content-Type', 'image/jpeg')
    return response


app.run(host='0.0.0.0', port=8000)
