from PIL import Image  
import os 

# 设置输入和输出文件夹路径  
input_dir = "/ytj_data/lunwen/GAN/dataset/teabud_real/zj_realteabud/zj_touming_danzhang"  
output_dir = "/ytj_data/lunwen/GAN/dataset/teabud_real/zj_realteabud/zj_touming_danzhang2"  

def convert_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            img_path = os.path.join(input_dir, filename)
            img = Image.open(img_path)
            
            # 将白色像素变为透明
            img = img.convert("RGBA")
            datas = img.getdata()
            new_data = []
            for item in datas:
                # 如果像素的RGB值都大于200，则将该像素的透明度设为0
                if all(channel < 10 for channel in item[:3]):
                    new_data.append((item[0], item[1], item[2], 0))
                else:
                    new_data.append(item)
            
            img.putdata(new_data)
            
            # 转换为PNG格式并保存
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")
            img.save(output_path, "PNG")
            
            print("转换完成：{}".format(output_path))

# 调用函数进行转换
convert_images(input_dir, output_dir)