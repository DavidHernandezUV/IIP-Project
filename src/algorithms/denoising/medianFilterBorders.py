import numpy as np


def meddian_filter_border(image):
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
    result = get_borders(filtered_image)
    return result[3]


def get_borders(filtered_image):
    dfdx = dfdy = dfdz = np.zeros_like(filtered_image)
    for x in range(1, filtered_image.shape[0] - 2):
        for y in range(1, filtered_image.shape[1] - 2):
            for z in range(1, filtered_image.shape[2] - 2):
                dfdx[x, y, z] = filtered_image[x + 1, y, z] - \
                    filtered_image[x - 1, y, z]
                dfdy[x, y, z] = filtered_image[x, y + 1, z] - \
                    filtered_image[x, y - 1, z]
                dfdz[x, y, z] = filtered_image[x, y, z + 1] - \
                    filtered_image[x, y, z - 1]

    magnitude = np.sqrt(np.power(dfdx, 2) +
                        np.power(dfdy, 2) + np.power(dfdz, 2))

    return [dfdx, dfdy, dfdz, magnitude]
