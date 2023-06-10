def z_score(image):
    std = image[image > 10].std()
    mean = image[image > 10].mean()
    rescaled_image = (image - mean) / std
    print(std, mean)
    return rescaled_image
