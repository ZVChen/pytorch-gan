from PIL import Image
import os

def resize_images(input_dir, output_dir, size):
    for img_name in os.listdir(input_dir):
        if img_name.endswith('.jpeg') or img_name.endswith('.jpg'):
            with Image.open(os.path.join(input_dir, img_name)) as img:
                img = img.convert("RGB")
                img = img.resize(size)
                img.save(os.path.join(output_dir, img_name))

input_dir = r'/ytj_data/lunwen/GAN/dataset/teabud_real/zj_realteabud/zj_yatou_jpg_resize_320'
output_dir = r'/ytj_data/lunwen/GAN/dataset/teabud_real/zj_realteabud/zj_yatou_jpg_resize_160'
size = (160, 160) #这里修改你想要的尺寸

resize_images(input_dir, output_dir, size)
