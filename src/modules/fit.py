import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from file_reader import InputReader, FitParametersReader
from spectra_calculator import Data
from grid import Grid
from models import Models
from initial_parameters_builder import BinaryInitialParameters, BinaryInitialParametersFixDM, BinaryInitialParametersFixXY,\
                                       TripleInitialParameters, TripleInitialParametersFixDM, TripleInitialParametersFixXY               
from masks import ring_logical_mask, elliptic_logical_mask



class FitResult:
    def __init__(self,filename_config,fit_parameters_config):
        #read config file
        files = InputReader()
        files.read(filename_config)
        #read fit parameters from file
        input_fit_parameters = FitParametersReader()
        input_fit_parameters.read(fit_parameters_config)

        self.star_type = input_fit_parameters.star_type
        self.method = input_fit_parameters.method
        self.x2_value = input_fit_parameters.x2
        self.y2_value = input_fit_parameters.y2
        self.dm21_value = input_fit_parameters.dm21
        self.f_ar = None
        self.I1_ar = None
        self.dm21_ar = None
        self.x2_ar = None
        self.y2_ar = None
        if self.star_type == 'triple':
            self.x3_value = input_fit_parameters.x3
            self.y3_value = input_fit_parameters.y3
            self.dm21_value = input_fit_parameters.dm31
            self.dm31_ar = None
            self.x3_ar = None
            self.y3_ar = None

    def read(self,folder_path):
        path = folder_path
        self.f_ar = np.load(path + '\\f_ar.npy')
        self.I1_ar = np.load(path + '\\I1_ar.npy')
        self.dm21_ar = np.load(path + '\\dm21_ar.npy')
        self.x2_ar = np.load(path + '\\x2_ar.npy')
        self.y2_ar = np.load(path + '\\y2_ar.npy')
        if self.star_type == 'triple':
            self.dm31_ar = np.load(path + '\\dm31_ar.npy')
            self.x3_ar = np.load(path + '\\x3_ar.npy')
            self.y3_ar = np.load(path + '\\y3_ar.npy')

    def fill_from_fit(self,frequencies,fitted_parameters):
        self.f_ar = frequencies
        size = len(frequencies)
        if self.star_type == 'binary':
            if self.method == 'standart':
                self.I1_ar = fitted_parameters[:,0]
                self.dm21_ar = fitted_parameters[:,1]
                self.x2_ar = fitted_parameters[:,2]
                self.y2_ar = fitted_parameters[:,3]
            elif self.method == 'fix_dm':
                self.I1_ar = fitted_parameters[:,0]
                self.dm21_ar = np.ones(size)*self.dm21_value
                self.x2_ar = fitted_parameters[:,1]
                self.y2_ar = fitted_parameters[:,2]
            elif self.method == 'fix_xy':
                self.I1_ar = fitted_parameters[:,0]
                self.dm21_ar = fitted_parameters[:,1]
                self.x2_ar = np.ones(size)*self.x2_value
                self.y2_ar = np.ones(size)*self.y2_value
            else:
                print(self.method, "method doesn't exist. Please, enter one of these: standart, fix_dm, fix_xy")

        elif self.star_type == 'triple':
            if self.method == 'standart':            
                self.I1_ar = fitted_parameters[:,0]
                self.dm21_ar = fitted_parameters[:,1]
                self.x2_ar = fitted_parameters[:,2]
                self.y2_ar = fitted_parameters[:,3]
                self.dm31_ar = fitted_parameters[:,4]
                self.x3_ar = fitted_parameters[:,5]
                self.y3_ar = fitted_parameters[:,6]
            elif self.method == 'dm_fix':
                self.dm21_ar = self.dm21_value
                self.dm31_ar = self.dm31_value
                self.I1_ar = fitted_parameters[:,0]
                self.x2_ar = fitted_parameters[:,1]
                self.y2_ar = fitted_parameters[:,2]
                self.x3_ar = fitted_parameters[:,3]
                self.y3_ar = fitted_parameters[:,4]
            elif self.method == 'xy_fix':
                self.x2_ar = self.x2_value
                self.y2_ar = self.y2_value
                self.x3_ar = self.x3_value
                self.y3_ar = self.y3_value
                self.I1_ar = fitted_parameters[:,0]
                self.dm21_ar = fitted_parameters[:,1]
                self.dm31_ar = fitted_parameters[:,2]
            else:
                print(self.method, "method is undefined. Please, enter one of these: standart, dm_fix, xy_fix")
        else:
            print(self.star_type, "star type is undefined. Please, enter one of these: binary, triple")

    def save(self,folder_path):
        path = folder_path
        np.save(path + '\\f_ar.npy',self.f_ar)
        np.save(path + '\\I1_ar.npy',self.I1_ar)
        np.save(path + '\\dm21_ar.npy',self.dm21_ar)
        np.save(path + '\\x2_ar.npy',self.x2_ar)
        np.save(path + '\\y2_ar.npy',self.y2_ar)
        if self.star_type == 'triple':
            np.save(path + '\\dm31_ar.npy',self.dm31_ar)
            np.save(path + '\\x3_ar.npy',self.x3_ar)
            np.save(path + '\\y3_ar.npy',self.y3_ar)

            
class Fit:
    def __init__(self,filename_config, fit_parameters_config):
        #read config file
        files = InputReader()
        files.read(filename_config)
        self.filename_config = filename_config
        self.fit_parameters_config = fit_parameters_config
        #read fit parameters from file
        input_fit_parameters = FitParametersReader()
        input_fit_parameters.read(fit_parameters_config)
        self.bandwidth = input_fit_parameters.bandwidth
        self.bottom_freq_border = input_fit_parameters.b_freq_border
        self.upper_freq_border = input_fit_parameters.up_freq_border
        self.star_type = input_fit_parameters.star_type
        self.rmbg_flag = input_fit_parameters.rmbg_flag
        self.zone_type = input_fit_parameters.zone_type
        self.method = input_fit_parameters.method
        #read data from files
        data = Data()
        data.read_from(files.data)
        if self.rmbg_flag == 'rmbg':
            fit_data = data.rmbg_final_ps
        elif self.rmbg_flag == 'no_rmbg':
            fit_data = data.final_ps        
        self.ps = fit_data
        self.frame_size = len(fit_data.values)

        if self.star_type == 'binary':
            if self.method == 'standart':
                self.model = Models.binary
                self.init_guess = BinaryInitialParameters(input_fit_parameters.dm21,input_fit_parameters.x2,input_fit_parameters.y2)
            elif self.method == 'fix_dm':
                self.model = Models.binary_fix_dm
                self.init_guess = BinaryInitialParametersFixDM(input_fit_parameters.x2,input_fit_parameters.y2)
                self.dm21_fixed_value = input_fit_parameters.dm21 #hidded model parameters initialization!
            elif self.method == 'fix_xy':
                self.model = Models.binary_fix_xy
                self.init_guess = BinaryInitialParametersFixXY(input_fit_parameters.dm21)
                self.x2_fixed_value = input_fit_parameters.x2 #hidded model parameters initialization!
                self.y2_fixed_value = input_fit_parameters.y2 #hidded model parameters initialization!
            else:
                print(self.method, "method is undefined. Please, enter one of these: standart, fix_dm, fix_xy")

        elif self.star_type == 'triple':
            if self.method == 'standart':
                self.model = Models.triple
                self.init_guess = TripleInitialParameters(input_fit_parameters.dm21,input_fit_parameters.x2,input_fit_parameters.y2,\
                                                         input_fit_parameters.dm31,input_fit_parameters.x3,input_fit_parameters.y3)
            elif self.method == 'fix_dm':
                self.model = Models.triple
                self.init_guess = TripleInitialParametersFixDM(input_fit_parameters.x2,input_fit_parameters.y2,\
                                                                input_fit_parameters.x3,input_fit_parameters.y3)
                self.dm21_fixed_value = input_fit_parameters.dm21 #hidded model parameters initialization!
                self.dm31_fixed_value = input_fit_parameters.dm31 #hidded model parameters initialization!

            elif self.method == 'fix_xy':
                self.model = Models.triple
                self.init_guess = TripleInitialParametersFixXY(input_fit_parameters.dm21,input_fit_parameters.dm31)
                self.x2_fixed_value = input_fit_parameters.x2 #hidded model parameters initialization!
                self.y2_fixed_value = input_fit_parameters.y2 #hidded model parameters initialization!
                self.x3_fixed_value = input_fit_parameters.x3 #hidded model parameters initialization!
                self.y3_fixed_value = input_fit_parameters.y3 #hidded model parameters initialization!
        else:
            print(self.star_type, "star type is undefined. Please, enter one of these: binary, triple")

        self.frequencies = np.arange(self.bottom_freq_border,self.upper_freq_border,self.bandwidth)
        self.uv_grid = Grid(self.frame_size).uv_meshgrid()

    def ring_masks(self):
        f_ar_lenght = len(self.frequencies)
        masks = np.ma.array(np.zeros((f_ar_lenght,self.frame_size,self.frame_size)))
        for i in range(f_ar_lenght-1):
            masks[i] = ring_logical_mask(self.frame_size,self.frequencies[i],self.frequencies[i+1])
        return masks

    def elliptic_masks(self,ellipse_params):
        f_ar_lenght = len(self.frequencies)
        masks = np.ma.array(np.zeros((f_ar_lenght,self.frame_size,self.frame_size)))
        for i in range(f_ar_lenght-1):
            masks[i] = elliptic_logical_mask(self.frame_size,self.frequencies[i],self.frequencies[i+1],ellipse_params)
        return masks
 
    def plot_model_in_masked_zone(self,mask,fitted_parameters):
        u,v = self.uv_grid
        half_frame_size = self.frame_size//2
        freq_axis = np.arange(-half_frame_size,half_frame_size)
        masked_zone_values = np.ma.array(self.ps.values,mask=mask)
        init_guess_values = np.ma.array(self.model(u,v,*self.init_guess.array()),mask=mask)
        model_values = np.ma.array(self.model(u,v,*fitted_parameters),mask=mask)
        ymin=0.; ymax=1.
        plt.figure()
        plt.plot(freq_axis, self.ps.values[half_frame_size,:],label='all data')
        plt.plot(freq_axis, masked_zone_values[half_frame_size,:],label='data')
        plt.plot(freq_axis, init_guess_values[half_frame_size,:], label='init guess')
        plt.plot(freq_axis, model_values[half_frame_size,:],label='model')
        plt.yscale('log')
        plt.title('x projection')
        plt.legend()

        plt.figure()
        plt.plot(freq_axis, self.ps.values[:,half_frame_size],label='all data')
        plt.plot(freq_axis, masked_zone_values[:,half_frame_size],label='data')
        plt.plot(freq_axis, init_guess_values[:,half_frame_size], label='init guess')
        plt.plot(freq_axis, model_values[:,half_frame_size],label='model')
        plt.yscale('log')
        plt.title('y projection')
        plt.legend()
        plt.show()

    def fit(self,masks):
        def residual_function(init_guess):
        #This function must be defined here
        #because she needs to know the model as the atribute of Fit class,
        # therefore, (self) should be determined above,
        #  and at the same time, the self can not be set as a function argument,
        #  because the residual function should has only one argument,
        #   the vector initial_guess.
            u,v = self.uv_grid
            masked_model = np.ma.array(self.model(u,v,*init_guess),mask=masks[i])
            return np.sum((masked_model - masked_image)**2)

        def residual_function_fix_dm(init_guess):
        #This function must be defined here
        #because she needs to know the model as the atribute of Fit class,
        # therefore, (self) should be determined above,
        #  and at the same time, the self can not be set as a function argument,
        #  because the residual function should has only one argument,
        #   the vector initial_guess.
            u,v = self.uv_grid
            dm21 = self.dm21_fixed_value
            masked_model = np.ma.array(self.model(u,v,dm21,*init_guess),mask=masks[i])
            return np.sum((masked_model - masked_image)**2)

        def residual_function_fix_xy(init_guess):
        #This function must be defined here
        #because she needs to know the model as the atribute of Fit class,
        # therefore, (self) should be determined above,
        #  and at the same time, the self can not be set as a function argument,
        #  because the residual function should has only one argument,
        #   the vector initial_guess.
            u,v = self.uv_grid
            x2 = self.x2_fixed_value
            y2 = self.y2_fixed_value
            masked_model = np.ma.array(self.model(u,v,x2,y2,*init_guess),mask=masks[i])
            return np.sum((masked_model - masked_image)**2)

        image_number = len(masks)
        fitted_parameters_number = len(self.init_guess.array())
        fitted_parameters = np.empty((image_number,fitted_parameters_number))
        print('start fitting dm and coords')
        print('iteration: .. from ',len(masks))
        for i in range(image_number):
            print(i)
            masked_image = np.ma.array(self.ps.values,mask=masks[i])
            scale = np.sqrt(np.nanmean(masked_image))
            self.init_guess.I1 = scale
            minimize_result = minimize(residual_function_fix_xy, self.init_guess.array(), method='L-BFGS-B', tol=1e-8)
            #self.plot_model_in_masked_zone(masks[i],minimize_result.x)
            fitted_parameters[i,:] = minimize_result.x
        return fitted_parameters


    def fit_i_xy_dm(self):
        #read config file
        files = InputReader()
        files.read(self.filename_config)

        if self.zone_type == 'ring':
            masks = self.ring_masks()
        elif self.zone_type == 'elliptic':
            ellipse_params = ellipse_parameters(data.star_ps.values,bottom_freq_border,upper_freq_border)
            masks = self.elliptic_masks(ellipse_params)
        else:
            print(zone_type, "zone type is undefined. Please, enter one of these: ring, elliptic")

        fitted_parameters =  self.fit(masks) #fitting
        fit_result = FitResult(self.filename_config, self.fit_parameters_config)
        fit_result.fill_from_fit(self.frequencies,fitted_parameters)
        fit_result.save(files.data)
        print('all fitted parameters were saved')


 

  





 






