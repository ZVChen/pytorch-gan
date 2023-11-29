import os
import random
from PIL import Image, ImageDraw

# 大图片文件夹路径
big_images_path = "/ytj_data/lunwen/GAN/dataset/back"
# 小图片文件夹路径
small_images_path = "/ytj_data/lunwen/GAN/dataset/teabud_real/zj_realteabud/zj_touming_danzhang2"
# 输出文件夹路径
output_path = "/ytj_data/lunwen/GAN/dataset/self_dataset"

# 合成图片尺寸
composite_size = (640, 640)
# 随机选择小图片数量
num_small_images = 30

# VOC格式头部信息
voc_header = '''\
<annotation>
    <folder>{}</folder>
    <filename>{}</filename>
    <size>
        <width>{}</width>
        <height>{}</height>
        <depth>{}</depth>
    </size>
    <segmented>0</segmented>
'''
# VOC格式标注框信息
voc_bndbox = '''\
    <object>
        <name>{}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>
'''
# VOC格式尾部信息
voc_footer = '''\
</annotation>
'''

def find_random_position(big_image_size, small_image_size):
    """在大图片中随机选择小图片位置并返回标注框坐标"""
    x_max = big_image_size[0] - small_image_size[0]
    y_max = big_image_size[1] - small_image_size[1]
    x = random.randint(0, x_max)
    y = random.randint(0, y_max)
    return (x, y, x + small_image_size[0], y + small_image_size[1])

# 获取大图片列表
big_images = [f for f in os.listdir(big_images_path) if os.path.isfile(os.path.join(big_images_path, f))]

for image_filename in big_images:
    # 加载大图片并创建合成图片及其对应的标注信息
    big_image_path = os.path.join(big_images_path, image_filename)
    big_image = Image.open(big_image_path).convert("RGBA")
    composite_image = big_image
    #composite_image = Image.new("RGBA", composite_size, color=(255, 255, 255))
    annotation_filename = os.path.splitext(image_filename)[0] + ".xml"
    annotation_path = os.path.join(output_path, "ann_zj", annotation_filename)
    with open(annotation_path, 'w') as annotation_file:
        # 写入VOC格式头部信息
        annotation_file.write(voc_header.format("img_zj", image_filename, *composite_size, 3))

        # 随机选择小图片并将其粘贴到合成图片中
        for i in range(num_small_images):
            small_image_filename = random.choice(os.listdir(small_images_path))
            small_image_path = os.path.join(small_images_path, small_image_filename)
            small_image = Image.open(small_image_path).convert("RGBA")
            small_image_alpha = small_image.split()[3]
            small_width_percent = random.uniform(0.025, 0.05)
            small_height_percent = random.uniform(0.05, 0.1)
            small_size = (int(composite_size[0] * small_width_percent), int(composite_size[1] * small_height_percent))
            #small_size = (composite_size[0], composite_size[1])
            small_image_resized = small_image.resize((small_size),Image.LANCZOS)
            #w = small_image.width  # 图片的宽
            #h = small_image.height  # 图片的高        
            print(type(small_image_resized))
            #small_size = (w,h)
            small_image_resized.convert("RGB")
            position = find_random_position(composite_size, small_size)
            composite_image.alpha_composite(small_image_resized, dest=(position[0], position[1]))
            annotation_file.write(voc_bndbox.format(small_image_filename, *position))

        # 写入VOC格式尾部信息
        annotation_file.write(voc_footer)

    # 保存合成图片
    composite_filename = os.path.splitext(image_filename)[0] + ".jpg"
    composite_path = os.path.join(output_path, "img_zj", composite_filename)
    composite_image.convert("RGB").save(composite_path)
