import os
import cv2
import numpy as np
import json


def segrose(image, img_name):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((9, 9), np.uint8)
    dilated_image = cv2.dilate(binary_image, kernel, iterations=1)
    filled_image = cv2.erode(dilated_image, kernel, iterations=1)

    contours, _ = cv2.findContours(
        binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = [
        contour for contour in contours if len(contour) >= 100]

    result_image = cv2.drawContours(
        image.copy(), filtered_contours, -1, (50, 255, 100), 4)

    # cv2.imshow('src',image)
    # cv2.imshow('binary',binary_image)
    # cv2.imshow('filled image',filled_image)
    # cv2.imshow('res',result_image)
    # cv2.waitKey(0)

    annotations = {
        "info": {
            "description": "ISAT",
            "folder": "",
            "name": img_name,
            "width": image.shape[1],
            "height": image.shape[0],
            "depth": 3,
            "note": ""
        }
    }
    annotations['objects'] = []
    for i, contour in enumerate(filtered_contours):
        # print(contour.shape)
        contour_ = contour.reshape(-1, 2)
        object = {}
        object['category'] = img_name[-6:-4]
        object['group'] = i
        object['segmentation'] = contour_.tolist()
        object['area'] = cv2.contourArea(contour)
        object['layer'] = 1.0
        x1, y1, w, h = cv2.boundingRect(contour)
        x2 = x1+w
        y2 = y1+h
        object['bbox'] = [x1, y1, x2, y2]
        object['incrowd'] = False
        object['note'] = ""
        annotations['objects'].append(object)

    # Save JSON file

    json_file_path = img_name[:-7] + ".json"
    with open(json_file_path, 'w') as json_file:
        json.dump(annotations, json_file, indent=4)
    print(img_name)


# 获取文件夹下所有图片的文件名并按名称排序
folder_path = 'rosedata-few'
img_list = os.listdir(folder_path)
img_list.sort()

# 分割图片中的玫瑰花并输出
for img_name in img_list:
    img_path = os.path.join(folder_path, img_name)

    # 读取图片
    img = cv2.imread(img_path)
    segrose(img, img_name)
    # 进行玫瑰花分割的处理，这里需要根据具体情况编写分割逻辑

    # 输出处理后的图片
   # output_path = os.path.join('output_folder', f'segmented_{img_name}')
   # cv2.imwrite(output_path, segmented_img)

print("玫瑰花分割完成，并输出到output_folder中。")
