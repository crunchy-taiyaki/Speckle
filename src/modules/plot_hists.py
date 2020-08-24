import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from models import Models
from fit import FitResult, FitParameters
from stats import shapiro_wilk_test

def show_stats(filename_config,fit_parameters_config):
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

    #mask for dm
    dm_mask = np.logical_and(fit_result.f_ar > 330, fit_result.f_ar < 372)


    #masking results
    #dm21 = fit_result.dm21_ar[mask_down_up]
    dm21 = fit_result.dm21_ar[dm_mask]
    x2 = fit_result.x2_ar[mask_up]
    y2 = fit_result.y2_ar[mask_up]
    if (input_fit_parameters.flag == 'triple'):
        dm31 = fit_result.dm31_ar[mask_down_up]
        x3 = fit_result.x3_ar[mask_up]
        y3 = fit_result.y3_ar[mask_up]


    #normality test
    print('--------------NORMALITY TEST-------------------')
    #________________dm21___________________________________
    print('dm21')
    shapiro_wilk_test(dm21)
    #shapiro_wilk_test(np.where(dm21 < 6.0))
    print('dm21 std:', np.std(dm21))

    #_________________x2____________________________________
    print('x2')
    shapiro_wilk_test(x2)
    shapiro_wilk_test(np.where(x2 < 254.0))
    print('x2 std:', np.std(x2))

    #_________________y2____________________________________
    print('y2')
    shapiro_wilk_test(y2)
    shapiro_wilk_test(np.where(y2 > 253.0))
    print('y2 std:', np.std(y2))

    if (input_fit_parameters.flag == 'triple'):
        print('dm31')
        shapiro_wilk_test(dm31)
        #shapiro_wilk_test(np.where(dm31 < 6.0))
        print('x3')
        shapiro_wilk_test(x3)
        #shapiro_wilk_test(np.where(x3 < 254.0))
        print('y3')
        shapiro_wilk_test(y3)
        #shapiro_wilk_test(np.where(y3 > 252.0))

    #plot histograms
    bins = 30
    plt.figure()
    plt.hist(dm21, bins)
    plt.title('dm21_hist')
    plt.savefig(files.images + '\\dm21_hist.png')

    plt.figure()
    plt.hist(x2, bins)
    plt.title('x2_hist')
    plt.savefig(files.images + '\\x2_hist.png')

    plt.figure()
    plt.hist(y2, bins)
    plt.title('y2_hist')
    plt.savefig(files.images + '\\y2_hist.png')
    plt.show()

    if (input_fit_parameters.flag == 'triple'):
        plt.figure()
        plt.hist(dm31, bins)
        plt.title('dm31_hist')
        plt.savefig(files.images + '\\dm31_hist.png')

        plt.figure()
        plt.hist(x3, bins)
        plt.title('x3_hist')
        plt.savefig(files.images + '\\x3_hist.png')

        plt.figure()
        plt.hist(y3, bins)
        plt.title('y3_hist')
        plt.savefig(files.images + '\\y3_hist.png')

    plt.show()


