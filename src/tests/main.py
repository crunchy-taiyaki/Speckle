import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
from info import input_files_info
from obj_spectra_preproc import objects_spectra_preproc
from final_ps import final_ps
from fit_params import fit_i_xy_dm
from find_xy import plot_acf
from plot_fit import plot_fitted_i_xy_dm
from plot_projections import plot_projections
from plot_hists import show_stats
from plot_images import plot_dark_flat_and_spectra_image

filename_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_251_input.txt'
fit_parameters_config = 'C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\pair_100_251_fit_parameters.txt'

#input_files_info(filename_config)
#objects_spectra_preproc(filename_config)
#final_ps(filename_config)
#plot_dark_flat_and_spectra_image(filename_config)
plot_acf(filename_config)
#fit_i_xy_dm(filename_config, fit_parameters_config)
#plot_fitted_i_xy_dm(filename_config)
#plot_projections(filename_config)
#show_stats(filename_config,fit_parameters_config)