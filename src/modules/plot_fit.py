import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from models import Models
from fit import FitResult
from plot import slice_image, define_ylim

def plot_fitted_i_xy_dm(filename_config):

    #read config file
    files = DataFiles()
    files.read_input(filename_config)
    files.info()

    #read data from files
    data = Data()
    data.read_from(files.data)

    #read i xy dm from files
    fit_result = FitResult('binary')
    fit_result.read_i_xy_dm_freq_from(files.data)

    # plot
    #____________amplitude________________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.I1_ar)
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    plt.title('amplitude')
    plt.savefig(files.images + '\\I.png')

    #_____________________max ps band_____________________
    plt.figure()
    plt.plot(slice_image(data.final_ps.values,x1=56,y1=256,x2=253.546,y2=253.277))
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    ymin,ymax=define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.title('max ps band')
    plt.savefig(files.images + '\\max_ps_band.png')

    #_____________________min ps band_____________________
    plt.figure()
    plt.plot(slice_image(data.final_ps.values,x1=256,y1=256,x2=512,y2=512))
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    ymin,ymax=define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.title('min ps band')
    plt.savefig(files.images + '\\min_ps_band.png')

    #______________________dm21_____________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.dm21_ar)
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    plt.title('dm21')
    plt.savefig(files.images + '\\dm21.png')

    #_____________________dm21 vs x ps___________________
    plt.figure(figsize=(8,8))
    plt.subplot(2,1,1)
    plt.scatter(fit_result.f_ar,fit_result.dm21_ar)
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    plt.title('dm21')
    plt.subplot(2,1,2)
    plt.plot(data.final_ps.values[256,:])
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    ymin,ymax=define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.xlim(256,512)
    #plt.xlim(fit_result.f_ar[0],fit_result.f_ar[-1])
    plt.title('x final ps')
    plt.savefig(files.images + '\\dm21_vs_x_ps.png')

    #_____________________dm21 vs y ps___________________
    plt.figure(figsize=(8,8))
    plt.subplot(2,1,1)
    plt.scatter(fit_result.f_ar,fit_result.dm21_ar)
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    plt.title('dm21')
    plt.subplot(2,1,2)
    plt.plot(data.final_ps.values[:,256])
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    ymin,ymax=define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.xlim(256,512)
    #plt.xlim(fit_result.f_ar[0],fit_result.f_ar[-1])
    plt.title('y final ps')
    plt.savefig(files.images + '\\dm21_vs_y_ps.png')

    #____________________x2____________________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.x2_ar)
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    plt.title('x2')
    plt.savefig(files.images + '\\x2.png')

    #_____________________x2 vs x ps___________________
    plt.figure(figsize=(8,8))
    plt.subplot(2,1,1)
    plt.scatter(fit_result.f_ar,fit_result.x2_ar)
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    plt.title('x2')
    plt.subplot(2,1,2)
    plt.plot(data.final_ps.values[256,:])
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    ymin,ymax=define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.xlim(256,512)
    #plt.xlim(fit_result.f_ar[0],fit_result.f_ar[-1])
    plt.title('x final ps')
    plt.savefig(files.images + '\\x2_vs_ps.png')

    #_______________________y2___________________
    plt.figure()
    plt.scatter(fit_result.f_ar,fit_result.y2_ar)
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    plt.title('y2')
    plt.savefig(files.images + '\\y2.png')

    #_____________________y2 vs y ps___________________
    plt.figure(figsize=(8,8))
    plt.subplot(2,1,1)
    plt.scatter(fit_result.f_ar,fit_result.y2_ar)
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    plt.title('y2')
    plt.subplot(2,1,2)
    plt.plot(data.final_ps.values[:,256])
    plt.axvline(data.final_ps.b_bound,color='green')
    plt.axvline(data.final_ps.up_bound,color='green')
    ymin,ymax=define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.xlim(256,512)
    #plt.xlim(fit_result.f_ar[0],fit_result.f_ar[-1])
    plt.title('y final ps')
    plt.savefig(files.images + '\\y2_vs_ps.png')

    plt.show()