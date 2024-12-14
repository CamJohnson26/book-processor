import psycopg2


def insert_section_query(sequence, work_id, text, database):
    try:
        cursor = database.cursor()
        cursor.execute("INSERT INTO section (id, sequence, work_id, text) VALUES (DEFAULT, %s, %s, %s) RETURNING id", [sequence, work_id, text])

        created_id = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        print(f'Successfully inserted section {created_id} {sequence} {work_id} {text[:20]}...')
        return created_id
    except Exception as e:
        print(f"Error creating section {text[:100]}...: {e}")
        database.rollback()
        raise e
