import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from grid import Grid
from masks import GaussEllipse, ring_mask,ring_logical_mask,elliptic_mask,elliptic_logical_mask

class FitResult():
    def __init__(self,flag):
        self.flag = flag
        self.f_ar = None
        self.residuals = None
        self.I1_ar = None
        self.dm21_ar = None
        self.x2_ar = None
        self.y2_ar = None
        # third star parameters
        self.dm31_ar = None
        self.x3_ar = None
        self.y3_ar = None

    def read_i_xy_dm_freq_from(self,result_folder_path):
        path = result_folder_path
        self.I1_ar = np.load(path + '\\I1_ar.npy')
        self.dm21_ar = np.load(path + '\\dm21_ar.npy')
        self.x2_ar = np.load(path + '\\x2_ar.npy')
        self.y2_ar = np.load(path + '\\y2_ar.npy')
        self.f_ar = np.load(path + '\\f_ar.npy')
        self.residuals = np.load(path + '\\residuals.npy')
        if(self.flag=='triple'):
            self.dm31_ar = np.load(path + '\\dm31_ar.npy')
            self.x3_ar = np.load(path + '\\x3_ar.npy')
            self.y3_ar = np.load(path + '\\y3_ar.npy')


class Fit:
    def __init__(self,ps,model,initial_parameters,uv_grid,\
                 bottom_freq_border,upper_freq_border,bandwidth,\
                 flag,zone_flag=None,ellipse_params=None):
        self.bandwidth = bandwidth
        self.bottom_freq_border = bottom_freq_border
        self.upper_freq_border = upper_freq_border
        self.ps = ps #ObjSpectrum()
        self.init_guess = initial_parameters
        self.model = model
        self.uv_grid = uv_grid
        self.flag = flag
        self.zone_flag = zone_flag
        if (self.zone_flag == 'ellipse'):
            self.ellipse_params = ellipse_params #GaussEllipse()
        self.result = FitResult(self.flag)

    def ring_zones(self,mask,size):
        f_ar_lenght = len(self.result.f_ar)
        for i in range(f_ar_lenght):
            mask[i] = ring_logical_mask(size,self.result.f_ar[i],self.result.f_ar[i]+self.bandwidth)

    def elliptic_zones(self,mask,size):
        f_ar_lenght = len(self.result.f_ar)
        for i in range(f_ar_lenght):
            mask[i] = elliptic_logical_mask(size,self.result.f_ar[i],self.result.f_ar[i]+self.bandwidth)

 
    def plot_fit_izone(self,i,mask,fit_result):
        u,v = self.uv_grid
        freq_axis = np.arange(-256.0,256.0)
        zone_values = np.ma.array(self.ps.values,mask=mask[i])
        init_guess_values = np.ma.array(self.model(u,v,*self.init_guess.array()),mask=mask[i])
        model_values = np.ma.array(self.model(u,v,*fit_result.x),mask=mask[i])
        ymin=0.; ymax=1.
        plt.figure()
        plt.plot(freq_axis, self.ps.values[256,:],label='all data')
        plt.plot(freq_axis, zone_values[256,:],label='data')
        plt.plot(freq_axis, init_guess_values[256,:], label='init guess')
        plt.plot(freq_axis, model_values[256,:],label='model')
        #plt.ylim(ymin,ymax)
        plt.yscale('log')
        plt.title('x projection')
        plt.legend()

        plt.figure()
        plt.plot(freq_axis, self.ps.values[:,256],label='all data')
        plt.plot(freq_axis, zone_values[:,256],label='data')
        plt.plot(freq_axis, init_guess_values[:,256], label='init guess')
        plt.plot(freq_axis, model_values[:,256],label='model')
        #plt.ylim(ymin,ymax)
        plt.yscale('log')
        plt.title('y projection')
        plt.legend()
        plt.show()

    def fit_i_xy_dm(self):

        def residual_function(init_guess):
        #This function must be defined here
        #because she needs to know the model as the atribute of Fit class,
        # therefore, (self) should be determined above,
        #  and at the same time, the self can not be set as a function argument,
        #  because the residual function should has only one argument,
        #   the vector initial_guess.
            masked_model = np.ma.array(self.model(u,v,*init_guess),mask=mask[i])
            return np.sum((masked_model - zone_values)**2)

        #init data
        u,v = self.uv_grid
        self.result.f_ar = np.arange(self.bottom_freq_border,self.upper_freq_border,self.bandwidth)
        f_ar_lenght = len(self.result.f_ar)
        self.result.I1_ar = np.zeros(f_ar_lenght)
        self.result.dm21_ar = np.zeros(f_ar_lenght)
        self.result.x2_ar = np.zeros(f_ar_lenght)
        self.result.y2_ar = np.zeros(f_ar_lenght)
        self.result.residuals = np.zeros(f_ar_lenght)

        if(self.flag == 'triple'):
            self.result.dm31_ar = np.zeros(f_ar_lenght)
            self.result.x3_ar = np.zeros(f_ar_lenght)
            self.result.y3_ar = np.zeros(f_ar_lenght)
        
        size = self.ps.values.shape[0]
        mask = np.ma.array(np.zeros((f_ar_lenght,size,size)))
        if (self.zone_flag == 'ellipse'):
            self.elliptic_zones(mask,size)
        else:
            self.ring_zones(mask,size)

        #fitting
        print('start fitting dm and xy')
        print('iteration: .. from ',len(mask))
        for i in range(len(mask)):
            print(i)
            zone_values = np.ma.array(self.ps.values,mask=mask[i])
            scale = np.sqrt(np.nanmean(zone_values))
            self.init_guess.I1 = scale
            fit_result = minimize(residual_function, self.init_guess.array(), method='L-BFGS-B', tol=1e-8)
            if(self.flag=='triple'):
                self.result.I1_ar[i] = fit_result.x[0]
                self.result.dm21_ar[i] = fit_result.x[1]
                self.result.x2_ar[i] = fit_result.x[2]
                self.result.y2_ar[i] = fit_result.x[3]
                self.result.dm31_ar[i] = fit_result.x[4]
                self.result.x3_ar[i] = fit_result.x[5]
                self.result.y3_ar[i] = fit_result.x[6]
                self.result.residuals[i] = np.sqrt(np.sum((self.model(u,v,\
                                                   self.result.I1_ar[i],self.result.dm21_ar[i],self.result.x2_ar[i],self.result.y2_ar[i],\
                                                   self.result.dm31_ar[i],self.result.x3_ar[i],self.result.y3_ar[i])-zone_values)**2)/np.sum(zone_values**2))
            else:
                self.result.I1_ar[i] = fit_result.x[0]
                self.result.dm21_ar[i] = fit_result.x[1]
                self.result.x2_ar[i] = fit_result.x[2]
                self.result.y2_ar[i] = fit_result.x[3]
                self.result.residuals[i] = np.sqrt(np.sum((self.model(u,v,self.result.I1_ar[i],self.result.dm21_ar[i],self.result.x2_ar[i],self.result.y2_ar[i])
                                                   - zone_values)**2)/np.sum(zone_values**2))

            #self.plot_fit_izone(i,mask,fit_result)

    def save_i_xy_dm_freq(self,result_folder_path):
        path = result_folder_path
        np.save(path + '\\I1_ar.npy',self.result.I1_ar)
        np.save(path + '\\dm21_ar.npy',self.result.dm21_ar)
        np.save(path + '\\x2_ar.npy',self.result.x2_ar)
        np.save(path + '\\y2_ar.npy',self.result.y2_ar)
        np.save(path + '\\f_ar.npy',self.result.f_ar)
        np.save(path + '\\residuals.npy',self.result.residuals)
        if(self.flag=='triple'):
            np.save(path + '\\dm31_ar.npy',self.result.dm31_ar)
            np.save(path + '\\x3_ar.npy',self.result.x3_ar)
            np.save(path + '\\y3_ar.npy',self.result.y3_ar)

    def read_i_xy_dm_freq_from(self,result_folder_path):
        path = result_folder_path
        self.result.I1_ar = np.load(path + '\\I1_ar.npy')
        self.result.dm21_ar = np.load(path + '\\dm21_ar.npy')
        self.result.x2_ar = np.load(path + '\\x2_ar.npy')
        self.result.y2_ar = np.load(path + '\\y2_ar.npy')
        self.result.f_ar = np.load(path + '\\f_ar.npy')
        if(self.flag=='triple'):
            self.result.dm31_ar = np.load(path + '\\dm31_ar.npy')
            self.result.x3_ar = np.load(path + '\\x3_ar.npy')
            self.result.y3_ar = np.load(path + '\\y3_ar.npy')

 

  





 






