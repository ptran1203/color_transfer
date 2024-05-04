# Performance comparision between this repo
# and https://github.com/chia56028/Color-Transfer-between-Images/blob/master/color_transfer.py
import time
import cv2
import numpy as np
from color_transfer.numpy import get_mean_and_std, color_transfer


def color_transfer_chia56028(src, target):
    src = cv2.cvtColor(src ,cv2.COLOR_BGR2LAB)
    target = cv2.cvtColor(target ,cv2.COLOR_BGR2LAB)
    s_mean, s_std = get_mean_and_std(src)
    t_mean, t_std = get_mean_and_std(target)

    height, width, channel = src.shape
    for i in range(0,height):
        for j in range(0,width):
            for k in range(0,channel):
                x = src[i,j,k]
                x = ((x-s_mean[k])*(t_std[k]/s_std[k]))+t_mean[k]
                # round or +0.5
                x = round(x)
                # boundary check
                x = 0 if x<0 else x
                x = 255 if x>255 else x
                src[i,j,k] = x


    src = cv2.cvtColor(src,cv2.COLOR_LAB2BGR)
    return src


def run_benchmark(func, iters):
    times = []
    
    src = cv2.imread("../examples/1/src.jpeg")
    target = cv2.imread("../examples/1/target.png")

    for i in range(iters):
        start = time.time()
        func(src, target)
        elapsed = time.time() - start

        times.append(elapsed)

    return times


if __name__ == '__main__':
    iters = 100
    times_1 = run_benchmark(color_transfer_chia56028, iters)
    times_2 = run_benchmark(color_transfer, iters)

    mean_1 = np.mean(times_1)
    mean_2 = np.mean(times_2)

    print(f"Benchmark result of {iters} runs:")
    print(f"color_transfer_chia56028: {mean_1:.3f} seconds (Average)")
    print(f"color_transfer: {mean_2:.3f} seconds (Average)")
