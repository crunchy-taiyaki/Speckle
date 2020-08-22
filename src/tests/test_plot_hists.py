import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import *
from power_spectrum import *
from models import Models
from fit import *
from stats import shapiro_wilk_test

#read config file
files = DataFiles()
files.read_input('C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TEST_star_input.txt')
files.info()

#read i xy dm from files
fit_result = FitResult('binary')
fit_result.read_i_xy_dm_freq_from(files.data)

#normality test
print('--------------NORMALITY TEST-------------------')
print('dm21')
shapiro_wilk_test(np.where(fit_result.dm21_ar < 6.0))
print('x2')
shapiro_wilk_test(np.where(fit_result.x2_ar < 254.0))
print('y2')
shapiro_wilk_test(np.where(fit_result.y2_ar > 252.0))

#plot histograms
bins = 30
plt.figure()
plt.hist(fit_result.dm21_ar, bins)
plt.title('dm21_hist')
plt.savefig(files.images + '\\dm21_hist.png')

plt.figure()
plt.hist(fit_result.x2_ar, bins)
plt.title('x2_hist')
plt.savefig(files.images + '\\x2_hist.png')

plt.figure()
plt.hist(fit_result.y2_ar, bins)
plt.title('y2_hist')
plt.savefig(files.images + '\\y2_hist.png')
plt.show()


