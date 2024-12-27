
def insert_daily_news_summary_query(text, database):
    try:
        cursor = database.cursor()
        # Use RETURNING to get the newly created id
        cursor.execute("INSERT INTO daily_news_summary (text) VALUES (%s) RETURNING id", [text])

        # Fetch the returned id
        created_id = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        print(f"Creation successful, ID: {created_id}")
        return created_id

    except Exception as e:
        print(f"Error creating {text[:150]}: {e}")
        database.rollback()
        raise e
