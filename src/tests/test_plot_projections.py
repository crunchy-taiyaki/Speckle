
import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
import numpy as np
import matplotlib.pyplot as plt
from initial_parameters import *
from power_spectrum import *
from plot import define_ylim

files = DataFiles()
files.read_input('C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TEST_star_input.txt')
files.info()

#read data from files
data = Data()
data.read_from(files.data)

###plot spectra for finding bound freq
#plt.figure()
#plt.plot(data.dark[256,:])
#plt.title('dark x')

#plt.figure()
#plt.plot(data.dark[:,256])
#plt.title('dark y')

#plt.figure()
#plt.plot(data.flat[256,:])
#plt.title('flat x')

#plt.figure()
#plt.plot(data.flat[:,256])
#plt.title('flat y')

plt.figure()
plt.plot(data.ref_ps.values[256,:])
plt.yscale('log')
ymin,ymax = define_ylim(data.ref_ps)
#plt.ylim(ymin,ymax)
plt.title('ref x')
plt.savefig(files.images + '\\ref_ps_x.png')

plt.figure()
plt.plot(data.ref_ps.values[:,256])
plt.yscale('log')
ymin,ymax = define_ylim(data.ref_ps)
#plt.ylim(ymin,ymax)
plt.title('ref y')
plt.savefig(files.images + '\\ref_ps_y.png')

plt.figure()
plt.plot(data.star_ps.values[256,:])
plt.yscale('log')
ymin,ymax = define_ylim(data.star_ps)
#plt.ylim(ymin,ymax)
plt.title('star x')
plt.savefig(files.images + '\\star_ps_x.png')

plt.figure()
plt.plot(data.star_ps.values[:,256])
plt.yscale('log')
ymin,ymax = define_ylim(data.star_ps)
#plt.ylim(ymin,ymax)
plt.title('star y')
plt.savefig(files.images + '\\star_ps_y.png')

plt.figure()
plt.plot(data.final_ps.values[256,:])
plt.title('final ps x')
ymin,ymax = define_ylim(data.final_ps)
plt.ylim(ymin,ymax)
plt.savefig(files.images + '\\final_ps_x.png')

plt.figure()
plt.plot(data.final_ps.values[:,256])
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