import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from models import Models
from fit import FitParameters, FitResult
from plot import slice_image, define_ylim, plot_rings_borders

def plot_fitted_i_xy_dm(filename_config,fit_parameters_config, rmbg_flag):

    #read config file
    files = DataFiles()
    files.read_input(filename_config)
    files.info()

    #read fit parameters from file
    input_fit_parameters = FitParameters()
    input_fit_parameters.read_input(fit_parameters_config)

    #read data from files
    data = Data()
    data.read_from(files.data)
    size = data.star_ps.values.shape[0]
    half_size = size//2

    #read i xy dm from files
    fit_result = FitResult(input_fit_parameters.flag)
    fit_result.read_i_xy_dm_freq_from(files.data)

    if rmbg_flag=='rmbg':
        fitted_data = data.rmbg_final_ps
    else:
        fitted_data = data.final_ps

    # plot
    half_freq_axis = np.arange(0,half_size)
    freq_axis = np.arange(-half_size,half_size)
    ymin,ymax=define_ylim(fitted_data)

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


    if (input_fit_parameters.flag == 'triple'):
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

