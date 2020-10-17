from initial_parameters import DataFiles
from power_spectrum import Data
import matplotlib.pyplot as plt

def final_ps(filename_config):

    files = DataFiles()
    files.read_input(filename_config)
    files.info()
    data = Data()

    #read data from files
    data.read_raw_data_from(files.data)
    data.define_freq_bounds()
    data.rmbg()
    data.find_final_ps()

    data.save_to(files.data)
    print('all data saved')
