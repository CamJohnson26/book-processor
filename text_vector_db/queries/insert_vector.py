def insert_vector_query(vector, starting_text, database):
    try:
        cursor = database.cursor()
        # Use RETURNING to get the newly created id
        cursor.execute("INSERT INTO test_vectors (id, my_vector, starting_text) VALUES (DEFAULT, %s, %s) RETURNING id", [vector, starting_text])

        # Fetch the returned id
        created_id = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        print(f"Vector creation successful, ID: {created_id}")
        return created_id

    except Exception as e:
        print(f"Error creating vector for {starting_text}: {e}")
        database.rollback()
        raise e
