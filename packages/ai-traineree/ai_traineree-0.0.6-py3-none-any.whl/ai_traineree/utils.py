import os
import torch

from numpy import ndarray
from pathlib import Path
from typing import Any, List, Tuple, Union


def to_tensor(x) -> torch.Tensor:
    if isinstance(x, torch.Tensor):
        return x
    elif isinstance(x, ndarray):
        return torch.from_numpy(x)
    elif isinstance(x, list) and isinstance(x[0], torch.Tensor):
        return torch.stack(x)
    else:
        return torch.tensor(x)


def save_gif(path, images: List[ndarray]) -> None:
    print(f"Saving as a gif to {path}")
    from PIL import Image
    imgs = [Image.fromarray(img[::2, ::2]) for img in images]  # Reduce /4 size; pick w/2 h/2 pix

    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    imgs[0].save(path, save_all=True, append_images=imgs[1:], optimize=True, quality=85)


def str_to_number(s: str) -> Union[int, float]:
    "Smartly converts string either to an int or float"
    return int(s) if "." not in s else float(s)


def str_to_list(s: str) -> Tuple:
    """Converts a string list of numbers into a evaluated list.

    Example:
        >>> str_to_list('[1, 2, 3]')
        [1, 2, 3]
        >>> str_to_list('2.5, 1')
        [2.5, 1]

    """
    if s[0] == '[' and s[-1] == ']':
        s = s[1:-1]
    elif s[0] == '[' or s[-1] == ']':
        raise ValueError(f"Passed a string `{s}` with uneven parathesis. Will not tolerate such disgrace.")

    return [str_to_number(num) for num in s.split(',')]


def str_to_tuple(s: str) -> Tuple:
    """Converts a string tuple of numbers into a evaluated tuple.

    Example:
        >>> str_to_tuple('(1, 2, 3)')
        (1, 2, 3)
        >>> str_to_tuple('2.5, 1')
        (2.5, 1)
        >>> str_to_tuple('(1,2,   3)')
        (1, 2, 3)

    """
    if s[0] == '(' and s[-1] == ')':
        s = s[1:-1]
    elif s[0] == '(' or s[-1] == ')':
        raise ValueError(f"Passed a string `{s}` with uneven parathesis. Will not tolerate such disgrace.")

    return tuple(map(str_to_number, s.split(",")))


def str_to_seq(s: str) -> Union[Tuple, List]:
    """Converts a string sequence of number into tuple or list.
    The distnction is based on the surrounding brackets. If no brackets detected then it attempts to cast to tuple.

    Example:
        >>> str_to_seq('(1, 2, 3)')
        (1, 2, 3)
        >>> str_to_seq('2.5, 1')
        (2.5, 1)
        >>> str_to_seq('[2.5, 1]')
        [2.5, 1]

    """
    if s[0] == "[":
        return str_to_list(s)
    else:
        return str_to_tuple(s)


def to_numbers_seq(x: Any) -> Union[Tuple, List]:
    if isinstance(x, (tuple, list)):
        return x
    elif isinstance(x, str):
        return str_to_seq(x)
    elif isinstance(x, (int, float)):
        return (x,)
    else:
        raise ValueError(f"Value `{x}` has unsporrted type for casting to a sequence of numbers. Please report, or fix.")
