import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data
from plot import define_ylim

def calc_acf(filename_config):
    files = DataFiles()
    files.read_input(filename_config)
    files.info()
    data = Data()

    #read data from files
    data.read_from(files.data)
    acf = np.abs(np.fft.ifft2(data.final_ps))
    acf = np.fft.fftshift(acf)
    return acf

def plot_acf(filename_config):
    acf = calc_acf(filename_config)
    plt.figure()
    plt.imshow(acf, cmap='gray')
    plt.title('acf')
    plt.savefig(files.images + '\\acf final_ps.png')
