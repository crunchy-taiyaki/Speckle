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
    acf = np.abs(np.fft.ifft2(data.final_ps.values))
    acf = np.fft.fftshift(acf)
    return acf

def plot_acf(filename_config):
    files = DataFiles()
    files.read_input(filename_config)
    acf = calc_acf(filename_config)
    plt.figure()
    plt.imshow(acf, cmap='gray', vmin=np.min(acf), vmax=np.max(acf)/100)
    plt.title('acf')
    plt.savefig(files.images + '\\acf final_ps.png')
    plt.show(block=False)

def guess_xy(filename_config):
    plot_acf(filename_config)
    x = float(input('enter x:'))
    y = float(input('enter y:'))
    print('please write to config..')
    print('x2 =', y-256, 'y2 = ', x-256)

