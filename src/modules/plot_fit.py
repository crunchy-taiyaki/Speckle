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

    #read i xy dm from files
    fit_result = FitResult(input_fit_parameters.flag)
    fit_result.read_i_xy_dm_freq_from(files.data)

    if rmbg_flag=='rmbg':
        fitted_data = data.rmbg_final_ps
    else:
        fitted_data = data.final_ps

    # plot
    half_freq_axis = np.arange(0,256.0)
    freq_axis = np.arange(-256.0,256.0)
    ymin,ymax=define_ylim(fitted_data)


    #____________amplitude________________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.I1_ar,color='orange')
    plt.imshow(fitted_data.values,cmap='gray',vmin=ymin,vmax=ymax, extent=[-256,256,-256,256])
    plot_rings_borders(0,0,fitted_data.b_bound,fitted_data.up_bound)
    plot_rings_borders(0,0,fitted_data.b_bound,160)
    plt.title('amplitude')
    plt.savefig(files.images + '\\I.png')

    ##_____________________ps 45 slice_____________________
    #plt.figure()
    #plt.plot(freq_axis, slice_image(fitted_data.values,x1=0,y1=0,x2=54,y2=256))
    #plt.axvline(fitted_data.b_bound, color='orange')
    #plt.axvline(fitted_data.up_bound, color='orange')
    #ymin,ymax=define_ylim(fitted_data)
    #plt.ylim(ymin,ymax)
    #plt.title('ps slice')
    #plt.savefig(files.images + '\\ps_slice.png')

    #______________________dm21_____________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.dm21_ar)
    plt.axvline(fitted_data.b_bound, color='orange')
    plt.axvline(fitted_data.up_bound, color='orange')
    plt.title('dm21')
    plt.savefig(files.images + '\\dm21.png')

    #______________________dm21 vs ps_____________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.dm21_ar, color='orange')
    plt.imshow(fitted_data.values,cmap='gray',vmin=ymin,vmax=ymax, extent=[-256,256,-256,256])
    plot_rings_borders(0,0,fitted_data.b_bound,fitted_data.up_bound)
    plt.title('dm21')
    plt.savefig(files.images + '\\dm21 vs ps.png')

    #____________________x2____________________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.x2_ar)
    plt.axvline(fitted_data.b_bound, color='orange')
    plt.axvline(fitted_data.up_bound, color='orange')
    plt.title('x2')
    plt.savefig(files.images + '\\x2.png')

    #____________________x2 vs ps____________________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.x2_ar, color='orange')
    plt.imshow(fitted_data.values,cmap='gray',vmin=ymin,vmax=ymax, extent=[-256,256,-256,256])
    plot_rings_borders(0,0,fitted_data.b_bound,fitted_data.up_bound)
    plt.title('x2')
    plt.savefig(files.images + '\\x2 vs ps.png')

    #_______________________y2___________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.y2_ar)
    plt.axvline(fitted_data.b_bound, color='orange')
    plt.axvline(fitted_data.up_bound, color='orange')
    plt.title('y2')
    plt.savefig(files.images + '\\y2.png')

    #_______________________y2 vs ps___________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.y2_ar, color='orange')
    plt.imshow(fitted_data.values,cmap='gray',vmin=ymin,vmax=ymax, extent=[-256,256,-256,256])
    plot_rings_borders(0,0,fitted_data.b_bound,fitted_data.up_bound)
    plt.title('y2')
    plt.savefig(files.images + '\\y2 vs ps.png') 

    if (input_fit_parameters.flag == 'triple'):
        #______________________dm31_____________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.dm31_ar)
        plt.axvline(fitted_data.b_bound, color='orange')
        plt.axvline(fitted_data.up_bound, color='orange')
        plt.title('dm31')
        plt.savefig(files.images + '\\dm31.png')

        #______________________dm31 vs ps_____________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.dm31_ar, color='orange')
        plt.imshow(fitted_data.values,cmap='gray',vmin=ymin,vmax=ymax, extent=[-256,256,-256,256])
        plot_rings_borders(0,0,fitted_data.b_bound,fitted_data.up_bound)
        plt.title('dm31')
        plt.savefig(files.images + '\\dm31 vs ps.png')

        #____________________x3____________________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.x3_ar)
        plt.axvline(fitted_data.b_bound, color='orange')
        plt.axvline(fitted_data.up_bound, color='orange')
        plt.title('x3')
        plt.savefig(files.images + '\\x3.png')

        #____________________x3 vs ps____________________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.x3_ar, color='orange')
        plt.imshow(fitted_data.values,cmap='gray',vmin=ymin,vmax=ymax, extent=[-256,256,-256,256])
        plot_rings_borders(0,0,fitted_data.b_bound,fitted_data.up_bound)
        plt.title('x3')
        plt.savefig(files.images + '\\x3 vs ps.png')

        #_______________________y3___________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.y3_ar)
        plt.axvline(fitted_data.b_bound, color='orange')
        plt.axvline(fitted_data.up_bound, color='orange')
        plt.title('y3')
        plt.savefig(files.images + '\\y3.png')

        #_______________________y3 vs ps___________________
        plt.figure()
        plt.scatter(fit_result.f_ar,fit_result.y3_ar, color='orange')
        plt.imshow(fitted_data.values,cmap='gray',vmin=ymin,vmax=ymax, extent=[-256,256,-256,256])
        plot_rings_borders(0,0,fitted_data.b_bound,fitted_data.up_bound)
        plt.title('y3')
        plt.savefig(files.images + '\\y3 vs ps.png')

    plt.show()

