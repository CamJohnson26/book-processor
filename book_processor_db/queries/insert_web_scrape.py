
def insert_web_scrape_query(source, text, connection_pool):
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        # Use RETURNING to get the newly created id
        cursor.execute("INSERT INTO web_scrape (source, text) VALUES (%s, %s) RETURNING id", [source, text])

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