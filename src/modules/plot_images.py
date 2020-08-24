import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from plot import define_ylim

def plot_dark_flat_and_spectra_image(filename_config):

    files = DataFiles()
    files.read_input(filename_config)
    files.info()
    data = Data()

    #read data from files
    data.read_from(files.data)

    #plot spectra for finding bound freq
    #plt.figure()
    #plt.imshow(data.dark, cmap='gray', vmin=195.0, vmax=210.0)
    #plt.title('dark')

    #plt.figure()
    #plt.imshow(data.flat, cmap='gray')
    #plt.title('flat')

    plt.figure()
    vmin,vmax = define_ylim(data.ref_ps)
    plt.imshow(data.ref_ps.values, cmap='gray',vmin=vmin,vmax=vmax/10)
    plt.title('ref')
    plt.savefig(files.images + '\\ref_ps.png')

    plt.figure()
    vmin,vmax = define_ylim(data.star_ps)
    plt.imshow(data.star_ps.values, cmap='gray',vmin=vmin,vmax=vmax/10)
    plt.title('star')
    plt.savefig(files.images + '\\star_ps.png')

    plt.figure()
    vmin,vmax = define_ylim(data.final_ps)
    plt.imshow(data.final_ps.values, cmap='gray',vmin=vmin,vmax=vmax)
    plt.title('final ps')
    plt.savefig(files.images + '\\final_ps.png')

    plt.figure()
    vmin,vmax = define_ylim(data.final_ps)
    plt.imshow(data.final_ps.clean_ps, cmap='gray',vmin=vmin,vmax=vmax)
    plt.title('rmbg final ps')
    plt.savefig(files.images + '\\final_rmbg_ps.png')
    plt.show()

