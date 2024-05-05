from typing import Tuple

import torch
from .utils import rgb_to_lab, lab_to_rgb


def get_mean_and_std(x):
    # X is sure to be channel first. compute mean and std
    # across H and W
    x_std, x_mean = torch.std_mean(x, dim=(-2, -1))
    x_mean = x_mean.view(-1)
    x_std = x_std.view(-1)

    return x_mean, x_std


def preprocess_input(img: torch.Tensor) -> Tuple[torch.Tensor, bool]:
    """
    Check if image is channel first. If not, convert to channel first
    then convert to Float and scale to [0, 1]

    Args:
        image (torch.Tensor): Image, can be 3 dims or 4 dims (batch images)

    Returns:
        Tuple[torch.Tensor, bool]:
            torch.Tensor: Image have channel first
            bool: True if image is converted, False if image is already channel first

    """
    is_channel_last = False
    if img.ndim == 4 and img.shape[1] != 3:
        image = img.permute(0, 3, 1, 2)
        is_channel_last = True
    elif img.ndim == 3 and img.shape[0] != 3:
        img =  img.permute(2, 0, 1)
        is_channel_last = True

    img = img.float()
    img = (img - img.min()) / (img.max() - img.min())
    return img, is_channel_last


def color_transfer_pytorch(
    src: torch.Tensor,
    target: torch.Tensor,
    inplace: bool = False,
) -> torch.Tensor:
    """
    Transfer color of src image based on the color of target

    Args:
        src (torch.Tensor): Source image, with shape `(*, 3, H, W)`
        target (torch.Tensor): Target image, with shape `(*, 3, H, W)`

    Returns:
        torch.Tensor: Color transfered image, output is in range `[0, 1]`
    """
    if src.ndim != target.ndim:
        raise ValueError((
            "`src` must have the same dimension as `target`"
            f", Got {src.ndim} and {target.ndim}"
        ))

    # Must be channel first
    src, src_ch_last = preprocess_input(src)
    target, _ = preprocess_input(target)

    src = rgb_to_lab(src)
    target = rgb_to_lab(target)

    src_mean, src_std = get_mean_and_std(src)
    target_mean, target_std = get_mean_and_std(target)

    std_ratio = target_std / src_std

    if not inplace:
        image = src.clone()
    else:
        image = src

    image = image.float()

    for c in range(3):
        if image.ndim == 4:
            image[:, c, ...] = (image[:, c, ...] - src_mean[c]) * std_ratio[c] + target_mean[c]
        else:
            image[c, ...] = (image[c, ...] - src_mean[c]) * std_ratio[c] + target_mean[c]


    image = lab_to_rgb(image)

    if src_ch_last:
        # Convert back to channel last
        image = (
            image.permute(0, 2, 3, 1)
            if image.ndim == 4
            else image.permute(1, 2, 0)
        )

    # Clip in range 0 255    
    # image = image.clamp(0, 255)
    return image
