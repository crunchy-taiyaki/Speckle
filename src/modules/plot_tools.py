import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.ndimage
from scipy.ndimage.interpolation import geometric_transform
from masks import ring_mask

def define_ylim(image):
    masked_image = ring_mask(image.values, image.b_bound, image.up_bound)
    ymin = np.min(masked_image)
    ymax = np.max(masked_image)
    return ymin,ymax

def plot_rings_borders(x_center,y_center,r1,r2):
    bottom_ring=plt.Circle((x_center,y_center), r1, color='orange', fill=False)
    upper_ring=plt.Circle((x_center,y_center), r2, color='orange', fill=False)
    plt.gcf().gca().add_artist(bottom_ring)
    plt.gcf().gca().add_artist(upper_ring)


def to_polar(img, origin, max_radius, order=1):
    """
    Transform img to its polar coordinate representation.

    order: int, default 1
        Specify the spline interpolation order. 
        High orders may be slow for large images.
    """
    # max_radius is the length of the diagonal 
    # from a corner to the mid-point of img.

    def transform(coords):
        # Put coord[1] in the interval, [-pi, pi]
        theta = 2*np.pi*coords[1] / (img.shape[1] - 1.)

        # Then map it to the interval [0, max_radius].
        #radius = float(img.shape[0]-coords[0]) / img.shape[0] * max_radius
        radius = max_radius * coords[0] / img.shape[0]

        i = origin[0] + radius*np.sin(theta)
        j = origin[1] + radius*np.cos(theta)
        return i,j

    polar = geometric_transform(img, transform, order=order)
    rads = max_radius * np.linspace(0,1,img.shape[0])
    angs = np.linspace(0, 2*np.pi, img.shape[1])
    return polar, angs

def angle_idx(max_idx,angle_in_deg):
    angle_in_rad = angle_in_deg*np.pi/180.0
    size = max_idx
    angle_idx = int((size-1)*angle_in_rad/(2*np.pi) + (size-1)/2)
    return angle_idx

def radius_idx(freq):
    radius_idx = int(freq/np.sqrt(2)) 
    return radius_idx






