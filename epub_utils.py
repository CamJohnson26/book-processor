import os
from ebooklib import epub
from bs4 import BeautifulSoup


def epub_to_txt(epub_file, output_txt_file):
    try:
        # Load the EPUB file
        book = epub.read_epub(epub_file)

        # Initialize a list to hold the text content
        text_content = []

        # Iterate through the items in the book
        for item in book.get_items():
            if item.media_type == 'application/xhtml+xml':
                # Parse the content using BeautifulSoup
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                # Extract and clean the text
                text_content.append(soup.get_text())

        # Join the extracted text and save it to a TXT file
        with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
            txt_file.write('\n\n'.join(text_content))

        print(f"Successfully converted '{epub_file}' to '{output_txt_file}'")
    except Exception as e:
        print(f"Error: {e}")
