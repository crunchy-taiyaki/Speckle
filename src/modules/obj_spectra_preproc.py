from initial_parameters import DataFiles
from power_spectrum import Data, middle_dark,middle_flat,obj_ps

def objects_spectra_preproc(filename_config):

    files = DataFiles()
    files.read_input(filename_config)
    files.info()
    data = Data()

    #calc all data
    print('data calculation...')
    data.dark = middle_dark(files.dark,files.dark_frames)
    data.ref_dark = middle_dark(files.ref_dark,files.ref_dark_frames)
    data.flat = middle_flat(files.flat,files.flat_frames)
    data.star_ps.values = obj_ps(files.star,files.star_frames, data.dark, data.flat)
    data.ref_ps.values = obj_ps(files.ref,files.ref_frames, data.ref_dark, data.flat)
    print('all done!')
    data.save_to(files.data)
    print('data saved')

