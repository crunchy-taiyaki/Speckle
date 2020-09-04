import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from initial_parameters import DataFiles
from power_spectrum import Data
from fit import FitParameters, FitResult

class ResultSample():

    def __init__(self,flag):
        self.flag = flag
        self.dm21 = None
        self.x2 = None
        self.y2 = None
        self.dm31 = None
        self.x3 = None
        self.y3 = None

    def save_to(self,result_folder_path):
        path = result_folder_path
        np.save(path + '\\dm21_sample.npy',self.dm21)
        np.save(path + '\\x2_sample.npy',self.x2)
        np.save(path + '\\y2_sample.npy',self.y2)
        if(self.flag=='triple'):
            np.save(path + '\\dm31_sample.npy',self.dm31)
            np.save(path + '\\x3_sample.npy',self.x3)
            np.save(path + '\\y3_sample.npy',self.y3)

    def read_from(self,result_folder_path):
        path = result_folder_path
        self.dm21 = np.load(path + '\\dm21_sample.npy')
        self.x2 = np.load(path + '\\x2_sample.npy')
        self.y2 = np.load(path + '\\y2_sample.npy')
        if(self.flag=='triple'):
            self.dm31 = np.load(path + '\\dm31_sample.npy')
            self.x3 = np.load(path + '\\x3_sample.npy')
            self.y3 = np.load(path + '\\y3_sample.npy')

def shapiro_wilk_test(data):
    # normality test
    stat, p = shapiro(data)
    print('Statistics=',stat,'p=',p)
    # interpret
    if (p > 0.05):
        print('Sample looks Gaussian')
    else:
        print("Sample doesn't look Gaussian")

def clean_stats(filename_config,fit_parameters_config):
    #read config file
    files = DataFiles()
    files.read_input(filename_config)
    files.info()

    #read data from files
    data = Data()
    data.read_from(files.data)

    #read i xy dm from files
    input_fit_parameters = FitParameters()
    input_fit_parameters.read_input(fit_parameters_config)
    fit_result = FitResult(input_fit_parameters.flag)
    fit_result.read_i_xy_dm_freq_from(files.data)

    #mask results outside frequence borders
    mask_down_up = np.logical_and(fit_result.f_ar > data.final_ps.b_bound, fit_result.f_ar < data.final_ps.up_bound)
    mask_up = fit_result.f_ar < data.final_ps.up_bound

    #masking results by frequencies
    dm21 = fit_result.dm21_ar[mask_down_up]
    x2 = fit_result.x2_ar[mask_up]
    y2 = fit_result.y2_ar[mask_up]
    if (input_fit_parameters.flag == 'triple'):
        dm31 = fit_result.dm31_ar[mask_down_up]
        x3 = fit_result.x3_ar[mask_up]
        y3 = fit_result.y3_ar[mask_up]

    #mask by values
    mask_dm21 = dm21[np.logical_and(dm21>input_fit_parameters.dm21_bottom, dm21<input_fit_parameters.dm21_upper)]
    mask_x2 = x2[np.logical_and(x2>input_fit_parameters.x2_bottom, x2<input_fit_parameters.x2_upper)]
    mask_y2 = y2[np.logical_and(y2>input_fit_parameters.y2_bottom, y2<input_fit_parameters.y2_upper)]

    # error '>' not supported between instances of 'float' and 'NoneType'
    #if (input_fit_parameters.flag == 'triple'):
    #    mask_dm31 = dm31[np.logical_and(dm31 > input_fit_parameters.dm31_bottom, dm31 < input_fit_parameters.dm31_upper)]
    #    mask_x3 = x3[np.logical_and(x3 > input_fit_parameters.x3_bottom, x3 < input_fit_parameters.x3_upper)]
    #    mask_y3 = y3[np.logical_and(y3 > input_fit_parameters.y3_bottom, y3 < input_fit_parameters.y3_upper)]

    #save clean samples
    sample = ResultSample(input_fit_parameters.flag)
    sample.dm21 = mask_dm21
    sample.x2 = mask_x2
    sample.y2 = mask_y2
    if (input_fit_parameters.flag == 'triple'):
        sample.dm31 = mask_dm31
        sample.x3 = mask_x3
        sample.y3 = mask_y3
    sample.save_to(files.data)

    #plot histograms
    bins = 50
    plt.figure()
    plt.hist(dm21, bins)
    plt.title('dm21_hist')
    plt.savefig(files.images + '\\dm21_hist.png')

    plt.figure()
    plt.hist(sample.dm21, bins)
    plt.title('mask dm21_hist')
    plt.savefig(files.images + '\\dm21_hist_mask.png')

    plt.figure()
    plt.hist(x2, bins)
    plt.title('x2_hist')
    plt.savefig(files.images + '\\x2_hist.png')

    plt.figure()
    plt.hist(sample.x2, bins)
    plt.title('mask x2_hist')
    plt.savefig(files.images + '\\x2_hist_mask.png')

    plt.figure()
    plt.hist(y2, bins)
    plt.title('y2_hist')
    plt.savefig(files.images + '\\y2_hist.png')

    plt.figure()
    plt.hist(sample.y2, bins)
    plt.title('mask y2_hist')
    plt.savefig(files.images + '\\y2_hist_mask.png')
    plt.show()

    if (input_fit_parameters.flag == 'triple'):
        plt.figure()
        plt.hist(dm31, bins)
        plt.title('dm31_hist')
        plt.savefig(files.images + '\\dm31_hist.png')

        plt.figure()
        plt.hist(sample.dm31, bins)
        plt.title('mask dm31_hist')
        plt.savefig(files.images + '\\dm31_hist_mask.png')

        plt.figure()
        plt.hist(x3, bins)
        plt.title('x3_hist')
        plt.savefig(files.images + '\\x3_hist.png')

        plt.figure()
        plt.hist(sample.x3, bins)
        plt.title('mask x3_hist')
        plt.savefig(files.images + '\\x3_hist_mask.png')

        plt.figure()
        plt.hist(y3, bins)
        plt.title('y3_hist')
        plt.savefig(files.images + '\\y3_hist.png')

        plt.figure()
        plt.hist(sample.y3, bins)
        plt.title('mask y3_hist')
        plt.savefig(files.images + '\\y3_hist_mask.png')

    plt.show()

def plot_residuals(filename_config,fit_parameters_config,rmbg_flag):
    #read config file
    files = DataFiles()
    files.read_input(filename_config)
    files.info()

    #read data from files
    data = Data()
    data.read_from(files.data)

    #read fit parameters config
    input_fit_parameters = FitParameters()
    input_fit_parameters.read_input(fit_parameters_config)

    #read i xy dm from files
    fit_result = FitResult(input_fit_parameters.flag)
    fit_result.read_i_xy_dm_freq_from(files.data)

    if rmbg_flag=='rmbg':
        fitted_data = data.rmbg_final_ps
    else:
        fitted_data = data.final_ps

    print('residuals:',fit_result.residuals)
    plt.figure()
    plt.scatter(fit_result.f_ar, fit_result.residuals)
    plt.axvline(fitted_data.b_bound, color='orange')
    plt.axvline(fitted_data.up_bound, color='orange')
    plt.savefig(files.images + '\\residuals.png')
    plt.show()

def define_sample(filename_config,fit_parameters_config,residual_level):
    #read config file
    files = DataFiles()
    files.read_input(filename_config)
    files.info()

    #read data from files
    data = Data()
    data.read_from(files.data)

    #read i xy dm from files
    input_fit_parameters = FitParameters()
    input_fit_parameters.read_input(fit_parameters_config)
    fit_result = FitResult(input_fit_parameters.flag)
    fit_result.read_i_xy_dm_freq_from(files.data)

    #mask results outside frequence borders
    mask_down_up = np.logical_and(fit_result.f_ar > data.final_ps.b_bound, fit_result.f_ar < data.final_ps.up_bound)
    mask_up = fit_result.f_ar < data.final_ps.up_bound
    residuals_mask = fit_result.residuals < residual_level

    #combine masks
    mask = np.logical_and(residuals_mask,mask_down_up)

    #masking results
    mask_dm21 = fit_result.dm21_ar[mask]
    mask_x2 = fit_result.x2_ar[mask]
    mask_y2 = fit_result.y2_ar[mask]
    if (input_fit_parameters.flag == 'triple'):
        mask_dm31 = fit_result.dm31_ar[mask]
        mask_x3 = fit_result.x3_ar[mask]
        mask_y3 = fit_result.y3_ar[mask]

    #save clean samples
    sample = ResultSample(input_fit_parameters.flag)
    sample.dm21 = mask_dm21
    sample.x2 = mask_x2
    sample.y2 = mask_y2
    if (input_fit_parameters.flag == 'triple'):
        sample.dm31 = mask_dm31
        sample.x3 = mask_x3
        sample.y3 = mask_y3
    sample.save_to(files.data)

    #plot histograms
    bins = 50
    plt.figure()
    plt.hist(fit_result.dm21_ar, bins)
    plt.title('dm21_hist')
    plt.savefig(files.images + '\\dm21_hist.png')

    plt.figure()
    plt.hist(sample.dm21, bins)
    plt.title('mask dm21_hist')
    plt.savefig(files.images + '\\dm21_hist_mask.png')

    plt.figure()
    plt.hist(fit_result.x2_ar, bins)
    plt.title('x2_hist')
    plt.savefig(files.images + '\\x2_hist.png')

    plt.figure()
    plt.hist(sample.x2, bins)
    plt.title('mask x2_hist')
    plt.savefig(files.images + '\\x2_hist_mask.png')

    plt.figure()
    plt.hist(fit_result.y2_ar, bins)
    plt.title('y2_hist')
    plt.savefig(files.images + '\\y2_hist.png')

    plt.figure()
    plt.hist(sample.y2, bins)
    plt.title('mask y2_hist')
    plt.savefig(files.images + '\\y2_hist_mask.png')

    if (input_fit_parameters.flag == 'triple'):
        plt.figure()
        plt.hist(fit_result.dm31_ar, bins)
        plt.title('dm31_hist')
        plt.savefig(files.images + '\\dm31_hist.png')

        plt.figure()
        plt.hist(sample.dm31, bins)
        plt.title('mask dm31_hist')
        plt.savefig(files.images + '\\dm31_hist_mask.png')

        plt.figure()
        plt.hist(fit_result.x3_ar, bins)
        plt.title('x3_hist')
        plt.savefig(files.images + '\\x3_hist.png')

        plt.figure()
        plt.hist(sample.x3, bins)
        plt.title('mask x3_hist')
        plt.savefig(files.images + '\\x3_hist_mask.png')

        plt.figure()
        plt.hist(fit_result.y3_ar, bins)
        plt.title('y3_hist')
        plt.savefig(files.images + '\\y3_hist.png')

        plt.figure()
        plt.hist(sample.y3, bins)
        plt.title('mask y3_hist')
        plt.savefig(files.images + '\\y3_hist_mask.png')

    plt.show()

def normality_test(filename_config,fit_parameters_config):

    #read config file
    files = DataFiles()
    files.read_input(filename_config)

    #read fit parameters config
    input_fit_parameters = FitParameters()
    input_fit_parameters.read_input(fit_parameters_config)
        
    #read samples
    sample = ResultSample(input_fit_parameters.flag)
    sample.read_from(files.data)

    #normality test
    print('--------------NORMALITY TEST-------------------')
    print('dm21')
    shapiro_wilk_test(sample.dm21)
    print('x2')
    shapiro_wilk_test(sample.x2)
    print('y2')
    shapiro_wilk_test(sample.y2)
    if (input_fit_parameters.flag == 'triple'):
        print('dm31')
        shapiro_wilk_test(sample.dm31)
        print('x3')
        shapiro_wilk_test(sample.x3)
        print('y3')
        shapiro_wilk_test(sample.y3)
