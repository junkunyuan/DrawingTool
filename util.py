import numpy as np
import yaml
from yaml.loader import Loader


def use_var(dataitems):
    """Judge the format of variance.
    Args:
        dataitems ([type]): data.

    Returns:
        [bool]: if data variance is not appropriate, like None or has different length with data, return False"""
    for item in dataitems:
        if item.var is None:
            return False
        else:
            if not len(item.var) == len(item.data):
                return False
    return True


def mm_datas(dataitems, low=1, up=1):
    """Get the maximum and minimum value of the data items."""
    mins, maxs = [], []
    for item in dataitems:
        mins.append(item.min)
        maxs.append(item.max)
    mins = min(mins) - low
    maxs = max(maxs) + up
    return mins, maxs


def init_yticks(dataitems, interval=1, low=1, up=1):
    """
    Set the yticks by using the data information.
    Args:
        dataitems ([type]): data.
        interval: interval of yticks.
        low (int, optional): difference between the lower bound of yticks and the minimum data value. Default: 1.
        up (int, optional): difference between the maximum data value and the upper bound of yticks. Default: 1.
    Returns:
        [list]: the displayed yticks.
    """
    mins, maxs = mm_datas(dataitems, low, up)
    mins_int = int(mins)
    maxs_int = int(maxs) + 1
    maxs_int = maxs_int + interval - (maxs_int - mins_int) % interval
    yticks = np.arange(mins_int, maxs_int + 1, interval)
    return yticks


def loadcfg(cfgpath):
    """Load config."""
    with open(cfgpath, 'r', encoding='utf-8') as f:
        contents = yaml.load(f.read(), Loader=yaml.FullLoader)
    return contents
