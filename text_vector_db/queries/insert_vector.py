from datetime import time


def insert_vector_query(vector, starting_text, connection_pool,  retry_count=3):
    for i in range(retry_count):
        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()
            # Use RETURNING to get the newly created id
            cursor.execute("INSERT INTO test_vectors (id, my_vector, starting_text) VALUES (DEFAULT, %s, %s) RETURNING id", [vector, starting_text])

            # Fetch the returned id
            created_id = cursor.fetchone()[0]

            conn.commit()
            cursor.close()
            print(f"Vector creation successful, ID: {created_id}")
            return created_id

        except Exception as e:
            print(f"Error creating vector for {starting_text}: {e}")
            conn.rollback()
            if i == retry_count - 1:
                raise e
            else:
                time.sleep(5)
        finally:
            connection_pool.putconn(conn)
