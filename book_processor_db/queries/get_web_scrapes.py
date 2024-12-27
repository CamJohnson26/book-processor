def get_web_scrapes_query(database):
    cursor = database.cursor()
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
