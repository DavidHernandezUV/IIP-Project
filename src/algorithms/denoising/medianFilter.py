import numpy as np
from src.algorithms.neighbors import get_neighbors


def median_filter(image):
    rows_image = image.shape[0]
    cols_image = image.shape[1]

    filtered_image = np.zeros_like(image)
    for row in range(rows_image):
        for col in range(cols_image):
            neighbors = get_neighbors(image, row, col, 1, 0, 0)
            neighbors_values = np.array([])
            for neighbor in neighbors:
                x_index = neighbor[0]
                y_index = neighbor[1]
                neighbors_values = np.append(
                    neighbors_values, image[x_index, y_index])
            filtered_image[row, col] = np.median(neighbors_values)
    return filtered_image
