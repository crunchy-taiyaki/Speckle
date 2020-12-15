
import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
from file_reader import FileInfoReader
from spectra_calculator import Data
from plot import plot_images, plot_spectra_slices
from find_xy import guess_xy
from fit import Fit
from plot_fit import plot_fitted_i_xy_dm
from stats import define_sample
from final_params import final_result

### TYC1947_00290_1 09 12 2019 700
filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912\\input.txt'
fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912\\fit_parameters.txt'
angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912\\angle.txt'

## TYC1947_00290_1 09 12 2019 700 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20190912_no_ref\\angle.txt'

## TYC1947_00290_1 08 03 2020 700 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200308_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200308_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200308_no_ref\\angle.txt'

## TYC1947_00290_1 11 05 2020 700 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200511_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200511_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TYC\\700_20200511_no_ref\\angle.txt'

#InputReader().info(filename_config)
#Data().calc_raw_data(filename_config,size=512)
#Data().calc_final_ps_from_raw_data(filename_config)
#plot_images(filename_config)
#plot_spectra_slices(filename_config)
#guess_xy(filename_config)
#Fit(filename_config, fit_parameters_config).fit_i_xy_dm()
#plot_fitted_i_xy_dm(filename_config,fit_parameters_config)
#define_sample(filename_config,fit_parameters_config)
#final_result(filename_config,fit_parameters_config,angle_config,'180')
