
import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from plot import define_ylim

def plot_projections(filename_config):

    files = DataFiles()
    files.read_input(filename_config)
    files.info()

    #read data from files
    data = Data()
    data.read_from(files.data)

    ###plot spectra for finding bound freq
    freq_axis = np.arange(-256.0,256.0)

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.values[256,:])
    plt.yscale('log')
    plt.title('ref x')
    plt.savefig(files.images + '\\ref_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.values[:,256])
    plt.yscale('log')
    plt.title('ref y')
    plt.savefig(files.images + '\\ref_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.clean_ps[256,:])
    plt.yscale('log')
    plt.title('rmbg ref x')
    plt.savefig(files.images + '\\rmbg_ref_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.clean_ps[:,256])
    plt.yscale('log')
    plt.title('rmbg ref y')
    plt.savefig(files.images + '\\rmbg_ref_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.values[256,:])
    plt.yscale('log')
    plt.title('star x')
    plt.savefig(files.images + '\\star_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.values[:,256])
    plt.yscale('log')
    plt.title('star y')
    plt.savefig(files.images + '\\star_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.clean_ps[256,:])
    plt.yscale('log')
    plt.title('rmbg star x')
    plt.savefig(files.images + '\\rmbg_star_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.clean_ps[:,256])
    plt.yscale('log')
    plt.title('rmbg star y')
    plt.savefig(files.images + '\\rmbg_star_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.final_ps.values[256,:])
    plt.title('final ps x')
    plt.savefig(files.images + '\\final_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.final_ps.values[:,256])
    plt.title('final ps y')
    plt.savefig(files.images + '\\final_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.rmbg_final_ps.values[256,:])
    plt.title('rmbg final ps x')
    plt.savefig(files.images + '\\final_rmbg_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.rmbg_final_ps.values[:,256])
    plt.title('rmbg final ps y')
    plt.savefig(files.images + '\\final_rmbg_ps_y.png')
    plt.show()