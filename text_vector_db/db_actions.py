import psycopg2
from dotenv import load_dotenv

import os


from ollama_apis.run_prompt import embed

from text_vector_db.queries.insert_vector import insert_vector_query

load_dotenv()
DATABASE_URL = os.getenv("TEXT_VECTOR_DATABASE_URL")

database = psycopg2.connect(DATABASE_URL)


def embed_and_insert_vector(text):
    try:
        vector = embed(text)
        print(vector)
        starting_text = text[:100]
        return insert_vector_query(vector, starting_text, database)
    except Exception as e:
        print(f'Error embedding text {text[:20]}', e)
        return None
