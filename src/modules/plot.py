import numpy as np
import matplotlib.pyplot as plt
from file_reader import InputReader
from spectra_calculator import Data

def plot_images(filename_config):
    files = InputReader()
    files.read(filename_config)
    data = Data()

    #read data from files
    data.read_from(files.data)
    size = data.star_ps.values.shape[0]
    half_size = size//2

    plt.figure()
    plt.imshow(np.log(data.star_ps.values),cmap='gray',extent=[-half_size,half_size,-half_size,half_size])
    plt.title('star')
    plt.colorbar()
    plt.savefig(files.images + '\\star_ps.png')

    if (files.ref is None):
        plt.figure()
        plt.imshow(np.log(data.final_ps.values), cmap='gray',extent=[-half_size,half_size,-half_size,half_size])
        plt.title('final ps')
        plt.colorbar()
        plt.savefig(files.images + '\\final_ps.png')

        plt.figure()
        plt.imshow(np.log(data.rmbg_final_ps.values), cmap='gray',extent=[-half_size,half_size,-half_size,half_size])
        plt.title('rmbg final ps')
        plt.colorbar()
        plt.savefig(files.images + '\\final_rmbg_ps.png')
    else:
        plt.imshow(np.log(data.ref_ps.values), cmap='gray',extent=[-half_size,half_size,-half_size,half_size])
        plt.title('ref')
        plt.colorbar()
        plt.savefig(files.images + '\\ref_ps.png')

        plt.figure()
        plt.imshow(data.final_ps.values, cmap='gray',extent=[-half_size,half_size,-half_size,half_size])
        plt.title('final ps')
        plt.colorbar()
        plt.savefig(files.images + '\\final_ps.png')

        plt.figure()
        plt.imshow(data.rmbg_final_ps.values, cmap='gray',extent=[-half_size,half_size,-half_size,half_size])
        plt.title('rmbg final ps')
        plt.colorbar()
        plt.savefig(files.images + '\\final_rmbg_ps.png')
    plt.show()


def plot_spectra_slices(filename_config):

    files = InputReader()
    files.read(filename_config)

    #read data from files
    data = Data()
    data.read_from(files.data)

    size = data.star_ps.values.shape[0]
    half_size = size//2
    freq_axis = np.arange(-half_size,half_size)

    scale = 'log'

    plt.plot(freq_axis, data.star_ps.values[half_size,:])
    plt.yscale(scale)
    plt.title('star x')
    plt.savefig(files.images + '\\star_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.values[:,half_size])
    plt.yscale(scale)
    plt.title('star y')
    plt.savefig(files.images + '\\star_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.clean_ps[half_size,:])
    plt.yscale(scale)
    plt.title('rmbg star x')
    plt.savefig(files.images + '\\rmbg_star_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.clean_ps[:,half_size])
    plt.yscale(scale)
    plt.title('rmbg star y')
    plt.savefig(files.images + '\\rmbg_star_ps_y.png')

    if (files.ref is not None):    
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

    if (files.ref is None):
        scale = 'log'
    else:
        scale = 'linear'

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
