import numpy as np


def k_means(image, groups):
    iterations = 60

    k_values = np.linspace(np.amin(image), np.amax(image), groups)

    for i in range(iterations):
        d_values = [np.abs(k - image) for k in k_values]
        segmentation = np.argmin(d_values, axis=0)

        for k in range(groups):
            k_values[k] = image[segmentation == k].mean()

    return segmentation
