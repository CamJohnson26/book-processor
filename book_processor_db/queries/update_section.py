import psycopg2


def update_section_query(section_id, embedding_id, connection_pool):
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("UPDATE section SET embedding_id=%s WHERE id=%s", (embedding_id, section_id))

        conn.commit()
        cursor.close()
        print(f'Successfully updated section {section_id}.')

    except Exception as e:
        print(f"Error updating section {section_id}...: {e}")
        conn.rollback()
        raise e

    finally:
        connection_pool.putconn(conn)
