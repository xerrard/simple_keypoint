import glob

import cmath
import cv2
import os

import math
import torch
from torch.utils.data import DataLoader
from torchvision import transforms

from datasets import KeyPointDatasets
from model import KeyPointModel
import PIL

SIZE = 640,480


transforms_test = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((480,640)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.4372, 0.4372, 0.4373],
                         std=[0.2479, 0.2475, 0.2485])
])

# datasets_test = KeyPointDatasets(root_dir=".\data", transforms=transforms_test)
#
#
# dataloader_test = DataLoader(
#     datasets_test, batch_size=4, shuffle=True, collate_fn=datasets_test.collect_fn)

model = KeyPointModel()

model.load_state_dict(torch.load("weights/epoch_290_0.053.pt"))

img_list = glob.glob(os.path.join(".\\test\\images", "*.jpg"))

save_path = ".\output"

img_tensor_list = []
img_name_list = []

for i in range(len(img_list)):
    img_path = img_list[i]
    img_name = os.path.basename(img_path)
    img_name_list.append(img_name)

    img = cv2.imread(img_path)
    img_tensor = transforms_test(img)
    img_tensor_list.append(img_tensor)

img_tensor_list = torch.stack(img_tensor_list, 0)

print(img_tensor_list.shape)

output = model(img_tensor_list)

print(output.shape)

bs = img_tensor_list.shape[0]

succ_count = 0

for i in range(bs):
    img_path = img_list[i]
    img = cv2.imread(img_path)

    point_ratio = output[i]

    # print(point_ratio.shape)

    x, y = SIZE[0] * point_ratio[0], SIZE[1] * point_ratio[1]

    x = int(x.item())
    y = int(y.item())

    # print(x, y)

    cv2.circle(img, (x, y), 5, (0, 0, 255), thickness=-1)

    label_X = int(img_name_list[i].split('_')[2])
    label_Y = int(img_name_list[i].split('_')[3])
    between = math.sqrt(pow(label_X - x,2) + pow(label_Y - y,2))
    if int(between) < 60:
        succ_count = succ_count + 1

    print(".\output\%s_out.jpg" % (img_name_list[i]) + " x"+ str(x) + " y" + str(y) + '.jpg')

    cv2.imwrite(".\output\%s_out" % (img_name_list[i]) + " x"+ str(x) + " y" + str(y) + '.jpg', img)

print("成功%d次，成功率%.2f%%" % (succ_count,succ_count/bs*100))
