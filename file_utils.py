import os
from os.path import join

from epub_utils import epub_to_txt

input_folder = 'input'
epub_folder = 'epub'
processing_folder = 'processing'
processed_folder = 'processed'


def get_input_files():
    os.makedirs(input_folder, exist_ok=True)
    file_names = os.listdir(input_folder)
    return [join(input_folder, file_name) for file_name in file_names if not file_name in ['.DS_Store'] ]


def get_processing_files():
    os.makedirs(processing_folder, exist_ok=True)
    file_names = os.listdir(processing_folder)
    return [join(processing_folder, file_name) for file_name in file_names if not file_name in ['.DS_Store']]


def move_processing_file_to_processed(file_name):
    os.makedirs(processing_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)
    source = join(processing_folder, file_name)
    destination = join(processed_folder, file_name)
    os.rename(source, destination)


def get_file_contents(file_name):
    with open(file_name, 'r', encoding='utf-8', errors='replace') as f:
        return f.read().replace('\x00', '')


def clear_input_folder():
    file_names = os.listdir(input_folder)
    for file_name in file_names:
        os.remove(join(input_folder, file_name))
    print(f'Cleared {len(file_names)} files from input folder')


def convert_epub():
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    processing_folder = os.path.join(epub_folder, 'processed')
    if not os.path.exists(processing_folder):
        os.makedirs(processing_folder)

    for filename in os.listdir(epub_folder):
        if filename.endswith('.epub'):
            epub_path = os.path.join(epub_folder, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(input_folder, txt_filename)
            epub_to_txt(epub_path, txt_path)
            processed_file_path = os.path.join(processing_folder, filename)
            os.rename(epub_path, processed_file_path)