import cv2
import os
import numpy as np
import random
from lxml import etree

# 小图片的路径和大图片的路径
small_dir = "small_images/"
big_dir = "big_images/"

# 合成图片和标注文件的输出路径
out_dir = "output/"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# 小图片和大图片的尺寸
small_size = (64, 64)
big_size = (512, 512)

# 随机选择要粘贴的小图片数量和每个小图片的位置
num_images = 10
positions = [(100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (600, 600), (700, 700), (800, 800), (900, 900), (1000, 1000)]

# 读取小图片和大图片
small_images = []
for filename in os.listdir(small_dir):
    if filename.endswith(".jpg"):
        img = cv2.imread(os.path.join(small_dir, filename))
        img = cv2.resize(img, small_size)
        small_images.append(img)
        
big_images = []
for filename in os.listdir(big_dir):
    if filename.endswith(".jpg"):
        img = cv2.imread(os.path.join(big_dir, filename))
        img = cv2.resize(img, big_size)
        big_images.append(img)

# 遍历大图片，随机粘贴小图片，并生成标注框
for i, big_img in enumerate(big_images):
    out_img = big_img.copy()
    boxes = []
    for j in range(num_images):
        small_img = random.choice(small_images)
        x, y = random.choice(positions)
        out_img[y:y+small_size[1], x:x+small_size[0]] = small_img
        box = (x, y, x+small_size[0], y+small_size[1])
        boxes.append(box)
    out_path = os.path.join(out_dir, "image{}.jpg".format(i))
    cv2.imwrite(out_path, out_img)
    
    # 生成标注文件
    xml_path = os.path.join(out_dir, "image{}.xml".format(i))
    annotation = etree.Element("annotation")

    fname = etree.Element("filename")
    fname.text = "image{}.jpg".format(i)
    annotation.append(fname)

    sz = etree.Element("size")
    width = etree.Element("width")
    width.text = str(big_size[0])
    sz.append(width)
    height = etree.Element("height")
    height.text = str(big_size[1])
    sz.append(height)
    depth = etree.Element("depth")
    depth.text = str(3)
    sz.append(depth)
    annotation.append(sz)

    for box in boxes:
        obj = etree.Element("object")
        name = etree.Element("name")
        name.text = "small"
        obj.append(name)
        bndbox = etree.Element("bndbox")
        xmin = etree.Element("xmin")
        xmin.text = str(box[0])
        bndbox.append(xmin)
        ymin = etree.Element("ymin")
        ymin.text = str(box[1])
        bndbox.append(ymin)
        xmax = etree.Element("xmax")
        xmax.text = str(box[2])
        bndbox.append(xmax)
        ymax = etree.Element("ymax")
        ymax.text = str(box[3])
        bndbox.append(ymax)
        obj.append(bndbox)
        annotation.append(obj)
    
    tree = etree.ElementTree(annotation)
    tree.write(xml_path, pretty_print=True)

print("Done.")