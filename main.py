#!/usr/bin/env python3
import time
import schedule
import os
import requests
import ssl
from dotenv import load_dotenv

from cli_app import CLIApp

def run_news_scraping_and_summary():
    """Run the news scraping and front page summary functions."""
    print(f"Running news scraping and summary at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Create an instance of CLIApp
    app = CLIApp()

    # Run the scrape_news function
    print("Scraping news...")
    CLIApp.do_scrape_news(app)

    # Run the front_page_summary function
    print("Generating front page summaries...")
    CLIApp.do_front_page_summary(app)

    for i in range(5):
        print(f"Generating daily news summary {i+1}...")
        CLIApp.do_daily_news_summary(app)

    print("News scraping and summary completed successfully.")

def run_healthcheck():
    """Send a healthcheck ping to the monitoring service."""
    healthcheck_url = os.environ.get('HEALTHCHECK_URL')
    if not healthcheck_url:
        print("Warning: HEALTHCHECK_URL environment variable not set. Skipping healthcheck.")
        return

    try:
        session = requests.Session()
        session.verify = ssl.get_default_verify_paths().cafile or ssl.get_default_verify_paths().capath

        response = session.get(healthcheck_url, timeout=10)
        if response.status_code == 200:
            print(f"Healthcheck successful at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"Healthcheck failed with status code {response.status_code}")
    except Exception as e:
        print(f"Healthcheck error: {str(e)}")

def main():
    """Main function to set up and run the scheduled tasks."""
    # Load environment variables
    load_dotenv()

    # Run the tasks immediately when the script starts
    run_healthcheck()
    run_news_scraping_and_summary()

    # Schedule the tasks
    schedule.every(12).hours.do(run_news_scraping_and_summary)
    schedule.every(5).minutes.do(run_healthcheck)

    # Keep the script running and check for scheduled tasks
    print("Scheduled tasks: News scraping every 12 hours, Healthcheck every 5 minutes. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
