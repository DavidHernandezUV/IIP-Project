def rescaling(image):

    min = image.min()
    max = image.max()

    rescaled_image = ((image - min)/max-min)

    return rescaled_image
