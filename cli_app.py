from cmd import Cmd

from dotenv import load_dotenv

from book_processor_db.db_actions import insert_work, insert_sections, insert_web_scrape, insert_front_page_summary, \
    get_web_scrapes, get_front_page_summaries, insert_daily_news_summary
from file_utils import clear_input_folder, get_processing_files, get_file_contents, move_processing_file_to_processed, \
    convert_epub
from news.sources import sources, topics
from ollama_apis.chain_prompt import summarize_long_text, compress_long_text
from ollama_apis.prompts import COMBINE_SUMMARIES_PROMPT_V1, SUMMARIZE_TEXT_PROMPT_V1, CREATE_NEWS_STORY_PROMPT_V1
from ollama_apis.run_prompt import chat
from s3_utils import upload_files, get_first_file_in_folder, download_all_files_in_folder, delete_file_in_folder
from scraping.scrape_url import scrape_url

load_dotenv()


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

    @staticmethod
    def do_scrape_news(self):
        source_urls = [s[1] for s in sources]
        for source in source_urls:
            success, content, error = scrape_url(source)
            if success:
                insert_web_scrape(source, content)
        print(f'Scraped {len(source_urls)} news sources')

    @staticmethod
    def do_front_page_summary(self):
        web_scrapes = get_web_scrapes()
        for web_scrape in web_scrapes:
            summary = summarize_long_text(web_scrape[2], SUMMARIZE_TEXT_PROMPT_V1)
            insert_front_page_summary(web_scrape[1], 'all', summary)

    @staticmethod
    def do_daily_news_summary(self):
        front_page_summaries = get_front_page_summaries()
        text = ''
        for front_page_summary in front_page_summaries:
            text += '\n' + front_page_summary[2]
        summary = summarize_long_text(text, CREATE_NEWS_STORY_PROMPT_V1, char_limit=10_000)

        insert_daily_news_summary(summary)


if __name__ == '__main__':
    CLIApp().cmdloop("Enter a command (process_files, convert_epub, scrape_news, front_page_summary, daily_news_summary, exit):")
