import cv2
from PIL import Image
import os
import shutil
#读取目标图片
target = cv2.imread(r"D:\\Downlond\\image.png")

def match(temp_file):
    #读取模板图片
    template = cv2.imread(temp_file)
    #获得模板图片的高宽尺寸
    # theight, twidth = template.shape[:2]
    #执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)
    #归一化处理
    cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
    #寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置 , max_val, min_loc, max_loc 
    min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
    return abs(min_val)

dst_path=r"D:\\Downlond\\233"
dirs = os.listdir(r"D:\\Downlond\\images")
count=0
for k in dirs:
    if(k.endswith('png')):
        count+=1
        print("processing on pic"+str(count))
        real_path=os.path.join(r"D:\\Downlond\\images",k)
        rect=match(real_path)
        if rect>1e-10:
            print(rect)
            shutil.move(real_path,dst_path)
    else:
        continue