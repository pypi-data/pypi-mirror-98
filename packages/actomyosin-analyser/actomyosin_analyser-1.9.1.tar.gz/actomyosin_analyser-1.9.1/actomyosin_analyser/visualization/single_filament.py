import numpy as np

def minimum_image_vectors_to_filament_coords(v: np.ndarray):
    shape = list(v.shape)
    shape[0] = shape[0] + 1
    coords = np.zeros(shape)
    coords[1:] = np.cumsum(v, axis=0)
    return coords
