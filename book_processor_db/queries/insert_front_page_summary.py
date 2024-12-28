
def insert_front_page_summary_query(source, topic, summary, connection_pool):
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        # Use RETURNING to get the newly created id
        cursor.execute("INSERT INTO front_page_summary (source, topic, summary) VALUES (%s, %s, %s) RETURNING id", [source, topic, summary])

        # Fetch the returned id
        created_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        print(f"Creation successful, ID: {created_id}")
        return created_id

    except Exception as e:
        print(f"Error creating {source}: {e}")
        conn.rollback()
        raise e

    finally:
        connection_pool.putconn(conn)