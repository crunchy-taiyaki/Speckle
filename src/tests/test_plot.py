import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import *
from power_spectrum import *

files = DataFiles()
files.read_input('C:\\Users\\Marta\\source\\repos\\PythonApplication5\\PythonApplication5\\inputs\\TEST_star_input.txt')
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
plt.imshow(data.ref_ps, cmap='gray',vmin=np.min(data.ref_ps),vmax=np.max(data.ref_ps)/1e5)
plt.title('ref')

plt.figure()
plt.imshow(data.star_ps, cmap='gray',vmin=np.min(data.star_ps),vmax=np.max(data.star_ps)/1e8)
plt.title('obj')

plt.figure()
plt.imshow(data.final_ps, cmap='gray',vmin=0,vmax=0.01)
plt.title('obj/ref')
plt.show()

