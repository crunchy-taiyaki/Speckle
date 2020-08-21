import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def ring_mask(img, r1, r2):
    H, W = img.shape
    x, y = np.meshgrid(np.arange(W), np.arange(H))
    d2 = (x - 256)**2 + (y - 256)**2
    mask = d2 < r1**2
    mask1 = d2 > r2**2
    img_masked_ring = np.copy(img)
    img_masked_ring = np.ma.array(img_masked_ring, mask = mask)
    img_masked_ring = np.ma.array(img_masked_ring, mask = mask1)
    return img_masked_ring




class BinaryInitialParameters:

    def __init__(self,dm21,x2,y2):
        self.I1 = None
        self.dm21 = dm21
        self.x2 = x2
        self.y2 = y2

    def array(self):
        return np.array([self.I1,self.dm,self.x2,self.y2])


class TripleInitialParameters:

    def __init__(self,dm21,dm31,x2,y2,x3,y3):
        self.I1 = None
        self.dm21 = dm21
        self.dm31 = dm31
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def array(self):
        return np.array([self.I1,self.dm21,self.dm31,self.x2,self.y2,self.x3,self.y3])


class Grid:

    def __init__(self,size=512):
        self.size = size

    def uv_meshgrid(self):
        U = np.arange(0,self.size)/self.size
        V = np.arange(0,self.size)/self.size
        u,v = np.meshgrid(U,V)
        return u,v


class Fit:

    def __init__(self,ps,model,initial_parameters,uv_grid,bandwidth=10,bottom_freq_border=5,upper_freq_border=210,flag='triple'):
        self.bandwidth = bandwidth
        self.bottom_freq_border = bottom_freq_border
        self.upper_freq_border = upper_freq_border
        self.ps = ps
        self.init_guess = initial_parameters
        self.model = model
        self.uv_grid = uv_grid
        self.flag = flag
        self.f_ar = None
        self.I1_ar = None
        self.dm21_ar = None
        self.x2_ar = None
        self.y2_ar = None
        self.r12_ar = None
        self.psi2_ar = None
        # third star parameters
        self.dm31_ar = None
        self.x3_ar = None
        self.y3_ar = None
        self.r13_ar = None
        self.psi3_ar = None

    def get_i_xy_dm(self):

        def residual_function(init_guess):
        #This function must be defined here
        #because she needs to know the model as the atribute of Fit class,
        # therefore, (self) should be determined above,
        #  and at the same time, the self can not be set as a function argument,
        #  because the residual function should has only one argument,
        #   the vector initial_guess.
            return np.sum((self.model(u,v,*init_guess) - ydata)**2)

        u,v = self.uv_grid
        self.f_ar = np.arange(self.bottom_freq_border,self.upper_freq_border,self.bandwidth)
        f_ar_lenght = len(self.f_ar)
        self.I1_ar = np.zeros(f_ar_lenght)
        self.dm21_ar = np.zeros(f_ar_lenght)
        self.x2_ar = np.zeros(f_ar_lenght)
        self.y2_ar = np.zeros(f_ar_lenght)

        if(self.flag=='triple'):
            self.dm31_ar = np.zeros(f_ar_lenght)
            self.x3_ar = np.zeros(f_ar_lenght)
            self.y3_ar = np.zeros(f_ar_lenght)

        #fitting
        for i in range(f_ar_lenght):
            print('freq:', self.f_ar[i])
            ydata = ring_mask(self.ps,self.f_ar[i],self.f_ar[i]+self.bandwidth)
            scale = np.sqrt(np.nanmean(ydata))
            self.init_guess.I1 = scale
            fit_result = minimize(residual_function, self.init_guess.array(), method='L-BFGS-B', tol=1e-8)

            if(self.flag=='triple'):
                self.I1_ar[i] = fit_result.x[0]
                self.dm21_ar[i] = fit_result.x[1]
                self.dm31_ar[i] = fit_result.x[2]
                self.x2_ar[i] = fit_result.x[3]
                self.y2_ar[i] = fit_result.x[4]
                self.x3_ar[i] = fit_result.x[5]
                self.y3_ar[i] = fit_result.x[6]
            else:
                self.I1_ar[i] = fit_result.x[0]
                self.dm21_ar[i] = fit_result.x[1]
                self.x2_ar[i] = fit_result.x[2]
                self.y2_ar[i] = fit_result.x[3]

    def save_i_xy_dm_freq(self,result_folder_path):
        path = result_folder_path
        np.save(path + '\\I1_ar.npy',self.I1_ar)
        np.save(path + '\\dm21_ar.npy',self.dm21_ar)
        np.save(path + '\\x2_ar.npy',self.x2_ar)
        np.save(path + '\\y2_ar.npy',self.y2_ar)
        np.save(path + '\\f_ar.npy',self.f_ar)
        if(self.flag=='triple'):
            np.save(path + '\\dm31_ar.npy',self.dm31_ar)
            np.save(path + '\\x3_ar.npy',self.x3_ar)
            np.save(path + '\\y3_ar.npy',self.y3_ar)

    def load_i_xy_dm_freq(self,result_folder_path):
        path = result_folder_path
        self.I1_ar = np.load(path + '\\I1_ar.npy')
        self.dm21_ar = np.load(path + '\\dm21_ar.npy')
        self.x2_ar = np.load(path + '\\x2_ar.npy')
        self.y2_ar = np.load(path + '\\y2_ar.npy')
        self.f_ar = np.load(path + '\\f_ar.npy')
        if(self.flag=='triple'):
            self.dm31_ar = np.load(path + '\\dm31_ar.npy')
            self.x3_ar = np.load(path + '\\x3_ar.npy')
            self.y3_ar = np.load(path + '\\y3_ar.npy')

    def xy_to_r_psi(self):
        x1 = 256.
        y1 = 256.
        if(self.flag=='triple'):
            self.r13_ar = np.sqrt((self.x3_ar-x1)**2 + (self.y3_ar-y1)**2)
            self.psi3_ar = np.arctan2(self.y3_ar-y1,self.x3_ar-x1)*180.0/np.pi
        self.r12_ar = np.sqrt((self.x2_ar-x1)**2 + (self.y2_ar-y1)**2)
        self.psi2_ar = np.arctan2(self.y2_ar-y1,self.x2_ar-x1)*180.0/np.pi

 

  





 






