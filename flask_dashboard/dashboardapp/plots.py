import numpy as np


def get_histogram(data):
    # Get the histogram of the data
    hist, bin_edges = np.histogram(data)
    return hist, bin_edges