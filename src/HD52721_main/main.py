import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
from info import input_files_info
from obj_spectra_preproc import objects_spectra_preproc
from final_ps import final_ps
from fit_params import fit_i_xy_dm
from find_xy import guess_xy
from plot_fit import plot_fitted_i_xy_dm
from plot_projections import plot_projections
from plot_images import plot_dark_flat_and_spectra_image
from stats import plot_residuals, define_sample, normality_test
from final_params import final_result


## test binary system
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_251_input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_251_fit_parameters.txt'

## test triple system
#filename_config = 'c:\\users\\marta\\source\\repos\\crunchy-taiyaki\\speckle\\src\\inputs\\pair_100_as_triple_input.txt'
#fit_parameters_config = 'c:\\users\\marta\\source\\repos\\crunchy-taiyaki\\speckle\\src\\inputs\\pair_100_as_triple_fit_parameters.txt'

# triple hd52721 550 04_03_2020
filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\input.txt'
fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\fit_parameters.txt'
angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020\\angle.txt'

## triple hd52721 550 04_03_2020 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_04032020_no_ref\\angle.txt'

## triple hd52721 694 04_03_2020
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_694_04032020\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_694_04032020\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_694_04032020\\angle.txt'

## triple hd52721 694 04_03_2020 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_694_04032020_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_694_04032020_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_694_04032020_no_ref\\angle.txt'

## triple hd52721 700 04_03_2020
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_700_04032020\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_700_04032020\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_700_04032020\\angle.txt'

## triple hd52721 700 04_03_2020 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_700_04032020_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_700_04032020_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_700_04032020_no_ref\\angle.txt'

## triple hd52721 800 04_03_2020
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_04032020\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_04032020\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_04032020\\angle.txt'

## triple hd52721 800 04_03_2020 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_04032020_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_04032020_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_04032020_no_ref\\angle.txt'

## triple hd52721 550 15_11_2019
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_15112019\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_15112019\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_15112019\\angle.txt'

### triple hd52721 550 15_11_2019 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_15112019_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_15112019_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_15112019_no_ref\\angle.txt'

### triple hd52721 800 15_11_2019 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_15112019_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_15112019_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_15112019_no_ref\\angle.txt'

### triple hd52721 550 08 04 2019
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_08042019\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_08042019\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_08042019\\angle.txt'

## triple hd52721 550 08 04 2019 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_08042019_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_08042019_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_550_08042019_no_ref\\angle.txt'

## triple hd52721 800 08 04 2019 no ref
#filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_08042019_no_ref\\input.txt'
#fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_08042019_no_ref\\fit_parameters.txt'
#angle_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\hd52721_800_08042019_no_ref\\angle.txt'


#input_files_info(filename_config)
#objects_spectra_preproc(filename_config)
#final_ps(filename_config)
#plot_dark_flat_and_spectra_image(filename_config)
#plot_projections(filename_config)
#guess_xy(filename_config)
fit_i_xy_dm(filename_config, fit_parameters_config,'rmbg','') #flags: 'rmbg' or '' and 'ellipse or '' 
#plot_fitted_i_xy_dm(filename_config,fit_parameters_config,'rmbg') #flag: 'rmbg' or ''
#plot_residuals(filename_config,fit_parameters_config,'rmbg') #flag: 'rmbg' or ''
#define_sample(filename_config,fit_parameters_config, residual_level=0.05)
#normality_test(filename_config,fit_parameters_config)
#final_result(filename_config,fit_parameters_config,angle_config,'180')