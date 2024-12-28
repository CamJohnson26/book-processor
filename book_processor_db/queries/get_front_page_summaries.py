def get_front_page_summaries_query(connection_pool):
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, source, summary
    FROM front_page_summary
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
