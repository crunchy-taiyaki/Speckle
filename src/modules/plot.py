import matplotlib.pyplot as plt
import numpy as np
from masks import ring_mask

def define_ylim(image):
    masked_image = ring_mask(image.values, image.b_bound, image.up_bound)
    ymin = np.min(masked_image)
    ymax = np.max(masked_image)
    return ymin,ymax

def slice_image(image,x1,y1,x2,y2):
    size = image.shape[0]
    projection = np.ones(size)*np.nan
    k = (y2-y1)/(x2-x1)
    for x in range(0, size):
        y = int(x*k-x2*k+y2)
        if y < 512 and y>0:
            projection[x] = image[x,y]
    return projection




