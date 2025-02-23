import requests
from bs4 import BeautifulSoup
import json
import csv
import random

# List of various user agents to mimic different browsers/devices
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

def get_random_headers():
    # Randomly select a user agent from the list
    return {'User-Agent': random.choice(USER_AGENTS)}

def scrape_website(url):
    # Set a random browser-like user agent
    headers = get_random_headers()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching URL: {url}\n{e}")
        return None

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove unwanted tags to clean the page (scripts, styles, nav bars, etc.)
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()

    # Extract the page title
    title = soup.title.get_text(strip=True) if soup.title else "No Title Found"

    # Extract headings (h1-h6)
    headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

    # Extract paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]

    # Combine the content in a structured format
    content = {
        "url": url,
        "title": title,
        "headings": headings,
        "paragraphs": paragraphs,
    }
    return content

def save_to_json(data, filename="scraped_data.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving JSON: {e}")

def save_to_csv(data, filename="scraped_data.csv"):
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # Write headers
            writer.writerow(['URL', 'Title', 'Headings', 'Paragraphs'])
            # Flatten the headings and paragraphs into strings
            writer.writerow([
                data['url'],
                data['title'],
                " | ".join(data['headings']),
                " ".join(data['paragraphs'])
            ])
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving CSV: {e}")

if __name__ == "__main__":
    url = input("Enter the website URL to scrape: ").strip()
    scraped_data = scrape_website(url)
    if scraped_data:
        # Save output in JSON and CSV formats
        save_to_json(scraped_data)
        save_to_csv(scraped_data)
