# Book Processor
A tool for processing and analyzing text content from various sources, including books and news articles.

## Features
- Text metadata extraction
- EPUB file conversion
- News scraping and summarization
- Front page summaries
- Daily news digests
- S3 integration for file storage

## Commands
- `process_files`: Upload and process files from the input folder
- `convert_epub`: Convert EPUB files to processable format
- `scrape_news`: Collect news from configured sources
- `front_page_summary`: Generate summaries of scraped news
- `daily_news_summary`: Create consolidated daily news digests
- `good_morning`: Run a complete news collection and summary workflow

## Automated News Scraping
The project includes a script for automated news scraping and summarization:

- `main.py`: Runs the news scraping and front page summary functions on a schedule
  - Executes immediately when started
  - Automatically runs every 12 hours
  - Can be run in the background as a service

To start the automated news scraping:
```bash
# Run in the foreground
./main.py

# Run in the background
nohup ./main.py > news_scraping.log 2>&1 &
```

## Project Structure
- `/epub`: EPUB processing utilities
- `/news`: News source configurations
- `/scraping`: Web scraping tools
- `/text_vector_db`: Vector database operations
- `/book_processor_db`: Database operations
- `/ollama_apis`: AI text processing

## Known Issues

### NaN problem
Sometimes embeddings glitch and treat the vector as all 0s or all 1s. This sql script will delete them:
Can't delete these easily with pgvector
Instead I just retry the embedding until they aren't all 1 or 0

### Server unexpectedly closed the connection
There's a lot of anger about how psycopg connection pools don't handle reconnection logic:
https://stackoverflow.com/questions/64603192/psycopg2-pool-crashes-when-the-thread-pool-runs-out

## Setup
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.sample` to `.env` and configure your environment variables
