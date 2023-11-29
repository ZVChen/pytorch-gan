import os
import cv2
import numpy as np


def segrose(image):
    # mask=np.zeros(image.shape[:2],np.unit8)
    # bgdmodel=np.zeros((1,65),np.float64)
    # fgdmodel=np.zeros((1,65),np.float64)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((9, 9), np.uint8)
    dilated_image = cv2.dilate(binary_image, kernel, iterations=1)
    filled_image = cv2.erode(dilated_image, kernel, iterations=1)

    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = [contour for contour in contours if len(contour) >= 100]

    result_image = cv2.drawContours(image.copy(), filtered_contours, -1, (50, 255, 100), 4)

    cv2.imshow('src',image)
    cv2.imshow('binary',binary_image)
    cv2.imshow('filled image',filled_image)
    cv2.imshow('res',result_image)
    cv2.waitKey(0)
    print(image.shape[0])
    with open('instance_segmentation.txt', 'w') as file:
        for i, contour in enumerate(filtered_contours):
            # 写入实例分割标注格式
            file.write(f'0 ')
            for point in contour:
                file.write(f'{point[0][0]/image.shape[1]} {point[0][1]/image.shape[0]} ')
            file.write('\n')  # 分隔不同实例的空行


# 获取文件夹下所有图片的文件名并按名称排序
folder_path = 'rosedata-few'
img_list = os.listdir(folder_path)
img_list.sort()

# 分割图片中的玫瑰花并输出
for img_name in img_list:
    img_path = os.path.join(folder_path, img_name)
    
    # 读取图片
    img = cv2.imread(img_path)
    segrose(img) 
    # 进行玫瑰花分割的处理，这里需要根据具体情况编写分割逻辑
    
    # 输出处理后的图片
   # output_path = os.path.join('output_folder', f'segmented_{img_name}')
   # cv2.imwrite(output_path, segmented_img)

print("玫瑰花分割完成，并输出到output_folder中。")
