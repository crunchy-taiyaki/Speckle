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

#read i xy dm from files
fit_result = FitResult('binary')
fit_result.read_i_xy_dm_freq_from(files.data)

plt.figure()
plt.scatter(fit_result.f_ar,fit_result.I1_ar)
plt.title('amplitude')
plt.savefig(files.images + '\\I.png')

plt.figure()
plt.scatter(fit_result.f_ar,fit_result.dm21_ar)
plt.title('dm21')
plt.savefig(files.images + '\\dm21.png')

plt.figure()
plt.scatter(fit_result.f_ar,fit_result.x2_ar)
plt.title('x2')
plt.savefig(files.images + '\\x2.png')

plt.figure()
plt.scatter(fit_result.f_ar,fit_result.y2_ar)
plt.title('y2')
plt.savefig(files.images + '\\y2.png')
plt.show()