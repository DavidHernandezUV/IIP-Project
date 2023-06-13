# Segmentation algorithms
from src.algorithms.segmentation.gMM import gaussian_mixture_model
from src.algorithms.segmentation.kMeans import k_means
from src.algorithms.segmentation.regionGrowing import region_growing
from src.algorithms.segmentation.thresholding import thresholding
# Denoising Algorithms
from src.algorithms.denoising.meanFilter import mean_filter
from src.algorithms.denoising.medianFilter import median_filter
from src.algorithms.denoising.medianFilterBorders import meddian_filter_border
# Standarization Algorithms
from src.algorithms.standarization.zScore import z_score
from src.algorithms.standarization.whiteStripe import white_stripe
from src.algorithms.standarization.histogramMatching import histogram_matching
from src.algorithms.standarization.rescaling import rescaling


class algorithmsCollection:

    # Segmentation
    def gaussian_mixture_model(image):
        return gaussian_mixture_model(image)

    def k_means(image, groups):
        return k_means(image, groups)

    def region_growing(x, y, z, tolerance, image):
        return region_growing(x, y, z, tolerance, image)

    def thresholding(tolerance, current_tau, image):
        return thresholding(tolerance, current_tau, image)

    # Denoising

    def mean_filter(image):
        return mean_filter(image)

    def median_filter(image):
        return median_filter(image)

    def meddian_filter_border(image):
        return meddian_filter_border(image)

    # Standarization
    def z_score(image):
        return z_score(image)

    def white_stripe(image):
        return white_stripe(image)

    def histogram_matching(image_src, image_ref, k):
        return histogram_matching(image_src, image_ref, k)

    def rescaling(image):
        return rescaling(image)
