import numpy as np
import matplotlib.pyplot as plt
from file_reader import InputReader, FitParametersReader
from spectra_calculator import Data
from models import Models
from fit import FitResult
from plot_tools import define_ylim

def plot_fitted_i_xy_dm(filename_config,fit_parameters_config):

    #read config file
    files = InputReader()
    files.read(filename_config)

    #read fit parameters from file
    input_fit_parameters = FitParametersReader()
    input_fit_parameters.read(fit_parameters_config)

    #read data from files
    data = Data()
    data.read_from(files.data)
    size = data.star_ps.values.shape[0]
    half_size = size//2

    #read i xy dm from files
    fit_result = FitResult(filename_config,fit_parameters_config)
    fit_result.read(files.data)

    if input_fit_parameters.rmbg_flag == 'rmbg':
        fitted_data = data.rmbg_final_ps
    else:
        fitted_data = data.final_ps

    # plot
    half_freq_axis = np.arange(0,half_size)
    freq_axis = np.arange(-half_size,half_size)

    #______________________I1_____________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.I1_ar)
    plt.axvline(fitted_data.b_bound, color='orange')
    plt.axvline(fitted_data.up_bound, color='orange')
    plt.title('I1')
    plt.savefig(files.images + '\\I1.png')

    #______________________dm21_____________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.dm21_ar)
    plt.axvline(fitted_data.b_bound, color='orange')
    plt.axvline(fitted_data.up_bound, color='orange')
    plt.title('dm21')
    plt.savefig(files.images + '\\dm21.png')


    #____________________x2____________________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.x2_ar)
    plt.axvline(fitted_data.b_bound, color='orange')
    plt.axvline(fitted_data.up_bound, color='orange')
    plt.title('x2')
    plt.savefig(files.images + '\\x2.png')


    #_______________________y2___________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.y2_ar)
    plt.axvline(fitted_data.b_bound, color='orange')
    plt.axvline(fitted_data.up_bound, color='orange')
    plt.title('y2')
    plt.savefig(files.images + '\\y2.png')


    if (input_fit_parameters.star_type == 'triple'):
        #______________________dm31_____________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.dm31_ar)
        plt.axvline(fitted_data.b_bound, color='orange')
        plt.axvline(fitted_data.up_bound, color='orange')
        plt.title('dm31')
        plt.savefig(files.images + '\\dm31.png')


        #____________________x3____________________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.x3_ar)
        plt.axvline(fitted_data.b_bound, color='orange')
        plt.axvline(fitted_data.up_bound, color='orange')
        plt.title('x3')
        plt.savefig(files.images + '\\x3.png')


        #_______________________y3___________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.y3_ar)
        plt.axvline(fitted_data.b_bound, color='orange')
        plt.axvline(fitted_data.up_bound, color='orange')
        plt.title('y3')
        plt.savefig(files.images + '\\y3.png')


    plt.show()

