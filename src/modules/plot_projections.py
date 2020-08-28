
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

    #plt.figure()
    #plt.plot(freq_axis, data.dark[256,:])
    #plt.title('dark x')

    #plt.figure()
    #plt.plot(freq_axis, data.dark[:,256])
    #plt.title('dark y')

    #plt.figure()
    #plt.plot(data.flat[256,:])
    #plt.title('flat x')

    #plt.figure()
    #plt.plot(freq_axis, data.flat[:,256])
    #plt.title('flat y')

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.values[256,:])
    plt.yscale('log')
    ymin,ymax = define_ylim(data.ref_ps)
    #plt.ylim(ymin,ymax)
    plt.title('ref x')
    plt.savefig(files.images + '\\ref_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.ref_ps.values[:,256])
    plt.yscale('log')
    ymin,ymax = define_ylim(data.ref_ps)
    #plt.ylim(ymin,ymax)
    plt.title('ref y')
    plt.savefig(files.images + '\\ref_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.values[256,:])
    plt.yscale('log')
    ymin,ymax = define_ylim(data.star_ps)
    #plt.ylim(ymin,ymax)
    plt.title('star x')
    plt.savefig(files.images + '\\star_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.star_ps.values[:,256])
    plt.yscale('log')
    ymin,ymax = define_ylim(data.star_ps)
    #plt.ylim(ymin,ymax)
    plt.title('star y')
    plt.savefig(files.images + '\\star_ps_y.png')

    plt.figure()
    plt.plot(freq_axis, data.final_ps.values[256,:])
    plt.title('final ps x')
    ymin,ymax = define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.savefig(files.images + '\\final_ps_x.png')

    plt.figure()
    plt.plot(freq_axis, data.final_ps.values[:,256])
    plt.title('final ps y')
    ymin,ymax = define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.savefig(files.images + '\\final_ps_y.png')

    plt.figure()
    plt.plot(data.final_ps.clean_ps[256,:])
    plt.title('rmbg final ps x')
    ymin,ymax = define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.savefig(files.images + '\\final_rmbg_ps_x.png')

    plt.figure()
    plt.plot(data.final_ps.clean_ps[:,256])
    plt.title('rmbg final ps y')
    ymin,ymax = define_ylim(data.final_ps)
    plt.ylim(ymin,ymax)
    plt.savefig(files.images + '\\final_rmbg_ps_y.png')
    plt.show()