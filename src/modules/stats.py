import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from file_reader import InputReader, FitParametersReader
from spectra_calculator import Data
from fit import FitResult

class ResultSample():

    def __init__(self,flag):
        self.flag = flag
        self.f = None
        self.I1 = None
        self.dm21 = None
        self.x2 = None
        self.y2 = None
        self.dm31 = None
        self.x3 = None
        self.y3 = None

    def save_to(self,folder_path):
        path = folder_path
        np.save(path + '\\f_sample.npy',self.f)
        np.save(path + '\\I1_sample.npy',self.I1)
        np.save(path + '\\dm21_sample.npy',self.dm21)
        np.save(path + '\\x2_sample.npy',self.x2)
        np.save(path + '\\y2_sample.npy',self.y2)
        if(self.flag=='triple'):
            np.save(path + '\\dm31_sample.npy',self.dm31)
            np.save(path + '\\x3_sample.npy',self.x3)
            np.save(path + '\\y3_sample.npy',self.y3)

    def read_from(self,folder_path):
        path = folder_path
        self.f = np.load(path + '\\f_sample.npy')
        self.I1 = np.load(path + '\\I1_sample.npy')
        self.dm21 = np.load(path + '\\dm21_sample.npy')
        self.x2 = np.load(path + '\\x2_sample.npy')
        self.y2 = np.load(path + '\\y2_sample.npy')
        if(self.flag=='triple'):
            self.dm31 = np.load(path + '\\dm31_sample.npy')
            self.x3 = np.load(path + '\\x3_sample.npy')
            self.y3 = np.load(path + '\\y3_sample.npy')


def define_sample(filename_config,fit_parameters_config):
    #read config file
    files = InputReader()
    files.read(filename_config)

    #read data from files
    data = Data()
    data.read_from(files.data)

    #read i xy dm from files
    input_fit_parameters = FitParametersReader()
    input_fit_parameters.read(fit_parameters_config)
    fit_result = FitResult(filename_config,fit_parameters_config)
    fit_result.read(files.data)

    #mask results outside frequence borders
    mask_freq = np.logical_and(fit_result.f_ar > input_fit_parameters.mask_b_freq_border,\
                               fit_result.f_ar < input_fit_parameters.mask_up_freq_border)

    #combine masks
    mask = mask_freq

    #masking results
    mask_f = fit_result.f_ar[mask]
    mask_I1 = fit_result.I1_ar[mask]
    mask_dm21 = fit_result.dm21_ar[mask]
    mask_x2 = fit_result.x2_ar[mask]
    mask_y2 = fit_result.y2_ar[mask]
    if input_fit_parameters.star_type == 'triple':
        mask_dm31 = fit_result.dm31_ar[mask]
        mask_x3 = fit_result.x3_ar[mask]
        mask_y3 = fit_result.y3_ar[mask]

    #save clean samples
    sample = ResultSample(input_fit_parameters.star_type)
    sample.f = mask_f
    sample.I1 = mask_I1
    sample.dm21 = mask_dm21
    sample.x2 = mask_x2
    sample.y2 = mask_y2
    if input_fit_parameters.star_type == 'triple':
        sample.dm31 = mask_dm31
        sample.x3 = mask_x3
        sample.y3 = mask_y3
    sample.save_to(files.data)


def shapiro_wilk_test(data):
    # normality test
    stat, p = shapiro(data)
    print('Statistics=',stat,'p=',p)
    # interpret
    if (p > 0.05):
        print('Sample looks Gaussian')
    else:
        print("Sample doesn't look Gaussian")


def normality_test(filename_config,fit_parameters_config):

    #read config file
    files = InputReader()
    files.read(filename_config)

    #read data from files
    data = Data()
    data.read_from(files.data)

    #read i xy dm from files
    input_fit_parameters = FitParametersReader()
    input_fit_parameters.read(fit_parameters_config)
        
    #read samples
    sample = ResultSample(input_fit_parameters.star_type)
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
