import numpy as np
import matplotlib.pyplot as plt
from file_reader import FileInfoReader, FitParametersReader
from spectra_calculator import Data
from models import Models
from fit import FitResult
from initial_parameters_builder import BinaryInitialParameters, BinaryInitialParametersFixDM, BinaryInitialParametersFixXY,\
                                       TripleInitialParameters, TripleInitialParametersFixDM, TripleInitialParametersFixXY 
from grid import Grid
from stats import ResultSample
from final_params import final_result
from masks import ring_logical_mask, ring_mask
from plot_tools import plot_rings_borders, to_polar, angle_idx, radius_idx

## triple hd52721 550 04_03_2020 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020_no_ref\\angle.txt'

## triple hd52721 550 04_03_2020
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\angle.txt'

## TYC1947_00290_1 09 12 2019 700
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912\\angle.txt'

## TYC1947_00290_1 09 12 2019 700 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912_no_ref\\angle.txt'

## TYC1947_00290_1 03 08 2020 700 no ref
filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200308_no_ref\\input.txt'
fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200308_no_ref\\fit_parameters.txt'
angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200308_no_ref\\angle.txt'

## TYC1947_00290_1 05 11 2020 700 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200511_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200511_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200511_no_ref\\angle.txt'

def residuals_by_ring(ps, model, fit_result):
    u,v = Grid(size).uv_meshgrid()
    model_frame = np.empty((size,size))
    f_ar_lenght = len(fit_result.f_ar)
    for i in range(f_ar_lenght-1):
        if (input_fit_parameters.star_type == 'triple'):
            i_model = model(u,v,fit_result.I1_ar[i],\
                        fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i],\
                        fit_result.dm31_ar[i],fit_result.x3_ar[i],fit_result.y3_ar[i])
        else:
            i_model = model(u,v,fit_result.I1_ar[i],\
                        fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i])
        mask = ring_logical_mask(size, fit_result.f_ar[i],fit_result.f_ar[i+1])
        model_frame = np.where(mask, model_frame, i_model)
    return ps - model_frame

def residuals(ps, model,I1_ar,f_ar, final_parameters):
    u,v = Grid(size).uv_meshgrid()
    model_frame = np.empty((size,size))
    f_ar_lenght = len(f_ar)
    for i in range(f_ar_lenght-1):
        if (input_fit_parameters.star_type == 'triple'):
            i_model = model(u,v,I1_ar[i],\
                        final_parameters.dm21,final_parameters.x2,final_parameters.y2,\
                        final_parameters.dm31,final_parameters.x3,final_parameters.y3)
        else:
            i_model = model(u,v,I1_ar[i],\
                        final_parameters.dm21,final_parameters.x2,final_parameters.y2)
        mask = ring_logical_mask(size, f_ar[i], f_ar[i+1])
        model_frame = np.where(mask, model_frame, i_model)
    return ps - model_frame

files = FileInfoReader()
files.read(filename_config)

data = Data()
data.read_from(files.data)
size = data.star_ps.values.shape[0]
half_size = size//2
ps = data.rmbg_final_ps.values

input_fit_parameters = FitParametersReader()
input_fit_parameters.read(fit_parameters_config)

if (input_fit_parameters.star_type == 'triple'):
    model = Models.triple
else:
    model = Models.binary


fit_result = FitResult(filename_config,fit_parameters_config)
fit_result.read(files.data)

ring_residual = residuals_by_ring(ps, model, fit_result)
plt.figure()
plt.imshow(ring_residual)
plt.colorbar()
plt.show()

sample = ResultSample(input_fit_parameters.star_type)
sample.read_from(files.data)
final_parameters = final_result(filename_config,fit_parameters_config,angle_config,'180')

residuals_data = residuals(ps, model, fit_result.I1_ar, fit_result.f_ar, final_parameters)
plt.figure()
plt.imshow(residuals_data)
plt.colorbar()
plt.show()




