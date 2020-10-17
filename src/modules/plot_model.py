import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from models import Models
from fit import FitParameters, BinaryInitialParameters, TripleInitialParameters, FitResult
from grid import Grid
from stats import ResultSample
from final_params import final_result
from masks import ring_logical_mask, ring_mask
from plot import plot_rings_borders

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
size = data.star_ps.shape[0]
half_size = size//2
u,v = Grid(size).uv_meshgrid()

#create zones
f_ar_lenght = len(fit_result.f_ar)
sample_f_ar_lenght = len(sample.f)
zones = np.empty((f_ar_lenght,size,size))
ps = data.rmbg_final_ps.values
model_data = np.empty_like(ps)
clean_model_data = np.empty_like(ps)


freq_axis = np.arange(-half_size,half_size)
print(sample.f)
if (input_fit_parameters.flag == 'triple'):
    model = Models.triple
    # model
    plt.figure()
    for i in range(f_ar_lenght):
        mask = ring_logical_mask(size,fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)
        model_data[mask] = model(u,v,fit_result.I1_ar[i],\
                                    fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i],\
                                    fit_result.dm31_ar[i],fit_result.x3_ar[i],fit_result.y3_ar[i])[mask]
    plot_rings_borders(0,0,input_fit_parameters.mask_b_freq_border,input_fit_parameters.mask_up_freq_border)
    plt.imshow(ring_mask(model_data,fit_result.f_ar[0],fit_result.f_ar[-11]), cmap='gray', extent=[-half_size,half_size,-half_size,half_size])
    plt.title('model')
    plt.colorbar()
    plt.savefig(files.images + '\\model_ps.png')

    #residuals
    plt.figure()
    for i in range(f_ar_lenght):
        mask = ring_logical_mask(size,fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)
        model_data[mask] = model(u,v,fit_result.I1_ar[i],\
                                    fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i],\
                                    fit_result.dm31_ar[i],fit_result.x3_ar[i],fit_result.y3_ar[i])[mask]
        values = np.sqrt((model_data[mask]-ps[mask])**2/ps[mask]**2)
        residuals[mask] = values
    plot_rings_borders(0,0,input_fit_parameters.mask_b_freq_border,input_fit_parameters.mask_up_freq_border)
    plt.imshow(ring_mask(residuals,fit_result.f_ar[0],fit_result.f_ar[-11]), cmap='gray', extent=[-half_size,half_size,-half_size,half_size]\
                                                 ,vmin=0,vmax=0.5)
    plt.colorbar()
    plt.savefig(files.images + '\\residuals2d.png')

    plt.figure()
    for i in range(sample_f_ar_lenght):
        mask = ring_logical_mask(size,sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)
        clean_model_data[mask] = model(u,v,sample.I1[i],\
                                    final_parameters.dm21,final_parameters.x2,final_parameters.y2,\
                                    final_parameters.dm31,final_parameters.x3,final_parameters.y3)[mask]
    plt.imshow(ring_mask(clean_model_data,sample.f[0],sample.f[-1]), cmap='gray', extent=[-half_size,half_size,-half_size,half_size])
    plt.colorbar()
    plt.savefig(files.images + '\\clean_model_ps.png')


    #clean residuals
    plt.figure()
    for i in range(sample_f_ar_lenght):
        mask = ring_logical_mask(size,sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)
        clean_model_data[mask] = model(u,v,sample.I1[i],\
                                    final_parameters.dm21,final_parameters.x2,final_parameters.y2,\
                                    final_parameters.dm31,final_parameters.x3,final_parameters.y3)[mask]
        values = np.sqrt((clean_model_data[mask]-ps[mask])**2/ps[mask]**2)
        residuals[mask] = values
    plt.imshow(ring_mask(residuals,sample.f[0],sample.f[-1]), cmap='gray',extent=[-half_size,half_size,-half_size,half_size],vmin=0,vmax=0.5)
    plt.colorbar()
    plt.savefig(files.images + '\\clean_residuals2d.png')


    plt.figure()
    plt.plot(ring_mask(model(u,v,1.0, final_parameters.dm21,final_parameters.x2,final_parameters.y2,\
                                    final_parameters.dm31,final_parameters.x3,final_parameters.y3),sample.f[0],sample.f[-1])[:,half_size],label='model')
    plt.plot(ring_mask(ps,sample.f[0],sample.f[-1])[:,half_size],label='ps')
    plt.legend()
    plt.show()

else:
    model = Models.binary
    if np.logical_not(np.all(np.isnan(data.ref_ps.values))):
        plt.figure()
        for i in range(f_ar_lenght):
            clean_model_data = model(u,v,fit_result.I1_ar[i],\
                                        fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i])
            plt.plot(freq_axis,ring_mask(clean_model_data,\
                fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[half_size,:],color='darkorange',label='model')
        plt.plot(freq_axis,ring_mask(ps,fit_result.f_ar[0],fit_result.f_ar[-1])[half_size,:],color='black',alpha=0.6,label='ps')
        plt.title('model_ps x')
        plt.savefig(files.images + '\\model_ps_x.png')

        plt.figure()
        for i in range(f_ar_lenght):
            clean_model_data = model(u,v,fit_result.I1_ar[i],\
                                        fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i])
            plt.plot(freq_axis,ring_mask(clean_model_data,\
                fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[:,half_size],color='darkorange',label='model')
        plt.plot(freq_axis,ring_mask(ps,fit_result.f_ar[0],fit_result.f_ar[-1])[:,half_size],color='black',alpha=0.6,label='ps')
        plt.title('model_ps y')
        plt.savefig(files.images + '\\model_ps_y.png')

        plt.figure()
        for i in range(sample_f_ar_lenght):
            clean_model_data = model(u,v,sample.I1[i],\
                                        final_parameters.dm21,final_parameters.x2,final_parameters.y2)
            plt.plot(freq_axis,ring_mask(clean_model_data,sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)[half_size,:],\
                                         color='darkorange',label='model')
        plt.plot(freq_axis,ring_mask(ps,sample.f[0],sample.f[-1])[half_size,:],color='black',alpha=0.6,label='ps')
        plt.title('clean model_ps x')
        plt.savefig(files.images + '\\clean_model_ps_x.png')

        plt.figure()
        for i in range(sample_f_ar_lenght):
            clean_model_data = model(u,v,sample.I1[i],\
                                        final_parameters.dm21,final_parameters.x2,final_parameters.y2)
            plt.plot(freq_axis,ring_mask(clean_model_data,sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)[:,half_size],\
                                      color='darkorange',label='model')
        plt.plot(freq_axis,ring_mask(ps,sample.f[0],sample.f[-1])[:,half_size],color='black',alpha=0.6,label='ps')
        plt.title('clean model_ps y')
        plt.savefig(files.images + '\\clean_model_ps_y.png')
    else:
        plt.figure()
        for i in range(f_ar_lenght):
            clean_model_data = model(u,v,fit_result.I1_ar[i],\
                                        fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i])
            plt.plot(freq_axis,ring_mask(clean_model_data,\
                fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[half_size,:],color='darkorange',label='model')
        plt.plot(freq_axis,ring_mask(ps,fit_result.f_ar[0],fit_result.f_ar[-1])[half_size,:],color='black',alpha=0.6,label='ps')
        plt.yscale('log')
        plt.title('model_ps x')
        plt.savefig(files.images + '\\model_ps_x.png')

        plt.figure()
        for i in range(f_ar_lenght):
            clean_model_data = model(u,v,fit_result.I1_ar[i],\
                                        fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i])
            plt.plot(freq_axis,ring_mask(clean_model_data,\
                fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[:,half_size],color='darkorange',label='model')
        plt.plot(freq_axis,ring_mask(ps,fit_result.f_ar[0],fit_result.f_ar[-1])[:,half_size],color='black',alpha=0.6,label='ps')
        plt.yscale('log')
        plt.title('model_ps y')
        plt.savefig(files.images + '\\model_ps_y.png')

        plt.figure()
        for i in range(sample_f_ar_lenght):
            clean_model_data = model(u,v,sample.I1[i],\
                                        final_parameters.dm21,final_parameters.x2,final_parameters.y2)
            plt.plot(freq_axis,ring_mask(clean_model_data,sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)[half_size,:],\
                      color='darkorange',label='model')
        plt.plot(freq_axis,ring_mask(ps,sample.f[0],sample.f[-1])[half_size,:],color='black',alpha=0.6,label='ps')
        plt.yscale('log')
        plt.title('clean model_ps x')
        plt.savefig(files.images + '\\clean_model_ps_x.png')

        plt.figure()
        for i in range(sample_f_ar_lenght):
            clean_model_data = model(u,v,sample.I1[i],\
                                        final_parameters.dm21,final_parameters.x2,final_parameters.y2)
            plt.plot(freq_axis,ring_mask(clean_model_data,sample.f[i],sample.f[i]+input_fit_parameters.bandwidth)[:,half_size],\
                                         color='darkorange',label='model')
        plt.plot(freq_axis,ring_mask(ps,sample.f[0],sample.f[-1])[:,half_size],color='black',alpha=0.6,label='ps')
        plt.yscale('log')
        plt.title('clean model_ps y')
        plt.savefig(files.images + '\\clean_model_ps_y.png')
    plt.show()




