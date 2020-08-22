import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import *
from power_spectrum import *
from models import Models
from fit import *


#read config file
files = DataFiles()
files.read_input('C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TEST_star_input.txt')
files.info()

#read data from files
data = Data()
data.read_from(files.data)
y0 = data.final_ps.values
model = Models.binary
initial_parameters = BinaryInitialParameters(dm21=1.,x2=253.546,y2=253.277)
uv_grid = Grid(size=512).uv_meshgrid()
bottom_freq_border = data.final_ps.b_bound
upper_freq_border = data.final_ps.up_bound
fit = Fit(data.final_ps.values,model,initial_parameters,uv_grid,bottom_freq_border,upper_freq_border,bandwidth=5,flag='binary')
fit.fit_i_xy_dm()
fit.save_i_xy_dm_freq(files.data)
