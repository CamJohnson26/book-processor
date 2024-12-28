import psycopg2
from dotenv import load_dotenv

import os


from ollama_apis.run_prompt import embed

from text_vector_db.queries.insert_vector import insert_vector_query

from psycopg2 import pool

load_dotenv()
DATABASE_URL = os.getenv("TEXT_VECTOR_DATABASE_URL")

connection_pool = pool.SimpleConnectionPool(
    1,      # Minimum number of connections
    10,     # Maximum number of connections
    DATABASE_URL
)


def embed_and_insert_vector(text):
    try:
        is_valid_vector = False
        while not is_valid_vector:
            vector = embed(text, model='Losspost/stella_en_1.5b_v5')
            print(is_valid_vector, vector)
            is_valid_vector = not all([v == 0 or v == 1 for v in vector])
        print(vector)
        starting_text = text[:100]
        return insert_vector_query(vector, starting_text, connection_pool)
    except Exception as e:
        print(f'Error embedding text {text[:20]}', e)
        return None
