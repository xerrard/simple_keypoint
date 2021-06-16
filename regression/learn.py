import os

# import cv2
# # img_path = os.path.dirname(__file__)+"/data/images/hand_20210122115213_8158875406564319.jpg"
# img_path = ".\data\images\hand_20210122115213_8158875406564319.jpg"
# img = cv2.imread(img_path)  # 读取图像
# cv2.imshow('image',img)
# cv2.waitKey(0)
name = 'detection_succ_345_94_1613981511769.jpg'
x = name.split('_')[2];
y = name.split('_')[3];
print(x)
print(y)