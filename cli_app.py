from cmd import Cmd

from dotenv import load_dotenv

from book_processor_db.db_actions import insert_work, insert_sections
from file_utils import clear_input_folder, get_processing_files, get_file_contents, move_processing_file_to_processed, \
    convert_epub
from s3_utils import upload_files, get_first_file_in_folder, download_all_files_in_folder, delete_file_in_folder
from text_vector_db.db_actions import embed_and_insert_vector

load_dotenv()
# token = os.environ.get("")


class CLIApp(Cmd):
    """A simple CLI app."""
    prompt = '>>> '

    @staticmethod
    def do_process_files(self):
        """Uploads all files in the input folder."""
        print('Uploading files...')
        upload_files()
        clear_input_folder()
        download_all_files_in_folder()
        files = get_processing_files()
        for file in files:
            file_name = file.split('/')[-1]
            work_id = insert_work(file_name)

            file_text = get_file_contents(file)
            insert_sections(work_id, file_text)
            delete_file_in_folder(file_name)
            move_processing_file_to_processed(file_name)


    def do_exit(self, args):
        """Exit the app."""
        raise SystemExit()


    @staticmethod
    def do_convert_epub(self):
        convert_epub()


if __name__ == '__main__':
    CLIApp().cmdloop("Enter a command (process_files, convert_epub, exit):")
