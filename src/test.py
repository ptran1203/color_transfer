
import os
import cv2
from color_transfer import color_transfer
from color_transfer import color_transfer_pytorch
from color_transfer.utils import rgb_to_lab, lab_to_rgb


src = cv2.imread("../examples/1/src.jpeg")
target = cv2.imread("../examples/1/target.png")

out = color_transfer(src.copy(), target)


cv2.imwrite("../examples/1/output.jpeg", out)


# Test pytorch
import torch

src = torch.from_numpy(src)
target = torch.from_numpy(target)

out_torch = color_transfer_pytorch(src, target)
# out_torch = lab_to_rgb(
#     rgb_to_lab((src.float() / 255.0).permute(2, 0, 1)), clip=False
# ).permute(1, 2, 0)
out_torch = out_torch.numpy() * 255.0
out_torch =out_torch.astype('uint8')
# print(out_torch)

cv2.imwrite("test.jpg", out_torch)

diff = (out - out_torch).mean()

print(diff)