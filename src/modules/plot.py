import matplotlib.pyplot as plt
import numpy as np
from masks import ring_mask

def define_ylim(image):
    masked_image = ring_mask(image.values, image.b_bound, image.up_bound)
    ymin = np.min(masked_image)
    ymax = np.max(masked_image)
    return ymin,ymax

def slice_image(image,x1,y1,x2,y2):
    x1+=256.0; x2+=256.0
    y1+=256.0; y2+=256.0
    projection = np.ones(512)*np.nan
    k = (y2-y1)/(x2-x1)
    for x in range(0, 511):
        y = int(k*(x-x1)+y1)
        if y > 0 and y < 512:
            projection[x] = image[x,y]
    return projection

def plot_rings_borders(x_center,y_center,r1,r2):
    bottom_ring=plt.Circle((x_center,y_center), r1, color='orange', fill=False)
    upper_ring=plt.Circle((x_center,y_center), r2, color='orange', fill=False)
    plt.gcf().gca().add_artist(bottom_ring)
    plt.gcf().gca().add_artist(upper_ring)




