import numpy as np
from scipy.signal import argrelmax


def get_white_matter(image):
    hist, bins = np.histogram(image[image > 10].flatten(), bins=100)
    peaks_indices = argrelmax(hist)[0]
    max_peak_values = bins[peaks_indices]
    get_white_matter_peak = max_peak_values[1] if len(
        max_peak_values) > 1 else None
    return get_white_matter_peak


def white_stripe(image):
    rescaled_image = image / get_white_matter(image)
    return rescaled_image
