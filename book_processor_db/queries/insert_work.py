import psycopg2


def insert_work_query(name, database):
    try:
        cursor = database.cursor()
        # Use RETURNING to get the newly created id
        cursor.execute("INSERT INTO work (id, name) VALUES (DEFAULT, %s) RETURNING id", [name])

        # Fetch the returned id
        created_id = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        print(f"Creation successful, ID: {created_id}")
        return created_id

    except Exception as e:
        print(f"Error creating {name}: {e}")
        database.rollback()
        raise e
