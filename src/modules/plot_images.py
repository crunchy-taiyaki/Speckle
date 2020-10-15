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
    plt.imshow(np.log(data.ref_ps.values), cmap='gray',vmin=10.,vmax=15.,extent=[-256.0,256.0,-256.0,256.0])
    plt.title('ref')
    plt.colorbar()
    plt.savefig(files.images + '\\ref_ps.png')

    plt.figure()
    vmin,vmax = define_ylim(data.star_ps)
    plt.imshow(np.log(data.star_ps.values), cmap='gray',vmin=11.,vmax=13.,extent=[-256.0,256.0,-256.0,256.0])
    plt.title('star')
    plt.colorbar()
    plt.savefig(files.images + '\\star_ps.png')

    plt.figure()
    vmin,vmax = define_ylim(data.final_ps)
    plt.imshow(data.final_ps.values, cmap='gray',vmin=vmin,vmax=vmax,extent=[-256.0,256.0,-256.0,256.0])
    plt.title('final ps')
    plt.colorbar()
    plt.savefig(files.images + '\\final_ps.png')

    plt.figure()
    vmin,vmax = define_ylim(data.rmbg_final_ps)
    plt.imshow(data.rmbg_final_ps.values, cmap='gray',vmin=vmin,vmax=vmax,extent=[-256.0,256.0,-256.0,256.0])
    plt.title('rmbg final ps')
    plt.colorbar()
    plt.savefig(files.images + '\\final_rmbg_ps.png')
    plt.show()

