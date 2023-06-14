import numpy as np
from src.algorithms.neighbors import get_neighbors


def median_filter(image):
    filtered_image = np.zeros_like(image)
    for x in range(1, image.shape[0] - 2):
        for y in range(1, image.shape[1] - 2):
            for z in range(1, image.shape[2] - 2):
                avg = 0
                for dx in range(-1, 1):
                    for dy in range(-1, 1):
                        for dz in range(-1, 1):
                            avg = avg + image[x + dx, y + dy, z + dz]
                filtered_image[x + 1, y + 1, z + 1] = avg / 27
    return filtered_image
