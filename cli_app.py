from cmd import Cmd

from dotenv import load_dotenv

from file_utils import clear_input_folder
from s3_utils import upload_files

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

    def do_exit(self, args):
        """Exit the app."""
        raise SystemExit()


if __name__ == '__main__':
    CLIApp().cmdloop("Enter a command (process_files, exit):")
