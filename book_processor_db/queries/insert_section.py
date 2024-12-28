from datetime import time

import psycopg2


def insert_section_query(sequence, work_id, text, summary, connection_pool, retry_count=3):
    for i in range(retry_count):
        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO section (id, sequence, work_id, text, summary) VALUES (DEFAULT, %s, %s, %s, %s) RETURNING id", [sequence, work_id, text, summary])

            created_id = cursor.fetchone()[0]

            conn.commit()
            cursor.close()
            print(f'Successfully inserted section {created_id} {sequence} {work_id} {text[:20]}...')
            return created_id
        except Exception as e:
            print(f"Error creating section {text[:100]}...: {e}")
            conn.rollback()
            if i == retry_count - 1:
                raise e
            else:
                time.sleep(5)
        finally:
            connection_pool.putconn(conn)