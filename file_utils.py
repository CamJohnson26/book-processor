import os
from os.path import join


folder = 'input'


def get_input_files():
    file_names = os.listdir(folder)
    return [join(folder, file_name) for file_name in file_names]


def clear_input_folder():
    file_names = os.listdir(folder)
    for file_name in file_names:
        os.remove(join(folder, file_name))
    print(f'Cleared {len(file_names)} files from input folder')