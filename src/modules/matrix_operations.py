import numpy as np
def rotate(x,y,angle): #angle in radians
    x_new = x*np.cos(angle) - y*np.sin(angle)
    y_new = x*np.sin(angle) + y*np.cos(angle)
    return x_new,y_new
