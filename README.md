# book-processor
Extract metadata about a given work of text

# NaN problem
Sometimes embeddings glitch and treat the vector as all 0s or all 1s. This sql script will delete them:
Can't delete these easily with pgvector
Instead I just retry the embedding until they aren't all 1 or 0

# Server unexpectedly closed the connection
There's a lot of anger about how psycopg connection pools don't handle reconnection logic:
https://stackoverflow.com/questions/64603192/psycopg2-pool-crashes-when-the-thread-pool-runs-out