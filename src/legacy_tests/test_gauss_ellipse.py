import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")

from initial_parameters import DataFiles
from power_spectrum import Data
from grid import Grid
from fit import FitParameters
from masks import gauss_2d, ellipse_parameters, elliptic_mask
from plot import define_ylim

def gauss_ellipse(filename_config, fit_parameters_config, rmbg_flag):

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

    #enter fit parameters
    bottom_freq_border = input_fit_parameters.b_freq_border
    upper_freq_border = input_fit_parameters.up_freq_border
    #if (rmbg_flag == 'rmbg'):
    #    fit_data = data.rmbg_final_ps
    #else:
    #    fit_data = data.final_ps
    fit_data = data.ref_ps

    #fit ellipse parameters
    params = ellipse_parameters(fit_data.values,bottom_freq_border,upper_freq_border)

    #calc gaussian
    u,v = Grid(size=512).uv_meshgrid()
    gauss = gauss_2d(u,v,*params.array())

    #plot
    vmin,vmax = define_ylim(fit_data) 
    #plt.figure()
    #plt.contour(gauss, colors='orange', extent=[-256.0,256.0,-256.0,256.0])
    #plt.imshow(fit_data.values,cmap='gray',vmin=vmin,vmax=vmax, extent=[-256.0,256.0,-256.0,256.0])
    #plt.title('ellipse fit')

    plt.figure()
    plt.contour(gauss, colors='orange', extent=[-256.0,256.0,-256.0,256.0])
    plt.imshow(elliptic_mask(fit_data.values,30,40,params),cmap='gray',vmin=vmin,vmax=vmax, extent=[-256.0,256.0,-256.0,256.0])

    plt.show()

filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_251_input.txt'
fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_251_fit_parameters.txt'    

gauss_ellipse(filename_config, fit_parameters_config, 'rmbg')