import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from models import Models
from fit import FitParameters, Fit, BinaryInitialParameters, TripleInitialParameters
from grid import Grid
from masks import ellipse_parameters

def fit_i_xy_dm(filename_config, fit_parameters_config, rmbg_flag, zone_flag):

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

    #enter fit parameters
    flag = input_fit_parameters.flag
    if flag =='triple':
        model = Models.triple
        initial_parameters = TripleInitialParameters(input_fit_parameters.dm21,input_fit_parameters.x2,input_fit_parameters.y2,\
                                                     input_fit_parameters.dm31,input_fit_parameters.x3,input_fit_parameters.y3)
    else:
        model = Models.binary
        initial_parameters = BinaryInitialParameters(input_fit_parameters.dm21,input_fit_parameters.x2,input_fit_parameters.y2)

    uv_grid = Grid(size).uv_meshgrid()
    bottom_freq_border = input_fit_parameters.b_freq_border
    upper_freq_border = input_fit_parameters.up_freq_border
    bandwidth = input_fit_parameters.bandwidth
    if (rmbg_flag == 'rmbg'):
        fit_data = data.rmbg_final_ps
    else:
        fit_data = data.final_ps

    if (zone_flag == 'ellipse'):
        ellipse_params = ellipse_parameters(data.star_ps.values,bottom_freq_border,upper_freq_border)
        fit = Fit(fit_data,model,initial_parameters,uv_grid,bottom_freq_border,upper_freq_border,bandwidth,flag,zone_flag,ellipse_params)
    else:
        fit = Fit(fit_data,model,initial_parameters,uv_grid,bottom_freq_border,upper_freq_border,bandwidth,flag,zone_flag)

    #fit
    fit.fit_i_xy_dm()

    #save
    fit.save_i_xy_dm_freq(files.data)
