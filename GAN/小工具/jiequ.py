import os
import cv2
#import utils

try:
    import xml.etree.cElementTree as ET  # 解析xml的c语言版的模块
except ImportError:
    import xml.etree.ElementTree as ET

img_path = r"/media/ytj-work-linux/D/lunwen/GANALL/dataset/smalldataset/LJ43/img"  
xml_path = r"/media/ytj-work-linux/D/lunwen/GANALL/dataset/smalldataset/LJ43/ann"  
img_names = os.listdir(img_path)
save_dir = r"/media/ytj-work-linux/D/lunwen/GANALL/dataset/smalldataset/LJ43/jiequ"
#os.mkdir(save_dir) 

for imgname in img_names:  
    pic = os.path.join(img_path, imgname)
    AnotPath = os.path.join(xml_path, imgname[:-4] + '.xml')
    if not pic.endswith('jpg'):
        continue       

    img = cv2.imread(pic)
    tree = ET.ElementTree(file=AnotPath)  # 打开文件，解析成一棵树型结构
    root = tree.getroot()  # 获取树型结构的根
    ObjectSet = root.findall('object')  # 找到文件中所有含有object关键字的地方，这些地方含有标注目标
    ObjBndBoxSet = {}  # 以目标类别为关键字，目标框为值组成的字典结构
    num = 0
    for Object in ObjectSet:
        ObjName = Object.find('name').text
        BndBox = Object.find('bndbox')
        x1 = int(float(BndBox.find('xmin').text))  # -1 #-1是因为程序是按0作为起始位置的
        y1 = int(float(BndBox.find('ymin').text))  # -1
        x2 = int(float(BndBox.find('xmax').text))  # -1
        y2 = int(float(BndBox.find('ymax').text))  # -1
        
        # 截取图片
        crop_img = img[y1:y2, x1:x2]
        new_jpg_name = imgname[:-4] + "_crop_" + str(num) + ".jpg" #存储图片的名称
        num += 1
        cv2.imwrite(os.path.join(save_dir, new_jpg_name), crop_img) #截取的图片

