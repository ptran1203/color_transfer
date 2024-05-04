import cv2
import numpy as np


def get_mean_and_std(x):
    x_mean, x_std = cv2.meanStdDev(x)
    x_mean = np.hstack(x_mean)
    x_std = np.hstack(x_std)
    return x_mean, x_std


def color_transfer(src: np.ndarray, target: np.ndarray) -> np.ndarray:
    """
    Transfer color of src image based on the color of target

    The math:
    ```
    
    ```
    """
    src = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB)

    src_mean, src_std = get_mean_and_std(src)
    target_mean, target_std = get_mean_and_std(target)

    std_ratio = target_std / src_std
    src_dtype = src.dtype

    image = src.copy().astype(float)
    image = (image - src_mean) * std_ratio + target_mean

    # Clip in range 0 255    
    image = image.clip(0, 255)

    image = image.astype(src_dtype)
    image = cv2.cvtColor(image,cv2.COLOR_LAB2BGR)

    return image
