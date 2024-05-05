# A demo to demonstrate multi images color transfer
import os
import torch
import numpy as np
import cv2
from color_transfer import color_transfer_pytorch

def load_resize(path):
    img = cv2.imread(path)
    return cv2.resize(img, (352, 352))


src1 = load_resize("examples/1/src.jpeg")
target1 = load_resize("examples/1/target.png")

src2 = load_resize("examples/2/src.jpeg")
target2 = load_resize("examples/2/target.png")

src3 = load_resize("examples/3/src.png")
target3 = load_resize("examples/3/target.png")

src = np.stack([src1, src2, src3], axis=0)
target = np.stack([target1, target2, target3], axis=0)

src = src.transpose(0, 3, 1, 2)
target = target.transpose(0, 3, 1, 2)

src = torch.tensor(src, dtype=torch.float64)
target = torch.tensor(target, dtype=torch.float64)

outs = color_transfer_pytorch(src, target)
print(outs.shape)

outs = outs.numpy().transpose(0, 2, 3, 1) * 255
outs= outs.astype('uint8')

for i in range(outs.shape[0]):
    out = outs[i]
    cv2.imwrite(f'examples/{i+1}/out.jpeg', out)
