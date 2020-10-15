import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from matrix_operations import rotate
from grid import Grid

def ring_mask(img, r1, r2):
    H, W = img.shape
    x, y = np.meshgrid(np.arange(W), np.arange(H))
    d2 = (x - 256)**2 + (y - 256)**2
    mask = d2 < (r1)**2
    mask1 = d2 > (r2)**2
    img_masked_ring = np.copy(img)
    img_masked_ring = np.ma.array(img_masked_ring, mask = mask)
    img_masked_ring = np.ma.array(img_masked_ring, mask = mask1)
    return img_masked_ring

def ring_logical_mask(frame_size, r1, r2):
    x, y = np.meshgrid(np.arange(frame_size), np.arange(frame_size))
    d2 = (x - 256)**2 + (y - 256)**2
    mask1 = d2 < (r1)**2
    mask2 = d2 > (r2)**2
    mask = np.logical_or(mask1,mask2)
    return mask

class GaussEllipse:
    def __init__(self,sigma_x=None,sigma_y=None,theta=None):
        self.sigma_x = sigma_x #[sigma_x] = 1 px
        self.sigma_y = sigma_y #[sigma_y] = 1 px 
        self.theta = theta #[theta] = 1 radian

    def array(self):
        return np.array([self.sigma_x,self.sigma_y,self.theta])

def gauss_2d(u,v,sigma_x,sigma_y,theta):
    a = np.cos(theta)**2/(2*sigma_x**2) + np.sin(theta)**2/(2*sigma_y**2)
    b = -np.sin(2*theta)/(4*sigma_x**2) + np.sin(2*theta)/(4*sigma_y**2)
    c = np.sin(theta)**2/(2*sigma_x**2) + np.cos(theta)**2/(2*sigma_y**2)
    return np.exp(- a*u**2 - 2*b*u*v - c*v**2)

def ellipse_parameters(ps,bottom_freq,upper_freq):
    def gauss_residual_function(init_guess):
        return np.sum((gauss_2d(u,v,*init_guess) - ps)**2)

    u,v = Grid(size=512).uv_meshgrid()
    init_guess = GaussEllipse()
    init_guess.sigma_x = (upper_freq-bottom_freq)/2
    init_guess.sigma_y = init_guess.sigma_x
    init_guess.theta = 0.
    gauss_residual_function(init_guess.array())
    fit_result = minimize(gauss_residual_function, init_guess.array(), method='L-BFGS-B', tol=1e-8).x
    return GaussEllipse(*fit_result)

def elliptic_mask(img,r1,r2,ellipse_params):
    a_bottom = r1
    b_bottom = r1*ellipse_params.sigma_y/ellipse_params.sigma_x
    a_upper = r2
    b_upper = r2*ellipse_params.sigma_y/ellipse_params.sigma_x
    H, W = img.shape
    x, y = np.meshgrid(np.arange(W), np.arange(H))
    x -= 256; y-= 256
    x_new, y_new = rotate(x,y,ellipse_params.theta)
    if (a_bottom==0 or b_bottom==0):
        mask = x_new**2/a_upper**2 + y_new**2/b_upper**2 > 1
    else:
        mask = np.logical_or(x_new**2/a_bottom**2 + y_new**2/b_bottom**2 < 1, x_new**2/a_upper**2 + y_new**2/b_upper**2 > 1)
    masked_img = np.ma.array(img,mask=mask)
    return masked_img

def elliptic_logical_mask(frame_size,r1,r2,ellipse_params):
    a_bottom = r1
    b_bottom = r1*ellipse_params.sigma_y/ellipse_params.sigma_x
    a_upper = r2
    b_upper = r2*ellipse_params.sigma_y/ellipse_params.sigma_x
    x, y = np.meshgrid(np.arange(frame_size), np.arange(frame_size))
    x -= 256; y-= 256
    x_new, y_new = rotate(x,y,ellipse_params.theta)
    if (a_bottom==0 or b_bottom==0):
        mask = x_new**2/a_upper**2 + y_new**2/b_upper**2 > 1
    else:
        mask = np.logical_or(x_new**2/a_bottom**2 + y_new**2/b_bottom**2 < 1, x_new**2/a_upper**2 + y_new**2/b_upper**2 > 1)
    return mask


