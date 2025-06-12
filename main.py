import requests
import re

# Define the crawl and the pattern to search for
CRAWL = 'CC-MAIN-2020-05'
BASE_URL = f'https://index.commoncrawl.org/{CRAWL}'

# Define the substring pattern to search for in URLs or content
# For broad scope, use '*' (wildcard)
# For example, searching for URLs containing 'example.com'
URL_SUBSTRING = '*'  # Use '*' for all URLs, or specify a particular substring

# Function to perform the query
def query_common_crawl(crawl, url_substring='*'):
    query_url = f'{BASE_URL}?url={url_substring}'
    print(f"Querying: {query_url}")
    response = requests.get(query_url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch index: {response.status_code}")
        return None

# Function to parse the index response and extract URLs
def parse_results(results_text):
    # Each line in the index is a JSON-like string with fields:
    # url, offset, length, filename, segment_id, mime_type, ...
    # But the index returns tab-separated values, so we parse accordingly.
    # Format example:
    # url http://example.com  offset length filename ...
    lines = results_text.strip().split('\n')
    urls = []
    for line in lines:
        parts = line.split('\t')
        if len(parts) >= 1:
            url = parts[0]
            urls.append(url)
    return urls

# Function to fetch URL content snippet (optional)
def fetch_url_content(url):
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.text
        else:
            return ''
    except:
        return ''

# Main function
def main():
    results_text = query_common_crawl(CRAWL, URL_SUBSTRING)
    if not results_text:
        return
    
    urls = parse_results(results_text)
    print(f"Found {len(urls)} URLs. Filtering for 64-character hex strings...")

    # Regex to match 64 hexadecimal characters
    pattern = re.compile(r'\b[a-fA-F0-9]{64}\b')

    # Check each URL or content for the pattern
    for url in urls:
        content = fetch_url_content(url)
        if pattern.search(content):
            print(f"Match found in URL: {url}")
        # Optional: Uncomment below to print URLs directly containing pattern in URL
        # if pattern.search(url):
        #     print(f"Match in URL: {url}")

if __name__ == "__main__":
    main()
