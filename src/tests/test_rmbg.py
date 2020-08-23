import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
import matplotlib.pyplot as plt
import numpy as np
from initial_parameters import DataFiles
from power_spectrum import Data, remove_background
from plot import define_ylim,slice_image


#read config file
files = DataFiles()
files.read_input('C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TEST_star_input.txt')
files.info()

#read data from files
data = Data()
data.read_from(files.data)

image = data.star_ps.values
new_image = remove_background(data.star_ps.values,512)

plt.figure()
plt.imshow(image,cmap='gray',vmin=np.min(image),vmax=np.max(image)/1e8)

plt.figure()
plt.imshow(new_image,cmap='gray',vmin=np.min(new_image),vmax=np.max(new_image)/1e8)

plt.figure()
plt.plot(slice_image(data.star_ps.values,0,0,512,512),label='star ps')
plt.plot(slice_image(remove_background(data.star_ps.values,512),0,0,512,512),label='rmbg star ps')
ymin,ymax = define_ylim(data.star_ps)
plt.ylim(ymin,ymax)
plt.yscale('log')
plt.legend()

plt.show()