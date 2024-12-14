import psycopg2
from dotenv import load_dotenv

import os

from book_processor_db.queries.insert_section import insert_section_query
from book_processor_db.queries.insert_work import insert_work_query
from book_processor_db.queries.update_section import update_section_query
from text_vector_db.db_actions import embed_and_insert_vector

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

database = psycopg2.connect(DATABASE_URL)

chunk_size = 2000


def insert_work(name):
    return insert_work_query(name, database)


def insert_sections(work_id, text):
    try:
        results = []
        for i in range(0, len(text), chunk_size):
            text_chunk = text[i:i + chunk_size]
            section_id = insert_section_query(i, work_id, text_chunk, database)
            results.append(section_id)
            embedding_id = embed_and_insert_vector(text_chunk)
            update_section_embedding_id(section_id, embedding_id)
        return results
    except Exception as e:
        raise 'Error in insert_sections: ' + str(e)


def update_section_embedding_id(section_id, embedding_id):
    return update_section_query(section_id, embedding_id, database)