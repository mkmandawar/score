import cloudscraper

scraper = cloudscraper.create_scraper()
url = "https://rrb.digialm.com//per/g22/pub/2667/touchstone/AssessmentQPHTMLMode1//2667O252/2667O252S47D85891/17559611765129741/226243123782986_2667O252S47D85891E1.html"

try:
    response = scraper.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Successfully fetched!")
        # Print a small snippet to confirm it's the right page
        print(response.text[:200])
    else:
        print("Failed to fetch.")
except Exception as e:
    print(f"Error: {e}")
