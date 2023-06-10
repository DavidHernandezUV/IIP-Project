import numpy as np


def get_percentiles(image, k, start=0, end=100):
    step = (end - start) / (k - 1)
    percentiles = np.arange(start, end + step, step)
    percentiles_values = np.percentile(image, percentiles)
    return percentiles_values


def histogram_matching(image_src, image_ref, k):
    x1 = get_percentiles(image_src, k)
    x2 = get_percentiles(image_ref, k)
    return np.interp(image_src, x1, x2)
