
import numpy as np
from src.algorithms.neighbors import get_neighbors


def region_growing(x, y, z, tolerance, image):
    mean_value_cluster = image[x, y, z]
    segmentation = np.zeros_like(image)
    rows_image = image.shape[0]
    radious = 1

    while radious < rows_image:

        neighbors = get_neighbors(image, x, y, radious, 0, image.shape[2]-1)

        for neighbor_index in neighbors:
            x_index = neighbor_index[0]
            y_index = neighbor_index[1]
            z_index = neighbor_index[2]

            if np.abs(mean_value_cluster - image[x_index, y_index, z_index]) < tolerance:
                segmentation[x_index, y_index, z_index] = 1
            else:
                segmentation[x_index, y_index, z_index] = 0

        radious = radious + 1
        #mean_value_cluster = image[segmentation == 1].mean()
    return segmentation
