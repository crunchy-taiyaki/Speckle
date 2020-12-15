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


files = FileInfoReader()
files.read(filename_config)

data = Data()
data.read_from(files.data)

input_fit_parameters = FitParametersReader()
input_fit_parameters.read(fit_parameters_config)

#read i xy dm from files
fit_result = FitResult(filename_config,fit_parameters_config)
fit_result.read(files.data)

sample = ResultSample(input_fit_parameters.star_type)
sample.read_from(files.data)

final_parameters = final_result(filename_config,fit_parameters_config,angle_config,'180')
size = data.star_ps.values.shape[0]
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
polar_residuals = np.empty((size,size))
i_residuals = np.empty((size,size))


if (input_fit_parameters.star_type == 'triple'):
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
        #plt.figure()
        #for i in range(f_ar_lenght):
        #    clean_model_data = model(u,v,fit_result.I1_ar[i],\
        #                                fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i])
        #    plt.plot(freq_axis,ring_mask(clean_model_data,\
        #        fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[half_size,:],color='darkorange',label='model')
        #plt.plot(freq_axis,ring_mask(ps,fit_result.f_ar[0],fit_result.f_ar[-1])[half_size,:],color='black',alpha=0.6,label='ps')
        #plt.yscale('log')
        #plt.title('model_ps x')
        #plt.savefig(files.images + '\\model_ps_x.png')

        #plt.figure()
        #for i in range(f_ar_lenght):
        #    clean_model_data = model(u,v,fit_result.I1_ar[i],\
        #                                fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i])
        #    plt.plot(freq_axis,ring_mask(clean_model_data,\
        #        fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[:,half_size],color='darkorange',label='model')
        #plt.plot(freq_axis,ring_mask(ps,fit_result.f_ar[0],fit_result.f_ar[-1])[:,half_size],color='black',alpha=0.6,label='ps')
        #plt.yscale('log')
        #plt.title('model_ps y')
        #plt.savefig(files.images + '\\model_ps_y.png')

        #fig = plt.figure()
        #ax = fig.add_subplot(121)
        #for i in range(f_ar_lenght):
        #    residuals = ps - model(u,v,fit_result.I1_ar[i],\
        #                                fit_result.dm21_ar[i],fit_result.x2_ar[i],fit_result.y2_ar[i])
        #    #plt.imshow(ring_mask(residuals,\
        #    #    fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth), cmap='gray', extent=[-256.0,256.0,256.0,-256.0])
        #    i_residuals, i_angs = to_polar(residuals,[0.,0.],512*np.sqrt(2))
        #    polar_residuals[radius_idx(fit_result.f_ar[i]),:] = i_residuals[radius_idx(fit_result.f_ar[i]),:]
        #np.save(files.data + '\\residuals.npy',polar_residuals)
        #plot = ax.imshow(polar_residuals, cmap='gray')
        #ax.set_xticks(range(0, polar_residuals.shape[1]+1, 50))
        #ax.set_xticklabels((i_angs[::50]*180/np.pi).round().astype(int))
        #ax.set_title('residuals: ps-model')
        ##fig.colorbar(plot)
        #fig.savefig(files.images + '\\residuals.png')

        #plt.figure()
        #for i in range(f_ar_lenght):
        #    clean_model_data = model(u,v,fit_result.I1_ar[i],\
        #                                final_parameters.dm21,final_parameters.x2,final_parameters.y2)
        #    plt.plot(freq_axis,ring_mask(clean_model_data,\
        #                                 fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[half_size,:],\
        #              color='red',label='model')
        #    clean_model_data = model(u,v,fit_result.I1_ar[i],\
        #                                0.2,final_parameters.x2,final_parameters.y2)
        #    plt.plot(freq_axis,ring_mask(clean_model_data,\
        #                                 fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[half_size,:],\
        #              color='blue',label='dm=0.2')
        #plt.plot(freq_axis,ring_mask(ps,fit_result.f_ar[0],fit_result.f_ar[-1])[half_size,:],color='black',alpha=0.6,label='ps')
        #plt.yscale('log')
        #plt.title('clean model_ps x')
        #plt.savefig(files.images + '\\clean_model_ps_x.png')

        #plt.figure()
        #for i in range(f_ar_lenght):
        #    clean_model_data = model(u,v,fit_result.I1_ar[i],\
        #                                final_parameters.dm21,final_parameters.x2,final_parameters.y2)
        #    plt.plot(freq_axis,ring_mask(clean_model_data,\
        #                                 fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[:,half_size],\
        #                                    color='red',label='model')
        #    clean_model_data = model(u,v,fit_result.I1_ar[i],\
        #                                0.2,final_parameters.x2,final_parameters.y2)
        #    plt.plot(freq_axis,ring_mask(clean_model_data,\
        #                                 fit_result.f_ar[i],fit_result.f_ar[i]+input_fit_parameters.bandwidth)[:,half_size],\
        #                                    color='blue',label='dm=0.2')
        #plt.plot(freq_axis,ring_mask(ps,fit_result.f_ar[0],fit_result.f_ar[-1])[:,half_size],color='black',alpha=0.6,label='ps')
        #plt.yscale('log')
        #plt.title('clean model_ps y')
        #plt.savefig(files.images + '\\clean_model_ps_y.png')


        def residuals_bound(freq):
            idx = np.where(fit_result.f_ar == freq)
            return ps - model(u,v,fit_result.I1_ar[idx],\
                                        fit_result.dm21_ar[idx],\
                                        fit_result.x2_ar[idx],fit_result.y2_ar[idx])

        def model_i(freq):
            idx = np.where(fit_result.f_ar == freq)
            return model(u,v,fit_result.I1_ar[idx],\
                                        fit_result.dm21_ar[idx],\
                                        fit_result.x2_ar[idx],fit_result.y2_ar[idx])
        def slice(image, freq):
                data = np.empty((512,512))
                for i in range(512):
                    for j in range(512):
                        if abs(((i-256)**2 + (j-256)**2) - freq**2) < 10**2:
                            data[i,j] = image[i,j]
                return data

        #image_polar = np.empty((512,512))
        #for freq in fit_result.f_ar:
        #    res_bound = residuals_bound(freq)
        #    data = slice(res_bound,freq)
        #    polar_test, angs = to_polar(data,[256.,256.],256*np.sqrt(2))
        #    image_polar[int(freq*np.sqrt(2)),:] = polar_test[int(freq*np.sqrt(2)),:]
        #fig,ax = plt.subplots(1,1,figsize=(6,8))
        #ax.imshow(image_polar,cmap='gray')
        #ax.set_xticks(range(0, polar_test.shape[1]+1, 50))
        #ax.set_xticklabels((angs[::50]*180/np.pi).round().astype(int))

        #freq = 118.
        #res_bound = residuals_bound(freq)
        #data = slice(res_bound,freq)
        #polar_test, angs = to_polar(data,[256.,256.],256*np.sqrt(2))
        #fig,ax = plt.subplots(1,1)
        #ax.plot(polar_test[int(freq*np.sqrt(2)),:])
        #ax.set_xticks(range(0, polar_test.shape[1]+1, 50))
        #ax.set_xticklabels((angs[::50]*180/np.pi).round().astype(int))  
        #plt.title('ps-model' + ' freq=' + str(freq))

        freq = 78.
        model_data = slice(model_i(freq),freq)
        ps_data = slice(ps,freq)
        polar_ps, angs = to_polar(ps_data,[256.,256.],256*np.sqrt(2))
        polar_model, angs = to_polar(model_data,[256.,256.],256*np.sqrt(2))
        fig,ax = plt.subplots(1,1)
        ax.plot(polar_ps[int(freq*np.sqrt(2)),:], label='ps')
        ax.plot(polar_model[int(freq*np.sqrt(2)),:], label='model')
        ax.set_xticks(range(0, 512, 50))
        ax.set_xticklabels((angs[::50]*180/np.pi).round().astype(int)) 
        plt.legend()
        plt.title('ps-model' + ' freq=' + str(freq))

    plt.show()




