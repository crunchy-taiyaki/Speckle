
import numpy as np
import matplotlib.pyplot as plt
from file_reader import FileInfoReader
from spectra_calculator import Data
from plot_tools import define_ylim

def plot_spectra_projections(filename_config):

    files = FileInfoReader()
    files.read(filename_config)

    #read data from files
    data = Data()
    data.read_from(files.data)

    ###plot spectra for finding bound freq
    size = data.star_ps.values.shape[0]
    half_size = size//2
    freq_axis = np.arange(-half_size,half_size)
    
    if (files.ref is None):
        scale = 'log'
    else:
        scale = 'linear'

    plt.plot(freq_axis, data.ref_ps.values[half_size,:])
    plt.yscale(scale)
    plt.title('ref x')
    plt.savefig(files.images + '\\ref_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.values[:,half_size])
    plt.yscale(scale)
    plt.title('ref y')
    plt.savefig(files.images + '\\ref_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.clean_ps[half_size,:])
    plt.yscale(scale)
    plt.title('rmbg ref x')
    plt.savefig(files.images + '\\rmbg_ref_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.clean_ps[:,half_size])
    plt.yscale(scale)
    plt.title('rmbg ref y')
    plt.savefig(files.images + '\\rmbg_ref_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.final_ps.values[half_size,:])
    plt.yscale(scale)
    plt.title('final ps x')
    plt.savefig(files.images + '\\final_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.final_ps.values[:,half_size])
    plt.yscale(scale)
    plt.title('final ps y')
    plt.savefig(files.images + '\\final_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.rmbg_final_ps.values[half_size,:])
    plt.yscale(scale)
    plt.title('rmbg final ps x')
    plt.savefig(files.images + '\\final_rmbg_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.rmbg_final_ps.values[:,half_size])
    plt.yscale(scale)
    plt.title('rmbg final ps y')
    plt.savefig(files.images + '\\final_rmbg_ps_y.png')
    plt.show()