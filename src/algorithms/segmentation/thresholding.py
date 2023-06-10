import numpy as np

"""
The tau controls the velocity of the convergence, it is obtained using the histogram.
The tolerance controls the difference of the tau.
"""


def thresholding(tolerance, current_tau, image):
    while True:

        # Threshold the image using the current threshold tau
        segmentation = image >= current_tau
        # Calculate the mean values for foreground and background regions
        mBG = image[np.multiply(image > 10, segmentation == 0)].mean()
        mFG = image[np.multiply(image > 10, segmentation == 1)].mean()

        # Re calculate the new threshold value
        new_tau = 0.5 * (mBG + mFG)
        print(new_tau)
        # When convergence is reached, break the loop
        if np.abs(current_tau - new_tau) < tolerance:
            return segmentation
        else:
            current_tau = new_tau
