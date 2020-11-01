import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from initial_parameters import DataFiles
from power_spectrum import Data
from fit import FitParameters, FitResult

## TYC1947_00290_1 08 03 2020 700 no ref
filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200308_no_ref\\input.txt'
fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200308_no_ref\\fit_parameters.txt'

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

mask_freq = np.logical_and(fit_result.f_ar > input_fit_parameters.mask_b_freq_border, fit_result.f_ar < input_fit_parameters.mask_up_freq_border)
dm_mask = (fit_result.dm21_ar > 1e-2)
mask = np.logical_and(dm_mask,mask_freq)
dm = fit_result.dm21_ar[mask]

print('dm21=',np.median(dm),'+-',np.std(dm))

plt.figure()
plt.hist(fit_result.dm21_ar[mask], bins=30)
plt.title('dm21_hist: 50-100')
plt.savefig(files.images + '\\dm21_hist_mask.png')
plt.show()