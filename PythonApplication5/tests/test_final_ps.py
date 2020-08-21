from initial_parameters import *
from power_spectrum import *

files = DataFiles()
files.read_input('C:\\Users\\Marta\\source\\repos\\PythonApplication5\\PythonApplication5\\inputs\\TEST_star_input.txt')
files.info()
data = Data()

##calc all data
#print('data calculation...')
#data.dark = middle_dark(files.dark,files.dark_frames)
#data.ref_dark = middle_dark(files.ref_dark,files.ref_dark_frames)
#data.flat = middle_flat(files.flat,files.flat_frames)
#data.star_ps = obj_ps(files.star,files.star_frames, data.dark, data.flat)
#data.ref_ps = obj_ps(files.ref,files.ref_frames, data.ref_dark, data.flat)
#print('all done!')
#data.save_to(files.data)
#print('data saved')

#read data from files
data.read_from(files.data)

data.star_ps = remove_background(data.star_ps,480)
data.ref_ps = remove_background(data.ref_ps,480)
data.final_power_spectrum()
data.save_to(files.data)
print('all data saved')
