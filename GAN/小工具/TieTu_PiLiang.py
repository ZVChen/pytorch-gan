from PIL import Image
import random
import os
from tqdm import tqdm
import configparser

def paste_enhance(png_path, images_paste_path, save_images_path, paste_num):
    os.makedirs(save_images_path, exist_ok=True)
    files = os.listdir(png_path) #小图像具体名称
    paste_files = os.listdir(images_paste_path)#原始图像具体名称
    
    #w, h = mainimg.size
    #print(files)
    for i in paste_files:
       mainimg = images_paste_path + i
       main_img_name = os.path.splitext(mainimg)
       #print(main_img_name)
       main_img = Image.open(f"{mainimg}").convert("RGBA")#将原图写入main_img中
       w, h = main_img.size
       #print(main_img)
       samples = random.sample(files, 30)#samples为files中随机取得20个小图像具体名称
       for j in samples:            
           
            beimg = png_path + j #beimg为20个随机小图像地址
            #print(beimg)
            im = Image.open(f"{beimg}").convert("RGBA")#将小图像写入im中
            #print(j)
            #print(im)
            random_result = dict()
            random_result['num_resize1'] = random.randint(20, 60)  # 闭区间,保存随机resize尺寸
            random_result['num_resize2'] = random.randint(40, 90)  # 闭区间,保存随机resize尺寸
            random_result['rotate_F'] = random.randint(1, 10)  # 随机逆时针旋转角度、随机顺时针旋转角度
            random_result['rotate_T'] = random.randint(-10, -1)  # 随机顺时针旋转角度
            random_result['status'] = random.randint(-1, 0)  # 随机抽状态，-1逆时针，0顺时针
            try:
               random_result['cut_x_left'] = random.randint(0, w - random_result['num_resize1'])  # 随机主图-蒙层图范围的左上角x
               random_result['cut_y_left'] = random.randint(0, h - random_result['num_resize2'])  # 随机主图-蒙层图范围的左上角y
            except ValueError:  # 蒙层图resize比主图尺寸大,那就不粘贴
                continue

            img_resize = im.resize((random_result['num_resize1'], random_result['num_resize2']))  # resize图片

            if random_result['status'] == -1:  # 随机旋转图片
                img_rotate = img_resize.rotate(random_result['rotate_F'])
            else:
                img_rotate = img_resize.rotate(random_result['rotate_T'])

                x_left, y_left = random_result['cut_x_left'], random_result['cut_y_left']
                x_right = random_result['cut_x_left'] + random_result['num_resize1']
                y_right = random_result['cut_y_left'] + random_result['num_resize2']
                
                main_img.paste(img_rotate, (x_left, y_left, x_right, y_right), img_rotate)  # 粘贴蒙层图片
                save_img = main_img.convert('RGB')  # 转换为jpg图片
                save_img.save(f"{save_images_path}/{i}_{paste_num}.jpg")
            
if __name__ == "__main__":

    num = 500
    png = "/ytj_data/lunwen/GAN/dataset/teabud_real/lj_realteabud/lj_touming_danzhang/"
    images_path = "/ytj_data/lunwen/GAN/dataset/back/"
    save_path = "/ytj_data/lunwen/GAN/dataset/self_dataset/"
    paste_enhance(png, images_path, save_path, num)