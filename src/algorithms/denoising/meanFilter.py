import numpy as np
from src.algorithms.neighbors import get_neighbors


def mean_filter(image):
    rows_image = image.shape[0]
    cols_image = image.shape[1]
    sum_values = 0
    filtered_image = np.zeros_like(image)
    for row in range(rows_image):
        for col in range(cols_image):
            neighbors = get_neighbors(image, row, col, 1, 0, 0)
            for neighbor in neighbors:
                x_index = neighbor[0]
                y_index = neighbor[1]
                sum_values += image[x_index, y_index]
            filtered_image[row, col] = sum_values / len(neighbors)
            sum_values = 0
    return filtered_image
