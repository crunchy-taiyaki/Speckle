from initial_parameters import DataFiles

def input_files_info(filenames_config):
    files = DataFiles()
    files.read_input(filenames_config)
    files.info()


