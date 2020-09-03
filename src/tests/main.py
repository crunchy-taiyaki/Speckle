import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
from info import input_files_info
from obj_spectra_preproc import objects_spectra_preproc
from final_ps import final_ps
from fit_params import fit_i_xy_dm
from find_xy import guess_xy
from plot_fit import plot_fitted_i_xy_dm
from plot_projections import plot_projections
from stats import plot_residuals, define_sample, normality_test, dm_xy_result
from plot_images import plot_dark_flat_and_spectra_image

## test binary system
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_251_input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_251_fit_parameters.txt'

## test triple system
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_as_triple_input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_as_triple_fit_parameters.txt'

## triple hd52721 550 04_03_2020
filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_04032020_550_input.txt'
fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_04032020_550_fit_parameters.txt'

#input_files_info(filename_config)
#objects_spectra_preproc(filename_config)
#final_ps(filename_config)
#plot_dark_flat_and_spectra_image(filename_config)
#plot_projections(filename_config)
#guess_xy(filename_config)
#fit_i_xy_dm(filename_config, fit_parameters_config,'rmbg','') #flags: 'rmbg' or '' and 'ellipse or '' 
#plot_fitted_i_xy_dm(filename_config,fit_parameters_config,'rmbg') #flag: 'rmbg' or ''
#plot_residuals(filename_config,fit_parameters_config,'rmbg') #flag: 'rmbg' or ''
#define_sample(filename_config,fit_parameters_config, residual_level=100.0)
normality_test(filename_config,fit_parameters_config)
dm_xy_result(filename_config,fit_parameters_config)