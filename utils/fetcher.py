import cloudscraper

def fetch_url(url):
    """
    Fetches the content of the given URL using cloudscraper to bypass bot protection.
    Returns the HTML content or None if failed.
    """
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch URL. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None
