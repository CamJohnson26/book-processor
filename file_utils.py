import os
from os.path import join


input_folder = 'input'
processing_folder = 'processing'
processed_folder = 'processed'


def get_input_files():
    os.makedirs(input_folder, exist_ok=True)
    file_names = os.listdir(input_folder)
    return [join(input_folder, file_name) for file_name in file_names]


def get_processing_files():
    os.makedirs(processing_folder, exist_ok=True)
    file_names = os.listdir(processing_folder)
    return [join(processing_folder, file_name) for file_name in file_names]


def move_processing_file_to_processed(file_name):
    os.makedirs(processing_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)
    source = join(processing_folder, file_name)
    destination = join(processed_folder, file_name)
    os.rename(source, destination)


def get_file_contents(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def clear_input_folder():
    file_names = os.listdir(input_folder)
    for file_name in file_names:
        os.remove(join(input_folder, file_name))
    print(f'Cleared {len(file_names)} files from input folder')