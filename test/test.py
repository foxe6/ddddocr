import ddddocrgpu.ddddocrgpu
from PIL import Image, ImageOps
import os
import numpy as np
import json
import time
import random
import cv2 as cv
from io import BytesIO


ocr = ddddocrgpu.ddddocrgpu.DdddOcr(show_ad=False, use_gpu=True)
det = ddddocrgpu.ddddocrgpu.DdddOcr(det=True, show_ad=False, use_gpu=True)


bg = "bg.jpg"
c = open(bg, "rb").read()
bg = BytesIO(c)
ws=["w0.jpg", "w1.jpg", "w2.jpg"]


ochrs=[]
for i, w in enumerate(ws):
    c = open(w, "rb").read()
    w = BytesIO(c)
    w = Image.open(w).convert('RGBA')
    background = Image.new('RGBA', w.size, (255, 255, 255))
    w = Image.alpha_composite(background, w)
    ws[i] = BytesIO()
    w.convert("RGB").save(ws[i], format="jpeg", quality=100)
    res = ocr.classification(ws[i].getvalue())
    ochrs.append(res[0] if res else res)
if any(not _ for _ in ochrs):
    raise

poses = det.detection(bg.getvalue())
if len(poses)<3:
    raise

#print(bg, poses)
im = cv.imdecode(np.frombuffer(bg.getvalue(), np.uint8), cv.IMREAD_COLOR)
chrs = []
inters = []
for i, box in enumerate(poses):
    x1, y1, x2, y2 = box
    x1-=5
    if x1<0:
        x1 = 0
    y1-=5
    if y1<0:
        y1 = 0
    x2+=5
    if x2>len(im[0]):
        x2 = len(im[0])
    y2+=5
    if y2>len(im):
        y2 = len(im)
    rgb = im[y1:y2,x1:x2]

    def rotate_image(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LANCZOS4)
        return result
    
    inter=[]
    w = rotate_image(rgb, -50)
    for ii, ang in enumerate(range(-40, 50, 10)):
        w = rotate_image(rgb, ang)
        w = Image.fromarray(w)
        #w = ImageOps.grayscale(w)
        tfn = "tmp/{}.jpg".format(time.time()).format(i, ii, ang)
        tb = BytesIO()
        w.save(tb, format="jpeg", quality=100)
        res = ocr.classification(tb.getvalue())
        if res:
            inter.append(res)
        w = ImageOps.invert(w)
        tfn = "tmp/{}.jpg".format(time.time())
        w.save(tb, format="jpeg", quality=100)
        res = ocr.classification(tb.getvalue())
        if res:
            inter.append(res)
    inter = [[_, inter.count(_)/len(inter)] for _ in inter]
    inters.append(inter)
    if inter:
        r = max(inter, key=lambda x: x[1])
        chrs.append([r, box])
    else:
        chrs.append([" ", box])

match = [_[0][0] in ochrs for _ in chrs]
print(ochrs, chrs, inters)
if match.count(False)>=2:
    raise

order = [None]*3
q = list(range(0,len(ochrs)))
for x in range(0, len(ochrs)):
    for i, (w, box) in enumerate(chrs):
        if w[0] == ochrs[x]:
            order[x] = w+[box]
            q.remove(i)
            break
for x in range(0, len(order)):
    if order[x] is None:
        w, box = chrs[q[0]]
        print(w,box)
        order[x] = w+[box]

print(order)
