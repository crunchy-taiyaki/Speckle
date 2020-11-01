import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import DataFiles
from power_spectrum import Data

def calc_acf(filename_config):
    files = DataFiles()
    files.read_input(filename_config)
    files.info()
    data = Data()

    #read data from files
    data.read_from(files.data)
    ps = data.final_ps.values
    acf = np.abs(np.fft.ifft2(ps))
    acf = np.fft.fftshift(acf)
    return acf

def plot_acf(filename_config):
    files = DataFiles()
    files.read_input(filename_config)
    acf = calc_acf(filename_config)
    size = acf.shape[0]
    half_size = size//2
    plt.figure()
    plt.imshow(acf, cmap='gray', vmin=np.min(acf), vmax=np.max(acf), extent=[-half_size,half_size,half_size,-half_size])
    plt.title('acf')
    plt.savefig(files.images + '\\acf final_ps.png')
    plt.show(block=False)

def guess_xy(filename_config):
    plot_acf(filename_config)
    x = float(input('enter x:'))
    y = float(input('enter y:'))
    print('please write to config..')
    print('x =', y, 'y = ', x)

