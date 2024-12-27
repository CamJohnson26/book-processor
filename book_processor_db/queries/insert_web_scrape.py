
def insert_web_scrape_query(source, text, database):
    try:
        cursor = database.cursor()
        # Use RETURNING to get the newly created id
        cursor.execute("INSERT INTO web_scrape (source, text) VALUES (%s, %s) RETURNING id", [source, text])

        # Fetch the returned id
        created_id = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        print(f"Creation successful, ID: {created_id}")
        return created_id

    except Exception as e:
        print(f"Error creating {source}: {e}")
        database.rollback()
        raise e
