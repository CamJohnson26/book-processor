import psycopg2


def update_section_query(section_id, embedding_id, database):
    try:
        cursor = database.cursor()
        cursor.execute("UPDATE section SET embedding_id=%s WHERE id=%s", (embedding_id, section_id))

        database.commit()
        cursor.close()
        print(f'Successfully updated section {section_id}.')

    except Exception as e:
        print(f"Error updating section {section_id}...: {e}")
        database.rollback()
        raise e
