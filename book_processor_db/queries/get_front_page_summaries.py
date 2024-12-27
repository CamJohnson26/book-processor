def get_front_page_summaries_query(database):
    cursor = database.cursor()
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
