def get_web_scrapes_query(connection_pool):
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, source, text
    FROM web_scrape
    WHERE created_at >= CURRENT_DATE
      AND created_at <= CURRENT_DATE + INTERVAL '1 day';""", [])
        records = cursor.fetchall()
        cursor.close()
        if records is not None:
            print(f"Fetched {len(records)} records")
            return records
        else:
            print(f"Couldn't find {id}")
            return None
    except Exception as e:
        print(e)
    finally:
        connection_pool.putconn(conn)
