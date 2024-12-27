import psycopg2
from dotenv import load_dotenv

import os

from book_processor_db.queries.get_front_page_summaries import get_front_page_summaries_query
from book_processor_db.queries.get_web_scrapes import get_web_scrapes_query
from book_processor_db.queries.insert_daily_news_summary import insert_daily_news_summary_query
from book_processor_db.queries.insert_front_page_summary import insert_front_page_summary_query
from book_processor_db.queries.insert_section import insert_section_query
from book_processor_db.queries.insert_web_scrape import insert_web_scrape_query
from book_processor_db.queries.insert_work import insert_work_query
from book_processor_db.queries.update_section import update_section_query
from ollama_apis.prompts import TEXT_SUMMARY_PROMPT_V1
from ollama_apis.run_prompt import chat
from text_vector_db.db_actions import embed_and_insert_vector

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

database = psycopg2.connect(DATABASE_URL)

chunk_size = 2000


def get_web_scrapes():
    return get_web_scrapes_query(database)


def get_front_page_summaries():
    return get_front_page_summaries_query(database)


def insert_work(name):
    return insert_work_query(name, database)


def insert_daily_news_summary(text):
    return insert_daily_news_summary_query(text, database)


def insert_sections(work_id, text):
    try:
        results = []
        for i in range(0, len(text), chunk_size):
            print(f'Processing {i}/{len(text)}')
            text_chunk = text[i:i + chunk_size]
            text_summary = chat(TEXT_SUMMARY_PROMPT_V1 + text_chunk)
            section_id = insert_section_query(i, work_id, text_chunk, text_summary, database)
            results.append(section_id)
            embedding_id = embed_and_insert_vector(text_summary)
            update_section_embedding_id(section_id, embedding_id)
        return results
    except Exception as e:
        raise 'Error in insert_sections: ' + str(e)


def update_section_embedding_id(section_id, embedding_id):
    return update_section_query(section_id, embedding_id, database)


def insert_web_scrape(source, text):
    insert_web_scrape_query(source, text, database)


def insert_front_page_summary(source, topic, summary):
    insert_front_page_summary_query(source, topic, summary, database)