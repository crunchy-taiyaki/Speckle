import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from models import Models
from fit import FitParameters, BinaryInitialParameters, TripleInitialParameters, FitResult
from grid import Grid
from stats import ResultSample
from final_params import final_result
from masks import ring_mask

## triple hd52721 550 04_03_2020
filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\input.txt'
fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\fit_parameters.txt'
angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\angle.txt'

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
flag = input_fit_parameters.flag

fit_result = FitResult(input_fit_parameters.flag)
fit_result.read_i_xy_dm_freq_from(files.data)
sample = ResultSample(input_fit_parameters.flag)
sample.read_from(files.data)

# fina parameters
final_parameters = final_result(filename_config,fit_parameters_config,angle_config,'180')

model = Models.triple
size = 512
u,v = Grid(size).uv_meshgrid()

#create zones
f_ar_lenght = len(fit_result.f_ar)
sample_f_ar_lenght = len(sample.f)
zones = np.ma.array(np.zeros((f_ar_lenght,size,size)))
ps_zones = np.ma.array(np.zeros((f_ar_lenght,size,size)))
residuals = np.ma.array(np.zeros((f_ar_lenght,size,size)))

# model
#plt.figure()
#for i in range(f_ar_lenght):
#    zones[i] = ring_mask(model(u,v,fit_result.I1_ar[i],\
#                                fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i],\
#                                fit_result.dm31_ar[i],fit_result.x3_ar[i],fit_result.y3_ar[i]),\
#                                fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)
#    plt.imshow(zones[i], cmap='gray')
#plt.savefig(files.images + '\\model_ps.png')


#residuals
for i in range(f_ar_lenght):
    zones[i] = ring_mask(model(u,v,fit_result.I1_ar[i],\
                                fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i],\
                                fit_result.dm31_ar[i],fit_result.x3_ar[i],fit_result.y3_ar[i]),\
                                fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)
    ps_zones[i] = ring_mask(data.rmbg_final_ps.values,fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)
    residuals[i] = (ps_zones[i]-zones[i])**2
residuals_frame = np.ma.concatenate([residuals[i] for i in range(f_ar_lenght)], axis=1)
plt.imshow(residuals_frame, cmap='gray')
plt.colorbar()
plt.savefig(files.images + '\\residuals2d.png')


#clean_model
#plt.figure()
#for i in range(sample_f_ar_lenght):
#    zones[i] = ring_mask(model(u,v,sample.I1[i],\
#                                final_parameters.dm21,final_parameters.x2,final_parameters.y2,\
#                                final_parameters.dm31,final_parameters.x3,final_parameters.y3),\
#                                sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)
#    plt.imshow(zones[i], cmap='gray')
#plt.savefig(files.images + '\\clean_model_ps.png')


##clean residuals
#plt.figure()
#for i in range(sample_f_ar_lenght):
#    zones[i] = ring_mask(model(u,v,sample.I1[i],\
#                                final_parameters.dm21,final_parameters.x2,final_parameters.y2,\
#                                final_parameters.dm31,final_parameters.x3,final_parameters.y3),\
#                                sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)
#    ps_zones[i] = ring_mask(data.rmbg_final_ps.values,sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)
#    plt.imshow((ps_zones[i]-zones[i])**2/ps_zones[i]**2, cmap='gray')
#plt.colorbar()
#plt.savefig(files.images + '\\clean_residuals2d.png')
plt.show()




