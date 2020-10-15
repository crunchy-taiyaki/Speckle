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
    x550 = np.array([256.0-256.0, 254.338-256.0])
    y550 = np.array([256.0-256.0, 252.83-256.0])
    files = DataFiles()
    files.read_input(filename_config)
    acf = calc_acf(filename_config)
    plt.figure()
    plt.imshow(acf, cmap='gray', vmin=np.min(acf), vmax=np.max(acf)/10000, extent=[-256.0,256.0,256.0,-256.0])
    plt.scatter(x550,y550, color='red', s=0.5)
    plt.title('acf')
    plt.savefig(files.images + '\\acf final_ps.png')
    plt.show(block=False)

def guess_xy(filename_config):
    plot_acf(filename_config)
    x = float(input('enter x:'))
    y = float(input('enter y:'))
    print('please write to config..')
    print('x =', y, 'y = ', x)

