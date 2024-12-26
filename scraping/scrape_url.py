import requests
from urllib.parse import urlparse
from typing import Optional, Tuple
from bs4 import BeautifulSoup
import re


def get_default_headers() -> dict:
    """
    Returns default headers that mimic a common browser request.
    """
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
    }


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validates if the given URL is properly formatted.
    Returns a tuple of (is_valid, error_message).
    """
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True, None
        return False, "URL is missing scheme (e.g., 'http://') or network location"
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"


def clean_text(text: str) -> str:
    """
    Cleans extracted text by removing extra whitespace and empty lines.
    """
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove empty lines
    text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
    return text.strip()


def extract_text_from_html(html_content: str) -> str:
    """
    Extracts readable text from HTML content while preserving some structure.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for element in soup(['script', 'style', 'meta', 'link', 'noscript']):
        element.decompose()

    # Get title if it exists
    title = soup.title.string if soup.title else ''

    # Extract text from specific content tags
    content_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'article'])

    # Build text content with structure
    text_parts = []
    if title:
        text_parts.append(f"Title: {title}\n")

    for tag in content_tags:
        # Skip empty tags or those with no text
        if not tag.get_text(strip=True):
            continue

        # Add appropriate spacing based on tag type
        if tag.name.startswith('h'):
            text_parts.append(f"\n{tag.get_text()}\n")
        elif tag.name == 'p':
            text_parts.append(f"{tag.get_text()}\n")
        else:
            text_parts.append(tag.get_text())

    # Join and clean the extracted text
    return clean_text('\n'.join(text_parts))


def scrape_url(url: str, timeout: int = 30) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Downloads and extracts readable text content from the specified URL.

    Args:
        url: The URL to download from
        timeout: Request timeout in seconds

    Returns:
        Tuple of (success, content, error_message)
    """
    # Validate URL first
    is_valid, error_msg = validate_url(url)
    if not is_valid:
        return False, None, error_msg

    try:
        # Make the request with browser-like headers
        response = requests.get(
            url,
            headers=get_default_headers(),
            timeout=timeout
        )

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Extract readable text from HTML
        text_content = extract_text_from_html(response.text)

        return True, text_content, None

    except requests.exceptions.Timeout:
        return False, None, f"Request timed out after {timeout} seconds"
    except requests.exceptions.TooManyRedirects:
        return False, None, "Too many redirects"
    except requests.exceptions.RequestException as e:
        return False, None, f"Error downloading content: {str(e)}"