import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import *
from power_spectrum import *

files = DataFiles()
files.read_input('C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TEST_star_input.txt')
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
plt.imshow(data.ref_ps.values, cmap='gray',vmin=np.min(data.ref_ps.values),vmax=np.max(data.ref_ps.values)/1e6)
plt.title('ref')
plt.savefig(files.images + '\\ref_ps.png')

plt.figure()
plt.imshow(data.star_ps.values, cmap='gray',vmin=np.min(data.star_ps.values),vmax=np.max(data.star_ps.values)/1e8)
plt.title('obj')
plt.savefig(files.images + '\\star_ps.png')

plt.figure()
plt.imshow(data.final_ps.values, cmap='gray',vmin=0,vmax=0.02)
plt.title('obj/ref')
plt.savefig(files.images + '\\final_ps.png')

plt.figure()
plt.imshow(data.final_ps.clean_ps, cmap='gray',vmin=0,vmax=0.02)
plt.title('rmbg obj/ref')
plt.savefig(files.images + '\\final_rmbg_ps.png')
plt.show()

